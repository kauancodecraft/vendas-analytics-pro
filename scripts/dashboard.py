#!/usr/bin/env python3
"""
Dashboard Interativo - Vendas Analytics Pro
Interface visual profissional para análise de vendas em tempo real.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configurações de página
st.set_page_config(
    page_title="Vendas Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    """Carrega os dados processados."""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendas_processadas.csv')
    df = pd.read_csv(path, parse_dates=['data_venda'])
    return df

def formatar_moeda(valor):
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

def criar_kpi_cards(df):
    """Cria cards com KPIs principais."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_vendas = len(df)
        st.metric("📦 Total de Vendas", f"{total_vendas:,}")
    
    with col2:
        receita_total = df['valor_final'].sum()
        st.metric("💰 Receita Total", formatar_moeda(receita_total))
    
    with col3:
        ticket_medio = df['valor_final'].mean()
        st.metric("🎯 Ticket Médio", formatar_moeda(ticket_medio))
    
    with col4:
        taxa_sucesso = (df['venda_sucesso'].sum() / len(df) * 100)
        st.metric("✅ Taxa de Sucesso", f"{taxa_sucesso:.1f}%")
    
    with col5:
        clientes_unicos = df['id_cliente'].nunique()
        st.metric("👥 Clientes Únicos", f"{clientes_unicos:,}")

def criar_filtros(df):
    """Cria filtros interativos na sidebar."""
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de data
    data_min = df['data_venda'].min()
    data_max = df['data_venda'].max()
    
    data_inicio, data_fim = st.sidebar.date_input(
        "Período de Análise",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )
    
    # Filtro de região
    regioes = st.sidebar.multiselect(
        "Regiões",
        options=sorted(df['regiao'].unique()),
        default=sorted(df['regiao'].unique())
    )
    
    # Filtro de status
    status = st.sidebar.multiselect(
        "Status de Venda",
        options=sorted(df['status'].unique()),
        default=sorted(df['status'].unique())
    )
    
    # Filtro de segmento de cliente
    segmentos = st.sidebar.multiselect(
        "Segmento de Cliente",
        options=sorted(df['segmento_cliente'].dropna().unique()),
        default=sorted(df['segmento_cliente'].dropna().unique())
    )
    
    # Filtro de forma de pagamento
    formas = st.sidebar.multiselect(
        "Forma de Pagamento",
        options=sorted(df['forma_pagamento'].unique()),
        default=sorted(df['forma_pagamento'].unique())
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['data_venda'].dt.date >= data_inicio) &
        (df['data_venda'].dt.date <= data_fim) &
        (df['regiao'].isin(regioes)) &
        (df['status'].isin(status)) &
        (df['segmento_cliente'].isin(segmentos)) &
        (df['forma_pagamento'].isin(formas))
    ]
    
    st.sidebar.info(f"📊 Registros após filtros: {len(df_filtrado):,} de {len(df):,}")
    
    return df_filtrado

