import pandas as pd

def parquet_to_json(parquet_file_path, json_output_path):
    # Lendo o arquivo Parquet usando pandas
    df = pd.read_parquet(parquet_file_path)
    
    # Convertendo o DataFrame para JSON e salvando o arquivo
    df.to_json(json_output_path, orient='records', lines=True)

# Caminho para o arquivo Parquet de entrada
parquet_file_path = 'ans/202405.parquet'

# Caminho para o arquivo JSON de saída
json_output_path = 'ans/202405.json'

# Convertendo Parquet para JSON
parquet_to_json(parquet_file_path, json_output_path)
