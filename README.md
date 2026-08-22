# 📈 Financial Market Dashboard

Aplicação de análise de mercado financeiro desenvolvida em Python, que consome dados da Alpha Vantage, armazena informações em PostgreSQL e disponibiliza análises interativas através de Streamlit.

O projeto também implementa ingestão incremental e previsão de séries temporais utilizando Prophet.

<img width="1280" height="576" alt="tela-financial" src="https://github.com/user-attachments/assets/46b64ea1-a641-4199-8989-5438d374d3ea" />

## 🎯 Objetivos

Os principais objetivos do projeto são:
- consumir dados de uma API externa;
- construir um processo de ingestão de dados;
- armazenar dados históricos em um banco relacional;
- evitar duplicação de registros;
- implementar atualização incremental dos dados;
- disponibilizar os dados através de uma aplicação interativa;
- realizar análises sobre séries temporais;
- gerar previsões de preços;
- organizar o código de forma modular e reutilizável.

# ⚙️ Funcionalidades

## 📡 Consumo de API

A aplicação possui um cliente dedicado para comunicação com a Alpha Vantage. O cliente é responsável por:
- realizar as requisições;
- autenticar utilizando API Key;
- receber os dados;
- tratar respostas da API;
- disponibilizar os dados para o pipeline de transformação.

A integração foi isolada no módulo: api/client.py

Isso evita que regras relacionadas à API fiquem espalhadas pelo restante da aplicação.

## 🔄 Ingestão incremental

Um dos principais componentes do projeto é o processo de ingestão incremental.

Ao solicitar uma atualização, a aplicação verifica qual é a data mais recente disponível no banco de dados.
```
             PostgreSQL
                  │
                  ▼
       Última data armazenada
                  │
                  ▼
          Consulta à API
                  │
                  ▼
       Existem dados novos?
             /          \
           NÃO          SIM
            │             │
            ▼             ▼
       Nada a fazer    Inserir
                         dados
                          │
                          ▼
                      PostgreSQL
```
Dessa maneira, o sistema evita inserir novamente registros que já existem na base.

## 📊 Dashboard interativo

A aplicação utiliza Streamlit para permitir que o usuário interaja com os dados. É possível:
- selecionar o ativo;
- selecionar o período de análise;
- visualizar os dados históricos;
- visualizar os preços de fechamento;
- consultar indicadores;
- atualizar os dados;
- gerar previsões.

## 📈 Análise histórica

O projeto realiza análises sobre os dados históricos dos ativos. Entre os cálculos implementados estão:
- retorno diário;
- retorno acumulado;
- média móvel;
- preço máximo;
- preço mínimo;
- resumo estatístico.

Os cálculos estão centralizados no módulo: analysis/metrics.py

## 🔮 Previsão

Para a previsão de preços futuros foi utilizado o Prophet.

O modelo utiliza os preços históricos como entrada e gera uma estimativa para períodos futuros.

O usuário pode definir o horizonte da previsão diretamente no dashboard.

⚠️ Aviso: as previsões apresentadas possuem finalidade exclusivamente educacional e analítica. O projeto não constitui recomendação ou aconselhamento financeiro.

## 🛠️ Tecnologias

| Tecnologia    | Utilização           |
| ------------- | -------------------- |
| Python        | Desenvolvimento      |
| Pandas        | Tratamento dos dados |
| Alpha Vantage | Fonte dos dados (API)|
| PostgreSQL    | Persistência         |
| SQLAlchemy    | ORM/conexão          |
| Streamlit     | Dashboard            |
| Prophet       | Forecast             |
| Git/GitHub    | Versionamento        |

## 🏗️ Arquitetura
<img width="1414" height="2000" alt="Documento A4 Floral Bege e Branco" src="https://github.com/user-attachments/assets/4fcb810c-fac3-4aec-9555-366e8accc08d" />

## 📂 Estrutura
```
financial-market-dashboard/
│
├── analysis/
│   ├── forecast.py      # Previsão dos dados
│   └── metrics.py       # Cálculo de indicadores
│
├── api/
│   └── client.py        # Conexão e consumo da API
│
├── data/
│   └── transform.py     # Tratamento dos dados
│
├── database/
│   ├── connection.py    # Conexão com PostgreSQL
│   ├── ingestion.py     # Inserção de dados no banco
│   ├── init_db.py       # Inicialização e criação das tabelas
│   ├── models.py        # Definição dos modelos/tabelas
│   └── repository.py    # Consulta e persistência dos dados
│
├── app.py               # Interface com usuário
├── main.py              # Back-end de ingestão dos dados 
├── seed_assets.py       # Cadastro dos ativos na aplicação
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Como executar
Clone o repositório:
```
git clone https://github.com/SEU_USUARIO/financial-market-dashboard.git
cd financial-market-dashboard
```

Crie o ambiente virtual:
```
python -m venv .venv
```

Ative o ambiente:
```
.venv\Scripts\activate
```

Instale as dependências:
```
pip install -r requirements.txt
```

Crie um arquivo na raiz do projeto chamado:
```
.env
```

Utilize o .env.example como referência:
```
ALPHA_VANTAGE_API_KEY = DIGITE AQUI SUA CHAVE DA API
DB_USER = postgres
DB_PASSWORD = DIGITE AQUI SUA SENHA DO POSTGRESQL
DB_HOST = localhost
DB_PORT = 5433
DB_NAME = db_financial
```

Inicialize o banco de dados:
```
python database/init_db.py
```

Cadastre os ativos da API previamente mapeados:
```
python seed_assets.py
```

Execute a aplicação:
```
streamlit run app.py
```

## 🖥️ Utilizando o dashboard

Ao iniciar a aplicação, o usuário poderá selecionar um ativo através do menu:
```
Selecionar ativo
       ↓
Selecionar período
       ↓
Visualizar dados
       ↓
Analisar histórico
       ↓
Gerar previsão
```

## 🔄 Atualização dos dados

O dashboard possui uma funcionalidade de atualização dos dados.

Ao solicitar uma atualização, o sistema verifica a última data armazenada para o ativo.

Caso os dados estejam atualizados:
```
✓ Dados já estão atualizados.
```
Caso existam dados novos:
```
✓ Novos dados encontrados.
✓ Banco de dados atualizado.
```
Essa abordagem reduz inserções desnecessárias e permite manter a base atualizada.

## 📸 Demonstração

### Dashboard:
<img width="1358" height="603" alt="image" src="https://github.com/user-attachments/assets/951daf4c-41cb-4c48-9548-a5aead521cfe" />

### Atualização dos Dados:
<img width="1280" height="568" alt="chrome-capture-2026-08-22" src="https://github.com/user-attachments/assets/e0176340-4b99-44cd-b6dd-0e132780554e" />

### Previsão:
<img width="1280" height="571" alt="chrome-capture-2026-08-22 (1)" src="https://github.com/user-attachments/assets/1de3fa9f-0694-49ea-87a4-eeef2030654b" />

## 🎓 Objetivo do projeto

Este projeto foi desenvolvido como parte do meu portfólio com o objetivo de demonstrar conhecimentos práticos em Python, análise de dados, integração com APIs, bancos de dados e desenvolvimento de aplicações de dados.

A proposta foi construir uma aplicação completa, desde a obtenção dos dados até sua disponibilização para análise através de uma interface interativa.

## 👨‍💻 Autor

Guilherme Georgetti Albuquerque Galvão

Analista de Dados / Engenheiro de Produção — UNESP

🔗 LinkedIn: www.linkedin.com/in/guilherme-georgetti 
