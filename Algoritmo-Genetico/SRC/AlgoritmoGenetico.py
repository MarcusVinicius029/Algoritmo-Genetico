import numpy as np
class AlgoritmoGenetico():
    """
    Implementação de um Algoritmo Genético para otimização de funções.
    """
    def __init__(self, x_min, x_max, tamanhoPopulacao, n_geracoes, taxa_mutacao, taxa_crossover, funcao):
        """
        Inicializa um objeto AlgoritmoGenetico.

        Args:
            x_min (float): Valor mínimo do intervalo de busca.
            x_max (float): Valor máximo do intervalo de busca.
            tamanhoPopulacao (int): Tamanho da população de indivíduos.
            n_geracoes (int): Número de gerações para a evolução da população.
            taxa_mutacao (float): Taxa de mutação dos indivíduos.
            taxa_crossover (float): Taxa de crossover entre os indivíduos.
            funcao (function): Função objetivo que o algoritmo visa otimizar.
        """        
        
        self.x_min = x_min
        self.x_max = x_max
        self.tamanhoPopulacao = tamanhoPopulacao
        self.n_geracoes = n_geracoes
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.populacao = self.gerar_populacao()
        self.funcao = funcao

    def codificar(self, n_int):
        """
        Codifica um número inteiro ou uma lista de números em formato binário.

        Args:
            n_int (int, float, list): Número inteiro, número de ponto flutuante ou lista de números.

        Returns:
            str or list: String binária representando o número ou lista de strings binárias.
        """        
        list_bin = []
        if type(n_int) == list:
            for n in range(len(n_int)):
                n_str = str(n_int[n])
                posicao = n_str.find(".")
                if posicao != -1: 
                    esquerda = n_str[0:posicao]
                    direita = n_str[posicao + 1:]
                    esquerdo_bin = bin(int(esquerda)).replace("0b", "0")
                    direita_bin = bin(int(direita)).replace("0b", "0")
                    n_bin = esquerdo_bin + "." + direita_bin
                    list_bin.append(n_bin.ljust(30, "0"))
                else:
                    n_bin = bin(int(n_str)).replace("0b", "0") + "." + "0"
                    list_bin.append(n_bin.ljust(30, "0"))
        elif type(n_int)  == int:
            n_bin = bin(n_int).replace("0b", "0") + "." + "0"
            return n_bin.ljust(30, "0")
        elif type(n_int) == float:
            n_str = str(n_int)
            posicao = n_str.find(".")
            esquerda = n_str[0:posicao]
            direita = n_str[posicao + 1:]
            esquerdo_bin = bin(int(esquerda)).replace("0b", "0")
            direita_bin = bin(int(direita)).replace("0b", "0")
            n_bin = esquerdo_bin + "." + direita_bin
            return n_bin.ljust(30, "0")
        return list_bin

    def decodificar(self, n_bin):
        """
        Decodifica uma string binária em um número inteiro ou de ponto flutuante.

        Args:
            n_bin (str or list): String binária ou lista de strings binárias.

        Returns:
            int, float or list: Número inteiro, número de ponto flutuante ou lista de números decodificados.
        """        
        list_int = []
        if type(n_bin) == list:
            for n in range(len(n_bin)):
                n_str = str(n_bin[n])
                posicao = n_str.find(".")
                if posicao != -1:
                    esquerda = str(int(n_str[0: posicao], 2))
                    direita = str(int(n_str[posicao+1:], 2))
                    n_int = esquerda + "." + direita
                    list_int.append(float(n_int))
        elif type(n_bin) == str:
            posicao = n_bin.find(".")
            esquerda = str(int(n_bin[0: posicao], 2))
            direita = str(int(n_bin[posicao+1:], 2))
            if direita.find("-") == -1:
                n_int = esquerda + "." + direita
            else: 
                new_direita = direita.replace("-", "")
                n_int = esquerda + "." + new_direita
            return float(n_int)
        elif type(n_bin) == float:
            n_str = str(n_bin)
            posicao = n_str.find(".")
            esquerda = str(int(n_str[0: posicao], 2))
            direita = str(int(n_str[posicao+1:], 2))
            n_int = esquerda + "." + direita
            return float(n_int)       
        return list_int
        
    def gerar_populacao(self):
        """
        Gera uma população inicial de indivíduos.

        Returns:
            list: Lista de indivíduos gerados.
        """
        pop = []
        for n in range(self.tamanhoPopulacao):
            pop.append(round(np.random.uniform(self.x_min, self.x_max), 2))
        return pop
    
    def funcaoObjetivo(self):
        """
        Calcula o valor da função objetivo para cada indivíduo da população.

        Returns:
            list: Lista contendo o valor da função objetivo para cada indivíduo.
        """
        resultados = []
        for n in range(len(self.populacao)):
            resultados.append(self.funcao(self.populacao[n]))
        return resultados
    
    def ajustar(self, individuo):
        """
        Ajusta o valor de um indivíduo para garantir que esteja dentro dos limites especificados.

        Args:
            individuo (int or float): Indivíduo a ser ajustado.

        Returns:
            int or float: Indivíduo ajustado.
        """
        if individuo <= self.x_min:
            return self.x_min
        elif individuo >= self.x_max:
            return self.x_max
        else:
            return individuo

    def mutacao(self, individuos):
        """
        Realiza a mutação em uma lista de indivíduos.

        Args:
            individuos (list): Lista de indivíduos a serem mutados.

        Returns:
            list: Lista de indivíduos mutados.
        """
        n = round(np.random.uniform(0.01, 1), 2)
        individuo_bin = self.codificar(individuos)
        individuos_mutados = []
        if n <= self.taxa_mutacao:
            for n in range(2):
                ponto_corte = np.random.randint(0, len(individuo_bin))
                new_individuo = list(individuo_bin[n])
                if new_individuo[ponto_corte] == "0":
                    new_individuo[ponto_corte] = "1"
                elif new_individuo[ponto_corte] == "1":
                    new_individuo[ponto_corte] = "0"
                value = "".join(new_individuo)
                new_individuo = self.decodificar(value)
                individuos_mutados.append(self.ajustar(new_individuo))
            return individuos_mutados
        else: 
            return individuos

    def cruzamento(self, pai, mae):
        """
        Realiza o cruzamento entre dois indivíduos para produzir filhos.

        Args:
            pai: Indivíduo pai.
            mae: Indivíduo mãe.

        Returns:
            list: Lista contendo os filhos gerados.
        """
        n = np.random.randint(0.01, 1)
        filhos = []
        if n <= self.taxa_crossover:
            for n in range(2): 
                bin_pai = self.codificar(pai)
                bin_mae = self.codificar(mae)

                posicao_pai = bin_pai.find(".")
                posicao_mae = bin_mae.find(".")

                new_bin_pai = bin_pai[:posicao_pai]
                new_bin_mae = bin_mae[:posicao_mae]

                ponto_corte = np.random.randint(0, len(bin_pai))

                filho = new_bin_pai[:ponto_corte] + new_bin_mae[ponto_corte:] + "." "0"

                int_filho = self.decodificar(filho)
                filhos.append(self.ajustar(int_filho))
            return filhos
        else:
            filhos = [pai, mae]
            return filhos

    def selecionar(self):
        """
        Seleciona indivíduos da população com base em sua aptidão para a reprodução.

        Returns:
            list: Lista de indivíduos selecionados.
        """
        aptidoes = self.funcaoObjetivo()
        n = sum(aptidoes)
        posicao_individuos = [sum(aptidoes[0:i]) for i in range(len(self.populacao))]
        resultado = []
        for j in range(2):
            posicao_sorteada = np.random.uniform(0, n)
            for i in range(len(self.populacao)):
                if (i + 1) < len(self.populacao):
                    if  posicao_sorteada >= posicao_individuos[i] and posicao_sorteada < posicao_individuos[i + 1]:
                        c = resultado.count(self.populacao[i])
                        if c == 0:
                            resultado.append(self.populacao[i])
                            break
                else:
                    resultado.append(self.populacao[-1])

        return resultado

