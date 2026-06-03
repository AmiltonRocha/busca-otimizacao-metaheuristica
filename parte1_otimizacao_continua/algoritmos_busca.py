import random
import math


def hill_climbing(f, x_min, x_max, epsilon=0.1, max_iter=1000, max_sem_melhora=50):

    # Ponto inicial: limite inferior do domínio (conforme enunciado)
    x1 = x_min
    x2 = x_min
    melhor_valor = f(x1, x2)

    # Histórico da evolução do melhor valor + contador de estagnação
    historico = [melhor_valor]
    historico_pos = [(x1, x2)]
    sem_melhora = 0

    # Loop principal (até max_iter)
    for i in range(1, max_iter + 1):

        # Gera candidato vizinho: xbest ± epsilon (vizinhança)
        candidato_x1 = x1 + random.uniform(-epsilon, epsilon)
        candidato_x2 = x2 + random.uniform(-epsilon, epsilon)

        # Garante que o candidato está dentro dos limites do domínio
        candidato_x1 = max(x_min, min(x_max, candidato_x1))
        candidato_x2 = max(x_min, min(x_max, candidato_x2))

        # Avalia o candidato na função objetivo
        valor_candidato = f(candidato_x1, candidato_x2)

        # Se candidato é melhor (menor custo), move para ele
        if valor_candidato < melhor_valor:
            x1, x2 = candidato_x1, candidato_x2
            melhor_valor = valor_candidato
            sem_melhora = 0
        else:
            sem_melhora += 1

        historico.append(melhor_valor)
        historico_pos.append((x1, x2))

        # Critério de parada antecipada: estagnação
        if sem_melhora >= max_sem_melhora:
            break

    return (x1, x2), melhor_valor, historico, historico_pos, i

#LRS: Local Random Search
def lrs(f, x_min, x_max, sigma=0.5, max_iter=1000, max_sem_melhora=50):
    x1 = random.uniform(x_min, x_max)
    x2 = random.uniform(x_min, x_max)
    melhor_valor = f(x1, x2)
    historico = [melhor_valor]
    historico_pos = [(x1, x2)]
    sem_melhora = 0
    for i in range(1, max_iter + 1):
        candidato_x1 = x1 + random.gauss(0, sigma)
        candidato_x2 = x2 + random.gauss(0, sigma)
        candidato_x1 = max(x_min, min(x_max, candidato_x1))
        candidato_x2 = max(x_min, min(x_max, candidato_x2))
        valor_candidato = f(candidato_x1, candidato_x2)

        if valor_candidato < melhor_valor:
            x1, x2 = candidato_x1, candidato_x2
            melhor_valor = valor_candidato
            sem_melhora = 0
        else:
            sem_melhora += 1

        historico.append(melhor_valor)
        historico_pos.append((x1, x2))
        if sem_melhora >= max_sem_melhora:
            break
    return (x1, x2), melhor_valor, historico, historico_pos, i

#GRS: Global Random Search
def grs(f, x_min, x_max, max_iter=1000, **kwargs):
    # No GRS não temos um ponto inicial — cada candidato é gerado do zero
    melhor_x1 = None
    melhor_x2 = None
    melhor_valor = float('inf')
    historico = []
    historico_pos = []

    for i in range(1, max_iter + 1):
        candidato_x1 = random.uniform(x_min, x_max)
        candidato_x2 = random.uniform(x_min, x_max)
        valor_candidato = f(candidato_x1, candidato_x2)

        if valor_candidato < melhor_valor:
            melhor_x1, melhor_x2 = candidato_x1, candidato_x2
            melhor_valor = valor_candidato
        
        historico.append(melhor_valor)
        historico_pos.append((melhor_x1, melhor_x2))

    return (melhor_x1, melhor_x2), melhor_valor, historico, historico_pos, i




