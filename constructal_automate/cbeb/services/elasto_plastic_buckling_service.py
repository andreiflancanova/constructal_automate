from decimal import Decimal
import os
from cbeb.models import StiffenedPlateAnalysis
from cbeb.config.mapdl_connection_pool import MapdlConnectionPool
from cbeb.models.elastic_buckling import ElasticBuckling
from csg.models import StiffenedPlate
from cbeb.models.processing_status import ProcessingStatus
from ansys.mapdl.core.errors import MapdlRuntimeError

LINES_CONTORNO_PLACA_TS = os.getenv('LINES_CONTORNO_PLACA_TS')
LINES_CONTORNO_PLACA_LS = os.getenv('LINES_CONTORNO_PLACA_LS')
LINES_BORDA_LS = os.getenv('LINES_BORDA_LS')
LINES_BORDA_TS = os.getenv('LINES_BORDA_TS')
IN_PROGRESS_PROCESSING_STATUS = ProcessingStatus.objects.get(name='In Progress')
COMPLETED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Completed')
FAILED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Failed')
CANCELLED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Cancelled')
LOAD_MULTIPLIER = 0.7


class ElastoPlasticBucklingService():
    def create(self,
               stiffened_plate: StiffenedPlate,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               elastic_buckling: ElasticBuckling
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        rst_file_path = stiffened_plate_analysis.analysis_rst_file_path
        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1
        h_s = stiffened_plate.h_s
        t_s = stiffened_plate.t_s
        csi_y = elastic_buckling.csi_y
        material = stiffened_plate_analysis.material

        mapdl_connection_pool = MapdlConnectionPool()

        mapdl_connection = mapdl_connection_pool.get_connection()

        mapdl = mapdl_connection.connection

        try:
            stiffened_plate_analysis.elasto_plastic_buckling_status = IN_PROGRESS_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            w0 = self.define_initial_deflection(b)
            self.load_previous_steps_analysis_db(mapdl, analysis_log_path, analysis_dir_path, analysis_db_path)
            self.define_nonlinear_analysis_params(mapdl, w0, rst_file_path, material, t_1)
            self.apply_loads(mapdl, h_s, t_s, buckling_load_type, material, t_1, csi_y)
            self.solve_elasto_plastic_buckling(mapdl)
            n_u, sigma_u = self.calc_ultimate_buckling_load_and_stress(mapdl, t_1)
            w_max = self.calc_z_deflection(mapdl, a, b)
            mapdl.finish()
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elasto_plastic_buckling_status = COMPLETED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elastic_buckling_status = FAILED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        # TODO: Implementar lógica para cancelar a request
        finally:
            mapdl_connection_pool.return_connection(mapdl_connection)
        return n_u, sigma_u, w_max

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        mapdl.resume(fname=f'{analysis_db_path}')
        mapdl.slashsolu()
        mapdl.asel("ALL")

    def define_initial_deflection(self, b):
        return b/2000

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00

    def define_nonlinear_analysis_params(self, mapdl, w0, rst_file_path, material, t_1):
        mapdl.prep7()
        # mapdl.ncnv(dlim=2000000)
        mapdl.upgeom(factor=w0, lstep="LAST", sbstep="LAST", fname=rst_file_path.removesuffix(".rst"), ext="")
        mapdl.tb(lab="BISO", mat=material.id, ntemp=1, npts=2)
        mapdl.tbtemp(0)
        mapdl.tbdata("", material.yielding_stress, material.tang_modulus, "")
        mapdl.run("/SOL")
        mapdl.run("ANTYPE,0")
        mapdl.nlgeom(key="ON")
        # mapdl.lnsrch(key="ON")
        # mapdl.autots(key="ON")
        mapdl.nsubst(200, 400, 100)
        mapdl.cnvtol(lab="F", value=0.1)
        mapdl.cnvtol(lab="U", value=0.1)
        # mapdl.outres("ERASE")
        # mapdl.outres("ALL", 1)
        mapdl.pstres(1)
        n_e = round(Decimal(LOAD_MULTIPLIER) * material.yielding_stress*t_1, 1)
        mapdl.time(n_e)

    def apply_loads(self, mapdl, h_s, t_s, buckling_load_type, material, t_1, csi_y):
        n_e = round(Decimal(LOAD_MULTIPLIER) * material.yielding_stress*t_1, 1)
        if self.is_stiffened_plate(h_s, t_s):
            if self.is_biaxial_buckling(buckling_load_type):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_e)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", round(csi_y * n_e, 1))
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_e)
                mapdl.sfl(LINES_BORDA_TS, "PRESS", round(csi_y * n_e, 1))
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_e)
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_e)
        else:
            if self.is_biaxial_buckling(buckling_load_type):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_e)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", round(csi_y * n_e, 1))
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_e)

    def solve_elasto_plastic_buckling(self, mapdl):
        mapdl.solve()
        mapdl.finish()
        mapdl.run("/POST1")

    def calc_ultimate_buckling_load_and_stress(self, mapdl, t_1):
        elasto_plastic_buckling_data_sets = mapdl.post_processing.time_values
        ultimate_buckling_load_position = len(elasto_plastic_buckling_data_sets) - 2
        n_u = elasto_plastic_buckling_data_sets[ultimate_buckling_load_position]
        sigma_u = n_u / t_1
        mapdl.save()
        return n_u, sigma_u

    def calc_z_deflection(self, mapdl, a, b):
        mapdl.run(f"NSEL,S,NODE,,NODE({float(a)*0.5},{float(b)*0.5},0)")
        z_deflection = abs(mapdl.prnsol(item="U", comp="Z").to_list()[0][1])
        return z_deflection
