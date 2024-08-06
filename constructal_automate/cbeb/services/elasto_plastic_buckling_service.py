from cbeb.models import StiffenedPlateAnalysis
from cbeb.config.mapdl_connection_pool import MapdlConnectionPool
from csg.models import StiffenedPlate

class ElastoPlasticBucklingService():
    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               ):

        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1
        rst_file_path = stiffened_plate_analysis.analysis_rst_file_path
        material = stiffened_plate_analysis.material
        sigma_e = material.yielding_stress
        n_e = sigma_e*t_1

        mapdl_connection_pool = MapdlConnectionPool()

        mapdl_connection = mapdl_connection_pool.get_connection()

        mapdl = mapdl_connection.connection

        w0 = self.define_initial_deflection(b)
        
        mapdl.prep7()
        mapdl.upgeom(factor=w0, lstep="LAST", sbstep="LAST", fname=rst_file_path, ext="rst")
        mapdl.tb(lab="BISO", mat=material.id, ntemp=1, npts=2)
        mapdl.tbtemp(0)
        mapdl.tbdata("", sigma_e, 0, "")
        mapdl.run("/SOL")
        mapdl.run("ANTYPE,0")
        mapdl.nlgeom(1)
        mapdl.nsubst(100, 200, 50)
        mapdl.outres("ERASE")
        mapdl.outres("ALL", 1)
        mapdl.pstres(1)
        mapdl.time(n_e)
        
        #TODO: Implementar lógica para 1A e 2A para Plate e StiffenedPlate
        # mapdl.flst(2, 4, 4, "ORDE", 4)
        # # Os números de linhas mudam quando não tem enrijecedores
        # mapdl.fitem(2, 2)
        # mapdl.fitem(2, 4)
        # # Para carga uniaxial, não tem esses caras
        # mapdl.fitem(2, 1)
        # mapdl.fitem(2, 3)
        # mapdl.run("/GO")
        # mapdl.sfl("P51X", "PRES", f'{carga_escoamento}')
        # mapdl.solve()
        # mapdl.finish()
        # mapdl.run("/POST1")
        # data_sets_flamb = mapdl.post_processing.time_values
        # carga_ultima_flambagem = data_sets_flamb[len(data_sets_flamb)-2]
        # tensao_ultima_flambagem = carga_ultima_flambagem/t_p

    def define_initial_deflection(self, b):
        return b/2000