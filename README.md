# 📊 Vendas Analytics Pro

Um projeto profissional e completo de análise de dados de vendas em Python, com pipeline ETL, análise exploratória (EDA) e dashboard interativo.

**Autor:** kauancodecraft

---

## 🎯 Objetivo

Este projeto demonstra as melhores práticas em análise de dados, incluindo:

- **Geração de dados realistas** com 5.000 registros de vendas
- **Pipeline ETL** robusto para limpeza e transformação de dados
- **Análise Exploratória (EDA)** com insights e visualizações
- **Dashboard interativo** profissional com Streamlit
- **Documentação completa** e código bem estruturado

---

## 📁 Estrutura do Projeto

```
vendas-analytics-pro/
├── data/
│   ├── vendas.csv                 # Dados brutos gerados
│   └── vendas_processadas.csv     # Dados após ETL
├── scripts/
│   ├── generate_sales_data.py     # Geração de dados
│   ├── etl_pipeline.py            # Pipeline ETL
│   ├── eda_analysis.py            # Análise exploratória
│   └── dashboard.py               # Dashboard Streamlit
├── notebooks/
│   ├── analise_regiao.png         # Gráficos EDA
│   ├── top_produtos.png
│   ├── analise_temporal.png
│   ├── segmentacao_clientes.png
│   ├── formas_pagamento.png
│   ├── status_vendas.png
│   └── relatorio_resumido.txt
├── README.md                       # Este arquivo
└── requirements.txt               # Dependências Python
```

---

## 🚀 Como Usar

### 1. Instalação de Dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install pandas numpy matplotlib seaborn streamlit plotly
```

### 2. Gerar Dados

Execute o script de geração de dados:

```bash
python3 scripts/generate_sales_data.py
```

**Saída esperada:**
- `data/vendas.csv` com 5.000 registros

### 3. Executar Pipeline ETL

Processe e enriqueça os dados:

```bash
python3 scripts/etl_pipeline.py
```

**Saída esperada:**
- `data/vendas_processadas.csv` com dados transformados
- Relatório de KPIs principais

### 4. Análise Exploratória (EDA)

Gere gráficos e insights:

```bash
python3 scripts/eda_analysis.py
```

**Saída esperada:**
- 6 gráficos PNG em `notebooks/`
- Relatório resumido em texto

### 5. Executar Dashboard Interativo

Inicie o dashboard Streamlit:

```bash
streamlit run scripts/dashboard.py
```

O dashboard abrirá em `http://localhost:8501`

---

## 📊 Principais Métricas

| Métrica | Valor |
|---------|-------|
| **Total de Vendas** | 5.000 |
| **Receita Total** | R$ 36.586.585,60 |
| **Ticket Médio** | R$ 7.317,32 |
| **Taxa de Sucesso** | 75,24% |
| **Clientes Únicos** | 3.773 |
| **Produtos Únicos** | 15 |
| **Margem Total** | R$ 10.975.975,68 |

---

## 🔍 Análises Incluídas

### 1. Análise por Região
- Receita total por região
- Quantidade de vendas
- Ticket médio
- Taxa de sucesso

### 2. Análise de Produtos
- Top 10 produtos por receita
- Quantidade vendida
- Ticket médio por produto
- Distribuição por categoria

### 3. Análise Temporal
- Série temporal de receita
- Tendências mensais
- Padrões por dia da semana
- Sazonalidade

### 4. Segmentação de Clientes
- Classificação: Bronze, Prata, Ouro
- Distribuição de clientes
- Receita por segmento
- Comportamento de compra

### 5. Formas de Pagamento
- Distribuição de métodos
- Receita por forma de pagamento
- Preferências regionais

### 6. Status de Vendas
- Distribuição: Concluída, Pendente, Cancelada, Devolvida
- Receita por status
- Taxa de sucesso

---

## 🎨 Dashboard Interativo

O dashboard oferece:

✅ **KPIs em tempo real** - Métricas principais em cards
✅ **Filtros dinâmicos** - Período, região, status, segmento, forma de pagamento
✅ **Gráficos interativos** - Plotly com zoom, pan e hover
✅ **Tabela de detalhes** - Visualização e download de dados
✅ **Exportação** - Baixar dados filtrados em CSV

### Funcionalidades:

- **Sidebar com filtros** - Customize a análise em tempo real
- **Gráficos responsivos** - Adapta-se a qualquer tamanho de tela
- **Tabela interativa** - Selecione colunas e ordene dados
- **Download de dados** - Exporte resultados em CSV

