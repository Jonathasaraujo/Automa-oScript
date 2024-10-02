import pandas as pd
from itertools import combinations
from datetime import datetime, timedelta


def gerar_query_sql(file_path, valor, idt_oper, num_parc, data):
    # Carrega o Excel
    df = pd.read_excel(file_path)
    
    # Converte a coluna de data para o tipo datetime (se ainda não estiver nesse formato)
    df['DAT_MOVI'] = pd.to_datetime(df['DAT_MOVI'], errors='coerce')
    
    # Filtra linhas onde o COD_TIPO_RESUL é 'CNCL'
    df_filtrado = df[df['COD_TIPO_RESUL'] == 'CNCL']
    
    # Aplica os filtros adicionais, se fornecidos
    if idt_oper is not None:
        df_filtrado = df_filtrado[df_filtrado['IDT_OPER'] == idt_oper]
    
    if num_parc is not None:
        df_filtrado = df_filtrado[df_filtrado['NUM_PARC'] == num_parc]
    
    if data is not None:
        df_filtrado = df_filtrado[df_filtrado['DAT_MOVI'] == data]
    
    # Extraímos os valores de VLR_TRAN e IDs correspondentes
    valores = df_filtrado['VLR_TRAN'].tolist()
    ids_exeo = df_filtrado['IDT_EXEO'].tolist()
    
    # Tentar encontrar combinações de valores que somem exatamente ao valor desejado
    for r in range(1, len(valores) + 1):
        for comb in combinations(zip(valores, ids_exeo), r):
            soma_comb = sum(v[0] for v in comb)
            if soma_comb == valor:
                ids_exeo_comb = [str(v[1]).replace('.', '').replace(',', '') for v in comb]
                ids_exeo_str = ', '.join(ids_exeo_comb)
                
                # Monta a query SQL
                query_sql = f"UPDATE tbsgc052 SET COD_TIPO_RESUL = 'CTBZ' WHERE IDT_EXEO IN ({ids_exeo_str});"
                return query_sql
    
    # Se nenhuma combinação for encontrada
    return "Nenhuma combinação de valores encontrada para atingir o valor especificado."

# Exemplo de uso
file_path = 'seu_arquivo.xlsx'
valor = -168  # Valor que deseja alcançar
idt_oper = 1  # Exemplo de IDT_OPER para filtrar (opcional)
num_parc = 2  # Exemplo de NUM_PARC para filtrar (opcional)
data = datetime(2024, 10, 2)  # Data específica para filtrar (opcional)

query = gerar_query_sql(file_path, valor, idt_oper, num_parc, data)
print(query)
