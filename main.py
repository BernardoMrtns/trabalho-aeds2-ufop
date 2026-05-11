import time
import tarefa
import ordenacao
from busca_sequencial import buscaSequencial
from busca_binaria import buscaBinaria

usuarios = {}
projetos = {}

def cadastrar_usuario(id_usr, nome):
    usuarios[id_usr] = nome
    print(f"[Sistema] Usuario '{nome}' cadastrado.")

def criar_projeto(id_proj, nome):
    projetos[id_proj] = nome
    print(f"[Sistema] Projeto '{nome}' criado.")

def main():
    print("--- CADASTROS INICIAIS ---")
    cadastrar_usuario(1, "Diogo V.")
    criar_projeto(1, "Migração de Dashboards")
    cadastrar_usuario(2, "Bernardo M.")
    criar_projeto(2, "Programar Backend")
    cadastrar_usuario(3, "Pedro R.")
    criar_projeto(3, "Programar Frontend")
    
    tamanhos = [10, 50, 100, 500, 1000]
    num_execucoes = 5
    
    print("\n--- INICIANDO TESTES E GERANDO LOGS ---")
    with open("log.txt", "w") as log:
        log.write("=== LOG DE DESEMPENHO DE BUSCAS ===\n\n")

        for i in range(num_execucoes):
            tam_atual = tamanhos[i]
            print(f"Processando base de {tam_atual} registros...")
            
            nome_arq = "tarefas_db.dat"
            
            # Gera a base embaralhada
            tarefa.criarBase(nome_arq, tam_atual)
            
            # Ordena a base no disco (necessário para a busca binária funcionar)
            with open(nome_arq, 'r+b') as f:
                ordenacao.insertionSort(f, tam_atual)
            
            # Vamos testar o pior caso buscando sempre o último ID gerado
            chave_busca = tam_atual
            
            with open(nome_arq, 'rb') as f:
                # Teste Busca Sequencial
                inicio_seq = time.perf_counter()
                _, comp_seq = buscaSequencial(chave_busca, f)
                fim_seq = time.perf_counter()
                tempo_seq = fim_seq - inicio_seq
                
                # Teste Busca Binária (passando início 1 e fim tam_atual)
                inicio_bin = time.perf_counter()
                _, comp_bin = buscaBinaria(chave_busca, f, 1, tam_atual)
                fim_bin = time.perf_counter()
                tempo_bin = fim_bin - inicio_bin
            
            # Salvando no txt conforme exigido
            res = (f"Tamanho da Base: {tam_atual} registros\n"
                   f"Busca Sequencial -> Comparacoes: {comp_seq} | Tempo (s): {tempo_seq:.6f}\n"
                   f"Busca Binaria    -> Comparacoes: {comp_bin} | Tempo (s): {tempo_bin:.6f}\n"
                   f"--------------------------------------------------\n")
            log.write(res)
            
    print("Processamento concluido! Cheque o arquivo 'log.txt'.")

if __name__ == "__main__":
    main()