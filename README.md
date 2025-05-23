# Streamlit BI App - Documentação

## Visão Geral

Esta aplicação web foi desenvolvida em Python utilizando Streamlit e Pandas para criar um sistema de Business Intelligence (BI) com as seguintes funcionalidades:

- Autenticação de usuário (inicialmente com credenciais fixas: admin/admin)
- Upload e processamento de arquivos CSV
- Dashboards interativos com gráficos e filtros
- Controle de sessão para usuários logados
- Preparado para deploy em Docker

## Estrutura do Projeto (MVC)

O projeto segue a arquitetura MVC (Model-View-Controller) para melhor organização e manutenção:

```
streamlit_bi_app/
│
├── models/              # Lógica de negócios e processamento de dados
│   └── data_processor.py
│
├── views/               # Interface do usuário
│   ├── login_view.py
│   ├── upload_view.py
│   └── dashboard_view.py
│
├── controllers/         # Controle de fluxo da aplicação
│   └── app_controller.py
│
├── utils/               # Utilitários e funções auxiliares
│   └── auth.py
│
├── data/                # Diretório para armazenamento de dados processados
│
├── src/                 # Código fonte principal
│   └── main.py
│
├── requirements.txt     # Dependências do projeto
└── Dockerfile           # Configuração para deploy em Docker
```

## Funcionalidades

### Autenticação de Usuário

- Login inicial com credenciais fixas: usuário `admin` e senha `admin`
- Estrutura preparada para futura integração com JWT e banco de dados relacional
- Controle de sessão para manter usuários logados

### Upload e Processamento de Dados

- Upload de arquivos CSV
- Processamento automático com Pandas
- Detecção de tipos de dados (numéricos, categóricos, datas)
- Análise preliminar dos dados (valores ausentes, estatísticas básicas)
- Armazenamento de múltiplos datasets na sessão

### Dashboards Interativos

- Visualização de dados em diferentes tipos de gráficos:
  - Gráficos de barras
  - Gráficos de pizza
  - Gráficos de linhas
  - Mapas de calor
- Filtros dinâmicos por:
  - Data (quando disponível)
  - Categorias
- Tabelas dinâmicas para visualização dos dados filtrados

## Requisitos Técnicos

- Python 3.11 ou superior
- Bibliotecas principais:
  - streamlit==1.32.0
  - pandas==2.1.0
  - plotly==5.18.0
  - numpy==1.26.0
  - python-dotenv==1.0.0
  - pyjwt==2.8.0

## Instalação e Execução

### Execução Local

1. Clone o repositório ou extraia os arquivos
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   streamlit run src/main.py
   ```

### Execução com Docker

1. Construa a imagem Docker:
   ```
   docker build -t streamlit-bi-app .
   ```
2. Execute o container:
   ```
   docker run -p 8501:8501 streamlit-bi-app
   ```
3. Acesse a aplicação em seu navegador:
   ```
   http://localhost:8501
   ```

## Uso da Aplicação

1. Faça login com as credenciais padrão (usuário: `admin`, senha: `admin`)
2. Na página de Upload, faça o upload de um arquivo CSV
3. Após o processamento, navegue para a página de Dashboard
4. Utilize os filtros na barra lateral para refinar os dados
5. Configure os gráficos selecionando as colunas apropriadas
6. Explore os diferentes tipos de visualização disponíveis

## Preparação para Futuras Expansões

### Autenticação Avançada

A estrutura atual está preparada para:
- Implementação de JWT para tokens de autenticação
- Integração com banco de dados relacional (PostgreSQL ou MySQL)
- Gerenciamento de múltiplos usuários e níveis de acesso

### Expansão de Funcionalidades

Possíveis expansões futuras:
- Exportação de dashboards em PDF ou Excel
- Agendamento de relatórios automáticos
- Integração com fontes de dados externas
- Implementação de machine learning para análise preditiva

## Notas de Segurança

- A implementação atual utiliza credenciais fixas apenas para demonstração
- Em ambiente de produção, recomenda-se:
  - Implementar autenticação baseada em JWT
  - Utilizar HTTPS para todas as comunicações
  - Armazenar senhas com hash seguro
  - Implementar controle de acesso baseado em funções (RBAC)
