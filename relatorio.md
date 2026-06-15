# Breve Relatório de Desempenho: Ordenação Externa

## Resultados Observados
Nos testes realizados, ambos os métodos tiveram desempenho similar na base pequena (1.000 registos, ~0,02s), pois volumes reduzidos são otimizados pela cache do sistema operativo. No entanto, o cenário mudou com o aumento dos dados. No teste de stress com 500.000 registos, obtivemos os seguintes resultados:

Seleção por Substituição + Árvore de Vencedores: ~4,8 segundos
Quicksort Externo: ~31,4 segundos (aproximadamente 6,5 vezes mais lento)

## Análise Técnica do Gargalo (E/S)
Esta diferença colossal ocorre devido ao padrão de acesso ao disco físico. O Quicksort Externo exige constantes acessos aleatórios, movimentando ponteiros de leitura e escrita de um lado para o outro do ficheiro, o que gera uma latência mecânica e eletrónica altíssima. 

Em contrapartida, a Seleção por Substituição auxiliada pela técnica de congelamento no heap e a Árvore de Vencedores operam com leituras e escritas estritamente sequenciais, extraindo a velocidade máxima de transferência do dispositivo de armazenamento.

## Conclusão
Conclui que o gargalo na ordenação externa não é o processamento (CPU), mas sim o custo de Entrada/Saída (E/S). Algoritmos baseados em trocas constantes no próprio ficheiro, como o Quicksort, tornam-se inviáveis na memória secundária. A estratégia de particionamento e intercalação provou ser a mais eficiente e escalável, o que justifica o uso de técnicas similares (Merge Sort Externo) por grandes Sistemas Gestores de Bases de Dados (SGBDs) em ambientes reais.