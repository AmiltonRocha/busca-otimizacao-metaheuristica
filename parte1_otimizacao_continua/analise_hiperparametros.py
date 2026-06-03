from funcao import *
from algoritmos_busca import hill_climbing, lrs

otimos = {
    "Quadratica": 0,
    "Gaussiana":  2.0031,
    "Ackley":     0,
    "Rastrigin":  0,
    "Mista":      2.0004,
    "Seno":       6.2523,
}

funcoes = [
    ("Quadratica", funcao_quadratica, -100, 100, "min"),
    ("Gaussiana",  funcao_gaussiana, -2, 5, "max"),
    ("Ackley",     funcao_ackley, -8, 8, "min"),
    ("Rastrigin",  funcao_rastrigin, -5.12, 5.12, "min"),
    ("Mista",      funcao_mista, -10, 10, "max"),
    ("Seno",       funcao_seno, -1, 3, "max"),
]

N_RODADAS = 30
MAX_ITER = 1000
MAX_SEM_MELHORA = 50
TOL = 0.5

epsilons = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100]
sigmas = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]

print("=" * 60)
print("MENOR EPSILON (Hill Climbing)")
print("=" * 60)
for nome, f, x_min, x_max, sentido in funcoes:
    f_uso = (lambda x1, x2, f=f: -f(x1, x2)) if sentido == "max" else f
    menor = None
    for eps in epsilons:
        acertos = 0
        for _ in range(N_RODADAS):
            res = hill_climbing(f_uso, x_min, x_max, epsilon=eps, max_iter=MAX_ITER, max_sem_melhora=MAX_SEM_MELHORA)
            v = -res[1] if sentido == "max" else res[1]
            if abs(v - otimos[nome]) <= TOL:
                acertos += 1
        if acertos >= N_RODADAS * 0.5:
            menor = eps
            break
    print(f"{nome:<12} menor epsilon = {menor if menor else 'N/A (nunca achou o otimo)'}")

print()
print("=" * 60)
print("MENOR SIGMA (LRS)")
print("=" * 60)
for nome, f, x_min, x_max, sentido in funcoes:
    f_uso = (lambda x1, x2, f=f: -f(x1, x2)) if sentido == "max" else f
    menor = None
    for sig in sigmas:
        acertos = 0
        for _ in range(N_RODADAS):
            res = lrs(f_uso, x_min, x_max, sigma=sig, max_iter=MAX_ITER, max_sem_melhora=MAX_SEM_MELHORA)
            v = -res[1] if sentido == "max" else res[1]
            if abs(v - otimos[nome]) <= TOL:
                acertos += 1
        if acertos >= N_RODADAS * 0.5:
            menor = sig
            break
    print(f"{nome:<12} menor sigma  = {menor if menor else 'N/A (nunca achou o otimo)'}")
