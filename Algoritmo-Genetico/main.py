from SRC.AlgoritmoGenetico import AlgoritmoGenetico
import numpy as np
import matplotlib.pyplot as plt

def funcao(n):
    return -n**2 + 5
def main():
    start = AlgoritmoGenetico(x_min = 0, x_max=10, tamanhoPopulacao = 10, n_geracoes = 1000, taxa_mutacao = 0.2, taxa_crossover = 0.1, funcao=funcao)
    print(start.populacao)
    melhor_aptidao = []
    aptidao_media = []
    geracoes = []
    for n in range(start.n_geracoes):
        new_pop = []
        while len(new_pop) <= start.tamanhoPopulacao:
            individuos = start.selecionar()
            filhos = start.cruzamento(individuos[0], individuos[1])
            filhos_final = start.mutacao(filhos)
            for a in range(2):
                new_pop.append(filhos_final[a])
        start.populacao = new_pop
        melhor_aptidao.append(max(start.funcaoObjetivo()))
        aptidao_media.append(sum(new_pop)/len(new_pop))
        geracoes.append(n)

    print(start.populacao)
    plt.plot(geracoes, melhor_aptidao, label = "Melhor Aptidão")
    plt.plot(geracoes, aptidao_media, label = "Aptidão Média")
    plt.title("Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Aptidão")
    plt.legend()
    plt.show()
    return 0

if __name__ == '__main__':
    main()
