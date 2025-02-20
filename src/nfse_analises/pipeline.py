from etl import *


if __name__ == "__main__":

    path = './data/'

    # Importar
    dados_pref = importar_dados_excel(path, "dados_nfse_prefeitura.xlsx", sheet_name= 'Resultado')
    dados_dominio = importar_dados_csv(path, "dados_nfse_dominio.csv", skiprows= 5, sep = ';', )



    # tratar colunas
    dados_pref.columns = [limpar_nome_coluna(c) for c in dados_pref.columns]
    dados_dominio.columns = [limpar_nome_coluna(c) for c in dados_dominio.columns]


    # tratamento específicio para dados da dominio
    dados_dominio = mudando_str_para_int('nota', dados_dominio)
    dados_dominio = mudando_str_para_float('valor_contabil', dados_dominio)

    # carregar dados em .csv
    carregar_dados(dados_dominio, 'csv')
    carregar_dados(dados_pref, 'csv')



    """
    TRATAMENTOS ANTES DO MERGE
    """

    # remoção de duplicatas (caso houver)
    dados_pref = dados_pref.drop_duplicates(subset=['numero'])
    dados_dominio = dados_dominio.drop_duplicates(subset=['nota'])

    


    totais_pref = dados_pref.groupby("uf_tomador")["valor_servicos"].sum()
    totais_dominio = dados_dominio.groupby("uf")["valor_contabil"].sum()

    # Comparação entre os dois
    comparacao = pd.DataFrame({
    "Prefeitura": totais_pref,
    "Domínio": totais_dominio
    }).fillna(0)  # Preenche valores ausentes com zero


    print(comparacao)

    print(dados_dominio.info())

