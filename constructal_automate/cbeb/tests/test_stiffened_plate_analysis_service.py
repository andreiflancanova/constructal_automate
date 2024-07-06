import os
from pathlib import Path
from django.test import SimpleTestCase
from unittest.mock import patch
from cbeb.services.stiffened_plate_analysis_service import StiffenedPlateAnalysisService

ROOT_DIR_COMPLETE_PATH = 'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_analysis_files'

class StiffenedPlateAnalysisServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = StiffenedPlateAnalysisService()

    def tearDown(self):
        # Limpar ou reverter qualquer alteração após cada teste
        test_dir_to_remove = [
            'dir_for_test_01',
            'dir_for_test_02'
        ]

        base_dir = ROOT_DIR_COMPLETE_PATH
        
        for test_dir in test_dir_to_remove:
            dir_to_remove = Path(base_dir) / test_dir
            if dir_to_remove.exists() and dir_to_remove.is_dir():
                # Remover o diretório e todos os seus conteúdos
                for item in dir_to_remove.glob('*'):
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        item.rmdir()
                dir_to_remove.rmdir()
                print(test_dir, "removed successfully.")

    def test_ensure_base_path_dir_creation_when_it_didnt_exist_before(self):
        test_dir = 'dir_for_test_01'
        base_path_string = f'{ROOT_DIR_COMPLETE_PATH}/{test_dir}'
        base_path = Path(base_path_string)

        # Garantir que o diretório não exista antes de chamar o método
        self.assertFalse(base_path.exists())

        # Chamar o método
        self.service.ensure_base_path_dir_exists(base_path_string)
        print(test_dir, "created.")

        # Verificar se o diretório foi criado
        self.assertTrue(base_path.exists())
        self.assertTrue(base_path.is_dir())

    def test_ensure_base_path_dir_exists_when_it_already_exists(self):
        test_dir = 'dir_for_test_02'
        base_path_string = f'{ROOT_DIR_COMPLETE_PATH}/{test_dir}'
        base_path = Path(base_path_string)

        # Criar o diretório manualmente antes de chamar o método
        base_path.mkdir()
        print(test_dir, "created.")

        # Chamar o método
        self.service.ensure_base_path_dir_exists(base_path_string)

        # Verificar se o diretório existe
        self.assertTrue(base_path.exists())
        self.assertTrue(base_path.is_dir())
