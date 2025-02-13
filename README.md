# Constructal Automate

## Configuração do Ambiente Virtual

Para criar o ambiente virtual que será utilizado:

```bash
python -m venv constructal_automate
```

Para ativar o ambiente virtual:

```bash
source "D:\01_Mestrando_Andrei_PPGMC_2022\python-env-dirs\constructal_automate\Scripts\activate"
```

## Instalação das Dependências

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

## Inicialização do Projeto Django

Para criar um novo projeto Django, execute:

```bash
django-admin startproject constructal_automate
```

Navegue até a pasta do projeto recém-criado:

```bash
cd constructal_automate
```

## Execução do Servidor de Desenvolvimento

Para iniciar o servidor de desenvolvimento do Django, execute:

```bash
python manage.py runserver --noreload
```

> **Nota:** A opção `--noreload` evita que o Django reinicie automaticamente quando arquivos do projeto são modificados, prevenindo possíveis interferências com a criação de conexões do `MapdlConnectionPool`.

## Criação das Aplicações Django

Para criar a aplicação **Calculate Stiffener Geometry (CSG)**:

```bash
python manage.py startapp csg
```

Para criar a aplicação **Calculate Biaxial Elastic Buckling (CBEB)**:

```bash
python manage.py startapp cbeb
```

## Configuração do Banco de Dados

Para criar as migrations do banco de dados:

```bash
python manage.py makemigrations
```

> **Importante:** Cada novo model deve ser importado no arquivo `/models/__init__.py` para que o Django o reconheça. Exemplo:
>
> ```python
> from .plate import Plate
> ```

Para aplicar as migrations da aplicação **CSG**:

```bash
python manage.py migrate csg
```

## Ativação do Ambiente Virtual e Execução do Projeto

Caso precise ativar novamente o ambiente virtual:

```bash
cd ../../python-env-dirs/
source constructal-automate-dev01-0.68/Scripts/activate
```

Executar o projeto:

```bash
python manage.py runserver --noreload
```

## Geração de Diagramas com Graphviz

Para gerar um arquivo **.dot** contendo a visão geral da arquitetura:

```bash
python manage.py graph_models -a --dot > uml/arquitetura_visao_geral.dot
```

Para converter o arquivo **.dot** em **PDF**:

```bash
dot -Tpdf uml/arquitetura_visao_geral.dot -o uml/arquitetura_visao_geral.pdf
```

```bash
dot -Tpdf uml/fluxograma_estudo_caso_design_construtal.dot -o uml/fluxograma_estudo_caso_design_construtal.pdf
```

Para gerar fluxogramas formatados em **LaTeX**:

```bash
dot2tex --format tikz uml/fluxograma_estudo_caso_design_construtal.dot > uml/fluxograma_estudo_caso_design_construtal.tex
```

Para compilar o arquivo **LaTeX** para **PDF**:

```bash
pdflatex uml/fluxograma_estudo_caso_design_construtal.tex
```

### Geração Automática a partir do Projeto Django

Gerar diagramas para a aplicação **CBEB**:

```bash
pyreverse -o dot -p cbeb constructal_automate/cbeb
```

```bash
dot -Tpdf classes_cbeb.dot -o classes_cbeb.pdf
```

Gerar diagramas para a aplicação **CSG**:

```bash
pyreverse -o dot -p csg constructal_automate/csg
```

```bash
dot -Tpdf classes_csg.dot -o classes_csg.pdf
```

## Docker

Para construir e executar os containers do projeto:

```bash
docker compose -p ca-press up --build --detach
```

Para parar e remover os containers:

```bash
docker-compose -p ca-press down
```

Para construir a imagem Docker da aplicação:

```bash
docker build -t ca-app -f Dockerfile.app .
```

