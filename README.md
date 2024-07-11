### Constructal Automate

Para criar o venv que você vai utilizar

```bash
python -m venv constructal_automate
```

Para utilizar o venv que você criou:
```bash
source "D:\01_Mestrando_Andrei_PPGMC_2022\python-env-dirs\constructal_automate\Scripts\activate"
```

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```
Para dar o quickstart do projeto, execute:

```bash
django-admin startproject constructal_automate
```

```bash
cd constructal_automate
```
Para executar o projeto 
```bash
python manage.py runserver --noreload
```

Criar a app 'Calculate Stiffener Geometry'
```bash
python manage.py startapp csg
```

Criar a app 'Calculate Biaxial Elastic Buckling'
```bash
python manage.py startapp cbeb
```

Criar as migrations do banco de dados
```bash
python manage.py makemigrations
```

OBS.: Lembrar de colocar cada model nova dentro de /models/__init__.py para o Django reconhecer, como no exemplo a seguir:

```bash
from .plate import Plate
```

Executar a migração das tabelas da app csg
```bash
python manage.py migrate csg
```

Executar o projeto:
```bash
python manage.py runserver --noreload
```

OBS.: Durante a implementação do MapdlConnectionPool, foi identificado que durante a criação das conexões com o MAPDL, algum arquivo é criado ou atualizado no diretório do projeto, e isso faz com que o Django reinicie. É por este motivo que é necessário passar a flag --noreload, para que o Django não reinicie quando da alteração de arquivos.
