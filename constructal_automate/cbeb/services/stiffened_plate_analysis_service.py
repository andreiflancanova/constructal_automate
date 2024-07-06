from pathlib import Path
import os

class StiffenedPlateAnalysisService():    
    def ensure_base_path_dir_exists(self, base_path_string):
        base_path = Path(base_path_string)
        if Path.is_dir(base_path):
            pass
        else:
            Path.mkdir(base_path)
    
    def remove_previous_analysis_files(self, analysis_dir_path_string):
        analysis_dir_path = Path(analysis_dir_path_string)
        if Path.is_dir(analysis_dir_path):
            for file_name in os.listdir(analysis_dir_path):
                file = f'{analysis_dir_path}/{file_name}'
                if os.path.isfile(file):
                    os.remove(file)
            print('Files were successfully removed.')    
    
    def create_analysis_dir(self, analysis_dir_path_string):
        analysis_dir_path = Path(analysis_dir_path_string)
        Path.mkdir(analysis_dir_path)