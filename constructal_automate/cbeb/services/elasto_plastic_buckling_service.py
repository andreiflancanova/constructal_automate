import os
from cbeb.models import StiffenedPlateAnalysis
from cbeb.strategies.plate_strategy import PlateStrategy
from csg.models import StiffenedPlate
from cbeb.models.processing_status import ProcessingStatus
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core import launch_mapdl
from rest_framework.exceptions import APIException
import re
import time

LINES_CONTORNO_PLACA_TS = os.getenv('LINES_CONTORNO_PLACA_TS')
LINES_CONTORNO_PLACA_LS = os.getenv('LINES_CONTORNO_PLACA_LS')
LINES_BORDA_LS = os.getenv('LINES_BORDA_LS')
LINES_BORDA_TS = os.getenv('LINES_BORDA_TS')
IN_PROGRESS_PROCESSING_STATUS = ProcessingStatus.objects.get(name='In Progress')
COMPLETED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Completed')
FAILED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Failed')
CANCELLED_PROCESSING_STATUS = ProcessingStatus.objects.get(name='Cancelled')

MAPDL_RUN_LOCATION = os.getenv('MAPDL_RUN_LOCATION')
MAPDL_START_TIMEOUT = int(os.getenv('MAPDL_START_TIMEOUT', 240))
MAPDL_GRPC_HOST = os.getenv('MAPDL_GRPC_HOST')
MAPDL_GRPC_PORT = os.getenv('MAPDL_GRPC_PORT')
MAPDL_LOG_LEVEL_ELASTO_PLASTIC_BUCKLING = os.getenv('MAPDL_LOG_LEVEL_ELASTO_PLASTIC_BUCKLING')

MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH')
MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH')
MAPDL_NUMBER_OF_PROCESSORS = os.getenv('MAPDL_NUMBER_OF_PROCESSORS')
NSUBST_NSBSTP = 200
NSUBST_NSBMX = 400
NSUBST_NSBMN = 50

