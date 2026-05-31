from abc import ABC, abstractmethod
import random
import math


class TemperaSimulada(ABC):

    def __init__(self, T_inicial=100.0, alpha=0.995, max_iter=10000):
        self.T_inicial = T_inicial
        self.alpha = alpha
        self.max_iter = max_iter

    @abstractmethod
    def estado_inicial(self):
        pass

    @abstractmethod
    def gerar_vizinho(self, estado):
        pass

    @abstractmethod
    def calcular_custo(self, estado):
        pass

    def resolver(self):
        estado = self.estado_inicial()
        custo = self.calcular_custo(estado)
        melhor_estado = estado[:]
        melhor_custo = custo

        T = self.T_inicial

        for _ in range(self.max_iter):
            if custo == 0:
                break

            vizinho = self.gerar_vizinho(estado)
            custo_vizinho = self.calcular_custo(vizinho)
            delta = custo_vizinho - custo

            if delta < 0 or random.random() < math.exp(-delta / T):
                estado = vizinho
                custo = custo_vizinho

                if custo < melhor_custo:
                    melhor_estado = estado[:]
                    melhor_custo = custo

            T *= self.alpha

        return melhor_estado, melhor_custo
