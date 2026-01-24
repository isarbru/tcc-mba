import awswrangler as wr
import boto3

def lambda_handler(event, context):
    bucket_in = "dadosentrada-797225460896-us-east-1"
    bucket_out = "dadossaida-797225460896-us-east-1"

    # Lista arquivos CSV no bucket de entrada
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_in)

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            print(f"Lendo arquivo: {key}")

            # Caminho completo do arquivo CSV
            input_path = f"s3://{bucket_in}/{key}"

            # Ler CSV direto do S3
            df = wr.s3.read_csv(path=input_path)

            # Tratamento simples: substituir "NA" por valores nulos
            df = df.replace("NA", None)

            # Caminho de saída em Parquet
            output_path = f"s3://{bucket_out}/parquet/{key.replace('.csv', '.parquet')}"

            # Salvar em Parquet
            wr.s3.to_parquet(df=df, path=output_path, dataset=False)

            print(f"Arquivo convertido salvo em {output_path}")
    else:
        print("Nenhum arquivo encontrado no bucket de entrada.")
