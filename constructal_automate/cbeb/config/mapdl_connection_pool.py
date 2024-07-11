from pathlib import Path
import os
# from multiprocessing import Pool
import threading
from concurrent.futures import ThreadPoolExecutor
from ansys.mapdl.core import launch_mapdl

MAPDL_TEMP_DIR_PREFIX = 'mapdl_connection_temp_dir'
MAPDL_LOG_LEVEL = 'WARNING'
MAPDL_START_TIMEOUT = 120

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
            self.connections.append(self._create_connection(i))

    def _create_connection(self, idx):
        print('Creating MAPDL connection #', idx)
        jobname = f'{MAPDL_TEMP_DIR_PREFIX}_{idx:02d}'
        run_location = Path(f'{self.base_dir}/{jobname}')
        os.makedirs(run_location, exist_ok=True)
        return launch_mapdl(
            run_location=run_location,
            jobname=jobname,
            override=True,
            loglevel=MAPDL_LOG_LEVEL,
            start_timeout=MAPDL_START_TIMEOUT,
            cleanup_on_exit=True,
            print_com=True,
            log_apdl=f'{run_location}/{jobname}.txt',
            *self.args,
            **self.kwargs
        )

    def get_connection(self):
        with self._lock:
            if not self.connections:
                raise RuntimeError("No available MAPDL connections")
            return self.connections.pop()

    def return_connection(self, connection):
        with self._lock:
            self.connections.append(connection)

    def close_all(self):
        with self._lock:
            for connection in self.connections:
                connection.exit()
            self.executor.shutdown(wait=True)
    #TODO: Fix 'UnboundLocalError: local variable 'lockfile' referenced before assignment'