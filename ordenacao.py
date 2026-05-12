import tarefa

def insertionSort(arquivo_dados, quantidade_registros):
    total_trocas = 0
    
    for posicao_atual in range(2, quantidade_registros + 1):
        # Lê a tarefa que queremos encaixar na posição certa
        arquivo_dados.seek((posicao_atual - 1) * tarefa.tamanho_registro())
        tarefa_atual = tarefa.le(arquivo_dados)
        
        posicao_anterior = posicao_atual - 1
        
        # Lê a tarefa que vem logo atrás dela
        arquivo_dados.seek((posicao_anterior - 1) * tarefa.tamanho_registro())
        tarefa_anterior = tarefa.le(arquivo_dados)
        
        # Enquanto a tarefa de trás tiver um ID maior que a nossa tarefa atual...
        while posicao_anterior > 0 and tarefa_anterior['cod'] > tarefa_atual['cod']:
            # Empurra a tarefa de trás uma posição para frente
            arquivo_dados.seek(posicao_anterior * tarefa.tamanho_registro())
            tarefa.salva(tarefa_anterior, arquivo_dados)
            total_trocas += 1
            
            posicao_anterior -= 1
            
            # Puxa a próxima tarefa de trás para continuar comparando
            if posicao_anterior > 0:
                arquivo_dados.seek((posicao_anterior - 1) * tarefa.tamanho_registro())
                tarefa_anterior = tarefa.le(arquivo_dados)
        
        # Encontrou o "buraco" correto, salva a tarefa atual ali
        arquivo_dados.seek(posicao_anterior * tarefa.tamanho_registro())
        tarefa.salva(tarefa_atual, arquivo_dados)
        total_trocas += 1
        
    return total_trocas