#!/usr/bin/env python3
"""
Análise Exploratória de Dados (EDA) - Vendas Analytics Pro
Gera insights, estatísticas e visualizações dos dados de vendas.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Configurações
INPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendas_processadas.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

# Estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

def carregar_dados():
    """Carrega os dados processados."""
    df = pd.read_csv(INPUT_PATH, parse_dates=['data_venda'])
    return df

def analise_vendas_por_regiao(df):
    """Analisa vendas por região."""
    print("\n📍 ANÁLISE POR REGIÃO")
    print("=" * 60)
    
    regiao_stats = df.groupby('regiao').agg({
        'id_venda': 'count',
        'valor_final': ['sum', 'mean'],
        'venda_sucesso': 'mean'
    }).round(2)
    
    regiao_stats.columns = ['Total Vendas', 'Receita Total', 'Ticket Médio', 'Taxa Sucesso']
    regiao_stats['Taxa Sucesso'] = (regiao_stats['Taxa Sucesso'] * 100).round(2)
    
    print(regiao_stats)
    
    # Visualização
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análise de Vendas por Região', fontsize=16, fontweight='bold')
    
    # Receita por região
    df.groupby('regiao')['valor_final'].sum().sort_values(ascending=False).plot(
        kind='bar', ax=axes[0, 0], color='#2E86AB'
    )
    axes[0, 0].set_title('Receita Total por Região')
    axes[0, 0].set_ylabel('Receita (R$)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Quantidade de vendas
    df['regiao'].value_counts().plot(kind='bar', ax=axes[0, 1], color='#A23B72')
    axes[0, 1].set_title('Quantidade de Vendas por Região')
    axes[0, 1].set_ylabel('Número de Vendas')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Ticket médio
    df.groupby('regiao')['valor_final'].mean().sort_values(ascending=False).plot(
        kind='bar', ax=axes[1, 0], color='#F18F01'
    )
    axes[1, 0].set_title('Ticket Médio por Região')
    axes[1, 0].set_ylabel('Valor (R$)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Taxa de sucesso
    (df.groupby('regiao')['venda_sucesso'].mean() * 100).sort_values(ascending=False).plot(
        kind='bar', ax=axes[1, 1], color='#06A77D'
    )
    axes[1, 1].set_title('Taxa de Sucesso por Região (%)')
    axes[1, 1].set_ylabel('Percentual (%)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'analise_regiao.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: analise_regiao.png")

def analise_produtos_top(df):
    """Analisa os produtos mais vendidos."""
    print("\n🛍️  PRODUTOS TOP 10")
    print("=" * 60)
    
    produtos_stats = df.groupby('produto').agg({
        'id_venda': 'count',
        'valor_final': ['sum', 'mean'],
        'quantidade': 'sum'
    }).round(2)
    
    produtos_stats.columns = ['Vendas', 'Receita Total', 'Ticket Médio', 'Quantidade']
    produtos_stats = produtos_stats.sort_values('Receita Total', ascending=False).head(10)
    
    print(produtos_stats)
    
    # Visualização
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Top 10 Produtos', fontsize=16, fontweight='bold')
    
    top_produtos = df.groupby('produto')['valor_final'].sum().nlargest(10).sort_values()
    top_produtos.plot(kind='barh', ax=axes[0, 0], color='#2E86AB')
    axes[0, 0].set_title('Receita Total')
    axes[0, 0].set_xlabel('Receita (R$)')
    
    top_vendas = df['produto'].value_counts().head(10).sort_values()
    top_vendas.plot(kind='barh', ax=axes[0, 1], color='#A23B72')
    axes[0, 1].set_title('Quantidade de Vendas')
    axes[0, 1].set_xlabel('Número de Vendas')
    
    top_ticket = df.groupby('produto')['valor_final'].mean().nlargest(10).sort_values()
    top_ticket.plot(kind='barh', ax=axes[1, 0], color='#F18F01')
    axes[1, 0].set_title('Ticket Médio')
    axes[1, 0].set_xlabel('Valor (R$)')
    
    top_quantidade = df.groupby('produto')['quantidade'].sum().nlargest(10).sort_values()
    top_quantidade.plot(kind='barh', ax=axes[1, 1], color='#06A77D')
    axes[1, 1].set_title('Quantidade Total Vendida')
    axes[1, 1].set_xlabel('Unidades')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'top_produtos.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: top_produtos.png")

def analise_temporal(df):
    """Analisa tendências temporais."""
    print("\n📅 ANÁLISE TEMPORAL")
    print("=" * 60)
    
    vendas_mes = df.groupby(df['data_venda'].dt.to_period('M')).agg({
        'id_venda': 'count',
        'valor_final': 'sum'
    })
    
    print("Vendas por Mês (últimos 12 meses):")
    print(vendas_mes.tail(12))
    
    # Visualização
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Análise Temporal de Vendas', fontsize=16, fontweight='bold')
    
    # Série temporal de receita
    df_temporal = df.set_index('data_venda').resample('D')['valor_final'].sum()
    df_temporal.plot(ax=axes[0], color='#2E86AB', linewidth=2)
    axes[0].set_title('Receita Diária (Série Temporal)')
    axes[0].set_ylabel('Receita (R$)')
    axes[0].grid(True, alpha=0.3)
    
    # Vendas por dia da semana
    vendas_dia_semana = df.groupby('dia_semana')['id_venda'].count()
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    vendas_dia_semana = vendas_dia_semana.reindex(ordem_dias)
    vendas_dia_semana.plot(kind='bar', ax=axes[1], color='#A23B72')
    axes[1].set_title('Vendas por Dia da Semana')
    axes[1].set_ylabel('Número de Vendas')
    axes[1].set_xlabel('Dia da Semana')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'analise_temporal.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: analise_temporal.png")

def analise_segmentacao_clientes(df):
    """Analisa segmentação de clientes."""
    print("\n👥 SEGMENTAÇÃO DE CLIENTES")
    print("=" * 60)
    
    segmento_stats = df.groupby('segmento_cliente').agg({
        'id_cliente': 'nunique',
        'id_venda': 'count',
        'valor_final': ['sum', 'mean']
    }).round(2)
    
    segmento_stats.columns = ['Clientes Únicos', 'Total Vendas', 'Receita Total', 'Ticket Médio']
    print(segmento_stats)
    
    # Visualização
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Segmentação de Clientes', fontsize=16, fontweight='bold')
    
    # Distribuição de clientes
    df.groupby('segmento_cliente')['id_cliente'].nunique().plot(
        kind='pie', ax=axes[0, 0], autopct='%1.1f%%', colors=['#2E86AB', '#A23B72', '#F18F01']
    )
    axes[0, 0].set_title('Distribuição de Clientes por Segmento')
    axes[0, 0].set_ylabel('')
    
    # Receita por segmento
    df.groupby('segmento_cliente')['valor_final'].sum().plot(
        kind='bar', ax=axes[0, 1], color=['#2E86AB', '#A23B72', '#F18F01']
    )
    axes[0, 1].set_title('Receita Total por Segmento')
    axes[0, 1].set_ylabel('Receita (R$)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Ticket médio por segmento
    df.groupby('segmento_cliente')['valor_final'].mean().plot(
        kind='bar', ax=axes[1, 0], color=['#2E86AB', '#A23B72', '#F18F01']
    )
    axes[1, 0].set_title('Ticket Médio por Segmento')
    axes[1, 0].set_ylabel('Valor (R$)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Quantidade de vendas por segmento
    df.groupby('segmento_cliente')['id_venda'].count().plot(
        kind='bar', ax=axes[1, 1], color=['#2E86AB', '#A23B72', '#F18F01']
    )
    axes[1, 1].set_title('Quantidade de Vendas por Segmento')
    axes[1, 1].set_ylabel('Número de Vendas')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'segmentacao_clientes.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: segmentacao_clientes.png")

def analise_formas_pagamento(df):
    """Analisa formas de pagamento."""
    print("\n💳 ANÁLISE DE FORMAS DE PAGAMENTO")
    print("=" * 60)
    
    pagamento_stats = df.groupby('forma_pagamento').agg({
        'id_venda': 'count',
        'valor_final': ['sum', 'mean']
    }).round(2)
    
    pagamento_stats.columns = ['Total Vendas', 'Receita Total', 'Ticket Médio']
    pagamento_stats = pagamento_stats.sort_values('Receita Total', ascending=False)
    print(pagamento_stats)
    
    # Visualização
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análise de Formas de Pagamento', fontsize=16, fontweight='bold')
    
    # Distribuição de vendas
    df['forma_pagamento'].value_counts().plot(
        kind='pie', ax=axes[0], autopct='%1.1f%%'
    )
    axes[0].set_title('Distribuição de Vendas por Forma de Pagamento')
    axes[0].set_ylabel('')
    
    # Receita por forma
    df.groupby('forma_pagamento')['valor_final'].sum().sort_values(ascending=False).plot(
        kind='bar', ax=axes[1], color='#2E86AB'
    )
    axes[1].set_title('Receita Total por Forma de Pagamento')
    axes[1].set_ylabel('Receita (R$)')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'formas_pagamento.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: formas_pagamento.png")

def analise_status_vendas(df):
    """Analisa status das vendas."""
    print("\n📊 ANÁLISE DE STATUS DE VENDAS")
    print("=" * 60)
    
    status_stats = df.groupby('status').agg({
        'id_venda': 'count',
        'valor_final': ['sum', 'mean']
    }).round(2)
    
    status_stats.columns = ['Total Vendas', 'Receita Total', 'Ticket Médio']
    status_stats['Percentual'] = (status_stats['Total Vendas'] / status_stats['Total Vendas'].sum() * 100).round(2)
    print(status_stats)
    
    # Visualização
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análise de Status de Vendas', fontsize=16, fontweight='bold')
    
    # Distribuição de status
    df['status'].value_counts().plot(
        kind='pie', ax=axes[0], autopct='%1.1f%%', colors=['#06A77D', '#F18F01', '#A23B72', '#2E86AB']
    )
    axes[0].set_title('Distribuição de Status')
    axes[0].set_ylabel('')
    
    # Receita por status
    df.groupby('status')['valor_final'].sum().sort_values(ascending=False).plot(
        kind='bar', ax=axes[1], color=['#06A77D', '#F18F01', '#A23B72', '#2E86AB']
    )
    axes[1].set_title('Receita Total por Status')
    axes[1].set_ylabel('Receita (R$)')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'status_vendas.png'), dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico salvo: status_vendas.png")

def gerar_relatorio_resumido(df):
    """Gera um relatório resumido em texto."""
    print("\n📄 RELATÓRIO RESUMIDO")
    print("=" * 60)
    
    relatorio = f"""
