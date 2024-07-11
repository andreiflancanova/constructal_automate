import atexit
from django.apps import AppConfig
from .config import MapdlConnectionPool


MAPDL_CONNECTION_POOL_SIZE = 3
MAPDL_ROOT_DIR_COMPLETE_PATH = 'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_analysis_files'

class CbebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbeb'

    def ready(self):
        global mapdl_connection_pool
        if not hasattr(self, 'pool_initialized'):
            mapdl_connection_pool = MapdlConnectionPool(
                pool_size=MAPDL_CONNECTION_POOL_SIZE,
                base_dir=MAPDL_ROOT_DIR_COMPLETE_PATH,
            )
            self.pool_initialized = True
            atexit.register(mapdl_connection_pool.close_all)
