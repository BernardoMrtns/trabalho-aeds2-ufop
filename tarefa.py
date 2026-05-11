import struct
import random

# Estrutura binária: id(int), proj_id(int), usr_id(int), status(int), desc(50 chars)
# i = 4 bytes, 50s = 50 bytes. Total = 66 bytes.
FORMATO = 'i i i i 50s'
TAM_REGISTRO = struct.calcsize(FORMATO)

def criar_tarefa(cod, proj_id, usr_id, status, desc):
    return {
        'cod': cod,
        'projeto_id': proj_id,
        'usuario_id': usr_id,
        'status': status,
        'descricao': desc # Agora mantemos como string pura na memória
    }

def salva(t, out_file):
    # A codificação para bytes com 50 posições ocorre apenas na hora de escrever no arquivo
    desc_bytes = t['descricao'].encode('utf-8')[:50].ljust(50, b'\x00')
    bloco = struct.pack(FORMATO, t['cod'], t['projeto_id'], t['usuario_id'], t['status'], desc_bytes)
    out_file.write(bloco)

def le(in_file):
    bloco = in_file.read(TAM_REGISTRO)
    if not bloco or len(bloco) < TAM_REGISTRO:
        return None
    dados = struct.unpack(FORMATO, bloco)
    return {
        'cod': dados[0],
        'projeto_id': dados[1],
        'usuario_id': dados[2],
        'status': dados[3],
        'descricao': dados[4].decode('utf-8').rstrip('\x00')
    }

def imprime(t):
    print("**********************************************")
    print(f"Tarefa de codigo {t['cod']}")
    print(f"Projeto ID: {t['projeto_id']} | Usuario ID: {t['usuario_id']} | Status: {t['status']}")
    print(f"Descricao: {t['descricao']}")
    print("**********************************************")

def tamanho_registro():
    return TAM_REGISTRO

def embaralha(vet):
    tam = len(vet)
    trocas = int((tam * 60) / 100)
    for _ in range(trocas):
        i = random.randint(0, tam - 1)
        j = random.randint(0, tam - 1)
        vet[i], vet[j] = vet[j], vet[i]

def criarBase(nome_arquivo, tam):
    vet = list(range(1, tam + 1))
    embaralha(vet)
    
    with open(nome_arquivo, 'wb') as out:
        for i in range(tam):
            proj_id = random.randint(1, 3)
            usr_id = random.randint(1, 3)
            # Status inicial 0 (Pendente)
            t = criar_tarefa(vet[i], proj_id, usr_id, 0, f"Atividade automatica {vet[i]}")
            salva(t, out)

def tamanho_arquivo(in_file):
    in_file.seek(0, 2) # Vai para o fim do arquivo
    tam = in_file.tell() // TAM_REGISTRO
    return int(tam)