from cbeb.models import StiffenedPlateAnalysis, BiaxialElasticBuckling
from csg.models import StiffenedPlate
from cbeb.config.mapdl_connection_pool import MapdlConnectionPool
from ansys.mapdl.core.errors import MapdlRuntimeError

LINES_CONTORNO_PLACA_TS = "lines_contorno_placa_ts"
LINES_CONTORNO_PLACA_LS = "lines_contorno_placa_ls"
LINES_BORDA_LS = "lines_borda_ls"
LINES_BORDA_TS = "lines_borda_ts"

class BiaxialElasticBucklingService():
    # TODO: Modificar para receber um biaxial_buckling
    def create(self,
               stiffened_plate_analysis: StiffenedPlateAnalysis,
               stiffened_plate: StiffenedPlate,
               n_x,
               csi_y
               ):
        analysis_dir_path = stiffened_plate_analysis.analysis_dir_path
        analysis_log_path = stiffened_plate_analysis.analysis_lgw_file_path
        analysis_db_path = analysis_log_path.replace('.txt', '.db')
        t_1 = stiffened_plate.t_1

        mapdl_connection_pool = MapdlConnectionPool()

        mapdl_connection = mapdl_connection_pool.get_connection()

        mapdl = mapdl_connection.connection

        try:
            mapdl.open_apdl_log(filename=analysis_log_path, mode='a')
            mapdl.cwd(analysis_dir_path)
            mapdl.resume(fname=f'{analysis_db_path}')
            #Added only in constructal_automate, but not in the original script
            mapdl.slashsolu()
            mapdl.cmsel("ALL")

            # TODO: Passar os components para variáveis de ambiente
            # Aplicar carregamento compressivo unitário
            mapdl.sfl(LINES_CONTORNO_PLACA_TS, "PRESS", n_x)
            mapdl.sfl(LINES_CONTORNO_PLACA_LS, "PRESS", csi_y*n_x)

            mapdl.sfl(LINES_BORDA_LS, "PRESS", n_x)
            mapdl.sfl(LINES_BORDA_TS, "PRESS", csi_y*n_x)

            # Resolver a flambagem elástica
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
            
            n_cr = mapdl.post_processing.time
            sigma_cr = n_cr/float(t_1)
            
            mapdl.save()
            analysis_rst_path = analysis_log_path.replace('.txt', '.rst')
            mapdl.reswrite(fname=analysis_rst_path)
            stiffened_plate_analysis.analysis_rst_file_path = analysis_rst_path
            stiffened_plate_analysis.save()
            mapdl.finish()
            # Retornar ao contexto original
            # mapdl.cwd(mapdl_connection.temp_run_location_absolute_path)
            # mapdl.filname(fname=mapdl_connection.jobname, key=0)
            # mapdl.resume(fname=f'{mapdl_connection.temp_run_location_absolute_path}/{mapdl_connection.jobname}.db')
            mapdl._close_apdl_log()
        except MapdlRuntimeError:
            mapdl._close_apdl_log()
        finally:
            mapdl_connection_pool.return_connection(mapdl_connection)
        return n_cr, sigma_cr