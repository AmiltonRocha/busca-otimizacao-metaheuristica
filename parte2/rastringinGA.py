import random
import math
import time
from algoritmoGenetico import AlgoritmoGenetico

class RastriginGA(AlgoritmoGenetico):
    """
    GA não-canônico para minimização da função Rastrigin com n=50.

    f(x) = 10*n + Σ(xi² - 10*cos(π*xi)),  xi ∈ [-5.12, 5.12]
    Mínimo global: f(0, ..., 0) = 0

    Operadores:
      - Recombinação: SBX (Simulated Binary Crossover) com η=1
      - Mutação:      Gaussiana com desvio-padrão σ aplicado a todos os genes
    """

    N     = 50
    X_MIN = -5.12
    X_MAX =  5.12

    def __init__(self, eta_sbx=1.0, sigma_mutacao=0.5, **kwargs):
        super().__init__(**kwargs)
        self.eta_sbx       = eta_sbx
        self.sigma_mutacao = sigma_mutacao

    # ── Função objetivo ────────────────────────────────────────────────────────

    def funcao_objetivo(self, x):
        return 10 * self.N + sum(xi**2 - 10 * math.cos(math.pi * xi) for xi in x)

    def calcular_custo(self, individuo):
        return self.funcao_objetivo(individuo)

    # ── Indivíduo: vetor real em [-5.12, 5.12] ────────────────────────────────

    def gerar_individuo(self):
        return [random.uniform(self.X_MIN, self.X_MAX) for _ in range(self.N)]

    # ── Recombinação SBX com η=1 ───────────────────────────────────────────────

    def recombinar(self, pai1, pai2):
        """
        Simulated Binary Crossover (SBX) com η=1.
        Para cada gene, sorteia u ~ U(0,1) e calcula o fator de espalhamento β:
          u ≤ 0.5 → β = (2u)^(1/(η+1))
          u >  0.5 → β = (1 / (2(1-u)))^(1/(η+1))
        filho = 0.5 * ((1+β)*p1 + (1-β)*p2)
        """
        eta = self.eta_sbx
        filho = []
        for p1, p2 in zip(pai1, pai2):
            u = random.random()
            if u <= 0.5:
                beta = (2 * u) ** (1 / (eta + 1))
            else:
                beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
            gene = 0.5 * ((1 + beta) * p1 + (1 - beta) * p2)
            gene = max(self.X_MIN, min(self.X_MAX, gene))
            filho.append(gene)
        return filho

    # ── Mutação gaussiana ──────────────────────────────────────────────────────

    def mutar(self, individuo):
        """
        Mutação gaussiana: aplica perturbação N(0, σ) a cada gene.
        Resultado é clampado ao domínio [-5.12, 5.12].
        """
        return [
            max(self.X_MIN, min(self.X_MAX, xi + random.gauss(0, self.sigma_mutacao)))
            for xi in individuo
        ]


# ── LRS: Local Random Search — método de comparação (baixo custo de memória) ──

def lrs_rastrigin(n=50, x_min=-5.12, x_max=5.12, sigma=0.5, max_iter=50000):
    """
    Local Random Search: mantém apenas 1 solução em memória.
    A cada iteração perturba gaussianamente UM gene; aceita se houver melhora.
    Custo de memória: O(n) contra O(N*n) do GA.
    """
    def f(x):
        return 10 * n + sum(xi**2 - 10 * math.cos(math.pi * xi) for xi in x)

    x     = [random.uniform(x_min, x_max) for _ in range(n)]
    custo = f(x)

    for _ in range(max_iter):
        x_novo       = x[:]
        i            = random.randint(0, n - 1)
        x_novo[i]    = max(x_min, min(x_max, x_novo[i] + random.gauss(0, sigma)))
        custo_novo   = f(x_novo)
        if custo_novo < custo:
            x, custo = x_novo, custo_novo

    return x, custo


# ── Análise: tamanho de população vs. custo computacional ─────────────────────

def analisar_tamanho_populacao(tamanhos, n_rodadas=5, max_geracoes=300):
    print(f"{'Pop':>6} | {'Custo médio':>12} | {'Melhor custo':>13} | {'Tempo médio':>12}")
    print("-" * 55)
    for pop in tamanhos:
        custos, tempos = [], []
        for _ in range(n_rodadas):
            t0 = time.time()
            p  = RastriginGA(
                n_individuos   = pop,
                max_geracoes   = max_geracoes,
                prob_mutacao   = 0.3,
                n_elite        = max(1, pop // 50),
                max_sem_melhora= 50,
                eta_sbx        = 1.0,
                sigma_mutacao  = 0.5,
            )
            _, custo, _, _ = p.evoluir()
            custos.append(custo)
            tempos.append(time.time() - t0)
        media  = sum(custos) / len(custos)
        melhor = min(custos)
        t_med  = sum(tempos) / len(tempos)
        print(f"{pop:>6} | {media:>12.4f} | {melhor:>13.4f} | {t_med:>11.2f}s")


if __name__ == "__main__":
    PARAMS = dict(
        n_individuos    = 100,
        max_geracoes    = 500,
        prob_mutacao    = 0.3,    # 30% dos indivíduos são mutados por geração
        n_elite         = 2,
        max_sem_melhora = 50,
        eta_sbx         = 1.0,
        sigma_mutacao   = 0.5,
    )

    # ── Execução do GA ─────────────────────────────────────────────────────────
    print("=== GA Não-Canônico — Rastrigin (n=50) ===\n")
    problema = RastriginGA(**PARAMS)
    t0 = time.time()
    solucao, custo_ga, historico, geracao = problema.evoluir()
    t_ga = time.time() - t0

    print(f"Melhor custo (GA):    {custo_ga:.4f}  (ótimo = 0)")
    print(f"Geração de parada:    {geracao}")
    print(f"Tempo:                {t_ga:.2f}s")
    print(f"Melhora:              {historico[0]:.2f} → {historico[-1]:.2f}\n")

    # ── Execução do LRS ────────────────────────────────────────────────────────
    # Orçamento equivalente: pop * geracoes ≈ 50.000 avaliações
    print("=== LRS (Local Random Search) — baixo custo de memória ===\n")
    t0 = time.time()
    _, custo_lrs = lrs_rastrigin(n=50, sigma=0.5, max_iter=50000)
    t_lrs = time.time() - t0

    print(f"Melhor custo (LRS):   {custo_lrs:.4f}  (ótimo = 0)")
    print(f"Tempo:                {t_lrs:.2f}s")
    print(f"GA melhora sobre LRS: {custo_lrs - custo_ga:.4f}\n")

    # ── Análise: tamanho de população ─────────────────────────────────────────
    print("=== Análise: equilíbrio entre tamanho da população e resultado ===\n")
    analisar_tamanho_populacao([20, 50, 100, 200, 500], n_rodadas=5)
