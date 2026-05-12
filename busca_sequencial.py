import tarefa

def buscaSequencial(id_buscado, arquivo_dados):
    quantidade_comparacoes = 0
    arquivo_dados.seek(0) # Posiciona no início do arquivo
    
    while True:
        tarefa_lida = tarefa.le(arquivo_dados)
        
        # Se retornou None, o arquivo acabou
        if not tarefa_lida:
            break
        
        quantidade_comparacoes += 1
        if tarefa_lida['cod'] == id_buscado:
            return tarefa_lida, quantidade_comparacoes
            
    return None, quantidade_comparacoes