class ElastoPlasticBucklingService():

    def __init__(self, strategy: PlateStrategy):
        self.strategy = strategy

    def create(self,
               stiffened_plate: StiffenedPlate,
               stiffened_plate_analysis: StiffenedPlateAnalysis
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_host_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_log_container_path = analysis_log_host_path.replace(MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH, MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH)
        analysis_db_host_path = analysis_log_host_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        rst_file_path = stiffened_plate_analysis.analysis_rst_file_path
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1

        material = stiffened_plate_analysis.material

        mapdl = launch_mapdl(
            run_location=MAPDL_RUN_LOCATION,
            ip=MAPDL_GRPC_HOST,
            port=MAPDL_GRPC_PORT,
            start_instance=False,
            nproc=MAPDL_NUMBER_OF_PROCESSORS,
            override=True,
            loglevel=MAPDL_LOG_LEVEL_ELASTO_PLASTIC_BUCKLING,
            remove_temp_files=True,
            cleanup_on_exit=True
        )

        try:
            stiffened_plate_analysis.elasto_plastic_buckling_status = IN_PROGRESS_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            w0 = self.define_initial_deflection(b)
            self.load_previous_steps_analysis_db(mapdl, analysis_log_container_path, analysis_dir_path, analysis_db_host_path)
            self.define_nonlinear_analysis_prep7(mapdl, w0, rst_file_path, material)
            self.define_nonlinear_solution_aspects(mapdl, material, t_1)
            p_u = self.strategy.apply_load_for_elasto_plastic_buckling(mapdl, buckling_load_type, material, t_1)
            print('Ro que deu a ideia deste print aqui')
            self.solve_elasto_plastic_buckling(mapdl)
            mapdl.post1()
            n_u, sigma_u = self.calc_ultimate_buckling_load_and_stress(mapdl, t_1, p_u)
            w_max = self.calc_z_deflection(mapdl, p_u)
            von_mises_dist_img_path, w_dist_img_path = self.plot_images(mapdl, analysis_db_host_path, material.yielding_stress, p_u)
            mapdl.finish()
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elasto_plastic_buckling_status = COMPLETED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            mapdl.save(slab='ALL')
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elasto_plastic_buckling_status = FAILED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        # finally:
        #     print('Andrei')
        #     print(locals())
        #     if 'ip' not in locals() or locals()['ip'] is None:
        #         mapdl.exit()
        return p_u, n_u, sigma_u, w_max, von_mises_dist_img_path, w_dist_img_path

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_container_path, analysis_dir_path, analysis_db_host_path):
        mapdl.open_apdl_log(filename=analysis_log_container_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        file_name = re.sub(r'^.*/([^/]+)\.db$', r'\1', analysis_db_host_path)
        mapdl.filname(fname=file_name, key=0)
        mapdl.resume(fname=file_name, ext = 'db')


    def define_initial_deflection(self, b):
        return b/2000

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00

    def define_nonlinear_analysis_prep7(self, mapdl, w0, rst_file_path, material):
        mapdl.allsel(labt="ALL", entity="ALL")

        # Entrar no /PREP7 para análise de flambagem elasto-plástica
        mapdl.prep7()

        ## Aumentar o limite de erros que a análise tolera antes de encerrar
        mapdl.run("/NERR,1000,99999999")

        ## Atualizar geometria do problema com base na análise elástica pelo fator w0 = B/2000
        mapdl.upgeom(factor=w0, lstep="LAST", sbstep="LAST", fname=rst_file_path.removesuffix(".rst"), ext="")

        ## Fornecer informações do material
        mapdl.tb(lab="BISO", mat=1, ntemp=1, npts=2)
        mapdl.tbtemp(0)
        mapdl.tbdata("", material.yielding_stress, material.tang_modulus, "")
        mapdl.finish()

    def define_nonlinear_solution_aspects(self, mapdl, material, t_1):
        # Entrar no /SOLU para análise de flambagem elasto-plástica
        mapdl.slashsolu()

        ## Tipo de análise: Análise estática de flambagem elasto-plástica com pré-tensão:
        mapdl.antype(antype="STATIC")
        mapdl.pstres(1)

        ## Habilitar grandes deslocamentos
        mapdl.nlgeom(key="ON")

        ## O ANSYS Mechanical APDL Structural Analysis Guide (pg.242) recomenda desabilitar o Nonlinear Predictor para análise de flambagem 
        mapdl.pred(sskey="OFF")

        ## Definir o número de sub-passos a serem utilizados para o Passo de Carga atual
        mapdl.nsubst(NSUBST_NSBSTP, NSUBST_NSBMX, NSUBST_NSBMN)

        ## Limpar os dados de solução salvos no DB do ANSYS para salvar os resultados dos sub-passos na análise de flambagem elasto-plástica
        print('Antes do OUTRES ERASE')
        mapdl.outres("ERASE")
        print('Depois do OUTRES ERASE')
        
        ## Escrever os resultados de todos os sub-passos no DB do ANSYS
        print('Antes do OUTRES ALL')
        mapdl.outres("ALL", "ALL")
        print('Depois do OUTRES ALL')
        ## Definir o valor da carga de referência ao final do Passo de Carga (após todos os sub-passos terem sido executados)
        n_e = round(material.yielding_stress*t_1, 1)
        mapdl.time(n_e)

    def solve_elasto_plastic_buckling(self, mapdl):
        try:
            print('Entering the elasto-plastic buckling SOLVE step')
            mapdl.solve()
        except Exception as e:
            print(f"An error occurred during the SOLVE step: {e}")
        mapdl.finish()

    def calc_ultimate_buckling_load_and_stress(self, mapdl, t_1, p_u):
        print(f"Antes de pegar o array de post_processing")
        position = self.calc_post_processing_frequency_values_arr_position_for_ultimate_load(mapdl, p_u)
        n_u = mapdl.post_processing.frequency_values[position]

        sigma_u = n_u/float(t_1)

        return n_u, sigma_u
    
    def calc_post_processing_frequency_values_arr_position_for_ultimate_load(self, mapdl, p_u):
        try:
            print("first_to_last_arr_position")
            first_to_last_arr_position = len(mapdl.post_processing.frequency_values)-2
            
            print("first_to_last_load")
            first_to_last_load = mapdl.post_processing.frequency_values[first_to_last_arr_position]

            print("second_to_last_arr_position")
            second_to_last_arr_position = len(mapdl.post_processing.frequency_values)-3
            print("second_to_last_load")
            second_to_last_load = mapdl.post_processing.frequency_values[second_to_last_arr_position]
        except IndexError as e:
            print(e)
            raise APIException(detail=str(e), code=500)

        diff_between_loads = first_to_last_load - second_to_last_load
        load_increment = p_u/NSUBST_NSBMX

        if diff_between_loads > load_increment:
            return first_to_last_arr_position
        else:
            return second_to_last_arr_position


    def calc_z_deflection(self, mapdl, p_u):
        position = self.calc_post_processing_frequency_values_arr_position_for_substep(mapdl, p_u)
        mapdl.set(lstep=1, sbstep=position)
        negative_z_deflection = min(mapdl.post_processing.nodal_displacement("Z"))
        abs_negative_z_deflection = abs(negative_z_deflection)

        positive_z_deflection = max(mapdl.post_processing.nodal_displacement("Z"))

        if abs_negative_z_deflection > positive_z_deflection:
            z_deflection = abs_negative_z_deflection
        else:
            z_deflection = positive_z_deflection
        return z_deflection
    
    def calc_post_processing_frequency_values_arr_position_for_substep(self, mapdl, p_u):
        return self.calc_post_processing_frequency_values_arr_position_for_ultimate_load(mapdl, p_u) + 1

    def plot_images(self, mapdl, analysis_db_host_path, material_yielding_stress, p_u):
        VON_MISES_IMG_SUFFIX = '_von_mises_dist.png'
        W_IMG_SUFFIX = '_w_dist.png'

        von_mises_dist_img_host_path = analysis_db_host_path.replace('.db', VON_MISES_IMG_SUFFIX)
        von_mises_dist_img_container_path = von_mises_dist_img_host_path.replace(MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH, MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH)
        w_dist_img_host_path = analysis_db_host_path.replace('.db', W_IMG_SUFFIX)
        w_dist_img_container_path = w_dist_img_host_path.replace(MAPDL_OUTPUT_BASEDIR_ABSOLUTE_HOST_PATH, MAPDL_OUTPUT_BASEDIR_ABSOLUTE_CONTAINER_PATH)

        position = self.calc_post_processing_frequency_values_arr_position_for_ultimate_load(mapdl, p_u)

        mapdl.result.plot_principal_nodal_stress(
            position,
            "SEQV",
            lighting=False,
            cpos="iso",
            background="white",
            text_color="black",
            add_text=False,
            show_edges=True,          
            edge_color="black",       
            cmap="jet",              
            rng=[0, material_yielding_stress],
            line_width=1.0,           
            off_screen=True,
            # screenshot=von_mises_dist_img_container_path,
            show_scalar_bar=True,
            # show_displacement=True,
            # displacement_factor=2,
            scalar_bar_args={
                "title": "Tensões (MPa)",
                "vertical": False,
                "fmt":"%8.2f",
                "width": 0.4,
                "position_x": 0.55,
                "position_y": 0.15,
                "title_font_size": 20,
                "label_font_size": 16,
            }
        )

        mapdl.result.plot_principal_nodal_stress(
            position,
            "SEQV",
            lighting=False,
            cpos="iso",
            background="white",
            text_color="black",
            add_text=False,
            show_edges=True,          
            edge_color="black",       
            cmap="jet",              
            rng=[0, material_yielding_stress],
            line_width=1.0,           
            off_screen=True,
            screenshot=von_mises_dist_img_container_path,
            show_scalar_bar=True,
            # show_displacement=True,
            # displacement_factor=2,
            scalar_bar_args={
                "title": "Tensões (MPa)",
                "vertical": False,
                "fmt":"%8.2f",
                "width": 0.4,
                "position_x": 0.55,
                "position_y": 0.15,
                "title_font_size": 20,
                "label_font_size": 16,
            }
        )

        mapdl.result.plot_nodal_displacement(
            position,
            "UZ",
            lighting=False,
            cpos="iso",
            background="white",
            text_color="black",
            add_text=False,
            show_edges=True,
            edge_color="black",
            cmap="jet",
            line_width=1.0,
            off_screen=True,
            screenshot=w_dist_img_container_path,
            show_scalar_bar=True,
            scalar_bar_args={
                "title": "Deslocamento em Z (mm)",
                "vertical": False,
                "fmt":"%8.2f",
                "width": 0.4,
                "position_x": 0.55,
                "position_y": 0.15,
                "title_font_size": 20,
                "label_font_size": 16,
            }
        )

        return von_mises_dist_img_host_path, w_dist_img_host_path