---

## 📈 Insights Principais

### Receita por Região
- **Sudeste** lidera com R$ 7.631.757,50
- **Centro-Oeste** com R$ 7.463.777,80
- Distribuição equilibrada entre regiões

### Produtos Top
1. **iPhone 15 Pro** - R$ 7.646.644,05
2. **Samsung Galaxy S24** - R$ 5.235.027,35
3. **Notebook Dell XPS 13** - R$ 4.508.550,00

### Segmentação de Clientes
- **Ouro** (549 clientes) - 44,8% da receita
- **Prata** (1.443 clientes) - 44,8% da receita
- **Bronze** (1.781 clientes) - 10,5% da receita

### Formas de Pagamento
- **Boleto** - R$ 7.896.282,90 (21,6%)
- **Cartão Crédito** - R$ 7.572.443,90 (20,7%)
- **Crediário** - R$ 7.359.812,90 (20,1%)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.11+ | Linguagem principal |
| **Pandas** | 2.0+ | Manipulação de dados |
| **NumPy** | 1.20+ | Operações numéricas |
| **Matplotlib** | 3.5+ | Visualizações estáticas |
| **Seaborn** | 0.12+ | Gráficos estatísticos |
| **Streamlit** | 1.20+ | Dashboard interativo |
| **Plotly** | 5.0+ | Gráficos interativos |

---

## 📋 Arquivos de Dados

### vendas.csv
Dados brutos com 5.000 registros e 15 colunas:
- `id_venda` - Identificador único
- `data_venda` - Data da transação
- `cliente_nome` - Nome do cliente
- `produto` - Produto vendido
- `valor_final` - Valor da venda
- `regiao` - Região geográfica
- `forma_pagamento` - Método de pagamento
- `status` - Status da venda

### vendas_processadas.csv
Dados enriquecidos após ETL com colunas adicionais:
- Componentes de data (ano, mês, trimestre, dia_semana)
- Faixas de valor
- Segmentação de clientes
- Indicadores de sucesso
- Tempo de entrega categorizado

---

## 🔧 Customização

### Alterar quantidade de registros
Edite `scripts/generate_sales_data.py`:
```python
NUM_RECORDS = 10000  # Aumentar para 10.000 registros
```

### Adicionar novos produtos
Edite a lista `PRODUTOS` em `generate_sales_data.py`:
```python
PRODUTOS = {
    'Novo Produto': 5000,
    # ... mais produtos
}
```

### Customizar período de análise
Edite as datas em `generate_sales_data.py`:
```python
data_inicio = datetime(2023, 1, 1)
data_fim = datetime(2025, 12, 31)
```

---

## 📚 Documentação Adicional

- **EDA Report** - Veja `notebooks/relatorio_resumido.txt`
- **Gráficos** - Verifique os arquivos PNG em `notebooks/`
- **Dados Processados** - Analise `data/vendas_processadas.csv`

---

## ⚠️ Requisitos do Sistema

- Python 3.8+
- 100MB de espaço em disco
- Navegador moderno (para Streamlit)
- Conexão com internet (para Plotly CDN)

---

## 🐛 Troubleshooting

### Streamlit não inicia
```bash
pip install --upgrade streamlit
streamlit run scripts/dashboard.py --logger.level=debug
```

### Erro ao carregar dados
Verifique se os arquivos CSV existem:
```bash
ls -la data/
```

### Gráficos não aparecem
Limpe o cache do Streamlit:
```bash
streamlit cache clear
```

---

## 📝 Licença

Este projeto é de código aberto e pode ser utilizado livremente para fins educacionais e comerciais.

---

## 👨‍💻 Autor

**kauancodecraft**

Desenvolvedor apaixonado por análise de dados e visualizações.

---

## 📞 Suporte

Para dúvidas ou sugestões sobre o projeto, entre em contato ou abra uma issue no repositório.

---

## 🎓 Aprendizados

Este projeto demonstra:

✅ Estrutura profissional de projetos Python
✅ Pipeline ETL completo
✅ Análise exploratória de dados
✅ Visualizações com Matplotlib e Seaborn
✅ Dashboard interativo com Streamlit
✅ Boas práticas de código
✅ Documentação clara e completa

---

**Última atualização:** 25/02/2026

Aproveite a análise! 📊
