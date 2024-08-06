from cbeb.models import StiffenedPlateAnalysis
from csg.models import StiffenedPlate
from cbeb.config.mapdl_connection_pool import MapdlConnectionPool
from ansys.mapdl.core.errors import MapdlRuntimeError

LINES_CONTORNO_PLACA_TS = "lines_contorno_placa_ts"
LINES_CONTORNO_PLACA_LS = "lines_contorno_placa_ls"
LINES_BORDA_LS = "lines_borda_ls"
LINES_BORDA_TS = "lines_borda_ts"


class ElasticBucklingService():
    # TODO: Modificar para receber um biaxial_buckling
    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               n_x,
               csi_y
               ):

        # TODO: Passar os components para variáveis de ambiente
        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        a = stiffened_plate.plate.a
        b = stiffened_plate.plate.b
        t_1 = stiffened_plate.t_1
        t_s = stiffened_plate.t_s
        h_s = stiffened_plate.h_s

        mapdl_connection_pool = MapdlConnectionPool()

        mapdl_connection = mapdl_connection_pool.get_connection()

        mapdl = mapdl_connection.connection

        try:
            self.load_previous_steps_analysis_db(mapdl, analysis_log_path, analysis_dir_path, analysis_db_path)
            self.apply_loads(mapdl, h_s, t_s, n_x, csi_y)
            self.solve_elastic_buckling(mapdl)
            n_cr, sigma_cr = self.calc_buckling_load_and_stress(mapdl, t_1)
            w_center = self.calc_z_deflection(mapdl, a, b)
            stiffened_plate_analysis.analysis_rst_file_path = analysis_log_path.replace('.txt', '.rst')
            stiffened_plate_analysis.save()
            mapdl.finish()
            mapdl._close_apdl_log()
        except MapdlRuntimeError as e:
            print(e)
            mapdl._close_apdl_log()
        finally:
            mapdl_connection_pool.return_connection(mapdl_connection)
        return n_cr, sigma_cr, w_center

    def load_previous_steps_analysis_db(self, mapdl, analysis_log_path, analysis_dir_path, analysis_db_path):
        mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
        mapdl.cwd(analysis_dir_path)
        mapdl.resume(fname=f'{analysis_db_path}')
        #Added only in constructal_automate, but not in the original script
        mapdl.slashsolu()
        mapdl.cmsel("ALL")

# TODO: Modificar lógica desse método para depender de BucklingType ao invés do csi_y
    def apply_loads(self, mapdl, h_s, t_s, n_x, csi_y):
        if self.is_stiffened_plate(h_s, t_s):
            if self.is_biaxial_buckling(csi_y):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", csi_y*n_x)
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_x)
                mapdl.sfl(LINES_BORDA_TS, "PRESS", csi_y*n_x)
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_BORDA_LS, "PRESS", n_x)
        else:
            if self.is_biaxial_buckling(csi_y):
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
                mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", csi_y*n_x)
            else:
                mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)

    def solve_elastic_buckling(self, mapdl):
        mapdl.solve()
        mapdl.finish()
        mapdl.run("/SOLU")
        mapdl.run("ANTYPE,1")
        mapdl.bucopt("LANB", 1, 0, 0, "CENTER")
        mapdl.mxpand(1, 0, 0, 0, 0.001)
        mapdl.solve()
        mapdl.finish()
        mapdl.save()
        mapdl.run("/POST1")

    def calc_buckling_load_and_stress(self, mapdl, t_1):
        n_cr = mapdl.post_processing.time
        sigma_cr = n_cr/float(t_1)
        mapdl.save()
        return n_cr, sigma_cr
    
    def calc_z_deflection(self, mapdl, a, b):
        mapdl.run(f"NSEL,S,NODE,,NODE({float(a)*0.5},{float(b)*0.5},0)")
        z_deflection = abs(mapdl.prnsol(item="U", comp="Z").to_list()[0][1])
        return z_deflection

    def is_biaxial_buckling(self, csi_y):
        return csi_y != 0.000

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00