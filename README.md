# Relatório de NPS com AWS Lambda e SNS

Este projeto implementa uma solução **serverless** utilizando **Amazon Web Services (AWS)** para automatizar o cálculo e envio de relatórios de satisfação de clientes com base na métrica **Net Promoter Score (NPS)**.  

Os dados de pesquisa pós-compra são armazenados em um bucket **Amazon S3**, processados diariamente por uma função **AWS Lambda** escrita em **Python**, e enviados por e‑mail através de um tópico **Amazon SNS**.

---

## 🚀 Funcionalidades
- Leitura automática de arquivos **Excel/CSV** armazenados no S3.  
- Cálculo das métricas de satisfação (baixo, médio e alto).  
- Geração do índice **NPS**.  
- Envio diário de relatório por e‑mail via SNS.  
- Execução agendada com **Amazon EventBridge**.  

---

## 🛠️ Tecnologias utilizadas
- **Python 3.x**  
- **AWS Lambda**  
- **Amazon S3**  
- **Amazon SNS**  
- **Amazon EventBridge**  
- Bibliotecas: `boto3`, `awswrangler`, `datetime`  

---

## 📂 Estrutura do projeto
├── lambda_function.py   # Código principal da função Lambda
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do repositório


---

## ⚙️ Como executar
1. Crie um bucket no **Amazon S3** e faça upload dos arquivos de pesquisa.  
2. Configure uma função **AWS Lambda** com o código deste repositório.  
3. Defina a variável de ambiente `SNS_TOPIC_ARN` com o ARN do tópico SNS.  
4. Configure um **trigger do EventBridge** para execução diária.  
5. Verifique o e‑mail subscrito no SNS para receber os relatórios.  

---

## 📊 Exemplo de saída
Relatório de NPS da loja - 2026-01-24

Total de respostas: 120
Nota alta: 80 (66.7%)
Nota média: 25 (20.8%)
Nota baixa: 15 (12.5%)

Média de satisfação: 66.7



## 🔑 Palavras-chave
AWS; Lambda; SNS; NPS; Automação
