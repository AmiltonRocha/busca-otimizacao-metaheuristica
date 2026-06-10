import random
import time
from temperaSimulada import TemperaSimulada


class OitoRainhas(TemperaSimulada):
    """
    Estado: vetor x com 8 componentes onde x[i] é a linha da rainha na coluna i.
    Espaço de estados: 8^8 = 16.777.216 arranjos (uma rainha por coluna).

    Função objetivo: f(x) = 28 - h(x)
      - h(x): número de pares atacantes (linha + diagonal)
      - 28 = C(8,2): total de pares possíveis
      - Ótimo global: f(x) = 28 (nenhum par em conflito, h(x) = 0)

    Como a SA minimiza, calcular_custo retorna h(x).
    Maximizar f(x) = 28 - h(x)  ≡  Minimizar h(x).
    """

    TOTAL_PARES = 28  # C(8, 2) = 28 pares possíveis

    def __init__(self, n=8, passo=4, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.passo = passo

    # Funções Avaliação
    def _h(self, estado):
        """Conta pares atacantes: conflitos de linha e de diagonal."""
        conflitos = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if estado[i] == estado[j]:                       # mesma linha
                    conflitos += 1
                elif abs(estado[i] - estado[j]) == abs(i - j):  # diagonal
                    conflitos += 1
        return conflitos

    def funcao_objetivo(self, estado):
        """f(x) = 28 - h(x). Valor ótimo: 28."""
        return self.TOTAL_PARES - self._h(estado)

    def calcular_custo(self, estado):
        """Minimizar h(x) equivale a maximizar f(x). Ótimo: 0."""
        return self._h(estado)

    # Gerador de vizinhos
    def estado_inicial(self):
        """Estado inicial completamente aleatório."""
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def gerar_vizinho(self, estado):
        """
        Perturba apenas UMA rainha por ±passo linhas.

        A vizinhança é uma faixa local de (2*passo + 1) posições para a
        coluna sorteada — não acessa todo o espaço de 8^8 estados.
        O clamping mantém a rainha dentro do tabuleiro sem circulação.
        """
        vizinho = estado[:]
        coluna = random.randint(0, self.n - 1)
        deslocamento = random.randint(-self.passo, self.passo)
        nova_linha = vizinho[coluna] + deslocamento
        nova_linha = max(0, min(self.n - 1, nova_linha))
        vizinho[coluna] = nova_linha
        return vizinho


    def imprimir_tabuleiro(self, estado):
        hx = self._h(estado)
        fx = self.funcao_objetivo(estado)
        print(f"Estado:       {estado}")
        print(f"h(x)        = {hx}  (pares atacantes)")
        print(f"f(x) = 28 - {hx} = {fx}  (ótimo = 28)\n")
        for linha in range(self.n):
            for col in range(self.n):
                print(" Q " if estado[col] == linha else " . ", end="")
            print()


    # Busca pelas 92 soluções distintas 
def _normalizar(solucao):
    """Converte lista para tupla (hashável) para armazenar em set."""
    return tuple(solucao)


def buscar_92_solucoes(T_inicial=10.0, alpha=0.9995, max_iter=30000, passo=4):
    """
    Executa a Têmpera Simulada em loop até que as 92 soluções distintas
    do problema das 8-rainhas sejam encontradas.

    A cada tentativa cria-se uma nova instância (temperatura reiniciada)
    com estado inicial aleatório, garantindo diversidade de exploração.

    Retorna:
        solucoes   : set com as 92 soluções (como tuplas)
        tentativas : número total de execuções da SA
        tempo_s    : tempo total em segundos
    """
    solucoes_distintas = set()
    tentativas = 0
    inicio = time.time()

    while len(solucoes_distintas) < 92:
        # Nova instância a cada tentativa — temperatura sempre reinicia
        problema = OitoRainhas(
            n=8,
            passo=passo,
            T_inicial=T_inicial,
            alpha=alpha,
            max_iter=max_iter,
        )
        solucao, custo = problema.resolver()
        tentativas += 1

        if custo == 0:
            solucoes_distintas.add(_normalizar(solucao))

        # Progresso a cada 500 tentativas
        if tentativas % 500 == 0:
            print(
                f"  Tentativas: {tentativas:6d} | "
                f"Soluções distintas encontradas: {len(solucoes_distintas):3d}/92"
            )

    tempo_total = time.time() - inicio
    return solucoes_distintas, tentativas, tempo_total


def exibir_relatorio_92(solucoes, tentativas, tempo_s):
    """Imprime o relatório de custo computacional da busca pelas 92 soluções."""
    print("\n" + "=" * 60)
    print("  RELATÓRIO — Busca pelas 92 soluções das 8-Rainhas")
    print("=" * 60)
    print(f"  Soluções distintas encontradas : {len(solucoes)}")
    print(f"  Total de execuções da SA       : {tentativas}")
    print(f"  Taxa de sucesso                : {len(solucoes)/tentativas*100:.1f}%")
    print(f"  Tempo total                    : {tempo_s:.2f} s")
    print(f"  Tempo médio por execução       : {tempo_s/tentativas*1000:.2f} ms")
    print("=" * 60)
    print("\nPrimeiras 10 soluções encontradas:")
    for i, sol in enumerate(sorted(solucoes)[:10], 1):
        print(f"  [{i:2d}] {list(sol)}")
    print("  ...")



if __name__ == "__main__":

    T_INICIAL = 10.0
    ALPHA     = 0.9995
    MAX_ITER  = 30000
    PASSO     = 4

    print("=" * 60)
    print("  Têmpera Simulada — 8 Rainhas  (rodada única)")
    print("=" * 60)

    problema = OitoRainhas(
        n=8,
        passo=PASSO,
        T_inicial=T_INICIAL,
        alpha=ALPHA,
        max_iter=MAX_ITER,
    )
    solucao, conflitos = problema.resolver()

    print()
    problema.imprimir_tabuleiro(solucao)

    if conflitos == 0:
        print(f"\nSolução ótima encontrada!  f(x) = {problema.funcao_objetivo(solucao)}")
    else:
        print(
            f"\nSolução subótima.  "
            f"f(x) = {problema.funcao_objetivo(solucao)},  h(x) = {conflitos}"
        )


    print("\n" + "=" * 60)
    print("  Buscando as 92 soluções distintas...")
    print("=" * 60)

    solucoes, tentativas, tempo_s = buscar_92_solucoes(
        T_inicial=T_INICIAL,
        alpha=ALPHA,
        max_iter=MAX_ITER,
        passo=PASSO,
    )

    exibir_relatorio_92(solucoes, tentativas, tempo_s)