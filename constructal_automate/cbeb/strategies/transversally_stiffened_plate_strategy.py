import os
from cbeb.strategies.plate_strategy import PlateStrategy
from cbeb.models.processing_status import ProcessingStatus

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
ELASTIC_BUCKLING_APPLIED_LOAD = 1

class TransversallyStiffenedPlateStrategy(PlateStrategy):

    def define_element_type_section_and_material(self, mapdl, E, poisson_ratio, t_1, t_s):
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
        # # Elemento Finito
        mapdl.et(1, "SHELL281")

        # # Material
        mapdl.mptemp("", "", "")
        mapdl.mptemp(1, 0)
        mapdl.mpdata("EX", 1, "", E)
        mapdl.mpdata("PRXY", 1, "", poisson_ratio)

        # Seções
        # # Seção da placa
        mapdl.run("sect,1,shell")
        mapdl.secdata(t_1, 1, 0, 5)
        mapdl.secoffset("TOP")
        # mapdl.seccontrol("", "", "", "", "", "")
        mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)

        # # Seção dos enrijecedores
        mapdl.run("sect,2,shell")
        mapdl.secdata(t_s, 1, 0, 5)
        mapdl.secoffset("MID")
        mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)

    def define_geometry(self, mapdl, a, b, N_ts, N_ls, h_s):
        # Definir espaçamento dos enrijecedores
        a_ts = float(round(a/(N_ts+1), 0))
        b_ls = float(round(b/(N_ls+1), 0))

        # Definir keypoints
        mapdl.k(1, a_ts, 0, 0)
        mapdl.k(2, a_ts, b, 0)
        mapdl.k(3, a_ts, b, h_s)
        mapdl.k(4, a_ts, 0, h_s)
        # mapdl.k(5, 0, b_ls, 0)
        # mapdl.k(6, a, b_ls, 0)
        # mapdl.k(7, a, b_ls, h_s)
        # mapdl.k(8, 0, b_ls, h_s)

        # Criar área do enrijecedor transversal
        mapdl.flst(2, 4, 3)
        mapdl.fitem(2, 1)
        mapdl.fitem(2, 2)
        mapdl.fitem(2, 3)
        mapdl.fitem(2, 4)
        mapdl.a("P51X")

        # Selection Logic para criar os enrijecedores
        # # Enrijecedores Transversais
        mapdl.asel("S", "LOC", "X", 0.99*a_ts, 1.01*a_ts)
        mapdl.cm(ENRIJECEDOR_TRANSVERSAL_PRE_APTN, "AREA")
        mapdl.agen(itime=N_ts, na1=ENRIJECEDOR_TRANSVERSAL_PRE_APTN, dx=a_ts)

        # # Componente dos Enrijecedores Transversais
        mapdl.asel("ALL")
        mapdl.cm(ENRIJECEDORES_TRANSVERSAIS_PRE_APTN, "AREA")
        
        # # Enrijecedores Longitudinais
        # mapdl.flst(2, 4, 3)
        # mapdl.fitem(2, 5)
        # mapdl.fitem(2, 6)
        # mapdl.fitem(2, 7)
        # mapdl.fitem(2, 8)
        # mapdl.a("P51X")

        # mapdl.asel("ALL")
        # mapdl.asel("S", "LOC", "Y", 0.99*b_ls, 1.01*b_ls)
        # mapdl.cm(ENRIJECEDOR_LONGITUDINAL_PRE_APTN, "AREA")
        # mapdl.agen(itime=N_ls, na1=ENRIJECEDOR_LONGITUDINAL_PRE_APTN, dy=b_ls)

        # # Componente dos Enrijecedores Longitudinais
        # mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_PRE_APTN)
        # mapdl.asel("INVE", "AREA")
        # mapdl.cm(ENRIJECEDORES_LONGITUDINAIS_PRE_APTN, "AREA")

        mapdl.rectng(x1=0, x2=a, y1=0, y2=b)
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_PRE_APTN)
        # mapdl.cmsel("A", ENRIJECEDORES_LONGITUDINAIS_PRE_APTN)
        mapdl.asel("INVE", "AREA")
        mapdl.cm(PLACA_PRE_APTN, "AREA")

    def define_discretization(self, mapdl, a, b, t_1, N_ts, N_ls, h_s, mesh_size, stiffened_plate_analysis):
        a_ts = float(round(a/(N_ts+1), 0))
        b_ls = float(round(b/(N_ls+1), 0))

        # Particionar as áreas para corrigir problemas de interface entre enrijecedores
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.aptn(na1="ALL")

        # Criar componente da PLACA_POS_APTN
        # mapdl.asel("ALL")
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.aglue(na1="ALL")
        mapdl.asel("S", "LOC", "X", round(OFFSET_PERCENTUAL_BORDA_INICIAL*float(a_ts), 1), round(OFFSET_PERCENTUAL_BORDA_FINAL*float(a_ts)), 1)
        for i in range(N_ts):
            mapdl.asel("A", "LOC", "X", round(((i+1)+OFFSET_PERCENTUAL_BORDA_INICIAL)*float(a_ts),1), round(((i+1)+OFFSET_PERCENTUAL_BORDA_FINAL)*float(a_ts)),1)
        mapdl.asel("R", "LOC", "Z", round(-0.5*float(t_1), 1), round(0.5*float(t_1)), 1)
        mapdl.cm(PLACA_POS_APTN, "AREA")

        # Criar componente da ENRIJECEDORES_LONGITUDINAIS_POS_APTN
        # mapdl.asel("ALL")
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.asel("S", "LOC", "X", round(OFFSET_PERCENTUAL_BORDA_INICIAL*float(a_ts), 1), round(OFFSET_PERCENTUAL_BORDA_FINAL*float(a_ts)), 1)
        # for i in range(N_ts):
        #     mapdl.asel("A", "LOC", "X", round(((i+1)+OFFSET_PERCENTUAL_BORDA_INICIAL)*float(a_ts), 1), round(((i+1)+OFFSET_PERCENTUAL_BORDA_FINAL)*float(a_ts)), 1)
        # mapdl.asel("R", "LOC", "Z", round(OFFSET_PERCENTUAL_Z_INICIAL*float(h_s), 1), round(OFFSET_PERCENTUAL_Z_FINAL*float(h_s)), 1)
        # mapdl.cm(ENRIJECEDORES_LONGITUDINAIS_POS_APTN, "AREA")

        # Criar componente da ENRIJECEDORES_TRANSVERSAIS_POS_APTN
        # mapdl.asel("ALL")
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.asel("S", "LOC", "Y", round(OFFSET_PERCENTUAL_BORDA_INICIAL*float(b_ls), 1), round(OFFSET_PERCENTUAL_BORDA_FINAL*float(b_ls), 1))
        for i in range(N_ls):
            mapdl.asel("A", "LOC", "Y", round(((i+1)+OFFSET_PERCENTUAL_BORDA_INICIAL)*float(b_ls), 1), round(((i+1)+0.52)*float(b_ls), 1))
        mapdl.asel("R", "LOC", "Z", round(OFFSET_PERCENTUAL_Z_INICIAL*float(h_s), 1), round(OFFSET_PERCENTUAL_Z_FINAL*float(h_s), 1))
        mapdl.cm(ENRIJECEDORES_TRANSVERSAIS_POS_APTN, "AREA")
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.nummrg(label="ALL", toler="", gtoler="", action="", switch="LOW")

        # Discretização
        # # Discretização da placa
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.mshape(0, "2D")
        mapdl.mshkey(0)

        mapdl.type(1)
        mapdl.mat(1)
        mapdl.run("REAL")
        mapdl.esys(0)
        mapdl.secnum(1)
        mapdl.aesize(PLACA_POS_APTN, mesh_size)
        mapdl.amesh(PLACA_POS_APTN)

        # # Discretização dos enrijecedores transversais
        mapdl.type(1)
        mapdl.mat(1)
        mapdl.run("REAL")
        mapdl.esys(0)
        mapdl.secnum(2)
        mapdl.aesize(ENRIJECEDORES_TRANSVERSAIS_POS_APTN, mesh_size)
        mapdl.amesh(ENRIJECEDORES_TRANSVERSAIS_POS_APTN)

        # # Discretização dos enrijecedores longitudinais
        # mapdl.type(1)
        # mapdl.mat(1)
        # mapdl.run("REAL")
        # mapdl.esys(0)
        # mapdl.secnum(2)
        # mapdl.aesize(ENRIJECEDORES_LONGITUDINAIS_POS_APTN, mesh_size)
        # mapdl.amesh(ENRIJECEDORES_LONGITUDINAIS_POS_APTN)

        num_elem = mapdl.get('NELEM', 'ELEM', '', 'count')
        stiffened_plate_analysis.num_elem = num_elem
        stiffened_plate_analysis.save()
        # Sair do PREP7 para ir para o /SOLU
        mapdl.finish()
    
    def define_components_and_apply_boundary_conditions(self, mapdl, a, b, t_1):
        # Entrar no /SOLU
        mapdl.slashsolu()
        mapdl.run("ANTYPE,0")
        mapdl.pstres(1)

        # Boundary Conditions
        # # Selecionar KP Inferior Esquerdo
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.ksll("S")
        mapdl.ksel("S", "LOC", "X", 0)
        mapdl.ksel("R", "LOC", "Y", 0)
        mapdl.cm(KP_INFERIOR_ESQUERDO, "KP")
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dk(KP_INFERIOR_ESQUERDO, "UX", 0)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dk(KP_INFERIOR_ESQUERDO, "UY", 0)

        # Selecionar KP Superior Esquerdo
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.cmsel("S", PLACA_POS_APTN)
        # mapdl.lsla("S")
        # mapdl.ksll("S")
        # mapdl.ksel("S", "LOC", "X", 0)
        # mapdl.ksel("R", "LOC", "Y", b)
        # mapdl.cm(KP_SUPERIOR_ESQUERDO, "KP")
        # mapdl.dk(KP_SUPERIOR_ESQUERDO, "UX", 0)


        # Selecionar KP Superior Direito
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.ksll("S")
        mapdl.ksel("S", "LOC", "X", a)
        mapdl.ksel("R", "LOC", "Y", b)
        mapdl.cm(KP_SUPERIOR_DIREITO, "KP")
        mapdl.dk(KP_SUPERIOR_DIREITO, "UY", 0)

        # Selecionar KP Inferior Direito
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.cmsel("S", PLACA_POS_APTN)
        # mapdl.lsla("S")
        # mapdl.ksll("S")
        # mapdl.ksel("S", "LOC", "X", a)
        # mapdl.ksel("R", "LOC", "Y", 0)
        # mapdl.cm(KP_INFERIOR_DIREITO, "KP")
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.dk(KP_INFERIOR_DIREITO, "UY", 0)

        # Adicionando componentes da placa
        # # Contorno da placa inteira
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("S", "LOC", "X", 0)
        mapdl.lsel("A", "LOC", "X", a)
        mapdl.lsel("A", "LOC", "Y", 0)
        mapdl.lsel("A", "LOC", "Y", b)
        mapdl.lsel("R", "LOC", "Z", 0, t_1)
        mapdl.cm(LINES_CONTORNO_PLACA, "LINE")

        # # Direção Longitudinal
        # ## Borda esquerda
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "X", 0)
        mapdl.cm(LINES_CONTORNO_PLACA_ESQUERDA, "LINE")

        # ## Borda direita
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "X", a)
        mapdl.cm(LINES_CONTORNO_PLACA_DIREITA, "LINE")

        mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_TS,
                    cnam1=LINES_CONTORNO_PLACA_ESQUERDA,
                    cnam2=LINES_CONTORNO_PLACA_DIREITA)

        # # Direção Longitudinal
        # ## Borda inferior
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "Y", 0)
        mapdl.cm(LINES_CONTORNO_PLACA_INFERIOR, "LINE")

        # ## Borda superior
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "Y", b)
        mapdl.cm(LINES_CONTORNO_PLACA_SUPERIOR, "LINE")

        # ## Bordas paralelas aos enrijecedores longitudinais
        mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_LS,
                    cnam1=LINES_CONTORNO_PLACA_INFERIOR,
                    cnam2=LINES_CONTORNO_PLACA_SUPERIOR)

        # Aplicar BCs de translação ao longo de z das linhas da placa
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dl(LINES_CONTORNO_PLACA, "", "UZ", 0)
        # mapdl.dl(LINES_CONTORNO_PLACA, "", "ROTZ", 0)

        # Adicionando componentes dos enrijecedores
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("R", "LOC", "Y", 0)
        mapdl.cm(LINES_BORDA_TS_INFERIOR, "LINE")

        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("R", "LOC", "Y", b)
        mapdl.cm(LINES_BORDA_TS_SUPERIOR, "LINE")

        mapdl.cmgrp(aname=LINES_BORDA_TS,
                    cnam1=LINES_BORDA_TS_INFERIOR,
                    cnam2=LINES_BORDA_TS_SUPERIOR)

        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.cmsel("S", ENRIJECEDORES_LONGITUDINAIS_POS_APTN)
        # mapdl.lsla("S")
        # mapdl.lsel("R", "LOC", "X", 0)
        # mapdl.cm(LINES_BORDA_LS_ESQUERDA, "LINE")

        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.cmsel("S", ENRIJECEDORES_LONGITUDINAIS_POS_APTN)
        # mapdl.lsla("S")
        # mapdl.lsel("R", "LOC", "X", a)
        # mapdl.cm(LINES_BORDA_LS_DIREITA, "LINE")

        # mapdl.cmgrp(aname=LINES_BORDA_LS,
        #             cnam1=LINES_BORDA_LS_ESQUERDA,
        #             cnam2=LINES_BORDA_LS_DIREITA)

        mapdl.cmgrp(aname=LINES_BORDA_ENRIJECEDORES,
                    cnam1=LINES_BORDA_TS)
                    # cnam2=LINES_BORDA_LS)

        # Aplicar BCs de translação ao longo de z das bordas dos enrijecedores
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dl(LINES_BORDA_ENRIJECEDORES, "", "UZ", 0)
        # mapdl.dl(LINES_BORDA_ENRIJECEDORES, "", "ROTZ", 0)
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.dl(LINES_CONTORNO_PLACA_LS, "", "ROTX", 0)
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.dl(LINES_BORDA_TS, "", "ROTX", 0)
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.dl(LINES_CONTORNO_PLACA_TS, "", "ROTY", 0)
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.dl(LINES_BORDA_LS, "", "ROTY", 0)
        mapdl.finish()

    def apply_load_for_elastic_buckling(self, mapdl, buckling_load_type):
        mapdl.allsel(labt="ALL", entity="ALL")
        if self.is_biaxial_buckling(buckling_load_type):
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            # mapdl.sfl(LINES_BORDA_LS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            mapdl.sfl(LINES_BORDA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
        else:
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            # mapdl.sfl(LINES_BORDA_LS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)

    # def apply_load_for_elasto_plastic_buckling(self, mapdl, buckling_load_type, material, t_eq_ts, t_eq_ls):
    def apply_load_for_elasto_plastic_buckling(self, mapdl, buckling_load_type, material, t_1):
        # p_u_ts = round(material.yielding_stress*t_eq_ts, 2)
        p_u_ts = round(material.yielding_stress*t_1, 2)

        if self.is_biaxial_buckling(buckling_load_type):
            # p_u_ls = round(material.yielding_stress*t_eq_ls, 2)
            p_u_ls = round(material.yielding_stress*t_1, 2)
        else:
            p_u_ls = 0
            
        if self.is_biaxial_buckling(buckling_load_type):
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", p_u_ts)
            mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", p_u_ls)
            # mapdl.sfl(LINES_BORDA_LS, "PRESS", p_u_ts)
            mapdl.sfl(LINES_BORDA_TS, "PRESS", p_u_ls)
        else:
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", p_u_ts)
            # mapdl.sfl(LINES_BORDA_LS, "PRESS", p_u_ts)
        return p_u_ts, p_u_ls

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'