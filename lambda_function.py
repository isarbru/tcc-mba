import awswrangler as wr
import boto3
import os

def lambda_handler(event, context):
    bucket_in = "dadosentrada-797225460896-us-east-1"
    sns_topic_arn = os.environ["SNS_TOPIC_ARN"]

    s3 = boto3.client("s3")
    sns = boto3.client("sns")

    response = s3.list_objects_v2(Bucket=bucket_in)

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            print(f"Lendo arquivo: {key}")
            input_path = f"s3://{bucket_in}/{key}"

            # Detecta se é Excel ou CSV
            if key.endswith(".xlsx"):
                df = wr.s3.read_excel(path=input_path)
            else:
                df = wr.s3.read_csv(path=input_path, sep=";", on_bad_lines="skip", encoding="latin1")

            # Calcula NPS
            total = len(df)
            detratores = len(df[df["NPS"] <= 1])
            neutros = len(df[(df["NPS"] >= 2) & (df["NPS"] <= 3)])
            promotores = len(df[df["NPS"] >= 4])

            perc_detratores = (detratores / total) * 100
            perc_promotores = (promotores / total) * 100
            nps = perc_promotores - perc_detratores

            # Monta relatório
            message = (
                f"Relatório de NPS - Arquivo {key}\n\n"
                f"Total de respostas: {total}\n"
                f"Promotores: {promotores} ({perc_promotores:.1f}%)\n"
                f"Neutros: {neutros}\n"
                f"Detratores: {detratores} ({perc_detratores:.1f}%)\n\n"
                f"NPS final: {nps:.1f}"
            )

            # Envia via SNS (e-mail)
            sns.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject="Relatório diário de NPS"
            )

            print("Relatório enviado por e-mail.")
    else:
        print("Nenhum arquivo encontrado no bucket de entrada.")
