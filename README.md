# Constructal Automate

Projeto desenvolvido durante a dissertação de mestrado em Modelagem Computacional pela Universidade Federal do Rio Grande do acadêmico Andrei Ferreira Lançanova, com o intuito de automatizar os fluxos de modelagem computacional e simulação numérica do problema de flambagem elasto-plástica biaxial de placas com enrijecedores.

## Subindo a Arquitetura na sua Máquina Local

### Requisitos

- **Git** instalado para clonar o repositório.
- **Docker e Docker Compose** instalados para gerenciar os containers.
- **PowerShell com privilégios de administrador** para iniciar o servidor GRPC do ANSYS MAPDL.

### Passos para iniciar a arquitetura

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/andreiflancanova/constructal_automate
   cd constructal_automate
   ```

2. **Subir os containers Docker**

   ```bash
   docker compose -p ca-press up --build --detach
   ```

3. **Iniciar o servidor GRPC do ANSYS MAPDL**

   O servidor **GRPC do ANSYS MAPDL** deve ser iniciado na porta **50052** usando o **PowerShell** como administrador:

   ```powershell
   Start-Process "C:\Program Files\ANSYS Inc\ANSYS Student\v242\ansys\bin\winx64\ANSYS242.exe" `
     -ArgumentList "-grpc -port 50052 -np 1 -dir `"D:\constructal_automate_analysis_files\ansys_mapdl_tmp_dir`"" `
     -Verb RunAs
   ```

### Parando e Removendo os Containers Docker

Caso precise parar e remover os containers Docker:

```bash
docker-compose -p ca-press down
```


## Dicas e Cuidados para Desenvolvedores

### Configuração do Ambiente Virtual

Para criar o ambiente virtual que será utilizado:

```bash
python -m venv constructal_automate
```

Para ativar o ambiente virtual:

```bash
source "D:\01_Mestrando_Andrei_PPGMC_2022\python-env-dirs\constructal_automate\Scripts\activate"
```

### Instalação das Dependências

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

### Inicialização do Projeto Django

Para criar um novo projeto Django:

```bash
django-admin startproject constructal_automate
```

Navegue até a pasta do projeto recém-criado:

```bash
cd constructal_automate
```

### Execução do Servidor de Desenvolvimento sem Docker

Caso prefira rodar o projeto localmente sem Docker, utilize o seguinte comando:

```bash
python manage.py runserver --noreload
```

> **Nota:** A opção `--noreload` evita que o Django reinicie automaticamente quando arquivos do projeto são modificados, prevenindo possíveis interferências com a criação de conexões do `MapdlConnectionPool`.

### Criação das Aplicações Django

Para criar a aplicação **Calculate Stiffener Geometry (CSG)**:

```bash
python manage.py startapp csg
```

Para criar a aplicação **Calculate Biaxial Elastic Buckling (CBEB)**:

```bash
python manage.py startapp cbeb
```

### Configuração do Banco de Dados

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

### Geração de Diagramas com Graphviz

Para gerar um arquivo **.dot** contendo a visão geral da arquitetura:

```bash
python manage.py graph_models -a --dot > uml/arquitetura_visao_geral.dot
```

Para converter o arquivo **.dot** em **PDF**:

```bash
dot -Tpdf uml/arquitetura_visao_geral.dot -o uml/arquitetura_visao_geral.pdf
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


