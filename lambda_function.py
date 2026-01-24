def lambda_handler(event, context):
    print("Evento recebido:", event)
    return {
        "statusCode": 200,
        "body": "Lambda processamentodadostcc executada com sucesso!"
    }
