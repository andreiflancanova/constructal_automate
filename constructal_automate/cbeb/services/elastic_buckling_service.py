import os
from cbeb.models import StiffenedPlateAnalysis
from cbeb.models.processing_status import ProcessingStatus
from csg.models import StiffenedPlate
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core import launch_mapdl
import re


LINES_CONTORNO_PLACA_TS = os.getenv('LINES_CONTORNO_PLACA_TS')
LINES_CONTORNO_PLACA_LS = os.getenv('LINES_CONTORNO_PLACA_LS')
LINES_BORDA_LS = os.getenv('LINES_BORDA_LS')
LINES_BORDA_TS = os.getenv('LINES_BORDA_TS')
IN_PROGRESS_PROCESSING_STATUS = ProcessingStatus.objects.get(name='In Progress')
COMPLETED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Completed')
FAILED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Failed')
CANCELLED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Cancelled')

MAPDL_RUN_LOCATION = os.getenv('MAPDL_RUN_LOCATION')
MAPDL_START_TIMEOUT = int(os.getenv('MAPDL_START_TIMEOUT', 30))

class ElasticBucklingService():

    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               n_x,
               csi_y
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1
        t_s = stiffened_plate.t_s
        h_s = stiffened_plate.h_s


        mapdl = launch_mapdl(
            run_location=MAPDL_RUN_LOCATION,
            nproc=4,
            override=True,
            loglevel="INFO",
            start_timeout=MAPDL_START_TIMEOUT,
            remove_temp_files=True,
            cleanup_on_exit=True,
        )

        try:
            stiffened_plate_analysis.elastic_buckling_status = IN_PROGRESS_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            self.load_previous_steps_analysis_db(mapdl, analysis_log_path, analysis_dir_path, analysis_db_path)
            self.apply_loads(mapdl, h_s, t_s, buckling_load_type, n_x, csi_y)
            self.solve_elastic_buckling(mapdl)
            n_cr, sigma_cr = self.calc_buckling_load_and_stress(mapdl, t_1)
            w_center = self.calc_z_deflection(mapdl, a, b)
            stiffened_plate_analysis.analysis_rst_file_path = analysis_log_path.replace('.txt', '.rst')
            mapdl.finish()
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elastic_buckling_status = COMPLETED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elastic_buckling_status = FAILED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        # TODO: Implementar lógica para cancelar a request
        finally:
            mapdl.exit()
        return n_cr, sigma_cr, w_center

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        file_name = re.sub(r'^.*/([^/]+)\.db$', r'\1', analysis_db_path)
        mapdl.filname(fname=file_name, key=0)
        mapdl.resume(fname=file_name, ext = 'db')
        mapdl.slashsolu()
        mapdl.allsel(labt="ALL", entity="ALL")

    def apply_loads(self, mapdl, h_s, t_s, buckling_load_type, n_x, csi_y):
        if self.is_stiffened_plate(h_s, t_s):
            if self.is_biaxial_buckling(buckling_load_type):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", csi_y * n_x)
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_x)
                mapdl.sfl(LINES_BORDA_TS, "PRESS", csi_y * n_x)
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_x)
        else:
            if self.is_biaxial_buckling(buckling_load_type):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", csi_y * n_x)
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)

    def solve_elastic_buckling(self, mapdl):
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.solve()
        mapdl.finish()
        mapdl.run("/SOLU")
        mapdl.run("ANTYPE,1")
        mapdl.bucopt("LANB", 1, 0, 0, "CENTER")
        mapdl.mxpand(1, 0, 0, 0, 0.001)
        mapdl.solve()
        mapdl.finish()
        mapdl.save(slab='ALL')
        mapdl.run("/POST1")

    def calc_buckling_load_and_stress(self, mapdl, t_1):
        n_cr = mapdl.post_processing.time
        sigma_cr = n_cr / float(t_1)
        mapdl.save(slab='ALL')
        return n_cr, sigma_cr

    def calc_z_deflection(self, mapdl, a, b):
        mapdl.mute = False
        mapdl.run(f"NSEL,S,NODE,,NODE({float(a)*0.5},{float(b)*0.5},0)")
        z_deflection = abs(mapdl.prnsol(item="U", comp="Z").to_list()[0][1])
        mapdl.mute = True
        return z_deflection

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00
