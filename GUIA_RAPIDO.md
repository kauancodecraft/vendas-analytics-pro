# 🚀 Guia Rápido - Vendas Analytics Pro

## Inicialização Rápida (Recomendado)

Execute o script de inicialização que faz tudo automaticamente:

```bash
cd vendas-analytics-pro
bash run.sh
```

Este script irá:
1. ✅ Instalar todas as dependências
2. ✅ Gerar 5.000 registros de vendas
3. ✅ Executar o pipeline ETL
4. ✅ Gerar gráficos de análise (EDA)
5. ✅ Iniciar o dashboard interativo

---

## Execução Passo a Passo

Se preferir executar cada etapa manualmente:

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Gerar Dados
```bash
python3 scripts/generate_sales_data.py
```
Cria: `data/vendas.csv` (5.000 registros)

### 3️⃣ Processar Dados (ETL)
```bash
python3 scripts/etl_pipeline.py
```
Cria: `data/vendas_processadas.csv` (dados enriquecidos)

### 4️⃣ Análise Exploratória
```bash
python3 scripts/eda_analysis.py
```
Cria: 6 gráficos PNG + relatório em `notebooks/`

### 5️⃣ Iniciar Dashboard
```bash
streamlit run scripts/dashboard.py
```
Abre: `http://localhost:8501`

---

## 📊 O que Você Encontrará

### Dados
- `data/vendas.csv` - 5.000 vendas com 15 colunas
- `data/vendas_processadas.csv` - Dados enriquecidos com 25+ colunas

### Análises
- `notebooks/analise_regiao.png` - Vendas por região
- `notebooks/top_produtos.png` - Produtos mais vendidos
- `notebooks/analise_temporal.png` - Série temporal
- `notebooks/segmentacao_clientes.png` - Segmentação
- `notebooks/formas_pagamento.png` - Métodos de pagamento
- `notebooks/status_vendas.png` - Status das vendas
- `notebooks/relatorio_resumido.txt` - Relatório executivo

### Dashboard Interativo
- Filtros dinâmicos (data, região, status, etc)
- 10+ gráficos interativos
- Tabela com 100 registros
- Download de dados em CSV

---

## 🎯 KPIs Principais

| Métrica | Valor |
|---------|-------|
| Total de Vendas | 5.000 |
| Receita Total | R$ 36.586.585,60 |
| Ticket Médio | R$ 7.317,32 |
| Taxa de Sucesso | 75,24% |
| Clientes Únicos | 3.773 |

---

## 💡 Dicas Úteis

### Customizar Quantidade de Dados
Edite `scripts/generate_sales_data.py`:
```python
NUM_RECORDS = 10000  # Aumentar para 10.000 registros
```

### Alterar Período de Análise
Edite `scripts/generate_sales_data.py`:
```python
data_inicio = datetime(2023, 1, 1)
data_fim = datetime(2025, 12, 31)
```

### Adicionar Novos Produtos
Edite a lista em `scripts/generate_sales_data.py`:
```python
PRODUTOS = {
    'Novo Produto': 5000,
    # ... mais produtos
}
```

---

## 🔧 Troubleshooting

### Erro: "Módulo não encontrado"
```bash
pip install --upgrade pandas numpy matplotlib seaborn streamlit plotly
```

### Dashboard não abre
```bash
streamlit run scripts/dashboard.py --logger.level=debug
```

### Dados não foram gerados
Verifique se existe a pasta `data/`:
```bash
mkdir -p data
python3 scripts/generate_sales_data.py
```

---

## 📚 Estrutura de Arquivos

```
vendas-analytics-pro/
├── data/                          # Dados
│   ├── vendas.csv
│   └── vendas_processadas.csv
├── scripts/                       # Scripts Python
│   ├── generate_sales_data.py
│   ├── etl_pipeline.py
│   ├── eda_analysis.py
│   └── dashboard.py
├── notebooks/                     # Resultados de análise
│   ├── *.png (gráficos)
│   └── relatorio_resumido.txt
├── run.sh                         # Script de inicialização
├── requirements.txt               # Dependências
├── README.md                      # Documentação completa
└── GUIA_RAPIDO.md                # Este arquivo
```

---

## 🎓 Aprendizados

Este projeto demonstra:

✅ Geração de dados realistas
✅ Pipeline ETL profissional
✅ Análise exploratória completa
✅ Visualizações com Matplotlib/Seaborn
✅ Dashboard interativo com Streamlit
✅ Boas práticas de código Python
✅ Estrutura profissional de projetos

---

## 📞 Próximos Passos

1. **Explore os dados** - Abra `data/vendas_processadas.csv` em Excel/Pandas
2. **Analise os gráficos** - Veja os PNGs em `notebooks/`
3. **Interaja com o dashboard** - Use os filtros e explore os dados
4. **Customize** - Altere produtos, períodos, regiões
5. **Expanda** - Adicione novas análises e visualizações

---

**Aproveite a análise! 📊**

Autor: kauancodecraft
