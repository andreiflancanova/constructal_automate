import atexit
from pathlib import Path
import os
import threading
from ansys.mapdl.core.pool import MapdlPool

MAPDL_EXEC_FILE = os.getenv('MAPDL_EXEC_FILE')
MAPDL_POOL_PROCESSORS_PER_CONNECTION = int(os.getenv('MAPDL_POOL_PROCESSORS_PER_CONNECTION', 1))
MAPDL_TEMP_DIR_PREFIX = os.getenv('MAPDL_TEMP_DIR_PREFIX', 'mapdl')
MAPDL_ENV_VARS = {"ANSYS_LOCK": "OFF"}
MAPDL_LOG_LEVEL = os.getenv('MAPDL_LOG_LEVEL', 'ERROR')
MAPDL_START_TIMEOUT = int(os.getenv('MAPDL_START_TIMEOUT', 30))
MAPDL_POOL_SIZE = int(os.getenv('MAPDL_POOL_SIZE', 4))
MAPDL_BASE_DIR = os.getenv('MAPDL_BASE_DIR', '/tmp/mapdl_pool')


class MapdlConnection:
    def __init__(self, connection, idx, temp_run_location_absolute_path, jobname):
        self.connection = connection
        self.idx = idx
        self.temp_run_location_absolute_path = temp_run_location_absolute_path
        self.jobname = jobname


class MapdlConnectionPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MapdlConnectionPool, cls).__new__(cls)
                    cls._instance._initialize_pool(*args, **kwargs)
                    atexit.register(cls._instance.close_all)
        return cls._instance

    def _initialize_pool(self, pool_size, base_dir, *args, **kwargs):
        self.pool_size = pool_size
        self.base_dir = base_dir
        self.args = args
        self.kwargs = kwargs

        analysis_dirs = [f'{MAPDL_TEMP_DIR_PREFIX}_{i}' for i in range(self.pool_size)]
        jobnames = ['file' for _ in range(self.pool_size)]
        run_locations = [Path(f'{self.base_dir}/{analysis_dir}') for analysis_dir in analysis_dirs]

        try:
            self.mapdl_pool = MapdlPool(
                n_instances=self.pool_size,
                run_location=self.base_dir,
                names=f'{MAPDL_TEMP_DIR_PREFIX}',
                exec_file=MAPDL_EXEC_FILE,
                nproc=MAPDL_POOL_PROCESSORS_PER_CONNECTION,
                loglevel=MAPDL_LOG_LEVEL,
                start_timeout=MAPDL_START_TIMEOUT,
                remove_temp_files=True,
                cleanup_on_exit=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MAPDL pool: {e}")
        
        self.available_connections = [
            MapdlConnection(connection, idx, str(run_location), jobname)
            for idx, (connection, run_location, jobname) in enumerate(zip(self.mapdl_pool, run_locations, jobnames))
        ]
        self.occupied_connections = []

    def get_connection(self):
        with self._lock:
            if not self.available_connections:
                raise RuntimeError("No available MAPDL connections")
            connection = self.available_connections.pop()
            self.occupied_connections.append(connection)
            return connection

    def return_connection(self, mapdl_connection):
        # TODO: Corrigir erro que ocorre quando se faz uma análise e a seção gRPC fecha
        with self._lock:
            self.occupied_connections.remove(mapdl_connection)
            self.available_connections.append(mapdl_connection)

    def close_all(self):
        with self._lock:
            for mapdl_connection in self.occupied_connections + self.available_connections:
                try:
                    mapdl_connection.connection.exit()
                except Exception as e:
                    print(f"Error closing MAPDL connection: {e}")
            self.mapdl_pool.exit()
