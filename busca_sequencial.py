import tarefa

def buscaSequencial(id_buscado, arquivo_dados):
    quantidade_comparacoes = 0
    arquivo_dados.seek(0)
    
    while True:
        tarefa_lida = tarefa.le(arquivo_dados)
        
        if not tarefa_lida:
            break
        
        quantidade_comparacoes += 1
        if tarefa_lida['cod'] == id_buscado:
            return tarefa_lida, quantidade_comparacoes
            
    return None, quantidade_comparacoes