import pandas as pd
import unicodedata
from typing import List, Union
import os


path = './data/'

# dados domínio

def importar_dados_csv(path: str, nome_do_arquivo: str, skiprows: int, sep: str)  -> pd.DataFrame:

    """
    Importa um arquivo CSV, removendo linhas inválidas e colunas vazias.

    Args:
        path (str): Caminho da pasta onde o arquivo está localizado.
        nome_do_arquivo (str): Nome do arquivo CSV.
        skiprows (int): Número de linhas a serem puladas no início do arquivo.
        sep (str): Separador de colunas no CSV.

    Returns:
        pd.DataFrame: DataFrame limpo e pronto para análise.
    """

    df = pd.read_csv(os.path.join(path, nome_do_arquivo),
                            skiprows = skiprows,
                            sep = sep,
                            encoding= 'ISO-8859-1'
                            )
    
    # Remover linhas que contêm palavras-chave irrelevantes
    palavras_chave_remover = [
        "ACOMPANHAMENTO DE SERVIÇOS",
        "Sistema licenciado para",
        "Total Estado",
        "Total Geral"
    ]

    df = df[~df.apply(lambda row: any(palavra in str(row.values) for palavra in palavras_chave_remover), axis = 1)]
    # Removar colunas completamente vazias
    df = df.dropna(axis = 1, how = 'all')
    # Remover linhas vazias
    #df = df.dropna(axis = 0, how = 'all')

    df = df.reset_index(drop= True)
    
    return df


def importar_dados_excel(path: str, nome_do_arquivo: str, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(os.path.join(path, nome_do_arquivo), engine = 'openpyxl',
    sheet_name = sheet_name)

     # Removar colunas completamente vazias
    df = df.dropna(axis = 1, how = 'all')
    # Remover linhas vazias
    df = df.dropna(axis = 0, how = 'all')

    df = df.reset_index(drop= True)

    return df


def remove_acentos(texto):
    """
    Remove acentos de uma string.
    """
    # Normaliza a string para separar os acentos dos caracteres
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Reconstrói a string apenas com os caracteres que não são marcas de acentuação (categoria 'Mn')
    return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

def limpar_nome_coluna(coluna: list):
    """
    Limpa o nome da coluna:
    - Remove acentos
    - Remove espaços desnecessários
    - Substitui espaços e '/' por underline
    - Remove parênteses
    - Converte para minúsculas
    """
    coluna = remove_acentos(coluna)
    coluna = coluna.strip()
    coluna = coluna.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
    coluna = coluna.lower()
    return coluna

def mudando_str_para_int(coluna: Union[str, List[str]], df: pd.DataFrame) -> pd.DataFrame:

    """
    Função que vai tornar a coluna de valores numericos em int64 e corrigir inconsistencias
    
    """

    # Se a coluna for uma stirng, transforma e lista para manter consistencia
    if isinstance(coluna, str):
        coluna = [coluna]

    for col in coluna:

        df[col]  = pd.to_numeric(df[col] , errors= 'coerce')
        df = df.dropna(subset=[col])
        df[col] = df[col].astype('int64')

    return df

def mudando_str_para_float(coluna: Union[str, List[str]], df: pd.DataFrame) -> pd.DataFrame:

    """
    Função que vai tornar a coluna de valores numericos em float e corrigir inconsistencias
    
    """

    # Se a coluna for uma stirng, transforma e lista para manter consistencia
    if isinstance(coluna, str):
        coluna = [coluna]

    for col in coluna:

        df[col] = df[col].astype(str).str.replace(",", ".")
        df[col]  = pd.to_numeric(df[col] , errors= 'coerce')
        df = df.dropna(subset=[col])
        df[col] = df[col].astype('float')

    return df

# print(data_pref.columns)
# print(data_dominio.columns)

# Padronizar os dados antes do merge
# data_pref['nome_razao_social_tomador'] = data_pref['nome_razao_social_tomador'].astype(str).str.strip().str.lower()
# data_dominio['cliente'] = data_dominio['cliente'].astype(str).str.strip().str.lower()

# data_pref['uf_tomador'] = data_pref['uf_tomador'].astype(str).str.strip().str.upper()
# data_dominio['uf'] = data_dominio['uf'].astype(str).str.strip().str.upper()

def merge_de_dados(df_left: pd.DataFrame, df_right: pd.DataFrame, chave: str, left_on: None, right_on: None) -> pd.DataFrame:

    resultado = pd.merge(
        df_left,
        df_right,
        how = chave,
        left_on = left_on,
        right_on = right_on,
        indicator= True # cria uma cooluna que indica a origiem do dado
    )

    return resultado

def clientes_nao_encontrados(df: pd.DataFrame, lado: str, colunas: list) -> pd.DataFrame:

    clientes_nao_encontrados = df[df["_merge"] == lado][colunas]

    clientes_nao_encontrados = clientes_nao_encontrados.rename(columns = {'numero': 'numero_nota'})

    return clientes_nao_encontrados


def carregar_dados(df: pd.DataFrame, formato_de_saida: str):

    """
    parametro que vai ser ou "csv" ou "excel" ou "os dois".

    """
    nome_do_arquivo = input("Digite o nome base do arquivo (sem extensão): ").strip()

    # Define o caminho do diretório onde o script está localizado
    caminho_script = os.path.dirname(os.path.realpath(__file__))
    arquivo_csv = os.path.join(caminho_script, f"{nome_do_arquivo}.csv")
    arquivo_xlsx = os.path.join(caminho_script, f"{nome_do_arquivo}.xlsx")

    arquivo_csv = f"{nome_do_arquivo}.csv"
    arquivo_xlsx = f"{nome_do_arquivo}.xlsx"



    if formato_de_saida == "csv":
            df.to_csv(arquivo_csv, index=False)
            print(f"ARquivos salvo com sucesso: {arquivo_csv}")

    elif formato_de_saida.lower() == "excel":
            df.to_excel(arquivo_xlsx, index = False)
            print(f"Arquivos salvos com sucesso: {arquivo_xlsx}")

    elif formato_de_saida.lower() == "ambos":
        df.to_csv(arquivo_csv, index=False)
        df.to_excel(arquivo_xlsx, index=False)
        print(f"Arquivos salvos com sucesso:\n- {arquivo_csv}\n- {arquivo_xlsx}")
        print(f"Arquivos salvos com sucesso:\n- {arquivo_csv}\n- {arquivo_xlsx}")

    else:
        print("Formato de saída inválido. Escolha 'csv', 'excel' ou 'ambos'.")
    

# print(data_dominio.info())
# print(data_pref.info())


print(clientes_nao_encontrados)
#clientes_nao_encontrados.to_csv("dados_clientes_nao_encontrados.csv")


