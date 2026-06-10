from abc import ABC, abstractmethod
import random


class AlgoritmoGenetico(ABC):

    def __init__(self, n_individuos=100, max_geracoes=500,
                 prob_mutacao=0.01, n_elite=2, max_sem_melhora=50):
        self.n_individuos = n_individuos
        self.max_geracoes = max_geracoes
        self.prob_mutacao = prob_mutacao
        self.n_elite = n_elite
        # max_sem_melhora: critério de parada por estagnação
        self.max_sem_melhora = max_sem_melhora


    @abstractmethod
    def gerar_individuo(self):
        pass

    @abstractmethod
    def calcular_custo(self, individuo):
        pass

    @abstractmethod
    def recombinar(self, pai1, pai2):
        pass

    @abstractmethod
    def mutar(self, individuo):
        pass


    def gerar_populacao(self):
        return [self.gerar_individuo() for _ in range(self.n_individuos)]

    def selecionar_por_torneio(self, populacao, custos, k=3):
        """
        Torneio: sorteia k candidatos aleatórios e retorna o de menor custo.
        Pressão seletiva controlada pelo tamanho k do torneio.
        """
        candidatos = random.sample(range(len(populacao)), k)
        melhor = min(candidatos, key=lambda i: custos[i])
        return populacao[melhor][:]

    def evoluir(self):
        populacao = self.gerar_populacao()
        custos = [self.calcular_custo(ind) for ind in populacao]

        idx = min(range(len(custos)), key=lambda i: custos[i])
        melhor_individuo = populacao[idx][:]
        melhor_custo = custos[idx]

        historico = [melhor_custo]
        sem_melhora = 0
        geracao_final = 0

        for geracao in range(1, self.max_geracoes + 1):
            geracao_final = geracao

            # para quando o melhor não melhora por max_sem_melhora gerações seguidas
            if sem_melhora >= self.max_sem_melhora:
                break

            # copia os n_elite melhores diretamente para a próxima geração
            indices_ord = sorted(range(len(custos)), key=lambda i: custos[i])
            elite = [populacao[i][:] for i in indices_ord[:self.n_elite]]

            nova_populacao = elite[:]
            while len(nova_populacao) < self.n_individuos:
                pai1 = self.selecionar_por_torneio(populacao, custos)
                pai2 = self.selecionar_por_torneio(populacao, custos)
                filho = self.recombinar(pai1, pai2)
                if random.random() < self.prob_mutacao:
                    filho = self.mutar(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao
            custos = [self.calcular_custo(ind) for ind in populacao]

            idx = min(range(len(custos)), key=lambda i: custos[i])
            if custos[idx] < melhor_custo:
                melhor_custo = custos[idx]
                melhor_individuo = populacao[idx][:]
                sem_melhora = 0
            else:
                sem_melhora += 1

            historico.append(melhor_custo)

        return melhor_individuo, melhor_custo, historico, geracao_final
