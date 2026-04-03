# Trabalho C1 - BI

Dashboard em Streamlit para analise exploratoria dos microdados de COVID-19 do Espirito Santo.

## Arquivos principais

- `app_streamlit_dashboard_covid_es.py`: dashboard principal
- `Atividade_C1_PedroBonela.ipynb`: notebook base da atividade

## Como executar

1. Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

2. Baixe o arquivo `MICRODADOS.csv` no painel oficial:

- https://coronavirus.es.gov.br/painel-covid-19-es

3. Coloque o `MICRODADOS.csv` na mesma pasta do projeto.

4. Execute:

```powershell
python -m streamlit run app_streamlit_dashboard_covid_es.py
```

## Fonte dos dados

- Painel COVID-19 ES: https://coronavirus.es.gov.br/painel-covid-19-es
