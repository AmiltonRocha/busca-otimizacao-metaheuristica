import random
from questao_2.tempera_simulada import TemperaSimulada


class OitoRainhas(TemperaSimulada):
    """
    Estado: vetor x com 8 componentes onde x[i] é a linha da rainha na coluna i.
    Espaço de estados: 8^8 = 16.777.216 arranjos (uma rainha por coluna).

    Função objetivo: f(x) = 28 - h(x)
      - h(x): número de pares atacantes (linha + diagonal)
      - 28 = C(8,2): total de pares possíveis
      - Ótimo global: f(x) = 28 (nenhum par em conflito)
    Como maximizamos f(x), equivale a minimizar h(x).
    """

    TOTAL_PARES = 28  # C(8, 2) = 28 pares possíveis

    def __init__(self, n=8, passo=2, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        # passo: janela de perturbação — rainha se desloca no máximo ±passo linhas
        self.passo = passo


    def _h(self, estado):
        """Conta pares atacantes: conflitos de linha e de diagonal."""
        conflitos = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if estado[i] == estado[j]:                          # mesma linha
                    conflitos += 1
                elif abs(estado[i] - estado[j]) == abs(i - j):     # diagonal
                    conflitos += 1
        return conflitos

    def funcao_objetivo(self, estado):
        """f(x) = 28 - h(x). Valor ótimo: 28."""
        return self.TOTAL_PARES - self._h(estado)

    def calcular_custo(self, estado):
        """Minimizar h(x) equivale a maximizar f(x). Ótimo: 0."""
        return self._h(estado)


    def gerar_vizinho(self, estado):
        """
        Perturba apenas UMA rainha por ±passo linhas.
        Não acessa o espaço inteiro — a vizinhança é uma faixa local de 2*passo+1
        posições para cada coluna, não todos os 8^8 estados.
        """
        vizinho = estado[:]
        coluna = random.randint(0, self.n - 1)
        deslocamento = random.randint(-self.passo, self.passo)
        nova_linha = vizinho[coluna] + deslocamento
        # Mantém dentro do tabuleiro sem circulação — clampando a faixa
        nova_linha = max(0, min(self.n - 1, nova_linha))
        vizinho[coluna] = nova_linha
        return vizinho


    def estado_inicial(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]


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


if __name__ == "__main__":
    T_INICIAL = 10.0

    # T(k) = T_0 * alpha^k  →  a cada iteração T *= alpha (implementado na classe base)
    ALPHA = 0.9995

    problema = OitoRainhas(
        n=8,
        passo=4,           # rainha se desloca no máximo 4 linhas por perturbação
        T_inicial=T_INICIAL,
        alpha=ALPHA,
        max_iter=30000,
    )

    solucao, conflitos = problema.resolver()

    print("=== Tempera Simulada - 8 Rainhas ===\n")
    problema.imprimir_tabuleiro(solucao)

    if conflitos == 0:
        print(f"\nSolucao otima encontrada!  f(x) = {problema.funcao_objetivo(solucao)}")
    else:
        print(f"\nSolucao subotima.  f(x) = {problema.funcao_objetivo(solucao)},  h(x) = {conflitos}")
