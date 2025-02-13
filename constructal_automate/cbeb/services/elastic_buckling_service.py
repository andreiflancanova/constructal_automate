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

MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH')
MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH')

MAPDL_GRPC_HOST = os.getenv('MAPDL_GRPC_HOST')
MAPDL_GRPC_PORT = os.getenv('MAPDL_GRPC_PORT')
MAPDL_LOG_LEVEL_ELASTIC_BUCKLING = os.getenv('MAPDL_LOG_LEVEL_ELASTIC_BUCKLING')
MAPDL_NUMBER_OF_PROCESSORS = os.getenv('MAPDL_NUMBER_OF_PROCESSORS')

class ElasticBucklingService():

    def __init__(self, strategy: PlateStrategy):
        self.strategy = strategy

    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_host_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_log_container_path = analysis_log_host_path.replace(MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH, MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH)
        analysis_db_path = analysis_log_host_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        t_1 = stiffened_plate.t_1

        mapdl = launch_mapdl(
            run_location=MAPDL_RUN_LOCATION,
            ip=MAPDL_GRPC_HOST,
            port=MAPDL_GRPC_PORT,
            start_instance=False,
            nproc=MAPDL_NUMBER_OF_PROCESSORS,
            override=True,
            loglevel=MAPDL_LOG_LEVEL_ELASTIC_BUCKLING,
            remove_temp_files=True,
            cleanup_on_exit=True
        )

        try:
            stiffened_plate_analysis.elastic_buckling_status = IN_PROGRESS_PROCESSING_STATUS
            self.load_previous_steps_analysis_db(mapdl, analysis_log_container_path, analysis_dir_path, analysis_db_path)
            self.strategy.apply_load_for_elastic_buckling(mapdl, buckling_load_type)
            self.solve_pre_buckling_static_analysis(mapdl)
            self.solve_elastic_buckling(mapdl)
            n_cr, sigma_cr  = self.calc_buckling_stress(mapdl, t_1)
            w_center = self.calc_z_deflection(mapdl)
            stiffened_plate_analysis.analysis_rst_file_path = analysis_log_host_path.replace('.txt', '.rst')
            stiffened_plate_analysis.elastic_buckling_status = COMPLETED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            mapdl.save(slab='ALL')
            mapdl.finish()
            mapdl._close_apdl_log()
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elastic_buckling_status = FAILED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        return n_cr, sigma_cr, w_center

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_container_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_container_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        file_name = re.sub(r'^.*/([^/]+)\.db$', r'\1', analysis_db_path)
        mapdl.filname(fname=file_name, key=0)
        mapdl.resume(fname=file_name, ext = 'db')

    def solve_pre_buckling_static_analysis(self, mapdl):
        
        mapdl.slashsolu()

        ## Selecionar tudo para resolver a análise estática pré-flambagem elástica
        mapdl.allsel(labt="ALL", entity="ALL")

        ## Resolver análise estática pré-flambagem elástica
        mapdl.solve()

        ## Encerrar /SOLU da análise estática pré-flambagem elástica
        mapdl.finish()

    def solve_elastic_buckling(self, mapdl):

        # Entrar no /SOLU (Solution)
        mapdl.slashsolu()

        ## Tipo de análise: Análise de flambagem elástica (É com pré-tensão)
        mapdl.antype(antype="BUCKLE")

        ## Usar o método Block Lanczos
        mapdl.bucopt("LANB", 1, 0, 0, "CENTER")

        ## Extrair somente o 1º modo de flambagem
        mapdl.mxpand(1, 0, 0, 0, 0.001)

        ## Resolver análise de flambagem elástica
        mapdl.solve()

        ## Encerrar /SOLU da análise de flambagem elástica
        mapdl.finish()

    def calc_buckling_stress(self, mapdl, t_1):
        mapdl.post1()
        n_cr = mapdl.post_processing.time
        sigma_cr = n_cr/float(t_1)
        return n_cr, sigma_cr

    def calc_z_deflection(self, mapdl):
        mapdl.set(lstep=1, sbstep=1)
        negative_z_deflection = min(mapdl.post_processing.nodal_displacement("Z"))
        abs_negative_z_deflection = abs(negative_z_deflection)

        positive_z_deflection = max(mapdl.post_processing.nodal_displacement("Z"))

        mapdl.finish()

        if abs_negative_z_deflection > positive_z_deflection:
            z_deflection = abs_negative_z_deflection
        else:
            z_deflection = positive_z_deflection
        return z_deflection

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00
