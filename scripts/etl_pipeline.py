#!/usr/bin/env python3
"""
Pipeline ETL (Extract, Transform, Load) para análise de vendas.
Realiza limpeza, transformação e enriquecimento dos dados.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendas.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendas_processadas.csv')

def carregar_dados():
    """Carrega os dados brutos."""
    print("📥 Carregando dados...")
    df = pd.read_csv(INPUT_PATH, parse_dates=['data_venda'])
    print(f"✅ {len(df)} registros carregados")
    return df

def limpar_dados(df):
    """Realiza limpeza básica dos dados."""
    print("\n🧹 Limpando dados...")
    
    # Remover duplicatas
    duplicatas_antes = len(df)
    df = df.drop_duplicates(subset=['id_venda'])
    print(f"  - Removidas {duplicatas_antes - len(df)} duplicatas")
    
    # Verificar valores nulos
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
        print(f"  - Valores nulos encontrados: {nulos[nulos > 0].to_dict()}")
    
    # Converter tipos de dados
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df['valor_unitario'] = df['preco_unitario'].astype(float)
    df['valor_total'] = df['valor_total'].astype(float)
    df['valor_final'] = df['valor_final'].astype(float)
    
    return df

def transformar_dados(df):
    """Realiza transformações e enriquecimento dos dados."""
    print("\n🔄 Transformando dados...")
    
    # Extrair componentes de data
    df['ano'] = df['data_venda'].dt.year
    df['mes'] = df['data_venda'].dt.month
    df['mes_nome'] = df['data_venda'].dt.strftime('%B')
    df['trimestre'] = df['data_venda'].dt.quarter
    df['semana'] = df['data_venda'].dt.isocalendar().week
    df['dia_semana'] = df['data_venda'].dt.day_name()
    
    # Criar faixas de valor
    df['faixa_valor'] = pd.cut(df['valor_final'], 
                                bins=[0, 1000, 5000, 10000, 50000],
                                labels=['Baixo (< 1k)', 'Médio (1k-5k)', 'Alto (5k-10k)', 'Premium (> 10k)'])
    
    # Calcular margem de lucro simulada (assumindo 30% de custo)
    df['margem_lucro'] = df['valor_final'] * 0.30
    
    # Classificar clientes por valor
    cliente_valor = df.groupby('id_cliente')['valor_final'].sum().reset_index()
    cliente_valor.columns = ['id_cliente', 'valor_total_cliente']
    cliente_valor['segmento_cliente'] = pd.cut(cliente_valor['valor_total_cliente'],
                                                bins=[0, 5000, 20000, 100000],
                                                labels=['Bronze', 'Prata', 'Ouro'])
    
    df = df.merge(cliente_valor[['id_cliente', 'segmento_cliente']], on='id_cliente', how='left')
    
    # Indicador de venda bem-sucedida
    df['venda_sucesso'] = (df['status'] == 'Concluída').astype(int)
    
    # Tempo de entrega categorizado
    df['tempo_entrega_cat'] = pd.cut(df['dias_para_entrega'],
                                      bins=[0, 7, 14, 21, 31],
                                      labels=['Rápido (1-7d)', 'Normal (8-14d)', 'Lento (15-21d)', 'Muito Lento (22-30d)'],
                                      include_lowest=True)
    
    print("  ✅ Componentes de data extraídos")
    print("  ✅ Faixas de valor criadas")
    print("  ✅ Segmentação de clientes realizada")
    print("  ✅ Indicadores de sucesso calculados")
    
    return df

def calcular_kpis(df):
    """Calcula KPIs principais."""
    print("\n📊 Calculando KPIs...")
    
    kpis = {
        'Total de Vendas': len(df),
        'Receita Total': df['valor_final'].sum(),
        'Ticket Médio': df['valor_final'].mean(),
        'Taxa de Sucesso': (df['venda_sucesso'].sum() / len(df) * 100),
        'Clientes Únicos': df['id_cliente'].nunique(),
        'Produtos Únicos': df['produto'].nunique(),
        'Valor Máximo': df['valor_final'].max(),
        'Valor Mínimo': df['valor_final'].min(),
        'Margem Total': df['margem_lucro'].sum(),
    }
    
    print("\n  KPIs Principais:")
    for chave, valor in kpis.items():
        if isinstance(valor, float):
            if 'Taxa' in chave or 'Percentual' in chave:
                print(f"    - {chave}: {valor:.2f}%")
            else:
                print(f"    - {chave}: R$ {valor:,.2f}" if 'Receita' in chave or 'Ticket' in chave or 'Margem' in chave or 'Valor' in chave else f"    - {chave}: {valor:.2f}")
        else:
            print(f"    - {chave}: {valor}")
    
    return kpis

def salvar_dados(df):
    """Salva os dados processados."""
    print("\n💾 Salvando dados processados...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    print(f"✅ Arquivo salvo em: {OUTPUT_PATH}")
    
    # Exibir amostra
    print(f"\n📋 Amostra dos dados processados:")
    print(df[['id_venda', 'data_venda', 'cliente_nome', 'produto', 'valor_final', 
              'regiao', 'status', 'segmento_cliente']].head(10))

def main():
    """Executa o pipeline completo."""
    print("=" * 60)
    print("🚀 PIPELINE ETL - ANÁLISE DE VENDAS")
    print("=" * 60)
    
    # Executar etapas
    df = carregar_dados()
    df = limpar_dados(df)
    df = transformar_dados(df)
    kpis = calcular_kpis(df)
    salvar_dados(df)
    
    print("\n" + "=" * 60)
    print("✅ Pipeline ETL concluído com sucesso!")
    print("=" * 60)

if __name__ == '__main__':
    main()
