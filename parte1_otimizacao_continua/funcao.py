import numpy as np  
# Função Objetiva 


#minimização
def funcao_quadratica (x1, x2):
    return x1**2 + x2**2 
#maxização 
def funcao_gaussiana (x1,x2):
     return np.exp(-(x1**2 + x2**2)) + 2 * np.exp(-((x1 - 1.7)**2 + (x2 - 1.7)**2))

def funcao_ackley (x1,x2):
    #puxa para perto do termo de origem
    termo1 = -20 * np.exp(-0.2 * np.sqrt(0.5 * (x1**2 + x2**2)))
    #criação de varias ondas
    termo2 = -np.exp(0.5 * (np.cos(2 * np.pi * x1) + np.cos(2 * np.pi * x2)))
    #Retorna o minimo global
    return termo1 +termo2 + 20 + np.e

#Função com muitos mínimos locais; mínimo global em (0,0)
def funcao_rastrigin(x1, x2):
 return (x1**2 - 10 * np.cos(2 * np.pi * x1) + 10) + (x2**2 - 10 * np.cos(2 * np.pi * x2) + 10)

#Maximizar: mistura de gaussiana, cosseno e termo linear
def funcao_mista(x1, x2):
     return (x1 * np.cos(x1)) / 20 + 2 * np.exp(-x1**2 - (x2 - 1)**2)  + 0.01 * x1 * x2

#Superfície ondulada com senos; maximizar
def funcao_seno(x1, x2):
    return x1 * np.sin(4 * np.pi * x1) - x2 * np.sin(4 * np.pi * x2 + np.pi) + 1

