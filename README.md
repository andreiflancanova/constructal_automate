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

```bash
python manage.py runserver
```

Criar a app 'Calculate Stiffener Geometry'
```bash
python manage.py startapp csg
```

```bash
python manage.py makemigrations
```

OBS.: Lembrar de colocar cada model nova dentro de /models/__init__.py para o Django reconhecer, como no exemplo a seguir:

```bash
from .plate import Plate
```

```bash
python manage.py migrate csg
```
