import time
import tarefa
import ordenacao
from busca_sequencial import buscaSequencial
from busca_binaria import buscaBinaria

def main():
    # ====================================================================
    # REQUISITOS 1 E 2 (4 pontos): Estruturas e Bases de Dados
    # A estrutura binária da Tarefa já está definida em tarefa.py.
    # Abaixo, criamos bases de dados físicas (arquivos) para as outras entidades.
    # ====================================================================
    with open("usuarios_db.txt", "w", encoding="utf-8") as f:
        f.write("1;Diogo V.\n2;Bernardo M.\n3;Pedro R.\n")
    with open("projetos_db.txt", "w", encoding="utf-8") as f:
        f.write("1;Migração de Dashboards\n2;Programar Backend\n3;Programar Frontend\n")

    # ====================================================================
    # REQUISITO 4 (2 pontos): Diferentes tamanhos de base
    # ====================================================================
    tamanhos_de_base = [10, 50, 100, 500, 1000]
    
    # ====================================================================
    # REQUISITO 5 (2 pontos): Contagem e log.txt
    # ====================================================================
    arquivo_log = open("log.txt", "w", encoding="utf-8")
    arquivo_log.write("=== LOG DE DESEMPENHO DE BUSCAS ===\n\n")

    for qtd in tamanhos_de_base:
        print(f"\n======================================")
        print(f"Iniciando execucao para base de {qtd} registros...")
        
        nome_arquivo_dados = "tarefas_db.dat"
        
        print("Gerando a base de dados e ordenando...")
        tarefa.criarBase(nome_arquivo_dados, qtd)
        
        with open(nome_arquivo_dados, 'r+b') as arquivo_dados:
            ordenacao.insertionSort(arquivo_dados, qtd)
        
        id_alvo_busca = qtd # Pior caso para a busca sequencial
        
        # ====================================================================
        # REQUISITO 3 (15 pontos): Estratégias de Busca iterando na base
        # ====================================================================
        with open(nome_arquivo_dados, 'rb') as arquivo_dados:
            inicio_seq = time.perf_counter()
            _, comp_seq = buscaSequencial(id_alvo_busca, arquivo_dados)
            tempo_seq = time.perf_counter() - inicio_seq
            
            inicio_bin = time.perf_counter()
            _, comp_bin = buscaBinaria(id_alvo_busca, arquivo_dados, 1, qtd)
            tempo_bin = time.perf_counter() - inicio_bin
        
        # Salvando medições (Req 5)
        arquivo_log.write(
            f"Tamanho da Base: {qtd} registros\n"
            f"Busca Sequencial -> Comparacoes: {comp_seq} | Tempo (s): {tempo_seq:.6f}\n"
            f"Busca Binaria    -> Comparacoes: {comp_bin} | Tempo (s): {tempo_bin:.6f}\n"
            f"--------------------------------------------------\n"
        )
        print(f"Arquivo 'log.txt' atualizado com os dados da base de {qtd}.")
        
    arquivo_log.close()


    # ====================================================================
    # REQUISITO 6 (12 pontos): Operações e interações utilizando as buscas
    # ====================================================================
    print("\n======================================")
    print("DEMONSTRANDO INTERAÇÕES ENTRE ENTIDADES")
    print("======================================")
    
    tamanho_base_atual = 1000 # Usaremos a última base (1000) para testar
    
    with open("tarefas_db.dat", 'r+b') as arquivo_dados:
        
        # Operação A: Editar e Atribuir (Usa Busca Binária)
        id_editar = 500
        print(f"\n[Ação] Atribuindo Tarefa {id_editar} ao Usuário 2 e alterando status...")
        t_encontrada, comparacoes = buscaBinaria(id_editar, arquivo_dados, 1, tamanho_base_atual)
        
        if t_encontrada:
            t_encontrada['usuario_id'] = 2 # Interação Tarefa -> Usuário Bernardo
            t_encontrada['status'] = 1     # 1 = Em Andamento
            arquivo_dados.seek((id_editar - 1) * tarefa.tamanho_registro())
            tarefa.salva(t_encontrada, arquivo_dados)
            print(f"-> Sucesso! Tarefa {id_editar} atualizada via Busca Binária (O(log n)).")

        # Operação B: Excluir Tarefa (Usa Busca Binária)
        id_excluir = 50
        print(f"\n[Ação] Excluindo logicamente a Tarefa {id_excluir}...")
        t_excluir, _ = buscaBinaria(id_excluir, arquivo_dados, 1, tamanho_base_atual)
        
        if t_excluir:
            t_excluir['status'] = -1 # Status -1 = Excluída
            arquivo_dados.seek((id_excluir - 1) * tarefa.tamanho_registro())
            tarefa.salva(t_excluir, arquivo_dados)
            print(f"-> Sucesso! Tarefa {id_excluir} excluída via Busca Binária.")

        # Operação C: Listar por Filtro (Usa Busca Sequencial)
        usuario_alvo = 2
        print(f"\n[Ação] Listando tarefas ativas do Usuário ID {usuario_alvo}...")
        arquivo_dados.seek(0)
        
        while True:
            t_lida = tarefa.le(arquivo_dados)
            if not t_lida:
                break
                
            # Filtra cruzando dados da entidade Tarefa com a entidade Usuário e Status
            if t_lida['usuario_id'] == usuario_alvo and t_lida['status'] != -1:
                print(f"-> Tarefa {t_lida['cod']} | Projeto: {t_lida['projeto_id']} | Status: {t_lida['status']}")

    print("\nTodas as execucoes finalizadas.")

if __name__ == "__main__":
    main()