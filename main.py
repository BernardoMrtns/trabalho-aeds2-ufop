import time
import os
import tarefa
import ordenacao
import quicksort_externo
import particoes_intercalacao
import tabela_hash
from busca_sequencial import buscaSequencial
from busca_binaria import buscaBinaria

def inicializar_arquivos():
    if not os.path.exists("usuarios_db.txt"):
        with open("usuarios_db.txt", "w", encoding="utf-8") as f:
            for i in range(1, 1001):
                f.write(f"{i};Usuario Placeholder {i}\n")
                
    if not os.path.exists("projetos_db.txt"):
        with open("projetos_db.txt", "w", encoding="utf-8") as f:
            for i in range(1, 501):
                f.write(f"{i};Projeto Placeholder {i}\n")

def executar_testes_desempenho():
    tamanhos_de_base = [1000, 10000, 100000, 500000]
    
    with open("log.txt", "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write("=== LOG DE DESEMPENHO DE ORDENAÇÃO EXTERNA ===\n\n")
        
        for qtd in tamanhos_de_base:
            print(f"Gerando base de {qtd} registros para testes...")
            nome_db_teste = f"tarefas_teste_{qtd}.dat"
            tarefa.criarBase(nome_db_teste, qtd)
            
            inicio_qs = time.perf_counter()
            with open(nome_db_teste, 'r+b') as f:
                quicksort_externo.executar(f, 1, qtd)
            tempo_qs = time.perf_counter() - inicio_qs
            
            tarefa.criarBase(nome_db_teste, qtd)
            
            inicio_pi = time.perf_counter()
            with open(nome_db_teste, 'rb') as f:
                arquivos_part = particoes_intercalacao.gerar_particoes_substituicao(f, qtd, tamanho_memoria=500)
            
            nome_db_ordenado = f"tarefas_ordenado_{qtd}.dat"
            particoes_intercalacao.intercalar_arvore_vencedores(arquivos_part, nome_db_ordenado)
            tempo_pi = time.perf_counter() - inicio_pi
            
            log_str = (
                f"Tamanho da Base: {qtd} registros\n"
                f"Quicksort Externo   -> Tempo (s): {tempo_qs:.6f}\n"
                f"Sel. Substituição + Árvore -> Tempo (s): {tempo_pi:.6f}\n"
                f"--------------------------------------------------\n"
            )
            arquivo_log.write(log_str)
            print(f"Concluído {qtd} registros. QS: {tempo_qs:.2f}s | Part+Int: {tempo_pi:.2f}s")
            
            if os.path.exists(nome_db_teste): os.remove(nome_db_teste)
            if os.path.exists(nome_db_ordenado): os.remove(nome_db_ordenado)
            
    print("\n[Sucesso] Testes concluídos. Resultados salvos em 'log.txt'.")
    print("Agora gere seu relatório final se baseando nas métricas do arquivo de log!")

def menu_principal():
    inicializar_arquivos()
    nome_db = "tarefas_db.dat"
    nome_hash = "tarefas_hash.dat"
    tabela_hash.inicializar_tabela_hash(nome_hash)
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
        print("8. Gerenciamento via Tabela Hash")
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

        elif opcao == "8":
            while True:
                print("\n--- GERENCIAMENTO: TABELA HASH ---")
                print("1. Inserir Tarefa")
                print("2. Buscar Tarefa")
                print("3. Remover Tarefa (Libera espaço)")
                print("0. Voltar ao Menu Principal")
                sub_op = input("Escolha: ")
                
                if sub_op == "1":
                    print("\n[Inserindo nova Tarefa na Hash]")
                    cod = int(input("ID da Tarefa: "))
                    proj = int(input("ID do Projeto: "))
                    usu = int(input("ID do Usuário: "))
                    status = int(input("Status (0/1/2): "))
                    desc = input("Descrição: ")
                    
                    # FALA: "Aqui eu chamo a inserção. Se houver um espaço removido (flag 2), ele será reaproveitado."
                    tabela_hash.inserir_hash(nome_hash, cod, proj, usu, status, desc)
                    
                elif sub_op == "2":
                    cod = int(input("\nQual ID deseja buscar? "))
                    # FALA: "A busca calcula o endereço e vai direto no byte certo no disco, complexidade média O(1)."
                    resultado = tabela_hash.buscar_hash(nome_hash, cod)
                    if resultado:
                        print(f"\n[Encontrado no Endereço Físico {resultado['endereco_fisico']}]")
                        print(f"ID: {resultado['cod']} | Proj: {resultado['projeto_id']} | Usu: {resultado['usuario_id']} | Status: {resultado['status']}")
                        print(f"Desc: {resultado['descricao']}")
                    else:
                        print("\n[Erro] Tarefa não encontrada na Tabela Hash.")
                        
                elif sub_op == "3":
                    cod = int(input("\nQual ID deseja remover? "))
                    # FALA: "A exclusão é lógica. Eu mudo a Flag do registro para 2 (Removido). Isso cumpre o requisito de Gerenciamento de Espaço."
                    tabela_hash.remover_hash(nome_hash, cod)
                    
                elif sub_op == "0":
                    break
        # =========================================================================

        elif opcao == "0":
            break

if __name__ == "__main__":
    menu_principal()