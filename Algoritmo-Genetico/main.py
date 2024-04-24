from SRC.AlgoritmoGenetico import AlgoritmoGenetico
import numpy as np
import matplotlib.pyplot as plt

def funcao(n):
    return round(n**2)

def main():
    start = AlgoritmoGenetico(x_min = 0, x_max=10, tamanhoPopulacao = 5, n_geracoes = 25, taxa_mutacao = 1, taxa_crossover = 50, funcao=funcao)
    print(start.populacao)
    aptidao_melhor = []
    aptidao_media = []
    geracoes = []
    for n in range(start.n_geracoes):
        new_pop = []
        while len(new_pop) <= start.tamanhoPopulacao:
            individuos = start.selecionar()
            filho = start.cruzamento(individuos[0], individuos[1])
            filho_final = start.mutacao(filho)
            new_pop.append(filho_final)
        start.populacao = new_pop
        aptidao_melhor.append(max(start.populacao))
        aptidao_media.append(sum(new_pop)/len(new_pop))
        geracoes.append(n)

    print(start.populacao)
    plt.plot(geracoes, aptidao_melhor, label = "Melhor Aptidão")
    plt.plot(geracoes, aptidao_media, label = "Aptidão Média")
    plt.title("Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Aptidão")
    plt.legend()
    plt.show()
    return 0

if __name__ == '__main__':
    main()
