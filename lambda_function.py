import boto3
import pandas as pd
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_in = "dadosentrada-797225460896-us-east-1" 
    bucket_out = "dadossaida-797225460896-us-east-1"
    response = s3.list_objects_v2(Bucket=bucket_in)

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            print(f"Lendo arquivo: {key}")

            # Baixar CSV
            file_obj = s3.get_object(Bucket=bucket_in, Key=key)
            data = file_obj["Body"].read().decode("utf-8")

            # Converter para DataFrame
            df = pd.read_csv(io.StringIO(data))

            # Exemplo de tratamento: substituir "NA" por valores nulos
            df = df.replace("NA", pd.NA)

            # Converter para Parquet
            buffer = io.BytesIO()
            df.to_parquet(buffer, index=False)

            # Salvar no bucket de saída
            output_key = f"parquet/{key.replace('.csv', '.parquet')}"
            s3.put_object(Bucket=bucket_out, Key=output_key, Body=buffer.getvalue())

            print(f"Arquivo convertido salvo em {bucket_out}/{output_key}")
    else:
        print("Nenhum arquivo encontrado no bucket de entrada.")
