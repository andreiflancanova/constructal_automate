import os
from cbeb.config.mapdl_connection_pool import MapdlConnectionPool
from cbeb.models.material import Material
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from csg.models.stiffened_plate import StiffenedPlate
from dotenv import load_dotenv
from pathlib import Path
from django.shortcuts import get_object_or_404

load_dotenv()
MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH')

#TODO: Remover Ansys Components para um arquivo externo
ENRIJECEDOR_LONGITUDINAL = "enrijecedor_longitudinal"
ENRIJECEDOR_TRANSVERSAL = "enrijecedor_transversal"

ENRIJECEDORES_LONGITUDINAIS = "enrijecedores_longitudinais"
ENRIJECEDORES_TRANSVERSAIS = "enrijecedores_transversais"
PLACA = "placa"
CONJUNTO = "conjunto"

KP_INFERIOR_ESQUERDO = "kp_inferior_esquerdo"
KP_SUPERIOR_ESQUERDO = "kp_superior_esquerdo"
KP_INFERIOR_DIREITO = "kp_inferior_direito"
KP_SUPERIOR_DIREITO = "kp_superior_direito"

LINES_CONTORNO_PLACA = "lines_contorno_placa"
LINES_CONTORNO_PLACA_ESQUERDA = "lines_contorno_placa_esquerda"
LINES_CONTORNO_PLACA_DIREITA = "lines_contorno_placa_direita"
LINES_CONTORNO_PLACA_TS = "lines_contorno_placa_ts"
LINES_CONTORNO_PLACA_INFERIOR = "lines_contorno_placa_inferior"
LINES_CONTORNO_PLACA_SUPERIOR = "lines_contorno_placa_superior"
LINES_CONTORNO_PLACA_LS = "lines_contorno_placa_ls"
LINES_BORDA_LS_ESQUERDA = "lines_borda_ls_esquerda"
LINES_BORDA_LS_DIREITA = "lines_borda_ls_direita"
LINES_BORDA_LS = "lines_borda_ls"
LINES_BORDA_TS_INFERIOR = "lines_borda_ts_inferior"
LINES_BORDA_TS_SUPERIOR = "lines_borda_ts_superior"
LINES_BORDA_TS = "lines_borda_ts"
LINES_BORDA_ENRIJECEDORES = "lines_borda_enrijecedores"


