import tarefa

def buscaSequencial(chave, in_file):
    comparacoes = 0
    in_file.seek(0)
    
    while True:
        t = tarefa.le(in_file)
        if not t:
            break
        
        comparacoes += 1
        if t['cod'] == chave:
            return t, comparacoes
            
    return None, comparacoes