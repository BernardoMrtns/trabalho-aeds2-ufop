import struct
import os

FORMATO_HASH = 'i i i i 50s i'
TAMANHO_REGISTRO_HASH = struct.calcsize(FORMATO_HASH)

M_HASH = 1009 

def h(chave):
    """Função de dispersão (Método da Divisão)"""
    return chave % M_HASH

def inicializar_tabela_hash(nome_arquivo):
    """Cria o arquivo da tabela hash com tamanho fixo e todos os espaços marcados como LIVRES (0)."""
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'wb') as f:
            registro_vazio = struct.pack(FORMATO_HASH, 0, 0, 0, 0, b'', 0)
            for _ in range(M_HASH):
                f.write(registro_vazio)

def inserir_hash(nome_arquivo, cod, proj_id, usu_id, status, desc):
    """Insere um registro, tratando colisões por tentativa linear e REUTILIZANDO espaços removidos."""
    endereco_base = h(cod)
    
    with open(nome_arquivo, 'r+b') as f:
        for k in range(M_HASH):
            endereco_tentativa = (endereco_base + k) % M_HASH
            f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
            bloco = f.read(TAMANHO_REGISTRO_HASH)
            dados = struct.unpack(FORMATO_HASH, bloco)
            flag_hash = dados[5]
            
            if flag_hash == 0 or flag_hash == 2:
                desc_formatada = desc.encode('utf-8')[:50].ljust(50, b'\x00')
                novo_registro = struct.pack(FORMATO_HASH, cod, proj_id, usu_id, status, desc_formatada, 1) # Flag 1 = Ocupado
                
                f.seek(endereco_tentativa * TAMANHO_REGISTRO_HASH)
                f.write(novo_registro)
                print(f"[Hash] Tarefa {cod} inserida no endereço físico {endereco_tentativa}.")
                return True
            
            if flag_hash == 1 and dados[0] == cod:
                print(f"[Erro] Chave {cod} já existe na tabela.")
                return False
                
        print("[Erro] Tabela Hash está cheia (Overflow)!")
        return False

def buscar_hash(nome_arquivo, cod_buscado):
    """Busca um registro calculando o endereço em disco com O(1) no melhor caso."""
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
    """Exclui logicamente um registro, alterando a FLAG para 2 (Removido)."""
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