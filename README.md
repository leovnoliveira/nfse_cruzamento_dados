# Cruzamento de dados de NFSe de diferentes fontes


Este repositório se trata de um ETL de dados de diferentes fontes.


## Fontes

1. Domínio Contábil (módulo Escrita Fiscal)
2. Prefeitura de Belo Horizonte (Relatório de notas fiscais emitidas por compotência)


## Problema de Negócio

Algumas notas fiscais extraídas da prefeitura de BH não foram escrituradas corretamente, resultando em diferença entre a rotina fiscal na Domínio e relatório de notas fiscais.

Por essa razão, realizou-se uma tabela Dinâmica em Google Sheets com o arquivo excel extraído da prefeitura para verificar o somantório de notas emitidas por UF.

Fazendo a mesma rotina na Domínio, constatou-se que o somatório de notas fiscais emitidas para as UFs de Minas Gerais e Rio de Janeiro. Por conta disso, fui em busca de identificar por que dessa diferença e quais notas essas que foram afetadas.

Assim, definiu-se três objetivos principais:

1. ETL dados prefeitura
2. ETL dados Dominio
3. Cruzamento de dados da Prefeitura e Domínio

Output final esperado do cruzamento seriam:

* Número da nota fiscal emitida;
* UF da nota fiscal;
* Valor da nota fiscal;
* Tomador do serviço


## Versionamento 

Para este projeto utilizou-se a versão 3.13.1 do Python. A instação ocorreu via `pyenv`.
1. `pyenv versions` para verificar as versões do python instaladas na sua máquina
2. `pyenv install 3.13.1` para instalar a versão que foi utilizada neste projeto;
3. `pyenv local 3.13.1` para setar a versão 3.13.1 para ser utilizada no seu projeto

Para saber mais sobre a instalação do pyenv, [acesso o a documentação do projeto](https://github.com/pyenv/pyenv).


## Gerenciamento de pacotes

Utilizou-se a biblioteca `Poetry` para criação do ambiente virtual e instalação dos pacotes necessários.

Para instalar o Poetry, no terminal do bash faça:

1. `pip install pipx` (para usuários de Windows, certifique-se que o pipx foi para seu path de variáveis de ambiente)
2. `pipx install poetry`
3. `poetry init`(para criar o arquivo pyproject.toml)
4. Ou, melhor ainda, faça `poetry new 'nome-do-seu-projeto'`, que já cria um ambiente básico de projeto, com pasta de test, pasta principal, o arquivo pyproject.toml, um README.md e um .gitignore.
5. `poetry add loguru` (para adicionar o pacote logurue ao pyproject.toml)
6. `poetry env activate` para ativar seu ambiente virtual com o pacote logoru. Este passo irá adicionar uma pasta .venv no seu projeto.
7. `poetry run python 'archive.py'` para rodar um script python no terminal utilizando seu ambiente virtual poetry.

Para mais detalhes sobre o poetry, [acesse a documentação da lib](https://python-poetry.org/docs/)

## Features

`etl.py`: script de execução de ordem do código
`pipeline.py`: execução do `etl.py`
`data/`: diretório de dados

## Tecnologias

Para verificar as tecnologias utilizadas neste projeto, acesso o arquivo `pyproject.toml`