import random
import math
import csv
from collections import Counter
from algoritmoGenetico import AlgoritmoGenetico


class CaixeiroViajanteGA(AlgoritmoGenetico):
    """
    Indivíduo: permutação dos índices dos pontos representando a ordem da rota.
    Custo: soma das distâncias euclidianas 3D entre pontos consecutivos (ida + retorno).
    Objetivo: minimizar o custo total da rota do drone.
    """

    def __init__(self, pontos, **kwargs):
        super().__init__(**kwargs)
        self.pontos = pontos
        self.n_pontos = len(pontos)

    def _distancia(self, i, j):
        xi, yi, zi = self.pontos[i]
        xj, yj, zj = self.pontos[j]
        return math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2)

    # ── Requisito 2 (indivíduo): permutação aleatória dos pontos ──────────────

    def gerar_individuo(self):
        rota = list(range(self.n_pontos))
        random.shuffle(rota)
        return rota

    # ── Função custo: Ψ(x) = soma das distâncias da rota ─────────────────────

    def calcular_custo(self, individuo):
        return sum(
            self._distancia(individuo[i], individuo[(i + 1) % self.n_pontos])
            for i in range(self.n_pontos)
        )

    # ── Requisito 4: recombinação de dois pontos (Order Crossover - OX) ───────

    def recombinar(self, pai1, pai2):
        """
        Variação de dois pontos para problemas combinatórios (sem genes repetidos):
        1. Sorteia dois pontos de corte e copia o segmento de pai1 para o filho.
        2. Preenche as posições restantes com os genes de pai2 na ordem original,
           pulando os que já estão no segmento copiado.
        """
        n = len(pai1)
        i, j = sorted(random.sample(range(n), 2))

        segmento = pai1[i:j + 1]
        segmento_set = set(segmento)

        filho = [None] * n
        filho[i:j + 1] = segmento

        resto = [g for g in pai2 if g not in segmento_set]
        pos = 0
        for k in range(n):
            if filho[k] is None:
                filho[k] = resto[pos]
                pos += 1

        return filho

    # ── Requisito 5: mutação por troca de dois genes (1%) ─────────────────────

    def mutar(self, individuo):
        """Troca dois genes aleatórios na sequência cromossômica."""
        mutante = individuo[:]
        i, j = random.sample(range(len(mutante)), 2)
        mutante[i], mutante[j] = mutante[j], mutante[i]
        return mutante

    def imprimir_resultado(self, individuo):
        custo = self.calcular_custo(individuo)
        rota = " → ".join(str(p) for p in individuo) + f" → {individuo[0]}"
        print(f"Custo da rota: {custo:.2f}")
        print(f"Rota: {rota}")


# ── Geração de pontos 3D por região (simula CaixeiroGrupos.csv) ───────────────

def gerar_pontos_3d_por_regiao(n_por_regiao, seed=None):
    """
    Gera n_por_regiao pontos em 4 regiões distintas do espaço 3D,
    simulando a distribuição exibida na Figura 2 do trabalho.
    """
    if seed is not None:
        random.seed(seed)

    regioes = [
        ((-30, -10), (-30, -10), (10, 30)),
        ((-30, -10), (10, 30), (-30, -10)),
        ((10, 30), (-30, -10), (-30, -10)),
        ((10, 30), (10, 30), (10, 30)),
    ]

    pontos = []
    for (x1, x2), (y1, y2), (z1, z2) in regioes:
        for _ in range(n_por_regiao):
            pontos.append((
                random.uniform(x1, x2),
                random.uniform(y1, y2),
                random.uniform(z1, z2),
            ))

    random.shuffle(pontos)
    return pontos


def carregar_csv(caminho):
    pontos = []
    with open(caminho, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                pontos.append(tuple(float(v) for v in row[:3]))
    return pontos


# ── Análise: moda de gerações e impacto do elitismo (Requisito 7) ─────────────

def analisar_geracoes(pontos, n_rodadas=30, **kwargs):
    geracoes = []
    custos = []
    for _ in range(n_rodadas):
        problema = CaixeiroViajanteGA(pontos=pontos, **kwargs)
        _, custo, _, geracao = problema.evoluir()
        geracoes.append(geracao)
        custos.append(custo)

    moda_geracao = Counter(geracoes).most_common(1)[0][0]
    media_custo = sum(custos) / len(custos)
    melhor_custo = min(custos)

    print(f"  Rodadas:       {n_rodadas}")
    print(f"  Moda gerações: {moda_geracao}")
    print(f"  Custo médio:   {media_custo:.2f}")
    print(f"  Melhor custo:  {melhor_custo:.2f}")
    return moda_geracao, media_custo


if __name__ == "__main__":
    # ── Requisito 1: 30 < Npontos < 60 ────────────────────────────────────────
    N_POR_REGIAO = 10          # 4 regiões × 10 pontos = 40 pontos total
    pontos = gerar_pontos_3d_por_regiao(N_POR_REGIAO, seed=42)
    print(f"Pontos gerados: {len(pontos)} (4 regiões × {N_POR_REGIAO})\n")

    # ── Requisito 2: N indivíduos e máximo de gerações ────────────────────────
    PARAMS = dict(
        n_individuos=100,
        max_geracoes=500,
        prob_mutacao=0.01,     # Requisito 5: mutação 1%
        n_elite=5,             # Requisito 7: elitismo com Ne=5
        max_sem_melhora=50,    # Requisito 6: estagnação
    )

    problema = CaixeiroViajanteGA(pontos=pontos, **PARAMS)
    solucao, custo, historico, geracao = problema.evoluir()

    print("=== Algoritmo Genético - Caixeiro Viajante 3D ===\n")
    problema.imprimir_resultado(solucao)
    print(f"Geração de parada: {geracao}")
    print(f"Melhora ao longo das gerações: {historico[0]:.2f} → {historico[-1]:.2f}\n")

    # ── Requisito 7: análise — moda de gerações e impacto do elitismo ─────────
    print("--- Análise: sem elitismo (n_elite=0) ---")
    analisar_geracoes(pontos, n_rodadas=30, **{**PARAMS, "n_elite": 0})

    print("\n--- Análise: com elitismo (n_elite=5) ---")
    analisar_geracoes(pontos, n_rodadas=30, **PARAMS)
