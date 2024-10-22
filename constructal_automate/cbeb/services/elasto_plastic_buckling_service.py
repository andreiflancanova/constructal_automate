import os
from cbeb.models import StiffenedPlateAnalysis
from cbeb.strategies.plate_strategy import PlateStrategy
from csg.models import StiffenedPlate
from cbeb.models.processing_status import ProcessingStatus
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
LOAD_MULTIPLIER = 1

MAPDL_RUN_LOCATION = os.getenv('MAPDL_RUN_LOCATION')
MAPDL_START_TIMEOUT = int(os.getenv('MAPDL_START_TIMEOUT', 30))

class ElastoPlasticBucklingService():

    def __init__(self, strategy: PlateStrategy):
        self.strategy = strategy

    def create(self,
               stiffened_plate: StiffenedPlate,
               stiffened_plate_analysis: StiffenedPlateAnalysis
               ):

        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        buckling_load_type = stiffened_plate_analysis.buckling_load_type.name
        rst_file_path = stiffened_plate_analysis.analysis_rst_file_path
        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1
        t_eq_ts = stiffened_plate.t_eq_ts
        t_eq_ls = stiffened_plate.t_eq_ls

        material = stiffened_plate_analysis.material


        mapdl = launch_mapdl(
            port=50052,
            run_location=MAPDL_RUN_LOCATION,
            nproc=4,
            override=True,
            loglevel="INFO",
            start_timeout=MAPDL_START_TIMEOUT,
            remove_temp_files=True,
            cleanup_on_exit=True,
        )

        try:
            stiffened_plate_analysis.elasto_plastic_buckling_status = IN_PROGRESS_PROCESSING_STATUS
            stiffened_plate_analysis.save()
            w0 = self.define_initial_deflection(b)
            self.load_previous_steps_analysis_db(mapdl, analysis_log_path, analysis_dir_path, analysis_db_path)
            self.define_nonlinear_analysis_params(mapdl, w0, rst_file_path, material, t_eq_ts, t_eq_ls)
            p_u_ts, p_u_ls = self.strategy.apply_load_for_elasto_plastic_buckling(mapdl, buckling_load_type, material, t_eq_ts, t_eq_ls)
            # p_u_ts, p_u_ls = self.strategy.apply_load_for_elasto_plastic_buckling(mapdl, buckling_load_type, material, t_1)
            
            try:
                self.solve_elasto_plastic_buckling(mapdl)
            except:
                mapdl = launch_mapdl(
                    port=50053,
                    run_location=MAPDL_RUN_LOCATION,
                    nproc=4,
                    override=True,
                    loglevel="INFO",
                    start_timeout=MAPDL_START_TIMEOUT,
                    remove_temp_files=True,
                    cleanup_on_exit=True,
                )
            n_u, sigma_u_ts, sigma_u_ls = self.calc_ultimate_buckling_load_and_stress(mapdl, buckling_load_type, t_eq_ts, t_eq_ls)
            # n_u, sigma_u_ts, sigma_u_ls = self.calc_ultimate_buckling_load_and_stress(mapdl, buckling_load_type, t_1)
            w_max = self.calc_z_deflection(mapdl, a, b)
            von_mises_dist_img_path, w_dist_img_path = self.plot_images(mapdl, analysis_db_path, material.yielding_stress)
            mapdl.finish()
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elasto_plastic_buckling_status = COMPLETED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
            stiffened_plate_analysis.elasto_plastic_buckling_status = FAILED_PROCESSING_STATUS
            stiffened_plate_analysis.save()
        finally:
            mapdl.exit()
        return p_u_ts, p_u_ls, n_u, sigma_u_ts, sigma_u_ls, w_max, von_mises_dist_img_path, w_dist_img_path

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        file_name = re.sub(r'^.*/([^/]+)\.db$', r'\1', analysis_db_path)
        mapdl.filname(fname=file_name, key=0)
        mapdl.resume(fname=file_name, ext = 'db')
        mapdl.slashsolu()


    def define_initial_deflection(self, b):
        return b/2000

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00

    def define_nonlinear_analysis_params(self, mapdl, w0, rst_file_path, material, t_eq_ts, t_eq_ls):
    # def define_nonlinear_analysis_params(self, mapdl, w0, rst_file_path, material, t_1):
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
        mapdl.nsubst(200, 400, 25)
        # mapdl.nsubst(1000, 500, 1)

        ## Limpar os dados de solução salvos no DB do ANSYS para salvar os resultados dos sub-passos na análise de flambagem elasto-plástica
        mapdl.outres("ERASE")

        ## Escrever os resultados de todos os sub-passos no DB do ANSYS
        mapdl.outres("ALL", "ALL")

        ## Definir o valor da carga de referência ao final do Passo de Carga (após todos os sub-passos terem sido executados)
        
        t_eq = max(t_eq_ts, t_eq_ls)

        n_e = round(material.yielding_stress*t_eq, 1)
        mapdl.time(n_e)
        # mapdl.neqit(neqit=100)

    def solve_elasto_plastic_buckling(self, mapdl):
        
        try:
            mapdl.solve()
        except:
            mapdl.save(slab='ALL')
            print("An error occurred, but the analysis will try to continue")
        mapdl.finish()

    def calc_ultimate_buckling_load_and_stress(self, mapdl, buckling_load_type, t_eq_ts, t_eq_ls):
    # def calc_ultimate_buckling_load_and_stress(self, mapdl, buckling_load_type, t_1):
        mapdl.post1()

        n_u = mapdl.result.time_values[len(mapdl.result.time_values)-2]
        
        if self.is_biaxial_buckling(buckling_load_type):
            sigma_u_ts = n_u/float(t_eq_ts)
            sigma_u_ls = n_u/float(t_eq_ls)
        else:
            sigma_u_ts = n_u/float(t_eq_ts)
            sigma_u_ls = 0
        
        # if self.is_biaxial_buckling(buckling_load_type):
        #     sigma_u_ts = n_u/float(t_1)
        #     sigma_u_ls = n_u/float(t_1)
        # else:
        #     sigma_u_ts = n_u/float(t_1)
        #     sigma_u_ls = 0
        mapdl.save()
        return n_u, sigma_u_ts, sigma_u_ls

    def calc_z_deflection(self, mapdl, a, b):
        mapdl.run(f"NSEL,S,NODE,,NODE({float(a)*0.5},{float(b)*0.5},0)")
        mapdl.set(lstep=1, sbstep=len(mapdl.result.time_values)-1)
        z_deflection = abs(mapdl.post_processing.nodal_displacement("Z")[0])
        return z_deflection

    def plot_images(self, mapdl, analysis_db_path, material_yielding_stress):
        VON_MISES_IMG_SUFFIX = '_von_mises_dist.png'
        W_IMG_SUFFIX = '_w_dist.png'

        von_mises_dist_img_path = analysis_db_path.replace('.db', VON_MISES_IMG_SUFFIX)
        w_dist_img_path = analysis_db_path.replace('.db', W_IMG_SUFFIX)

        mapdl.result.plot_principal_nodal_stress(
            len(mapdl.result.time_values)-2,
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
            # screenshot=von_mises_dist_img_path,
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
            len(mapdl.result.time_values)-2,
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
            screenshot=von_mises_dist_img_path,
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
            len(mapdl.result.time_values)-2,
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
            screenshot=w_dist_img_path,
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
        

        return von_mises_dist_img_path, w_dist_img_path
