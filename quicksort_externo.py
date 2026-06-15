import tarefa

def particao(arquivo, esq, dir):
    meio = (esq + dir) // 2
    arquivo.seek((meio - 1) * tarefa.tamanho_registro())
    pivo = tarefa.le(arquivo)
    
    i = esq
    j = dir
    
    while True:
        arquivo.seek((i - 1) * tarefa.tamanho_registro())
        reg_i = tarefa.le(arquivo)
        while reg_i['cod'] < pivo['cod']:
            i += 1
            arquivo.seek((i - 1) * tarefa.tamanho_registro())
            reg_i = tarefa.le(arquivo)
            
        arquivo.seek((j - 1) * tarefa.tamanho_registro())
        reg_j = tarefa.le(arquivo)
        while reg_j['cod'] > pivo['cod']:
            j -= 1
            arquivo.seek((j - 1) * tarefa.tamanho_registro())
            reg_j = tarefa.le(arquivo)
            
        if i >= j:
            return j
            
        arquivo.seek((i - 1) * tarefa.tamanho_registro())
        tarefa.salva(reg_j, arquivo)
        
        arquivo.seek((j - 1) * tarefa.tamanho_registro())
        tarefa.salva(reg_i, arquivo)
        
        i += 1
        j -= 1

def executar(arquivo, esq, dir):
    if esq < dir:
        p = particao(arquivo, esq, dir)
        executar(arquivo, esq, p)
        executar(arquivo, p + 1, dir)