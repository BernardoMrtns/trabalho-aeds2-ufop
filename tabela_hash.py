import struct
import os

FORMATO_HASH = 'i i i i 50s i'
TAMANHO_REGISTRO_HASH = struct.calcsize(FORMATO_HASH)

M_HASH = 1009 

def h(chave):
    return chave % M_HASH

def inicializar_tabela_hash(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'wb') as f:
            registro_vazio = struct.pack(FORMATO_HASH, 0, 0, 0, 0, b'', 0)
            for _ in range(M_HASH):
                f.write(registro_vazio)

def inserir_hash(nome_arquivo, cod, proj_id, usu_id, status, desc):
    endereco_base = h(cod)
    primeiro_removido = None
    endereco_insercao = None
    
    with open(nome_arquivo, 'r+b') as f:
        for k in range(M_HASH):
            endereco_tentativa = (endereco_base + k) % M_HASH
            f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
            bloco = f.read(TAMANHO_REGISTRO_HASH)
            dados = struct.unpack(FORMATO_HASH, bloco)
            flag_hash = dados[5]
            
            if flag_hash == 2 and primeiro_removido is None:
                primeiro_removido = endereco_tentativa
                
            elif flag_hash == 1 and dados[0] == cod:
                print(f"[Erro] Chave {cod} já existe na tabela.")
                return False
                
            elif flag_hash == 0:
                endereco_insercao = primeiro_removido if primeiro_removido is not None else endereco_tentativa
                break
                
        else:
            if primeiro_removido is not None:
                endereco_insercao = primeiro_removido
            else:
                print("[Erro] Tabela Hash está cheia (Overflow)!")
                return False

        desc_formatada = desc.encode('utf-8')[:50].ljust(50, b'\x00')
        novo_registro = struct.pack(FORMATO_HASH, cod, proj_id, usu_id, status, desc_formatada, 1) 
        
        f.seek(endereco_insercao * TAMANHO_REGISTRO_HASH)
        f.write(novo_registro)
        
        saltos = (endereco_insercao - endereco_base) % M_HASH
        msg_saltos = f"(após {saltos} salto(s) por colisão)" if saltos > 0 else "(sem colisões, direto no base)"
        
        print(f"[Hash] Tarefa {cod} inserida no endereço {endereco_insercao} {msg_saltos}.")
        return True
    
def buscar_hash(nome_arquivo, cod_buscado):
    endereco_base = h(cod_buscado)
    
    with open(nome_arquivo, 'rb') as f:
        for k in range(M_HASH):
            endereco_tentativa = (endereco_base + k) % M_HASH
            f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
            bloco = f.read(TAMANHO_REGISTRO_HASH)
            dados = struct.unpack(FORMATO_HASH, bloco)
            flag_hash = dados[5]
            
            if flag_hash == 0:
                break
                
            if flag_hash == 1 and dados[0] == cod_buscado:
                return {
                    'cod': dados[0],
                    'projeto_id': dados[1],
                    'usuario_id': dados[2],
                    'status': dados[3],
                    'descricao': dados[4].decode('utf-8').rstrip('\x00'),
                    'endereco_fisico': endereco_tentativa
                }
                
    return None

def remover_hash(nome_arquivo, cod_remover):
    endereco_base = h(cod_remover)
    
    with open(nome_arquivo, 'r+b') as f:
        for k in range(M_HASH):
            endereco_tentativa = (endereco_base + k) % M_HASH
            f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
            bloco = f.read(TAMANHO_REGISTRO_HASH)
            dados = list(struct.unpack(FORMATO_HASH, bloco))
            flag_hash = dados[5]
            
            if flag_hash == 0:
                break
                
            if flag_hash == 1 and dados[0] == cod_remover:
                dados[5] = 2 
                registro_atualizado = struct.pack(FORMATO_HASH, *dados)
                f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
                f.write(registro_atualizado)
                print(f"[Hash] Tarefa {cod_remover} removida com sucesso. Espaço liberado para reúso.")
                return True
                
    print(f"[Erro] Tarefa {cod_remover} não encontrada para remoção.")
    return False

def imprimir_estado_hash(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print("[Erro] Arquivo da Tabela Hash não encontrado.")
        return

    ocupados = 0
    removidos = 0
    vazios = 0
    
    print("\n--- MAPA FÍSICO DA TABELA HASH (Apenas Ocupados/Removidos) ---")
    with open(nome_arquivo, 'rb') as f:
        for k in range(M_HASH):
            f.seek(k * TAMANHO_REGISTRO_HASH)
            bloco = f.read(TAMANHO_REGISTRO_HASH)
            if not bloco: break
            
            dados = struct.unpack(FORMATO_HASH, bloco)
            flag_hash = dados[5]
            
            if flag_hash == 1:
                print(f"Endereço {k:04d}: [ OCUPADO ] -> Tarefa ID: {dados[0]}")
                ocupados += 1
            elif flag_hash == 2:
                print(f"Endereço {k:04d}: [ REMOVIDO] -> (Espaço marcado para reúso)")
                removidos += 1
            else:
                vazios += 1
                
    print("-" * 62)
    print(f"RESUMO FÍSICO: {ocupados} Ocupados | {removidos} Removidos (Reaproveitáveis) | {vazios} Vazios")
    print("-" * 62)