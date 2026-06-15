import tarefa
import heapq
import os

def gerar_particoes_substituicao(arquivo_entrada, qtd_registros, tamanho_memoria=100):
    arquivo_entrada.seek(0)
    heap = []
    congelados = []
    arquivos_particoes = []
    num_particao = 1
    
    for i in range(min(tamanho_memoria, qtd_registros)):
        reg = tarefa.le(arquivo_entrada)
        if reg:
            heapq.heappush(heap, (reg['cod'], i, reg))
            
    id_leitura = tamanho_memoria
    registros_lidos = tamanho_memoria
    
    while heap or congelados:
        nome_particao = f"particao_{num_particao}.dat"
        arquivos_particoes.append(nome_particao)
        
        with open(nome_particao, 'wb') as arq_part:
            while heap:
                menor_cod, _, reg_min = heapq.heappop(heap)
                tarefa.salva(reg_min, arq_part)
                
                if registros_lidos < qtd_registros:
                    novo_reg = tarefa.le(arquivo_entrada)
                    registros_lidos += 1
                    id_leitura += 1
                    
                    if novo_reg['cod'] < menor_cod:
                        congelados.append((novo_reg['cod'], id_leitura, novo_reg))
                    else:
                        heapq.heappush(heap, (novo_reg['cod'], id_leitura, novo_reg))
                        
        num_particao += 1
        for item in congelados:
            heapq.heappush(heap, item)
        congelados.clear()
        
    return arquivos_particoes

def intercalar_arvore_vencedores(particoes, arquivo_saida_nome):
    arquivos_abertos = [open(p, 'rb') for p in particoes]
    heap_vencedores = []
    
    for i, arq in enumerate(arquivos_abertos):
        reg = tarefa.le(arq)
        if reg:
            heapq.heappush(heap_vencedores, (reg['cod'], i, reg))
            
    with open(arquivo_saida_nome, 'wb') as arq_saida:
        while heap_vencedores:
            menor_cod, indice_arq, reg_vencedor = heapq.heappop(heap_vencedores)
            tarefa.salva(reg_vencedor, arq_saida)
            
            arq_origem = arquivos_abertos[indice_arq]
            novo_reg = tarefa.le(arq_origem)
            if novo_reg:
                heapq.heappush(heap_vencedores, (novo_reg['cod'], indice_arq, novo_reg))
                
    for arq in arquivos_abertos:
        arq.close()
    for p in particoes:
        os.remove(p)