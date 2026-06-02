from funcao import *
from algoritmos_busca import hill_climbing, lrs, grs
from collections import Counter

funcoes = [
    ("Quadratica", funcao_quadratica, -100, 100),
    ("Gaussiana",  funcao_gaussiana, -2, 5),
    ("Ackley",     funcao_ackley, -8, 8),
    ("Rastrigin",  funcao_rastrigin, -5.12, 5.12),
    ("Mista",      funcao_mista, -10, 10),
    ("Seno",       funcao_seno, -1, 3),
]

N_RODADAS = 100
MAX_ITER = 1000
MAX_SEM_MELHORA = 50

for nome, f, x_min, x_max in funcoes:
    print(f"\n=== {nome} ===")

    for nome_algoritmo, algoritmo in [("Hill", hill_climbing), ("LRS", lrs), ("GRS", grs)]:
        solucoes = []
        for _ in range(N_RODADAS):
            res = algoritmo(f, x_min, x_max, max_iter=MAX_ITER, max_sem_melhora=MAX_SEM_MELHORA)
            solucoes.append(round(res[1], 4))

        moda = Counter(solucoes).most_common(1)[0][0]
        print(f"  {nome_algoritmo}: moda = {moda}")

