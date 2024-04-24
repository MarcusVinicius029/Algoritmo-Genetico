import numpy as np
class AlgoritmoGenetico():
    def __init__(self, x_min, x_max, tamanhoPopulacao, n_geracoes, taxa_mutacao, taxa_crossover, funcao):
        self.x_min = x_min
        self.x_max = x_max
        self.tamanhoPopulacao = tamanhoPopulacao
        self.n_geracoes = n_geracoes
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.populacao = self.gerar_populacao()
        self.funcao = funcao

    def codificar(self, n_int):
        if type(n_int) == list:
            if type(n_int[0]) == int:
                n_bin = []
                for n in range(len(n_int)):
                    n_bin.append(bin(n_int[n]).replace("0b","-" if n_int[n] < 0 else "+"))
                return n_bin
            elif type(n_int[0]) == float:
                n_bin = []
                for n in range(len(n_int)):
                    bin_string = str(n_int[n])
                    posicao = bin_string.find(".")
                    if posicao == -1:
                        n_bin.append(bin(n_int[n]).replace("0b", "-" if n_int[n] < 0 else "+"))
                    else:
                        direita = int(bin_string[0: posicao])
                        esquerda = int(bin_string[posicao + 1:])
                        new_sring = bin(direita).replace("0b", "-" if n_int[n] < 0 else "+") + "." + bin(esquerda).replace("0b", "")
                        n_bin.append(new_sring)
                return n_bin
            elif type(n_int[0]) == str:
                n_bin = []
                for n in range(len(n_int)):
                    n_bin.append(bin(int("".join(n_int[n]))).replace("0b", "-" if n_int < 0 else "+"))
                return n_bin
        elif type(n_int) == int:
            return bin(n_int).replace("0b",'-' if n_int < 0 else "+")
        elif type(n_int) == float:
            bin_string = str(n_int)
            posicao = bin_string.find(".")
            direita = int(bin_string[0: posicao])
            esquerda = int(bin_string[posicao + 1:])
            new_sring = bin(direita).replace("0b", "-" if n_int < 0 else "+") + "." + bin(esquerda).replace("0b", "")
            n_bin = new_sring
            return n_bin
        elif type(n_int) == str:
            bin_string = n_int
            posicao = bin_string.find(".")
            direita = int(bin_string[0: posicao])
            esquerda = int(bin_string[posicao + 1:])
            new_sring = bin(direita).replace("0b", "-" if n_int < 0 else "+") + "." + bin(esquerda).replace("0b", "")
            n_bin = new_sring
            return n_bin

    def decodificar(self, n_bin):

        if type(n_bin) == list:
            if type(n_bin[0]) == str:
                n_int = []
                for n in range(len(n_bin)):
                    numero = str(n_bin[n])
                    posicao = numero.find(".")
                    if posicao == -1:
                        n_int.append(int(n_bin[n], 2))
                    else:
                        direito = numero[0: posicao]
                        esquerdo = numero[posicao + 1:]
                        int_direiro = str(int(direito, 2))
                        int_esquerdo = str(int(esquerdo, 2))
                        new_numero = int_direiro + "." + int_esquerdo
                        n_int.append(float(new_numero))
                return n_int
        elif type(n_bin) == str:
            posicao = n_bin.find(".")
            direita = n_bin[0: posicao]
            esquerda = n_bin[posicao + 1: ]
            int_string = str(int(direita)) + "." + str(int(esquerda))
            return float(int_string)
        
    def gerar_populacao(self):
        pop = []
        for n in range(self.tamanhoPopulacao):
            pop.append(round(np.random.uniform(self.x_min, self.x_max), 2))
        return pop
    
    def funcaoObjetivo(self):
        resultados = []
        for n in range(len(self.populacao)):
            resultados.append(self.funcao(self.populacao[n]))
        return resultados
    
    def ajustar(self, individuo):
        if individuo <= self.x_min:
            return self.x_min
        elif individuo >= self.x_max:
            return self.x_max
        else:
            return individuo

    def mutacao(self, individuo):
        n = round(np.random.uniform(0.1, 10), 2)
        individuo_bin = self.codificar(individuo)
        if n <= self.taxa_mutacao:
            ponto_corte = np.random.randint(0, len(individuo_bin))
            new_individuo = list(individuo_bin)
            if new_individuo[ponto_corte] == "0":
                new_individuo[ponto_corte] = "1"
            elif new_individuo[ponto_corte] == "1":
                new_individuo[ponto_corte] = "0"
            value = "".join(new_individuo)
            new_individuo = self.decodificar(value)
            return self.ajustar(new_individuo)
        else: 
            return self.ajustar(individuo)

    def cruzamento(self, pai, mae):
        n = np.random.randint(0, 100)
        if n <= self.taxa_crossover:
            bin_pai = self.codificar(pai)
            bin_mae = self.codificar(mae).ljust(30, '0')
            ponto_corte = np.random.randint(0, len(bin_pai) - 1)
            filho = bin_pai[0:ponto_corte] + bin_mae[ponto_corte + 1:]
            int_filho = self.decodificar(filho)
            return self.ajustar(int_filho)
        else:
            return pai

    def selecionar(self):
        individuos_selecionados = []
        for n in range(0, 2):    
            roleta = []
            faixa_inicio = 0

            for valor, probabilidade in zip(self.populacao, self.funcaoObjetivo()):
                faixa_fim = faixa_inicio + probabilidade
                roleta.append((faixa_inicio, faixa_fim, valor))
                faixa_inicio = faixa_fim
            ponto_selecionado = np.random.uniform(0, faixa_inicio)
            for faixa_inicio, faixa_fim, valor in roleta:
                if faixa_inicio <= ponto_selecionado < faixa_fim:
                    individuos_selecionados.append(valor)
                    
        return individuos_selecionados

