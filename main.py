import time
import os
import tarefa
import ordenacao
from busca_sequencial import buscaSequencial
from busca_binaria import buscaBinaria

def inicializar_arquivos():
    if not os.path.exists("usuarios_db.txt"):
        with open("usuarios_db.txt", "w", encoding="utf-8") as f:
            f.write("1;Diogo V.\n2;Bernardo M.\n3;Pedro R.\n")
    if not os.path.exists("projetos_db.txt"):
        with open("projetos_db.txt", "w", encoding="utf-8") as f:
            f.write("1;Sistema de Vendas ERP\n2;Aplicativo Mobile de Entregas\n3;Novo Portal Corporativo\n")

def executar_testes_desempenho():
    tamanhos_de_base = [10, 50, 100, 500, 1000]
    with open("log.txt", "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write("=== LOG DE DESEMPENHO DE BUSCAS ===\n\n")
        
        for qtd in tamanhos_de_base:
            print(f"Gerando e ordenando base de {qtd} registros...")
            tarefa.criarBase("tarefas_db.dat", qtd)
            
            with open("tarefas_db.dat", 'r+b') as f:
                ordenacao.insertionSort(f, qtd)
                
                id_alvo = qtd
                
                inicio_seq = time.perf_counter()
                _, comp_seq = buscaSequencial(id_alvo, f)
                tempo_seq = time.perf_counter() - inicio_seq
                
                inicio_bin = time.perf_counter()
                _, comp_bin = buscaBinaria(id_alvo, f, 1, qtd)
                tempo_bin = time.perf_counter() - inicio_bin
                
                arquivo_log.write(
                    f"Tamanho da Base: {qtd} registros\n"
                    f"Busca Sequencial -> Comparacoes: {comp_seq} | Tempo (s): {tempo_seq:.6f}\n"
                    f"Busca Binaria    -> Comparacoes: {comp_bin} | Tempo (s): {tempo_bin:.6f}\n"
                    f"--------------------------------------------------\n"
                )
    print("\n[Sucesso] Testes concluídos. Resultados salvos em 'log.txt'.")

def menu_principal():
    inicializar_arquivos()
    nome_db = "tarefas_db.dat"
    if not os.path.exists(nome_db):
        tarefa.criarBase(nome_db, 100)
        with open(nome_db, 'r+b') as f:
            ordenacao.insertionSort(f, 100)

    while True:
        print("\n--- SISTEMA DE GERENCIAMENTO DE PROJETOS ---")
        print("1. Cadastrar Usuário / Criar Projeto")
        print("2. Criar Nova Tarefa")
        print("3. Editar Status da Tarefa (Busca Binária)")
        print("4. Atribuir Tarefa a Usuário (Busca Binária)")
        print("5. Excluir Tarefa (Logicamente - Busca Binária)")
        print("6. Listar Tarefas por Filtro (Busca Sequencial)")
        print("7. Rodar Testes de Desempenho")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tipo = input("Deseja cadastrar (U)suário ou (P)rojeto? ").upper()
            nome = input("Nome/Título: ")
            arquivo = "usuarios_db.txt" if tipo == "U" else "projetos_db.txt"
            with open(arquivo, "a", encoding="utf-8") as f:
                num_lines = sum(1 for line in open(arquivo)) + 1
                f.write(f"{num_lines};{nome}\n")
            print("Cadastro realizado com sucesso!")

        elif opcao == "2":
            with open(nome_db, "r+b") as f:
                qtd = tarefa.tamanho_arquivo(f)
                novo_id = qtd + 1
                print(f"Criando tarefa ID {novo_id}")
                proj_id = int(input("ID do Projeto: "))
                desc = input("Descrição da tarefa: ")
                nova = tarefa.criar_tarefa(novo_id, proj_id, 0, 0, desc)
                f.seek(0, 2)
                tarefa.salva(nova, f)
                ordenacao.insertionSort(f, novo_id)
            print("Tarefa criada e base re-ordenada!")

        elif opcao in ["3", "4", "5"]:
            id_busca = int(input("Informe o ID da Tarefa: "))
            with open(nome_db, "r+b") as f:
                qtd = tarefa.tamanho_arquivo(f)
                t, _ = buscaBinaria(id_busca, f, 1, qtd)
                
                if t:
                    if opcao == "3":
                        t['status'] = int(input("Novo Status (0-Pendente, 1-Em Andamento, 2-Concluída): "))
                    elif opcao == "4":
                        t['usuario_id'] = int(input("ID do Usuário responsável: "))
                    elif opcao == "5":
                        t['status'] = -1
                    
                    f.seek((id_busca - 1) * tarefa.tamanho_registro())
                    tarefa.salva(t, f)
                    print(f"Tarefa {id_busca} atualizada com sucesso!")
                else:
                    print("Erro: Tarefa não encontrada.")

        elif opcao == "6":
            print("Filtros: (1) Por Usuário (2) Por Projeto (3) Por Status")
            f_tipo = input("Escolha o filtro: ")
            valor_alvo = int(input("Informe o ID/Código do valor buscado: "))
            
            with open(nome_db, "rb") as f:
                print("\n--- RESULTADOS DA BUSCA SEQUENCIAL ---")
                while True:
                    t = tarefa.le(f)
                    if not t: break
                    
                    match = False
                    if f_tipo == "1" and t['usuario_id'] == valor_alvo: match = True
                    elif f_tipo == "2" and t['projeto_id'] == valor_alvo: match = True
                    elif f_tipo == "3" and t['status'] == valor_alvo: match = True
                    
                    if match:
                        print(f"ID: {t['cod']} | Desc: {t['descricao']} | Status: {t['status']}")
        
        elif opcao == "7":
            executar_testes_desempenho()

        elif opcao == "0":
            break

if __name__ == "__main__":
    menu_principal()