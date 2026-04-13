import awswrangler as wr
import boto3
import os
from datetime import datetime, timedelta

BUCKET_DADOS = "dadosentrada-797225460896-us-east-1"
SNS_TOPIC = os.environ["SNS_TOPIC_ARN"]


def le_dados():
    try:
        s3_client = boto3.client("s3")
        response = s3_client.list_objects_v2(Bucket=BUCKET_DADOS)
    except:
        print("Erro na leitura de dados")
    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            print(f"Lendo arquivo: {key}")
            input_path = f"s3://{BUCKET_DADOS}/{key}"
            df = wr.s3.read_excel(path=input_path)
        
        return df
    else:
        print("Nenhum arquivo encontrado no bucket de entrada.")
        return None


def tratativa_nps(dados):
    total = len(dados)

    detratores = len(dados[dados["metrica_nps"] <= 6])
    neutros = len(dados[(dados["metrica_nps"] >= 7) & (dados["metrica_nps"] <= 8)])
    promotores = len(dados[dados["metrica_nps"] >= 9])

    data = datetime.now() - timedelta(days=1)

    porcentagem_detratores = (detratores / total) * 100
    porcentagem_neutros = (neutros / total) * 100
    porcentagem_promotores = (promotores / total) * 100

    nps = porcentagem_promotores - porcentagem_detratores

    message = (
        f"Relatório de NPS da loja - {data.date()}\n\n"
        f"Total de respostas: {total}\n"
        f"Promotores: {promotores} ({porcentagem_promotores:.1f}%)\n"
        f"Neutros: {neutros} ({porcentagem_neutros:.1f}%)\n"
        f"Detratores: {detratores} ({porcentagem_detratores:.1f}%)\n\n"
        f"NPS: {nps:.1f}"
    )
    
    return message


def manda_email(message):
    try:
        sns_client = boto3.client("sns")
        sns_client.publish(
                TopicArn=SNS_TOPIC,
                Message=message,
                Subject="Relatório diário de NPS"
            )

        print("Relatório enviado por e-mail.")
    except:
        print("Erro ao enviar relatório por email")


def lambda_handler(event, context):
    dados = le_dados()
    if dados is not None and not dados.empty:
        message = tratativa_nps(dados)
        manda_email(message)