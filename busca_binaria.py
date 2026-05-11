import tarefa

def buscaBinaria(chave, in_file, inicio, fim):
    comparacoes = 0
    t = None
    cod = -1

    while inicio <= fim and cod != chave:
        meio = (inicio + fim) // 2
        # A lógica da professora usa o meio-1 para posicionar o ponteiro
        in_file.seek((meio - 1) * tarefa.tamanho_registro())
        t = tarefa.le(in_file)
        
        if t:
            comparacoes += 1
            cod = t['cod']
            if cod > chave:
                fim = meio - 1
            elif cod < chave:
                inicio = meio + 1

    if cod == chave:
        return t, comparacoes
    return None, comparacoes