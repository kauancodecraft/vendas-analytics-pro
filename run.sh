#!/bin/bash

# Script de inicialização - Vendas Analytics Pro
# Este script executa todo o pipeline de forma automática

echo "=========================================="
echo "🚀 VENDAS ANALYTICS PRO - INICIALIZAÇÃO"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 não encontrado. Por favor, instale Python 3.8+${NC}"
    exit 1
fi

echo -e "${BLUE}✅ Python encontrado: $(python3 --version)${NC}"

# Instalar dependências
echo -e "\n${BLUE}📦 Instalando dependências...${NC}"
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
else
    echo -e "${YELLOW}⚠️  Erro ao instalar dependências${NC}"
    exit 1
fi

# Gerar dados
echo -e "\n${BLUE}📊 Gerando dados de vendas...${NC}"
python3 scripts/generate_sales_data.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dados gerados com sucesso${NC}"
else
    echo -e "${YELLOW}⚠️  Erro ao gerar dados${NC}"
    exit 1
fi

# Executar ETL
echo -e "\n${BLUE}🔄 Executando pipeline ETL...${NC}"
python3 scripts/etl_pipeline.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pipeline ETL concluído${NC}"
else
    echo -e "${YELLOW}⚠️  Erro ao executar ETL${NC}"
    exit 1
fi

# Executar EDA
echo -e "\n${BLUE}🔍 Executando análise exploratória...${NC}"
python3 scripts/eda_analysis.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Análise exploratória concluída${NC}"
else
    echo -e "${YELLOW}⚠️  Erro ao executar EDA${NC}"
    exit 1
fi

# Iniciar dashboard
echo -e "\n${GREEN}=========================================="
echo -e "✅ PIPELINE CONCLUÍDO COM SUCESSO!"
echo -e "==========================================${NC}"
echo -e "\n${BLUE}🎯 Iniciando dashboard Streamlit...${NC}"
echo -e "${YELLOW}O dashboard abrirá em: http://localhost:8501${NC}\n"

streamlit run scripts/dashboard.py
