import tarefa

def buscaBinaria(id_buscado, arquivo_dados, posicao_inicio, posicao_fim):
    quantidade_comparacoes = 0
    tarefa_encontrada = None
    id_tarefa_atual = -1

    while posicao_inicio <= posicao_fim and id_tarefa_atual != id_buscado:
        posicao_meio = (posicao_inicio + posicao_fim) // 2
        
        # Pula direto para a posição do meio
        arquivo_dados.seek((posicao_meio - 1) * tarefa.tamanho_registro())
        tarefa_encontrada = tarefa.le(arquivo_dados)
        
        if tarefa_encontrada:
            quantidade_comparacoes += 1
            id_tarefa_atual = tarefa_encontrada['cod']
            
            if id_tarefa_atual > id_buscado:
                posicao_fim = posicao_meio - 1
            elif id_tarefa_atual < id_buscado:
                posicao_inicio = posicao_meio + 1

    if id_tarefa_atual == id_buscado:
        return tarefa_encontrada, quantidade_comparacoes
        
    return None, quantidade_comparacoes