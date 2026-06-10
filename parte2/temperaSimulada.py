from abc import ABC, abstractmethod
import random
import math


class TemperaSimulada(ABC):
    """
    Classe base abstrata para Têmpera Simulada.

    Subclasses devem implementar:
        - estado_inicial()  → gera um estado inicial
        - gerar_vizinho(estado) → gera um vizinho do estado atual
        - calcular_custo(estado) → retorna o custo (a ser minimizado)
    """

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
        """
        Executa uma rodada completa da Têmpera Simulada.

        Critérios de parada:
            1. Máximo de iterações atingido (self.max_iter).
            2. Custo ótimo (0) encontrado — parada antecipada.

        Decaimento de temperatura: geométrico  T(k+1) = T(k) * alpha.

        Retorna:
            melhor_estado : lista com o melhor estado encontrado
            melhor_custo  : custo associado ao melhor estado
        """
        estado = self.estado_inicial()
        custo = self.calcular_custo(estado)
        melhor_estado = estado[:]
        melhor_custo = custo

        T = self.T_inicial

        for _ in range(self.max_iter):
            # Parada antecipada: ótimo global já atingido
            if custo == 0:
                break

            vizinho = self.gerar_vizinho(estado)
            custo_vizinho = self.calcular_custo(vizinho)
            delta = custo_vizinho - custo

            # Critério de aceitação de Metropolis
            if delta < 0 or random.random() < math.exp(-delta / T):
                estado = vizinho
                custo = custo_vizinho

                if custo < melhor_custo:
                    melhor_estado = estado[:]
                    melhor_custo = custo

            # Decaimento geométrico da temperatura
            T *= self.alpha

        return melhor_estado, melhor_custo