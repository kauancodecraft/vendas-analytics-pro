#!/usr/bin/env python3
"""
Script para gerar dados realistas de vendas para análise.
Cria um dataset com informações de clientes, produtos e transações.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Configurações
SEED = 42
NUM_RECORDS = 5000
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendas.csv')

# Definir seed para reprodutibilidade
np.random.seed(SEED)
random.seed(SEED)

# Listas de dados realistas
PRODUTOS = {
    'Notebook Dell XPS 13': 4500,
    'iPhone 15 Pro': 7999,
    'Samsung Galaxy S24': 5999,
    'iPad Air': 4999,
    'Apple Watch Series 9': 3499,
    'AirPods Pro': 1899,
    'Monitor LG 27"': 1299,
    'Teclado Mecânico': 599,
    'Mouse Logitech': 299,
    'Webcam HD': 399,
    'Headset Gamer': 799,
    'SSD 1TB': 699,
    'Memória RAM 16GB': 399,
    'Placa de Vídeo RTX 4070': 3999,
    'Processador Intel i9': 2499,
}

REGIOES = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
CATEGORIAS = ['Eletrônicos', 'Periféricos', 'Componentes', 'Acessórios', 'Smartphones']
FORMAS_PAGAMENTO = ['Cartão Crédito', 'Cartão Débito', 'PIX', 'Boleto', 'Crediário']
STATUS = ['Concluída', 'Pendente', 'Cancelada', 'Devolvida']

def gerar_dados():
    """Gera dados realistas de vendas."""
    
    data_inicio = datetime(2023, 1, 1)
    data_fim = datetime(2025, 2, 25)
    
    dados = {
        'id_venda': [],
        'data_venda': [],
        'id_cliente': [],
        'cliente_nome': [],
        'produto': [],
        'categoria': [],
        'quantidade': [],
        'preco_unitario': [],
        'valor_total': [],
        'desconto_percentual': [],
        'valor_final': [],
        'regiao': [],
        'forma_pagamento': [],
        'status': [],
        'dias_para_entrega': [],
    }
    
    for i in range(NUM_RECORDS):
        # ID e data
        id_venda = f'VND{i+1:06d}'
        dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)
        data_venda = data_inicio + timedelta(days=dias_aleatorios)
        
        # Cliente
        id_cliente = f'CLI{random.randint(1000, 9999)}'
        nomes = ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Ferreira',
                 'Juliana Rocha', 'Lucas Martins', 'Fernanda Lima', 'Roberto Alves', 'Patricia Gomes',
                 'Felipe Souza', 'Beatriz Ribeiro', 'Gustavo Pereira', 'Camila Nunes', 'Ricardo Dias']
        cliente_nome = random.choice(nomes)
        
        # Produto
        produto = random.choice(list(PRODUTOS.keys()))
        preco_unitario = PRODUTOS[produto]
        categoria = random.choice(CATEGORIAS)
        
        # Quantidade e valores
        quantidade = random.randint(1, 5)
        valor_total = preco_unitario * quantidade
        desconto_percentual = random.choice([0, 0, 0, 5, 10, 15, 20])  # Mais vendas sem desconto
        valor_desconto = valor_total * (desconto_percentual / 100)
        valor_final = valor_total - valor_desconto
        
        # Região e pagamento
        regiao = random.choice(REGIOES)
        forma_pagamento = random.choice(FORMAS_PAGAMENTO)
        status = random.choices(STATUS, weights=[0.75, 0.15, 0.05, 0.05])[0]
        
        # Dias para entrega
        dias_entrega = random.randint(1, 30) if status == 'Concluída' else None
        
        # Adicionar aos dados
        dados['id_venda'].append(id_venda)
        dados['data_venda'].append(data_venda)
        dados['id_cliente'].append(id_cliente)
        dados['cliente_nome'].append(cliente_nome)
        dados['produto'].append(produto)
        dados['categoria'].append(categoria)
        dados['quantidade'].append(quantidade)
        dados['preco_unitario'].append(preco_unitario)
        dados['valor_total'].append(valor_total)
        dados['desconto_percentual'].append(desconto_percentual)
        dados['valor_final'].append(valor_final)
        dados['regiao'].append(regiao)
        dados['forma_pagamento'].append(forma_pagamento)
        dados['status'].append(status)
        dados['dias_para_entrega'].append(dias_entrega)
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Salvar CSV
    df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    
    print(f"✅ Dataset gerado com sucesso!")
    print(f"📊 Total de registros: {len(df)}")
    print(f"💾 Arquivo salvo em: {OUTPUT_PATH}")
    print(f"\nPrimeiras linhas:")
    print(df.head())
    print(f"\nInformações do dataset:")
    print(df.info())
    print(f"\nEstatísticas básicas:")
    print(df.describe())

if __name__ == '__main__':
    gerar_dados()
