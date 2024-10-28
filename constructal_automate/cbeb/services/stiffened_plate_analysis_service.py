import os
from cbeb.models.material import Material
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.models.processing_status import ProcessingStatus
from cbeb.strategies.plate_strategy import PlateStrategy
from csg.models.stiffened_plate import StiffenedPlate
from pathlib import Path
from ansys.mapdl.core import launch_mapdl

MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH')

ENRIJECEDOR_LONGITUDINAL_PRE_APTN = os.getenv('ENRIJECEDOR_LONGITUDINAL_PRE_APTN')
ENRIJECEDOR_TRANSVERSAL_PRE_APTN = os.getenv('ENRIJECEDOR_TRANSVERSAL_PRE_APTN')

ENRIJECEDORES_LONGITUDINAIS_PRE_APTN = os.getenv('ENRIJECEDORES_LONGITUDINAIS_PRE_APTN')
ENRIJECEDORES_TRANSVERSAIS_PRE_APTN = os.getenv('ENRIJECEDORES_TRANSVERSAIS_PRE_APTN')
PLACA_PRE_APTN = os.getenv('PLACA_PRE_APTN')
ENRIJECEDORES_LONGITUDINAIS_POS_APTN = os.getenv('ENRIJECEDORES_LONGITUDINAIS_POS_APTN')
ENRIJECEDORES_TRANSVERSAIS_POS_APTN = os.getenv('ENRIJECEDORES_TRANSVERSAIS_POS_APTN')
PLACA_POS_APTN = os.getenv('PLACA_POS_APTN')
CONJUNTO = os.getenv('CONJUNTO')

KP_INFERIOR_ESQUERDO = os.getenv('KP_INFERIOR_ESQUERDO')
KP_SUPERIOR_ESQUERDO = os.getenv('KP_SUPERIOR_ESQUERDO')
KP_INFERIOR_DIREITO = os.getenv('KP_INFERIOR_DIREITO')
KP_SUPERIOR_DIREITO = os.getenv('KP_SUPERIOR_DIREITO')

LINES_CONTORNO_PLACA = os.getenv('LINES_CONTORNO_PLACA')
LINES_CONTORNO_PLACA_ESQUERDA = os.getenv('LINES_CONTORNO_PLACA_ESQUERDA')
LINES_CONTORNO_PLACA_DIREITA = os.getenv('LINES_CONTORNO_PLACA_DIREITA')
LINES_CONTORNO_PLACA_TS = os.getenv('LINES_CONTORNO_PLACA_TS')
LINES_CONTORNO_PLACA_INFERIOR = os.getenv('LINES_CONTORNO_PLACA_INFERIOR')
LINES_CONTORNO_PLACA_SUPERIOR = os.getenv('LINES_CONTORNO_PLACA_SUPERIOR')
LINES_CONTORNO_PLACA_LS = os.getenv('LINES_CONTORNO_PLACA_LS')
LINES_BORDA_LS_ESQUERDA = os.getenv('LINES_BORDA_LS_ESQUERDA')
LINES_BORDA_LS_DIREITA = os.getenv('LINES_BORDA_LS_DIREITA')
LINES_BORDA_LS = os.getenv('LINES_BORDA_LS')
LINES_BORDA_TS_INFERIOR = os.getenv('LINES_BORDA_TS_INFERIOR')
LINES_BORDA_TS_SUPERIOR = os.getenv('LINES_BORDA_TS_SUPERIOR')
LINES_BORDA_TS = os.getenv('LINES_BORDA_TS')
LINES_BORDA_ENRIJECEDORES = os.getenv('LINES_BORDA_ENRIJECEDORES')
PENDING_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Pending')

OFFSET_PERCENTUAL_BORDA_INICIAL = 0.40
OFFSET_PERCENTUAL_BORDA_FINAL = 0.60
OFFSET_PERCENTUAL_Z_INICIAL = 0.40
OFFSET_PERCENTUAL_Z_FINAL = 0.60

MAPDL_RUN_LOCATION = os.getenv('MAPDL_RUN_LOCATION')
MAPDL_START_TIMEOUT = int(os.getenv('MAPDL_START_TIMEOUT', 30))

