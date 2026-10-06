import pandas as pd
import numpy as np
import os

def processar_dados_complexos(caminho_entrada, caminho_saida="dados_processados.xlsx"):
    """
    Realiza o tratamento avançado de um conjunto de dados, incluindo limpeza,
    cálculos estatísticos e agrupamentos estruturados.
    """
    if not os.path.exists(caminho_entrada):
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return None

    try:
        # 1. Carregamento dos dados
        print("Carregando o arquivo...")
        if caminho_entrada.endswith('.csv'):
            df = pd.read_csv(caminho_entrada)
        else:
            df = pd.read_excel(caminho_entrada)

        print(f"Total inicial de registros: {len(df)}")

        # 2. Padronização de colunas (removendo espaços e colocando em minúsculas)
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # 3. Tratamento de valores ausentes (Nulos)
        # Preenche colunas numéricas com a mediana e texto com 'Não Informado'
        for coluna in df.select_dtypes(include=[np.number]).columns:
            df[coluna] = df[coluna].fillna(df[coluna].median())
        
        for coluna in df.select_dtypes(include=['object']).columns:
            df[coluna] = df[coluna].fillna("Não Informado")

        # 4. Criação de métricas/colunas derivadas (exemplo de regra de negócio)
        # Se houver colunas de quantidade e valor unitário, calcula o total
        if 'quantidade' in df.columns and 'valor_unitario' in df.columns:
            df['valor_total'] = df['quantidade'] * df['valor_unitario']

        # 5. Agrupamento e Sumarização Avançada (Exemplo por categoria)
        if 'categoria' in df.columns and 'valor_total' in df.columns:
            resumo_categoria = df.groupby('categoria').agg(
                total_vendas=('valor_total', 'sum'),
                media_vendas=('valor_total', 'mean'),
                quantidade_registros=('valor_total', 'count')
            ).reset_index()
            
            print("\nResumo Agrupado por Categoria:")
            print(resumo_categoria)

        # 6. Exportação do resultado processado
        df.to_excel(caminho_saida, index=False)
        print(f"\nSucesso! Arquivo processado salvo com segurança em: '{caminho_saida}'")
        
        return df

    except Exception as e:
        print(f"Ocorreu um erro durante o processamento avançado: {e}")
        return None

if __name__ == "__main__":
    # Exemplo de chamada da função
    arquivo_alvo = "base_dados.xlsx"
    processar_dados_complexos(arquivo_alvo)
