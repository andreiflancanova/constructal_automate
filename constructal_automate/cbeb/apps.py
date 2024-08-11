import atexit
import os
from django.apps import AppConfig
from .config import MapdlConnectionPool

MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH')
MAPDL_POOL_NUMBER_OF_CONNECTIONS = int(os.getenv('MAPDL_POOL_NUMBER_OF_CONNECTIONS'))


class CbebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbeb'

    def ready(self):
        if not hasattr(self, 'pool_initialized'):
            mapdl_connection_pool = MapdlConnectionPool(
                pool_size=MAPDL_POOL_NUMBER_OF_CONNECTIONS,
                base_dir=MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH,
            )
            self.pool_initialized = True
            atexit.register(mapdl_connection_pool.close_all)
