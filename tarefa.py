import struct
import random

FORMATO_BINARIO = 'i i i i 50s'
TAMANHO_REGISTRO = struct.calcsize(FORMATO_BINARIO)

def criar_tarefa(id_tarefa, id_projeto, id_usuario, status_tarefa, descricao_tarefa):
    return {
        'cod': id_tarefa,
        'projeto_id': id_projeto,
        'usuario_id': id_usuario,
        'status': status_tarefa,
        'descricao': descricao_tarefa
    }

def salva(dados_tarefa, arquivo_destino):
    descricao_formatada = dados_tarefa['descricao'].encode('utf-8')[:50].ljust(50, b'\x00')
    
    bloco_bytes = struct.pack(
        FORMATO_BINARIO, 
        dados_tarefa['cod'], 
        dados_tarefa['projeto_id'], 
        dados_tarefa['usuario_id'], 
        dados_tarefa['status'], 
        descricao_formatada
    )
    arquivo_destino.write(bloco_bytes)

def le(arquivo_origem):
    bloco_bytes = arquivo_origem.read(TAMANHO_REGISTRO)
    if not bloco_bytes or len(bloco_bytes) < TAMANHO_REGISTRO:
        return None
        
    dados_desempacotados = struct.unpack(FORMATO_BINARIO, bloco_bytes)
    return {
        'cod': dados_desempacotados[0],
        'projeto_id': dados_desempacotados[1],
        'usuario_id': dados_desempacotados[2],
        'status': dados_desempacotados[3],
        'descricao': dados_desempacotados[4].decode('utf-8').rstrip('\x00')
    }

def imprime(dados_tarefa):
    print("**********************************************")
    print(f"Tarefa de codigo {dados_tarefa['cod']}")
    print(f"Projeto ID: {dados_tarefa['projeto_id']} | Usuario ID: {dados_tarefa['usuario_id']} | Status: {dados_tarefa['status']}")
    print(f"Descricao: {dados_tarefa['descricao']}")
    print("**********************************************")

def tamanho_registro():
    return TAMANHO_REGISTRO

def embaralha(lista_ids):
    tamanho_lista = len(lista_ids)
    quantidade_trocas = int((tamanho_lista * 60) / 100)
    for _ in range(quantidade_trocas):
        indice_a = random.randint(0, tamanho_lista - 1)
        indice_b = random.randint(0, tamanho_lista - 1)
        lista_ids[indice_a], lista_ids[indice_b] = lista_ids[indice_b], lista_ids[indice_a]

def criarBase(nome_arquivo, quantidade_registros):
    lista_ids = list(range(1, quantidade_registros + 1))
    embaralha(lista_ids)
    
    with open(nome_arquivo, 'wb') as arquivo_destino:
        for indice in range(quantidade_registros):
            id_projeto_aleatorio = random.randint(1, 500)
            id_usuario_aleatorio = random.randint(1, 1000)
            id_tarefa_atual = lista_ids[indice]
            
            nova_tarefa = criar_tarefa(
                id_tarefa_atual, 
                id_projeto_aleatorio, 
                id_usuario_aleatorio, 
                status_tarefa=0, 
                descricao_tarefa=f"Atividade automatica {id_tarefa_atual}"
            )
            salva(nova_tarefa, arquivo_destino)
            
def tamanho_arquivo(arquivo_origem):
    arquivo_origem.seek(0, 2)
    total_bytes = arquivo_origem.tell()
    return int(total_bytes // TAMANHO_REGISTRO)