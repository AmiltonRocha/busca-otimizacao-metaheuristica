from funcao import *
from algoritmos_busca import hill_climbing, lrs, grs
from collections import Counter

funcoes = [
    ("Quadratica", funcao_quadratica, -100, 100, "min", 0),
    ("Gaussiana",  funcao_gaussiana, -2, 5, "max", 2.0031),
    ("Ackley",     funcao_ackley, -8, 8, "min", 0),
    ("Rastrigin",  funcao_rastrigin, -5.12, 5.12, "min", 0),
    ("Mista",      funcao_mista, -10, 10, "max", 2.0004),
    ("Seno",       funcao_seno, -1, 3, "max", 6.2523),
]

N_RODADAS = 100
MAX_ITER = 1000
MAX_SEM_MELHORA = 50

print("=" * 75)
print(f"{'Funcao':<12} {'Algoritmo':<10} {'Moda':<12} {'Esperado':<12} {'Acertou?':<10}")
print("=" * 75)

for nome, f, x_min, x_max, sentido, esperado in funcoes:
    if sentido == "max":
        f_uso = lambda x1, x2, f=f: -f(x1, x2)
    else:
        f_uso = f

    for nome_algoritmo, algoritmo in [("Hill", hill_climbing), ("LRS", lrs), ("GRS", grs)]:
        solucoes = []
        for _ in range(N_RODADAS):
            res = algoritmo(f_uso, x_min, x_max, max_iter=MAX_ITER, max_sem_melhora=MAX_SEM_MELHORA)
            valor = -res[1] if sentido == "max" else res[1]
            solucoes.append(round(valor, 4))

        moda = Counter(solucoes).most_common(1)[0][0]
        acertou = "SIM" if abs(moda - esperado) < 0.5 else "nao"
        print(f"{nome:<12} {nome_algoritmo:<10} {moda:<12} {esperado:<12} {acertou:<10}")

print("=" * 75)

