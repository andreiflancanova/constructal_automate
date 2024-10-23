import os
from cbeb.models import StiffenedPlateAnalysis
from cbeb.models.processing_status import ProcessingStatus
from cbeb.strategies.plate_strategy import PlateStrategy
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
ELASTIC_BUCKLING_APPLIED_LOAD = 1

class ElasticBucklingService():

    def __init__(self, strategy: PlateStrategy):
        self.strategy = strategy

    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.plate.t_1
        # length_ts = stiffened_plate.length_ts
        # length_ls = stiffened_plate.length_ls
        # area_ts = stiffened_plate.area_ts
        # area_ls = stiffened_plate.area_ls

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
            self.load_previous_steps_analysis_db(mapdl, analysis_log_path, analysis_dir_path, analysis_db_path)
            self.strategy.apply_load_for_elastic_buckling(mapdl, buckling_load_type)
            self.solve_elastic_buckling(mapdl)
            # n_cr, sigma_cr_ts, sigma_cr_ls  = self.calc_buckling_load_and_stress(mapdl, buckling_load_type, length_ts, length_ls, area_ts, area_ls)
            # n_cr, sigma_cr_ts, sigma_cr_ls  = self.calc_buckling_load_and_stress(mapdl, buckling_load_type, t_1)
            n_cr, sigma_cr  = self.calc_buckling_load_and_stress(mapdl, buckling_load_type, t_1)
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
        finally:
            mapdl.exit()
        # return n_cr, sigma_cr_ts, sigma_cr_ls, w_center
        return n_cr, sigma_cr, w_center

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        file_name = re.sub(r'^.*/([^/]+)\.db$', r'\1', analysis_db_path)
        mapdl.filname(fname=file_name, key=0)
        mapdl.resume(fname=file_name, ext = 'db')
        mapdl.slashsolu()

    def solve_elastic_buckling(self, mapdl):

        ## Selecionar tudo para resolver a análise estática pré-flambagem elástica
        mapdl.allsel(labt="ALL", entity="ALL")

        ## Resolver análise estática pré-flambagem elástica
        mapdl.solve()

        ## Encerrar /SOLU da análise estática pré-flambagem elástica
        mapdl.finish()

        # Entrar no /SOLU (Solution)
        mapdl.slashsolu()

        ## Tipo de análise: Análise de flambagem elástica (É com pré-tensão?)
        mapdl.antype(antype="BUCKLE")

        ## Usar o método Block Lanczos
        mapdl.bucopt("LANB", 1, 0, 0, "CENTER")

        ## Extrair somente o 1º modo de flambagem
        mapdl.mxpand(1, 0, 0, 0, 0.001)

        ## Resolver análise de flambagem elástica
        mapdl.solve()

        ## Encerrar /SOLU da análise de flambagem elástica
        mapdl.finish()
        mapdl.save(slab='ALL')
        # mapdl.run("/POST1")
        mapdl.post1()

    # def calc_buckling_load_and_stress(self, mapdl, buckling_load_type, length_ts, length_ls, area_ts, area_ls):
    def calc_buckling_load_and_stress(self, mapdl, buckling_load_type, t_1):
        n_cr = mapdl.post_processing.time

        if self.is_biaxial_buckling(buckling_load_type):
            # sigma_cr_ts = n_cr * (float(length_ts)/float(area_ts))
            # sigma_cr_ls = n_cr * (float(length_ls)/float(area_ls))
            sigma_cr = n_cr/float(t_1)
            # sigma_cr_ts = n_cr/float(t_1)
            # sigma_cr_ls = n_cr/float(t_1)
        else:
            # sigma_cr_ts = n_cr * (float(length_ts)/float(area_ts))
            sigma_cr = n_cr/float(t_1)
            # sigma_cr_ts = n_cr/float(t_1)
            # sigma_cr_ls = 0
        mapdl.save(slab='ALL')
        # return n_cr, sigma_cr_ts, sigma_cr_ls
        return n_cr, sigma_cr

    def calc_z_deflection(self, mapdl, a, b):
        mapdl.run(f"NSEL,S,NODE,,NODE({float(a)*0.5},{float(b)*0.5},0)")
        z_deflection = abs(mapdl.prnsol(item="U", comp="Z").to_list()[0][1])
        return z_deflection

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00