class StiffenedPlateAnalysisService():

    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               material: Material
               ):

        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        E = material.young_modulus
        poisson_ration = material.poisson_ration
        t_1 = stiffened_plate.t_1
        t_s = stiffened_plate.t_s
        h_s = stiffened_plate.h_s
        phi = stiffened_plate.phi
        k = stiffened_plate.k
        N_ts = stiffened_plate.N_ts
        N_ls = stiffened_plate.N_ls
        mesh_size = stiffened_plate_analysis.mesh_size
        
        analysis_name = f'phi_{phi}_Nls_{N_ls}_Nts_{N_ts}_k_{k}'
        self.create_dir_structure(stiffened_plate_analysis.case_study, analysis_name)

        mapdl_pool = MapdlConnectionPool()
        mapdl_connection_wrapper = mapdl_pool.get_connection_wrapper()
        mapdl = mapdl_connection_wrapper.connection

        #TODO: Ver cenários onde a placa é retangular sem enrijecedor, pois está dando erro

        try:
            mapdl.run("WPSTYLE,,,,,,,,0")
            mapdl.cwd(f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{stiffened_plate_analysis.case_study}/{analysis_name}')
            mapdl.save(slab='ALL')
            # mapdl.open_apdl_log(f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{stiffened_plate_analysis.case_study}/{analysis_name}')
            mapdl.open_apdl_log(f'{MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH}/{stiffened_plate_analysis.case_study}/{analysis_name}/{analysis_name}.txt')
            mapdl.filname(fname=analysis_name, key=0)
            mapdl.title(analysis_name)

            mapdl.prep7()

            mapdl._run("/NOPR")
            mapdl.keyw("PR_SET", 1)
            mapdl.keyw("PR_STRUC", 1)
            mapdl.keyw("PR_THERM", 0)
            mapdl.keyw("PR_FLUID", 0)
            mapdl.keyw("PR_ELMAG", 0)
            mapdl.keyw("MAGNOD", 0)
            mapdl.keyw("MAGEDG", 0)
            mapdl.keyw("MAGHFE", 0)
            mapdl.keyw("MAGELC", 0)
            mapdl.keyw("PR_MULTI", 0)
            mapdl.run("/GO")
            
            # Parâmetros de discretização
            ## Elemento Finito
            mapdl.et(1, "SHELL281")
            
            ## Material
            mapdl.mptemp("", "", "")
            mapdl.mptemp(1, 0)
            mapdl.mpdata("EX", 1, "", E)
            mapdl.mpdata("PRXY", 1, "", poisson_ration)
            
            # Seções
            ## Seção da placa
            mapdl.run("sect,1,shell")
            mapdl.secdata(t_1, 1, 0, 3)
            mapdl.secoffset("TOP")
            mapdl.seccontrol("", "", "", "", "", "")
            
            ## Seção dos enrijecedores transversais
            mapdl.run("sect,2,shell")
            mapdl.secdata(t_s, 1, 0, 3)
            mapdl.secoffset("MID")
            mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)
            
            ## Seção dos enrijecedores longitudinais
            mapdl.run("sect,3,shell")
            mapdl.secdata(t_s, 1, 0, 3)
            mapdl.secoffset("MID")
            mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)
            
            
            #Definir espaçamento dos enrijecedores
            
            a_ts = float(round(a/(N_ts+1), 3))
            b_ls = float(round(b/(N_ls+1), 3))
            
            #Definir keypoints
            mapdl.k(1, a_ts, 0, 0)
            mapdl.k(2, a_ts, b, 0)
            mapdl.k(3, a_ts, b, h_s)
            mapdl.k(4, a_ts, 0, h_s)
            mapdl.k(5, 0, b_ls, 0)
            mapdl.k(6, a, b_ls, 0)
            mapdl.k(7, a, b_ls, h_s)
            mapdl.k(8, 0, b_ls, h_s)

            #Criar área do enrijecedor longitudinal
            mapdl.flst(2, 4, 3)
            mapdl.fitem(2, 1)
            mapdl.fitem(2, 2)
            mapdl.fitem(2, 3)
            mapdl.fitem(2, 4)
            mapdl.a("P51X")
            
            #Selection Logic para criar os enrijecedores
            # Enrijecedores Transversais
            mapdl.asel("S", "LOC", "X", 0.99*a_ts, 1.01*a_ts)
            mapdl.cm(ENRIJECEDOR_TRANSVERSAL, "AREA")
            mapdl.agen(itime=N_ts, na1=ENRIJECEDOR_TRANSVERSAL, dx=a_ts)
            
            ## Componente dos Enrijecedores Transversais
            mapdl.asel("ALL")
            mapdl.cm(ENRIJECEDORES_TRANSVERSAIS, "AREA")
            
            # Enrijecedores Longitudinais
            mapdl.flst(2, 4, 3)
            mapdl.fitem(2, 5)
            mapdl.fitem(2, 6)
            mapdl.fitem(2, 7)
            mapdl.fitem(2, 8)
            mapdl.a("P51X")
            
            mapdl.asel("ALL")
            mapdl.asel("S", "LOC", "Y", 0.99*b_ls, 1.01*b_ls)
            mapdl.cm(ENRIJECEDOR_LONGITUDINAL, "AREA")
            
            mapdl.agen(itime=N_ls, na1=ENRIJECEDOR_LONGITUDINAL, dy=b_ls)
            mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS)

            ## Componente dos Enrijecedores Longitudinais
            mapdl.asel("INVE", "AREA")
            mapdl.cm(ENRIJECEDORES_LONGITUDINAIS, "AREA")

            mapdl.rectng(x1=0, x2=a, y1 = 0, y2 = b)
            mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS)
            mapdl.cmsel("A", ENRIJECEDORES_LONGITUDINAIS)
            mapdl.asel("INVE", "AREA")
            mapdl.cm(PLACA, "AREA")
            
            # Para todas as áreas aparecerem quando dar o Plot Areas
            mapdl.asel("ALL")
            
            mapdl.mshape(0, "2D")
            mapdl.mshkey(0)
            
            # Discretização
            ## Discretização da placa
            mapdl.type(1)
            mapdl.mat(1)
            mapdl.run("REAL")
            mapdl.esys(0)
            mapdl.secnum(1)
            mapdl.aesize(PLACA, mesh_size)
            mapdl.amesh(PLACA)
            
            ## Discretização dos enrijecedores transversais
            mapdl.type(1)
            mapdl.mat(1)
            mapdl.run("REAL")
            mapdl.esys(0)
            mapdl.secnum(2)
            mapdl.aesize(ENRIJECEDORES_TRANSVERSAIS, mesh_size)
            mapdl.amesh(ENRIJECEDORES_TRANSVERSAIS)
            
            ## Discretização dos enrijecedores longitudinais
            mapdl.type(1)
            mapdl.mat(1)
            mapdl.run("REAL")
            mapdl.esys(0)
            mapdl.secnum(3)
            mapdl.aesize(ENRIJECEDORES_LONGITUDINAIS, mesh_size)
            mapdl.amesh(ENRIJECEDORES_LONGITUDINAIS)

            # Mergear áreas coincidentes
            # POWER = "0.1"
            # mapdl.shrink(ratio="0.000001")
            # mapdl.nummrg(label="NODE",toler="", gtoler=POWER, action="", switch="LOW")
            # mapdl.nummrg(label="KP",toler="", gtoler=POWER, action="", switch="LOW")
            mapdl.aptn("ALL")
            mapdl.nummrg(label="ALL",toler="", gtoler="", action="", switch="LOW")
            
            # no_erro = 10563
            # coord_x_erro = mapdl.get(f'x,node,{no_erro},LOC,X')
            # coord_y_erro = mapdl.get(f'y,node,{no_erro},LOC,Y')
            # coord_z_erro = mapdl.get(f'z,node,{no_erro},LOC,Z')
            
            # print('x = ', coord_x_erro)
            # print('y = ', coord_y_erro)
            # print('z = ', coord_z_erro)
            
            #Sair do PREP7 para ir para o /SOLU
            mapdl.finish()
            
            #Entrar no /SOLU
            mapdl.slashsolu()
            mapdl.run("ANTYPE,0")
            mapdl.pstres(1)
            
            #Boundary Conditions
            ## Selecionar KP Inferior Esquerdo
            mapdl.cmsel("S", PLACA)
            mapdl.lsla("S")
            mapdl.ksll("S")
            mapdl.ksel("S", "LOC", "X", 0)
            mapdl.ksel("R", "LOC", "Y", 0)
            mapdl.cm(KP_INFERIOR_ESQUERDO, "KP")
            mapdl.dk(KP_INFERIOR_ESQUERDO, "UX", "UY", 0, 0)
            
            ## Selecionar KP Superior Esquerdo
            mapdl.cmsel("S", PLACA)
            mapdl.lsla("S")
            mapdl.ksll("S")
            mapdl.ksel("S", "LOC", "X", 0)
            mapdl.ksel("R", "LOC", "Y", b)
            mapdl.cm(KP_SUPERIOR_ESQUERDO, "KP")
            mapdl.dk(KP_SUPERIOR_ESQUERDO, "UX", 0)
            
            ## Selecionar KP Inferior Direito
            mapdl.cmsel("S", PLACA)
            mapdl.lsla("S")
            mapdl.ksll("S")
            mapdl.ksel("S", "LOC", "X", a)
            mapdl.ksel("R", "LOC", "Y", 0)
            mapdl.cm(KP_INFERIOR_DIREITO, "KP")
            mapdl.dk(KP_INFERIOR_DIREITO, "UY", 0)
            
            #Adicionando componentes da placa
            ## Contorno da placa inteira
            mapdl.cmsel("S", PLACA)
            mapdl.lsla("S")
            mapdl.cm(LINES_CONTORNO_PLACA , "LINE")
            
            ## Direção Longitudinal
            ### Borda esquerda
            mapdl.cmsel("S", LINES_CONTORNO_PLACA)
            mapdl.lsel("R", "LOC", "X", 0)
            mapdl.cm(LINES_CONTORNO_PLACA_ESQUERDA, "LINE")
            
            ### Borda direita
            mapdl.cmsel("S", LINES_CONTORNO_PLACA)
            mapdl.lsel("R", "LOC", "X", a)
            mapdl.cm(LINES_CONTORNO_PLACA_DIREITA, "LINE")
            
            mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_TS,
                cnam1=LINES_CONTORNO_PLACA_ESQUERDA,
                cnam2=LINES_CONTORNO_PLACA_DIREITA)
            
            ## Direção Longitudinal
            ### Borda inferior
            mapdl.cmsel("S", LINES_CONTORNO_PLACA)
            mapdl.lsel("R", "LOC", "Y", 0)
            mapdl.cm(LINES_CONTORNO_PLACA_INFERIOR, "LINE")
            
            ### Borda superior
            mapdl.cmsel("S", LINES_CONTORNO_PLACA)
            mapdl.lsel("R", "LOC", "Y", b)
            mapdl.cm(LINES_CONTORNO_PLACA_SUPERIOR, "LINE")
            
            ### Bordas paralelas aos enrijecedores longitudinais   
            mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_LS,
                cnam1=LINES_CONTORNO_PLACA_INFERIOR,
                cnam2=LINES_CONTORNO_PLACA_SUPERIOR)
            
            #Aplicar BCs de translação ao longo de z das linhas da placa
            mapdl.dl(LINES_CONTORNO_PLACA, "", "UZ", 0)
            
            #Adicionando componentes dos enrijecedores
            mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS)
            mapdl.lsla("S")
            mapdl.lsel("R", "LOC", "Y", 0)
            mapdl.cm(LINES_BORDA_TS_INFERIOR, "LINE")
            
            mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS)
            mapdl.lsla("S")
            mapdl.lsel("R", "LOC", "Y", b)
            mapdl.cm(LINES_BORDA_TS_SUPERIOR, "LINE")
            
            mapdl.cmgrp(aname=LINES_BORDA_TS,
                cnam1=LINES_BORDA_TS_INFERIOR,
                cnam2=LINES_BORDA_TS_SUPERIOR)
            
            mapdl.cmsel("S", ENRIJECEDORES_LONGITUDINAIS)
            mapdl.lsla("S")
            mapdl.lsel("R", "LOC", "X", 0)
            mapdl.cm(LINES_BORDA_LS_ESQUERDA, "LINE")
            
            mapdl.cmsel("S", ENRIJECEDORES_LONGITUDINAIS)
            mapdl.lsla("S")
            mapdl.lsel("R", "LOC", "X", a)
            mapdl.cm(LINES_BORDA_LS_DIREITA, "LINE")

            mapdl.cmgrp(aname=LINES_BORDA_LS,
                cnam1=LINES_BORDA_LS_ESQUERDA,
                cnam2=LINES_BORDA_LS_DIREITA)
            
            mapdl.cmgrp(aname=LINES_BORDA_ENRIJECEDORES,
                cnam1=LINES_BORDA_TS,
                cnam2=LINES_BORDA_LS)
            
            #Aplicar BCs de translação ao longo de z das bordas dos enrijecedores
            mapdl.dl(LINES_BORDA_ENRIJECEDORES, "", "UZ", 0)
            #Salvar as alterações
            mapdl.save(slab='ALL')
            #Deixar no contexto inicial de novo
            mapdl.resume(fname=f'{mapdl_connection_wrapper.temp_run_location_absolute_path}/{mapdl_connection_wrapper.jobname}.db')
            
        finally:
            mapdl_pool.return_connection(mapdl)
        
        
    
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