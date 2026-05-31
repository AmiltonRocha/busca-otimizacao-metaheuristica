import random
from tempera_simulada import TemperaSimulada


class OitoRainhas(TemperaSimulada):

    def __init__(self, n=8, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    def estado_inicial(self):
        estado = list(range(self.n))
        random.shuffle(estado)
        return estado

    def gerar_vizinho(self, estado):
        vizinho = estado[:]
        i, j = random.sample(range(self.n), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
        return vizinho

    def calcular_custo(self, estado):
        conflitos = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if abs(estado[i] - estado[j]) == abs(i - j):
                    conflitos += 1
        return conflitos

    def imprimir_tabuleiro(self, estado):
        print(f"Estado: {estado}  |  Conflitos: {self.calcular_custo(estado)}\n")
        for linha in range(self.n):
            for col in range(self.n):
                print(" Q " if estado[col] == linha else " . ", end="")
            print()


if __name__ == "__main__":
    problema = OitoRainhas(n=8, T_inicial=100.0, alpha=0.995, max_iter=10000)
    solucao, conflitos = problema.resolver()

    print("=== Tempera Simulada - 8 Rainhas ===\n")
    problema.imprimir_tabuleiro(solucao)

    if conflitos == 0:
        print("\nSolucao encontrada!")
    else:
        print(f"\nNao encontrou solucao. Conflitos restantes: {conflitos}")