class StiffenedPlateAnalysisService():

    def __init__(self, strategy: PlateStrategy):
        self.strategy = strategy

    def format_field(self, value, decimal_places):
        # Formata o número com as casas decimais especificadas
        formatted_value = f"{value:.{decimal_places}f}"
        
        # Remove a parte decimal se for zero
        if formatted_value.endswith("0" * decimal_places):
            return formatted_value.split(".")[0]
        else:
            return formatted_value.rstrip("0").rstrip(".")
        
    def format_filename(self, filename):
        # Define os pontos onde os underscores serão inseridos
        insertion_points = ["k", "MS", "SP"]
        
        # Se o comprimento do nome for menor que 32 caracteres, adiciona os underscores
        if len(filename) < 32:
            remaining_chars = 32 - len(filename)
            
            # Verifica se há espaço suficiente para inserir os underscores
            if remaining_chars >= 3:
                offset = 0  # Deslocamento causado pela inserção de underscores
                for point in insertion_points:
                    index = filename.find(point)
                    # Insere o underscore antes do ponto de inserção e atualiza o filename
                    if index != -1:
                        filename = filename[:index + offset] + "_" + filename[index + offset:]
                        # offset += 1  # Atualiza o deslocamento para a próxima inserção
                    
        # Garante que o nome final não exceda 32 caracteres
        return filename[:32]

    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               material: Material
               ):

        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        stiffened_plate_id = stiffened_plate.id
        E = material.young_modulus
        poisson_ratio = material.poisson_ratio
        t_1 = stiffened_plate.t_1
        t_s = stiffened_plate.t_s
        h_s = float(stiffened_plate.h_s) + float(t_1)*0.5
        phi = self.format_field(stiffened_plate.phi, 2)
        k = self.format_field(stiffened_plate.k, 3)
        N_ts = stiffened_plate.N_ts
        N_ls = stiffened_plate.N_ls
        mesh_size = self.format_field(stiffened_plate_analysis.mesh_size, 1)
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.id
        material_id = stiffened_plate_analysis.material.id

        analysis_name = self.format_filename(f'BL{buckling_load_type}M{material_id}P{phi}L{N_ls}T{N_ts}k{k}MS{mesh_size}SP{stiffened_plate_id}')
        self.create_dir_structure(stiffened_plate_analysis.case_study, analysis_name)

        analysis_cwd_path = f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{stiffened_plate_analysis.case_study}/{analysis_name}'
        analysis_log_path = f'{analysis_cwd_path}/{analysis_name}.txt'


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
            self.create_mapdl_initial_files(mapdl, analysis_name, analysis_cwd_path, analysis_log_path, stiffened_plate_analysis)

            self.strategy.define_element_type_section_and_material(mapdl, E, poisson_ratio, t_1, t_s)
            self.strategy.define_geometry(mapdl, a, b, t_1, N_ts, N_ls, h_s)
            self.strategy.define_discretization(mapdl, mesh_size, stiffened_plate_analysis)
            self.strategy.define_components_and_apply_boundary_conditions(mapdl, a, b, t_1)

            mapdl.save(slab='ALL')
            mapdl._close_apdl_log()
        finally:
            mapdl.exit()

    def create_dir_structure(self, case_study_name, analysis_name):

        self.ensure_dir_exists(MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH)

        case_study_dir_absolute_path = f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{case_study_name}'
        self.ensure_dir_exists(case_study_dir_absolute_path)

        analysis_dir_absolute_path_string = f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{case_study_name}/{analysis_name}'
        self.ensure_dir_exists(analysis_dir_absolute_path_string)
        self.remove_previous_analysis_files(analysis_dir_absolute_path_string)

    def ensure_dir_exists(self, absolute_path_string):
        absolute_path = Path(absolute_path_string)
        if Path.is_dir(absolute_path):
            pass
        else:
            Path.mkdir(absolute_path)

    def remove_previous_analysis_files(self, analysis_dir_absolute_path_string):
        analysis_dir_absolute_path = Path(analysis_dir_absolute_path_string)
        if Path.is_dir(analysis_dir_absolute_path):
            for file_name in os.listdir(analysis_dir_absolute_path_string):
                file = f'{analysis_dir_absolute_path_string}/{file_name}'
                if os.path.isfile(file):
                    os.remove(file)
            print('Previous analysis files were successfully removed.')
        else:
            print('No previous analysis files to remove.')

    def create_mapdl_initial_files(self, mapdl, analysis_name, analysis_cwd_path, analysis_log_path, stiffened_plate_analysis):
        try:
            mapdl.clear()
            mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
            mapdl.cwd(analysis_cwd_path)
            mapdl.filname(fname=analysis_name, key=1)
            mapdl.title(analysis_name)
        finally:
            stiffened_plate_analysis.analysis_dir_path = analysis_cwd_path
            stiffened_plate_analysis.analysis_lgw_file_path = analysis_log_path
            stiffened_plate_analysis.elastic_buckling_status = PENDING_PROCESSING_STATUS
            stiffened_plate_analysis.elasto_plastic_buckling_status = PENDING_PROCESSING_STATUS
            stiffened_plate_analysis.save()
