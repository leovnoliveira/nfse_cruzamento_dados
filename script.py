import pandas as pd
from typing import Union, List
import unicodedata
import os

def carregar_dados(pref_path: str, dominio_path: str) -> tuple:
    """
    Carrega os dados da Prefeitura e da Domínio.
    
    Args:
        pref_path (str): Caminho do arquivo de dados da Prefeitura (.xlsx)
        dominio_path (str): Caminho do arquivo de dados da Domínio (.csv)
    
    Returns:
        tuple: DataFrames df_pref (Prefeitura) e df_dominio (Domínio)
    """
    try:
        df_pref = pd.read_excel(pref_path, engine="openpyxl", sheet_name= 'Resultado')
        df_dominio = pd.read_csv(dominio_path, skiprows= 5, sep = ";", encoding="ISO-8859-1")
        return df_pref, df_dominio
    except Exception as e:
        print(f"Erro ao carregar arquivos: {e}")
        return None, None
    

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



def limpar_dados(df_pref: pd.DataFrame, df_dominio: pd.DataFrame) -> tuple:
    """
    Limpa e padroniza os dados para evitar erros no merge.
    
    Args:
        df_pref (pd.DataFrame): Dados da Prefeitura
        df_dominio (pd.DataFrame): Dados da Domínio
    
    Returns:
        tuple: DataFrames limpos
    """
    # Padronizar colunas de nome e número da nota
    df_pref.rename(columns={'nome_razao_social_tomador': 'cliente', 'numero': 'numero_nota'}, inplace=True)
    df_dominio.rename(columns={'nota': 'numero_nota'}, inplace=True)

    # Converter para string e remover espaços extras
    df_pref['cliente'] = df_pref['cliente'].astype(str).str.strip().str.lower()
    df_dominio['cliente'] = df_dominio['cliente'].astype(str).str.strip().str.lower()

    # Padronizar a UF
    df_pref['uf_tomador'] = df_pref['uf_tomador'].astype(str).str.strip().str.upper()
    df_dominio['uf'] = df_dominio['uf'].astype(str).str.strip().str.upper()

    return df_pref, df_dominio


def realizar_merge(df_pref: pd.DataFrame, df_dominio: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o merge dos dados da Prefeitura e Domínio para identificar notas que estão na Prefeitura mas não na Domínio.

    Args:
        df_pref (pd.DataFrame): Dados da Prefeitura
        df_dominio (pd.DataFrame): Dados da Domínio
    
    Returns:
        pd.DataFrame: DataFrame com registros que estão na Prefeitura mas não na Domínio
    """
    resultado = pd.merge(
        df_dominio,
        df_pref,
        how='right',  # Mantém todos os valores da Prefeitura e tenta casar com os da Domínio
        left_on=['cliente', 'numero_nota'],
        right_on=['cliente', 'numero_nota'],
        indicator=True
    )

    # Filtrar registros que estão na Prefeitura mas não na Domínio
    clientes_nao_encontrados = resultado[resultado["_merge"] == "right_only"][['cliente', 'numero_nota', 'uf_tomador']]
    
    return clientes_nao_encontrados

def salvar_resultado(df: pd.DataFrame, output_path: str):
    """
    Salva o resultado final em um arquivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os clientes que estão na Prefeitura mas não na Domínio
        output_path (str): Caminho onde o arquivo será salvo
    """
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Arquivo salvo com sucesso em {output_path}")

# 🏁 Execução do script
if __name__ == "__main__":
    # Definir caminhos dos arquivos
    caminho_pref = os.path.join("./data/", "dados_nfse_prefeitura.xlsx")
    caminho_dominio = os.path.join("./data/", "dados_nfse_dominio.csv")
    caminho_saida = "clientes_para_busca.csv"

    # Carregar dados
    df_pref, df_dominio = carregar_dados(caminho_pref, caminho_dominio)

    # Tratar nomes
    df_pref.columns = [limpar_nome_coluna(c) for c in df_pref.columns]
    df_dominio.columns = [limpar_nome_coluna(c) for c in df_dominio.columns]

    # Tratamento específico para a tabela da dominio

     # tratamento específicio para dados da dominio
    df_dominio = mudando_str_para_int('nota', df_dominio)
    df_dominio = mudando_str_para_float('valor_contabil', df_dominio)


    if df_pref is not None and df_dominio is not None:
        # Limpar dados
        df_pref, df_dominio = limpar_dados(df_pref, df_dominio)

        # Realizar merge e encontrar clientes que precisam de busca na Prefeitura
        clientes_nao_encontrados = realizar_merge(df_pref, df_dominio)

        # Salvar resultado final
        salvar_resultado(clientes_nao_encontrados, caminho_saida)