def criar_graficos_vendas(df):
    """Cria gráficos de análise de vendas."""
    st.header("📈 Análise de Vendas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Receita por região
        receita_regiao = df.groupby('regiao')['valor_final'].sum().sort_values(ascending=False)
        fig_regiao = px.bar(
            x=receita_regiao.index,
            y=receita_regiao.values,
            title="Receita por Região",
            labels={'x': 'Região', 'y': 'Receita (R$)'},
            color=receita_regiao.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    with col2:
        # Vendas por status
        vendas_status = df['status'].value_counts()
        fig_status = px.pie(
            values=vendas_status.values,
            names=vendas_status.index,
            title="Distribuição de Vendas por Status",
            color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6']
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Série temporal
    vendas_diarias = df.set_index('data_venda').resample('D')['valor_final'].sum()
    fig_temporal = px.line(
        x=vendas_diarias.index,
        y=vendas_diarias.values,
        title="Receita Diária (Série Temporal)",
        labels={'x': 'Data', 'y': 'Receita (R$)'},
        markers=True
    )
    fig_temporal.update_traces(line=dict(color='#3498db', width=2))
    st.plotly_chart(fig_temporal, use_container_width=True)

def criar_graficos_produtos(df):
    """Cria gráficos de análise de produtos."""
    st.header("🛍️  Análise de Produtos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 produtos por receita
        top_produtos = df.groupby('produto')['valor_final'].sum().nlargest(10).sort_values()
        fig_produtos = px.barh(
            y=top_produtos.index,
            x=top_produtos.values,
            title="Top 10 Produtos por Receita",
            labels={'x': 'Receita (R$)', 'y': 'Produto'},
            color=top_produtos.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_produtos, use_container_width=True)
    
    with col2:
        # Distribuição por categoria
        vendas_categoria = df['categoria'].value_counts()
        fig_categoria = px.pie(
            values=vendas_categoria.values,
            names=vendas_categoria.index,
            title="Distribuição de Vendas por Categoria"
        )
        st.plotly_chart(fig_categoria, use_container_width=True)

def criar_graficos_clientes(df):
    """Cria gráficos de análise de clientes."""
    st.header("👥 Análise de Clientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Segmentação de clientes
        segmento_clientes = df['segmento_cliente'].value_counts()
        fig_segmento = px.pie(
            values=segmento_clientes.values,
            names=segmento_clientes.index,
            title="Distribuição de Clientes por Segmento",
            color_discrete_sequence=['#3498db', '#e74c3c', '#f39c12']
        )
        st.plotly_chart(fig_segmento, use_container_width=True)
    
    with col2:
        # Receita por segmento
        receita_segmento = df.groupby('segmento_cliente')['valor_final'].sum().sort_values(ascending=False)
        fig_receita_seg = px.bar(
            x=receita_segmento.index,
            y=receita_segmento.values,
            title="Receita por Segmento de Cliente",
            labels={'x': 'Segmento', 'y': 'Receita (R$)'},
            color=receita_segmento.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_receita_seg, use_container_width=True)

def criar_graficos_pagamento(df):
    """Cria gráficos de análise de pagamento."""
    st.header("💳 Análise de Formas de Pagamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de formas de pagamento
        formas = df['forma_pagamento'].value_counts()
        fig_formas = px.pie(
            values=formas.values,
            names=formas.index,
            title="Distribuição de Formas de Pagamento"
        )
        st.plotly_chart(fig_formas, use_container_width=True)
    
    with col2:
        # Receita por forma de pagamento
        receita_forma = df.groupby('forma_pagamento')['valor_final'].sum().sort_values(ascending=False)
        fig_receita_forma = px.bar(
            x=receita_forma.index,
            y=receita_forma.values,
            title="Receita por Forma de Pagamento",
            labels={'x': 'Forma de Pagamento', 'y': 'Receita (R$)'},
            color=receita_forma.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_receita_forma, use_container_width=True)

def criar_tabela_detalhes(df):
    """Cria tabela com detalhes das vendas."""
    st.header("📋 Detalhes das Vendas")
    
    # Seleção de colunas para exibição
    colunas = st.multiselect(
        "Selecione as colunas para exibir",
        options=df.columns.tolist(),
        default=['id_venda', 'data_venda', 'cliente_nome', 'produto', 'valor_final', 'regiao', 'status']
    )
    
    # Ordenação
    coluna_ordem = st.selectbox("Ordenar por:", options=colunas, index=0)
    
    # Exibir tabela
    df_exibicao = df[colunas].sort_values(by=coluna_ordem, ascending=False).head(100)
    st.dataframe(df_exibicao, use_container_width=True)
    
    # Download dos dados
    csv = df_exibicao.to_csv(index=False, encoding='utf-8')
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name=f"vendas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def main():
    """Função principal do dashboard."""
    # Título
    st.title("📊 Vendas Analytics Pro")
    st.markdown("---")
    
    # Carregar dados
    df = carregar_dados()
    
    # Criar filtros
    df_filtrado = criar_filtros(df)
    
    # KPIs principais
    criar_kpi_cards(df_filtrado)
    st.markdown("---")
    
    # Gráficos
    criar_graficos_vendas(df_filtrado)
    st.markdown("---")
    
    criar_graficos_produtos(df_filtrado)
    st.markdown("---")
    
    criar_graficos_clientes(df_filtrado)
    st.markdown("---")
    
    criar_graficos_pagamento(df_filtrado)
    st.markdown("---")
    
    # Tabela de detalhes
    criar_tabela_detalhes(df_filtrado)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 12px;'>
        <p>Vendas Analytics Pro © 2026 | Dashboard desenvolvido com Streamlit</p>
        <p>Última atualização: {}</p>
    </div>
    """.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
