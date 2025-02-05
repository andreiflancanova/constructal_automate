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

Ativar o virtualenv
```bash
cd ../../python-env-dirs/
source constructal-automate-dev01-0.68/Scripts/activate
```

Executar o projeto:
```bash
python manage.py runserver --noreload
```

OBS.: Durante a implementação do MapdlConnectionPool, foi identificado que durante a criação das conexões com o MAPDL, algum arquivo é criado ou atualizado no diretório do projeto, e isso faz com que o Django reinicie. É por este motivo que é necessário passar a flag --noreload, para que o Django não reinicie quando da alteração de arquivos.


#### Graphviz
Para usar arquivo dot seja gerado, execute:

```bash
python manage.py graph_models -a --dot > uml/arquitetura_visao_geral.dot
```

Para gerar o pdf do UML a partir do dot:

```bash
dot -Tpdf uml/arquitetura_visao_geral.dot -o uml/arquitetura_visao_geral.pdf
```

```bash
dot -Tpdf uml/fluxograma_estudo_caso_design_construtal.dot -o uml/fluxograma_estudo_caso_design_construtal.pdf
```

Para gerar fluxogramas com formatação Latex
```bash
dot2tex --format tikz uml/fluxograma_estudo_caso_design_construtal.dot > uml/fluxograma_estudo_caso_design_construtal.tex
```

Para compilar para pdf:
```bash
pdflatex uml/fluxograma_estudo_caso_design_construtal.tex
```

Para gerar automaticamente a partir do projeto Django:

```bash
pyreverse -o dot -p cbeb constructal_automate/cbeb
```

```bash
dot -Tpdf classes_cbeb.dot -o classes_cbeb.pdf
```

```bash
pyreverse -o dot -p csg constructal_automate/csg
```

```bash
dot -Tpdf classes_csg.dot -o classes_csg.pdf
```

### Docker

docker compose -p ca-press up -d ca-db

docker-compose -p ca-press down

 docker build -t ca-app -f Dockerfile.app .