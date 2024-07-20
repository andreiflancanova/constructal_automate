import os
from dotenv import load_dotenv
from django.apps import AppConfig
from .config import MapdlConnectionPool

load_dotenv()
MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH = os.getenv('MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH')
MAPDL_POOL_NUMBER_OF_INSTANCES = int(os.getenv('MAPDL_POOL_NUMBER_OF_INSTANCES'))


class CbebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbeb'

    def ready(self):
        global mapdl_connection_pool
        if not hasattr(self, 'pool_initialized'):
            mapdl_connection_pool = MapdlConnectionPool(
                pool_size=MAPDL_POOL_NUMBER_OF_INSTANCES,
                base_dir=MAPDL_OUTPUT_BASEDIR_ABSOLUTE_PATH,
            )
            self.pool_initialized = True
