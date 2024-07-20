from pathlib import Path
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from ansys.mapdl.core import launch_mapdl

MAPDL_EXEC_FILE = os.getenv('MAPDL_EXEC_FILE')
MAPDL_HOST_IP = os.getenv('MAPDL_HOST_IP')
MAPDL_TEMP_DIR_PREFIX = os.getenv('MAPDL_TEMP_DIR_PREFIX')
MAPDL_ENV_VARS = {"ANSYS_LOCK": "OFF"}
MAPDL_LOG_LEVEL = os.getenv('MAPDL_LOG_LEVEL')
MAPDL_START_TIMEOUT = os.getenv('MAPDL_START_TIMEOUT')

class MapdlConnection:
    def __init__(self, connection, idx, temp_run_location_absolute_path):
        self.connection = connection
        self.idx = idx
        self.temp_run_location_absolute_path = temp_run_location_absolute_path

class MapdlConnectionPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MapdlConnectionPool, cls).__new__(cls)
                    cls._instance._initialize_pool(*args, **kwargs)
        return cls._instance

    def _initialize_pool(self, pool_size, base_dir, *args, **kwargs):
        self.pool_size = pool_size
        self.base_dir = base_dir
        self.args = args
        self.kwargs = kwargs
        self.executor = ThreadPoolExecutor(max_workers=pool_size)
        self.connections = []
        self._initialize_connections()

    def _initialize_connections(self):
        for i in range(self.pool_size):
            self.connections.append(self._create_connection(i+1))

    def _create_connection(self, idx):
        print('Creating MAPDL connection #', idx)
        jobname_string = f'{MAPDL_TEMP_DIR_PREFIX}_{idx:02d}'
        temp_run_location_absolute_path_string = f'{self.base_dir}/{jobname_string}'
        temp_run_location_absolute_path = Path(temp_run_location_absolute_path_string)
        os.makedirs(temp_run_location_absolute_path, exist_ok=True)
        
        connection = launch_mapdl(
            exec_file=MAPDL_EXEC_FILE,
            ip='127.0.0.1',
            port='50052',
            run_location=f'{temp_run_location_absolute_path_string}',
            jobname=jobname_string,
            add_env_vars=MAPDL_ENV_VARS,
            override=True,
            loglevel=MAPDL_LOG_LEVEL,
            start_timeout=MAPDL_START_TIMEOUT,
            cleanup_on_exit=True,
            print_com=True,
            log_apdl=f'{temp_run_location_absolute_path}/{jobname_string}.txt',
            *self.args,
            **self.kwargs
        )

        mapdl_connection_wrapper = MapdlConnection(connection, idx, temp_run_location_absolute_path_string)

        mapdl = mapdl_connection_wrapper.connection

        mapdl.save(slab='ALL')

        return mapdl_connection_wrapper

    def get_connection_wrapper(self):
        with self._lock:
            if not self.connections:
                raise RuntimeError("No available MAPDL connections")
            return self.connections.pop()

    def return_connection(self, mapdl_connection):
        with self._lock:
            self.connections.append(mapdl_connection)

    def close_all(self):
        with self._lock:
            for mapdl_connection in self.connections:
                mapdl_connection.connection.exit()
            self.executor.shutdown(wait=True)
