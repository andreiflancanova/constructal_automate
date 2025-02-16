import os
from cbeb.strategies.plate_strategy import PlateStrategy
from cbeb.models.processing_status import ProcessingStatus


ENRIJECEDOR_LONGITUDINAL_PRE_APTN = os.getenv('ENRIJECEDOR_LONGITUDINAL_PRE_APTN')
ENRIJECEDOR_TRANSVERSAL_PRE_APTN = os.getenv('ENRIJECEDOR_TRANSVERSAL_PRE_APTN')

ENRIJECEDORES_LONGITUDINAIS_PRE_APTN = os.getenv('ENRIJECEDORES_LONGITUDINAIS_PRE_APTN')
ENRIJECEDORES_TRANSVERSAIS_PRE_APTN = os.getenv('ENRIJECEDORES_TRANSVERSAIS_PRE_APTN')
PLACA_PRE_APTN = os.getenv('PLACA_PRE_APTN')
CONJUNTO_PRE_APTN = os.getenv('CONJUNTO_PRE_APTN')

ENRIJECEDORES_LONGITUDINAIS_POS_APTN = os.getenv('ENRIJECEDORES_LONGITUDINAIS_POS_APTN')
ENRIJECEDORES_TRANSVERSAIS_POS_APTN = os.getenv('ENRIJECEDORES_TRANSVERSAIS_POS_APTN')
ENRIJECEDORES_POS_APTN = os.getenv('ENRIJECEDORES_POS_APTN')
PLACA_POS_APTN = os.getenv('PLACA_POS_APTN')
CONJUNTO_POS_APTN = os.getenv('CONJUNTO_POS_APTN')

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
        
        # Pré-Processamento
        mapdl.prep7()

        ## Definição do elemento
        mapdl.run("/GO")
        mapdl.et(1, "SHELL281")

        ## Definição do material
        mapdl.mptemp("", "", "")
        mapdl.mptemp(1, 0)
        mapdl.mpdata("EX", 1, "", E)
        mapdl.mpdata("PRXY", 1, "", poisson_ratio)

        ## Definição das seções
        ### Seção da placa
        mapdl.run("sect,1,shell")
        mapdl.secdata(t_1, 1, 0, 5)
        mapdl.secoffset("MID")
        mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)

        ### Seção dos enrijecedores
        mapdl.run("sect,2,shell")
        mapdl.secdata(t_s, 1, 0, 5)
        mapdl.secoffset("MID")
        mapdl.seccontrol(0, 0, 0, 0, 1, 1, 1)

    def define_geometry(self, mapdl, a, b, t_1, N_ts, N_ls, h_s):
        
        ## Calcular espaçamento dos enrijecedores
        a_ts = float(round(a/(N_ts+1), 0))
        b_ls = float(round(b/(N_ls+1), 0))

        ## Definição dos KPs
        mapdl.k(1, a_ts, 0, 0)
        mapdl.k(2, a_ts, b, 0)
        mapdl.k(3, a_ts, b, h_s)
        mapdl.k(4, a_ts, 0, h_s)

        ## Geometria
        ### Enrijecedores transversais
        #### Criação da área base
        mapdl.flst(2, 4, 3)
        mapdl.fitem(2, 1)
        mapdl.fitem(2, 2)
        mapdl.fitem(2, 3)
        mapdl.fitem(2, 4)
        mapdl.a("P51X")

        #### Criação do componente base
        mapdl.cm(ENRIJECEDOR_TRANSVERSAL_PRE_APTN, "AREA")

        #### Geração dos NTS enrijecedores transversais
        mapdl.agen(itime=N_ts, na1=ENRIJECEDOR_TRANSVERSAL_PRE_APTN, dx=a_ts)

        #### Criação do componente dos enrijecedores transversais
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cm(ENRIJECEDORES_TRANSVERSAIS_PRE_APTN, "AREA")

        ### Placa
        #### Criação da área
        mapdl.rectng(x1=0, x2=a, y1=0, y2=b)

        #### Criação do componente
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("U", ENRIJECEDORES_TRANSVERSAIS_PRE_APTN)
        mapdl.cm(PLACA_PRE_APTN, "AREA")

        ### Agrupamento dos componentes para aplicação do APTN
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_PRE_APTN)
        mapdl.cmsel("A", PLACA_PRE_APTN)
        mapdl.cmgrp(aname=CONJUNTO_PRE_APTN,
                    cnam1=ENRIJECEDORES_TRANSVERSAIS_PRE_APTN,
                    cnam2=PLACA_PRE_APTN)
        
        ### Aplicação do APTN (Area Partition)
        mapdl.aptn(na1="ALL")

        ### Recriação dos componentes após uso do APTN (os componentes originais são apagados)
        #### Placa
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.asel("S", "LOC", "Z", round(-0.5*float(t_1), 1), round(0.5*float(t_1)), 1)
        mapdl.cm(PLACA_POS_APTN, "AREA")

        #### Enrijecedores Transversais
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.asel("S", "LOC", "Y", round(OFFSET_PERCENTUAL_BORDA_INICIAL*float(b_ls), 1), round(OFFSET_PERCENTUAL_BORDA_FINAL*float(b_ls), 1))
        for i in range(N_ls):
            mapdl.asel("A", "LOC", "Y", round(((i+1)+OFFSET_PERCENTUAL_BORDA_INICIAL)*float(b_ls), 1), round(((i+1)+0.52)*float(b_ls), 1))
        mapdl.asel("R", "LOC", "Z", round(OFFSET_PERCENTUAL_Z_INICIAL*float(h_s), 1), round(OFFSET_PERCENTUAL_Z_FINAL*float(h_s), 1))
        mapdl.cm(ENRIJECEDORES_TRANSVERSAIS_POS_APTN, "AREA")

        ### Agrupamento dos enrijecedores para execução do AGLUE ("colar" faces comuns)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmgrp(aname=ENRIJECEDORES_POS_APTN,
            cnam1=ENRIJECEDORES_TRANSVERSAIS_POS_APTN)

        ### Agrupamento da placa com os enrijecedores para execução do AGLUE ("colar" faces comuns)
        mapdl.cmgrp(aname=CONJUNTO_POS_APTN,
            cnam1=ENRIJECEDORES_POS_APTN,
            cnam2=PLACA_POS_APTN)
        
        ### Aplicação do AGLUE no conjunto de placa e enrijecedores
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.aglue(na1=CONJUNTO_POS_APTN)

        ### Aplicação do NUMMRG para mergear entidades comuns que existem por conta da sobreposição
        # mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.nummrg(label="ALL", toler="", gtoler="", action="", switch="LOW")

    def define_discretization(self, mapdl, mesh_size, stiffened_plate_analysis):
        
        ## Meshing
        ### Definição do contexto de meshing
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.mshape(0, "2D")
        mapdl.mshkey(0)

        ### Meshing da placa
        mapdl.type(1)
        mapdl.mat(1)
        mapdl.run("REAL")
        mapdl.esys(0)
        mapdl.secnum(1)
        mapdl.aesize(PLACA_POS_APTN, mesh_size)
        mapdl.amesh(PLACA_POS_APTN)

        ### Meshing dos enrijecedores transversais
        mapdl.type(1)
        mapdl.mat(1)
        mapdl.run("REAL")
        mapdl.esys(0)
        mapdl.secnum(2)
        mapdl.aesize(ENRIJECEDORES_TRANSVERSAIS_POS_APTN, mesh_size)
        mapdl.amesh(ENRIJECEDORES_TRANSVERSAIS_POS_APTN)


        ### Aplicação do NUMMRG para mergear entidades comuns que existem por conta da sobreposição
        mapdl.allsel(labt="ALL", entity="ALL")
        # mapdl.nummrg(label="ALL", toler="", gtoler="", action="", switch="LOW")
        mapdl.nummrg(label="KP", toler="", gtoler="", action="", switch="LOW")
        mapdl.nummrg(label="NODE", toler="", gtoler="", action="", switch="LOW")

        ### Contagem do total de elementos
        num_elem = mapdl.get('NELEM', 'ELEM', '', 'count')

        stiffened_plate_analysis.num_elem = num_elem
        stiffened_plate_analysis.save()
        
        ## Encerrar /PREP7
        mapdl.finish()
    
    def define_components_and_apply_boundary_conditions(self, mapdl, a, b, t_1):
        # Entrar no /SOLU (Solution)
        mapdl.slashsolu()
        # mapdl.run("ANTYPE,0")
        mapdl.antype(antype="STATIC")
        mapdl.pstres(1)

        ## Criação dos componentes para aplicação das condições de contorno
        ### Placa
        #### Componente do KP Inferior Esquerdo:
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.ksll("S")
        mapdl.ksel("S", "LOC", "X", 0)
        mapdl.ksel("R", "LOC", "Y", 0)
        mapdl.cm(KP_INFERIOR_ESQUERDO, "KP")

        #### Componente do KP Superior Direito
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.ksll("S")
        mapdl.ksel("S", "LOC", "X", a)
        # mapdl.ksel("R", "LOC", "Y", b)
        # mapdl.cm(KP_SUPERIOR_DIREITO, "KP")
        mapdl.ksel("R", "LOC", "Y", 0)
        mapdl.cm(KP_INFERIOR_DIREITO, "KP")

        #### Componente das linhas do contorno da placa
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", PLACA_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("S", "LOC", "X", 0)
        mapdl.lsel("A", "LOC", "X", a)
        mapdl.lsel("A", "LOC", "Y", 0)
        mapdl.lsel("A", "LOC", "Y", b)
        mapdl.lsel("R", "LOC", "Z", t_1)
        # mapdl.lsel("R", "LOC", "Z", 0, t_1)
        mapdl.cm(LINES_CONTORNO_PLACA, "LINE")


        #### Componente das linhas da borda esquerda da placa (X = 0)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "X", 0)
        mapdl.cm(LINES_CONTORNO_PLACA_ESQUERDA, "LINE")

        #### Componente das linhas da borda direita da placa (X = A)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "X", a)
        mapdl.cm(LINES_CONTORNO_PLACA_DIREITA, "LINE")

        #### Componente do agrupamento das linhas das bordas transversais da placa
        mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_TS,
                    cnam1=LINES_CONTORNO_PLACA_ESQUERDA,
                    cnam2=LINES_CONTORNO_PLACA_DIREITA)

        #### Componente das linhas da borda inferior da placa (Y = 0)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "Y", 0)
        mapdl.cm(LINES_CONTORNO_PLACA_INFERIOR, "LINE")

        #### Componente das linhas da borda superior da placa  (Y = B)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", LINES_CONTORNO_PLACA)
        mapdl.lsel("R", "LOC", "Y", b)
        mapdl.cm(LINES_CONTORNO_PLACA_SUPERIOR, "LINE")

        #### Componente do agrupamento das linhas das bordas longitudinais da placa
        mapdl.cmgrp(aname=LINES_CONTORNO_PLACA_LS,
                    cnam1=LINES_CONTORNO_PLACA_INFERIOR,
                    cnam2=LINES_CONTORNO_PLACA_SUPERIOR)
        
        ### Enrijecedores Transversais
        #### Componente das linhas da borda inferior dos enrijecedores transversais (Y = 0)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("R", "LOC", "Y", 0)
        mapdl.cm(LINES_BORDA_TS_INFERIOR, "LINE")

        #### Componente das linhas da borda superior dos enrijecedores transversais (Y = B)
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.cmsel("S", ENRIJECEDORES_TRANSVERSAIS_POS_APTN)
        mapdl.lsla("S")
        mapdl.lsel("R", "LOC", "Y", b)
        mapdl.cm(LINES_BORDA_TS_SUPERIOR, "LINE")

        #### Componente do agrupamento das linhas das bordas dos enrijecedores transversais
        mapdl.cmgrp(aname=LINES_BORDA_TS,
                    cnam1=LINES_BORDA_TS_INFERIOR,
                    cnam2=LINES_BORDA_TS_SUPERIOR)

        #### Componente do agrupamento das linhas das bordas dos enrijecedores
        mapdl.cmgrp(aname=LINES_BORDA_ENRIJECEDORES,
                    cnam1=LINES_BORDA_TS)

        ## Aplicação das condições de contorno

        ### Deslocamento
        #### KPs
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dk(KP_INFERIOR_ESQUERDO, "UX", 0)
        mapdl.dk(KP_INFERIOR_ESQUERDO, "UY", 0)
        # mapdl.dk(KP_SUPERIOR_DIREITO, "UY", 0)
        mapdl.dk(KP_INFERIOR_DIREITO, "UY", 0)

        #### Linhas
        ##### Placa
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dl(LINES_CONTORNO_PLACA, "", "UZ", 0)


        ##### Enrijecedores
        mapdl.allsel(labt="ALL", entity="ALL")
        mapdl.dl(LINES_BORDA_ENRIJECEDORES, "", "UZ", 0)
        mapdl.finish()

    def apply_load_for_elastic_buckling(self, mapdl, buckling_load_type):
        mapdl.slashsolu()
        ### Cargas de Superficie
        mapdl.allsel(labt="ALL", entity="ALL")
        if self.is_biaxial_buckling(buckling_load_type):
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
            mapdl.sfl(LINES_BORDA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
        else:
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", ELASTIC_BUCKLING_APPLIED_LOAD)
        mapdl.finish()

    def apply_load_for_elasto_plastic_buckling(self, mapdl, buckling_load_type, material, t_1):
        p_u = round(material.yielding_stress*t_1, 2)
            
        if self.is_biaxial_buckling(buckling_load_type):
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", p_u)
            mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", p_u)
            mapdl.sfl(LINES_BORDA_TS, "PRESS", p_u)
        else:
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", p_u)
        return p_u

    def is_biaxial_buckling(self, buckling_load_type):
        return buckling_load_type == '2A'