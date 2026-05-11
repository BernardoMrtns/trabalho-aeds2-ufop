import tarefa

def insertionSort(in_file, tam):
    trocas = 0
    for j in range(2, tam + 1):
        in_file.seek((j - 1) * tarefa.tamanho_registro())
        tj = tarefa.le(in_file)
        i = j - 1
        
        in_file.seek((i - 1) * tarefa.tamanho_registro())
        ti = tarefa.le(in_file)
        
        while i > 0 and ti['cod'] > tj['cod']:
            in_file.seek(i * tarefa.tamanho_registro())
            tarefa.salva(ti, in_file)
            trocas += 1
            
            i -= 1
            if i > 0:
                in_file.seek((i - 1) * tarefa.tamanho_registro())
                ti = tarefa.le(in_file)
        
        in_file.seek(i * tarefa.tamanho_registro())
        tarefa.salva(tj, in_file)
        trocas += 1
        
    return trocas