RELATÓRIO EXECUTIVO - VENDAS ANALYTICS PRO
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

MÉTRICAS PRINCIPAIS:
- Total de Vendas: {len(df):,}
- Receita Total: R$ {df['valor_final'].sum():,.2f}
- Ticket Médio: R$ {df['valor_final'].mean():,.2f}
- Valor Máximo: R$ {df['valor_final'].max():,.2f}
- Valor Mínimo: R$ {df['valor_final'].min():,.2f}
- Taxa de Sucesso: {(df['venda_sucesso'].sum() / len(df) * 100):.2f}%

CLIENTES E PRODUTOS:
- Clientes Únicos: {df['id_cliente'].nunique():,}
- Produtos Únicos: {df['produto'].nunique()}
- Categorias: {df['categoria'].nunique()}

DISTRIBUIÇÃO GEOGRÁFICA:
- Regiões: {', '.join(df['regiao'].unique())}
- Região com Maior Receita: {df.groupby('regiao')['valor_final'].sum().idxmax()}

SEGMENTAÇÃO DE CLIENTES:
{df['segmento_cliente'].value_counts().to_string()}

FORMAS DE PAGAMENTO:
{df['forma_pagamento'].value_counts().to_string()}

PERÍODO ANALISADO:
- Data Inicial: {df['data_venda'].min().strftime('%d/%m/%Y')}
- Data Final: {df['data_venda'].max().strftime('%d/%m/%Y')}
"""
    
    print(relatorio)
    
    # Salvar relatório
    with open(os.path.join(OUTPUT_DIR, 'relatorio_resumido.txt'), 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print("\n✅ Relatório salvo: relatorio_resumido.txt")

def main():
    """Executa a análise completa."""
    print("\n" + "=" * 60)
    print("🔍 ANÁLISE EXPLORATÓRIA DE DADOS (EDA)")
    print("=" * 60)
    
    # Criar diretório de saída
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Carregar dados
    df = carregar_dados()
    
    # Executar análises
    analise_vendas_por_regiao(df)
    analise_produtos_top(df)
    analise_temporal(df)
    analise_segmentacao_clientes(df)
    analise_formas_pagamento(df)
    analise_status_vendas(df)
    gerar_relatorio_resumido(df)
    
    print("\n" + "=" * 60)
    print("✅ Análise EDA concluída com sucesso!")
    print(f"📁 Arquivos salvos em: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
