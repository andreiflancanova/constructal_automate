from pathlib import Path
import os
from ansys.mapdl.core import launch_mapdl


ROOT_DIR_COMPLETE_PATH = 'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_analysis_files'


class StiffenedPlateAnalysisService():

    def ensure_base_path_dir_exists(self):
        base_path = Path(ROOT_DIR_COMPLETE_PATH)
        if Path.is_dir(base_path):
            pass
        else:
            Path.mkdir(base_path)

    def ensure_analysis_dir_exists(self, analysis_dir_name):
        global analysis_dir_path_string
        analysis_dir_path_string = f'{ROOT_DIR_COMPLETE_PATH}/{analysis_dir_name}'
        if Path.is_dir(Path(analysis_dir_path_string)):
            for file_name in os.listdir(analysis_dir_path_string):
                file = f'{analysis_dir_path_string}/{file_name}'
                if os.path.isfile(file):
                    os.remove(file)
            print('Previous files were successfully removed.')    
        else:
            Path.mkdir(Path(analysis_dir_path_string))

    def create_initial_analysis_files(self, analysis_name):
        self.ensure_base_path_dir_exists()
        self.ensure_analysis_dir_exists(analysis_name)
        # self.validate_mapdl_connection(analysis_dir_path_string, analysis_name)


    # def validate_mapdl_connection(self, execution_dir, execution_file_name):
    #     try:
    #         pymapdl = launch_mapdl(
    #             run_location=f'{execution_dir}/',
    #             jobname=execution_file_name,
    #             override=True,
    #             cleanup_on_exit=True,
    #             loglevel='WARNING',
    #             start_timeout=120,
    #             log_apdl=f'{execution_dir}/{execution_file_name}.txt',
    #             print_com=True
    #         )
            
    #         print(pymapdl)
            
    #         return str(pymapdl)
    #     finally:
    #         pymapdl.save()
    #         pymapdl.exit()
        