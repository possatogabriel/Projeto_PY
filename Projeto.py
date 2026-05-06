import random

cartas = []
jogador_1 = []
jogador_2 = []
monte_empate = []

# Isso aqui puxa as cartas do TXT, precisa chamar
# DETALHE >> IMPORTANTE <<: Além do mesmo nome, o TXT precisa estar na mesma pasta do .py
def gerar_cartas():
    lista = open("Cartas.txt", "r", encoding="utf-8") 
    linhas = lista.readlines()
    lista.close()

    carta = []

    for linha in linhas:
        linha = linha.strip() 

        if not linha:
            continue

        partes = linha.split(":")
        if len(partes) > 1:
            valor = partes[1].strip()

            if valor.isdigit():
                carta.append(int(valor))
            else:
                carta.append(valor)    

        if len(carta) == 7:
            cartas.append(carta)
            carta = []

# Isso aqui distribui as cartas entre os jogadores depois de, obviamente, puxar as cartas do TXT, precisa chamar também (sim, as cartas são aleatórias)
def distribuir_cartas():
    random.shuffle(cartas)

    for i in range(6):
        jogador_1.append(cartas[i])

    for j in range(6, 12):
        jogador_2.append(cartas[j])

# É o poder de decisão do "bot" (caso o jogador escolha jogar sozinho), precisa chamar se ele optar por isso
def escolher_atributo():
    carta = jogador_2[0]
    valores = carta[2:7]
    maximo = max(valores)

    # DETALHE >> IMPORTANTE <<: Aqui ele retorna o ÍNDICE do valor que ele escolheu, não o próprio valor (então, ele retorna, por exemplo, "1" e não "Sangue", que é o valor do índice 1)
    if (maximo <= 4):
        return 1
    else:
        return valores.index(maximo) + 2

# É a comparação com o atributo "elemento" que é diferente (por ser string e por ser coisa relacionada ao mundo de Ordem)
# Caso você precise chamar, esse código, em teoria, deveria funcionar considerando que o "elemento_1" seria o valor do índice 1 do jogador da rodada atual (então, tanto faz ser o jogador_2 ou o jogador_1), enquanto o elemento_2 seria do adversário -> mais pra frente eu mostro como acessar esses valores se você não souber
def comparar_elementos(elemento_1, elemento_2):
    regras = [
        ["Sangue", "Conhecimento"],
        ["Conhecimento", "Energia"],
        ["Energia", "Morte"],
        ["Morte", "Sangue"]
    ]

    # DETALHE >> IMPORTANTE <<: Já aqui ele retorna o PRÓPRIO VALOR que ganharia, então, se precisar chamar, sai "Sangue", "Morte" etc.
    for regra in regras:
        if (elemento_1 == regra[0] and elemento_2 == regra[1]):
            return elemento_1
        if (elemento_2 == regra[0] and elemento_1 == regra[1]):
            return elemento_2
            
        return "EMPATE"
    
# É a comparação comum entre os valores (e o mesmo vale aqui, o valor_1 pode ser do jogador_1 ou do jogador_2, não importa, considerei apenas que seria o valor do jogador atual da rodada e do seu adversário, respectivamente)
def comparar_valores(valor_1, valor_2):

    # DETALHE >> IMPORTANTE <<: Aqui ele também retorna o PRÓPRIO VALOR do atributo, então vai sair algo tipo "10", "8" etc.
    if (valor_1 > valor_2):
        return valor_1
    elif (valor_2 > valor_1):
        return valor_2
    else:
        return "EMPATE"
    
# A função que faz as comparações (>> IMPORTANTE <<: o "valor_vencedor" é o valor que você recebe ou do "comparar_valores" ou do "comparar_elementos", dependendo do atributo que foi escolhido) -> além disso, o atributo é o ÍNDICE do atributo que venceu, que só é usado pra poder printar essa linha ai de "RESULTADO: " -> já o jogador_1 e o jogador_2 são as listas das cartas dos, bom, jogador_1 ou jogador_2 (looool)
def determinar_rodada(valor_vencedor, atributo, jogador_1, jogador_2):
    print(f"\n{jogador_1[0][0]} ({jogador_1[0][atributo]}) VS. {jogador_2[0][0]} ({jogador_2[0][atributo]})")

    # DETALHE >> IMPORTANTE <<: os índices tão certos, ok? O índice do "Elemento", por exemplo, é 1 mesmo, índice 0 é o nome das cartas (como dá pra ver ai e na função "menu" lá embaixo)
    if (valor_vencedor == jogador_1[0][atributo]):
        print(f"\n> RESULTADO: JOGADOR 1 ({jogador_1[0][0]}) VENCEU!")

        # Só pelo bem do entendimento, irei explicar o que isso aqui tudo faz:
        # A ideia do Supertrunfo, de acordo com o Felipe, é que, se empatar essa rodada, você e seu adversário deixam a carta de lado até um de vocês vencer e o vencedor pegar todas as cartas que estavam de lado (até as do adversário) pra colocar no monte dele -> é isso que esse "for c..." faz
        for c in monte_empate:
            jogador_1.append(c)

        # Como, nesse caso, o jogador_1 venceu, ele pega a carta que o adversário dele tava usando (a do topo também) pra ele e coloca no final do baralho
        jogador_1.append(jogador_2[0])
        # Seguindo nessa lógica, a brincadeira é que você pega a carta do topo e escolhe um atributo pra comparar. Independente se você vencer ou não, você coloca essa carta no final do seu baralho
        jogador_1.append(jogador_1[0])

        # Ai aqui só remove mesmo as cartas (pro jogador_1 só remove pra colocar ela de volta no final, e do jogador_2 remove porque ele perdeu a carta mesmo)
        jogador_1.pop(0)
        jogador_2.pop(0)
    elif (valor_vencedor == jogador_2[0][atributo]):
        print(f"\n>RESULTADO: JOGADOR 2 ({jogador_2[0][0]}) VENCEU!")

        # A lógica é a mesma aqui, só que ao contrário
        for c in monte_empate:
            jogador_2.append(c)

        jogador_2.append(jogador_1[0])
        jogador_2.append(jogador_2[0])
        jogador_2.pop(0)
        jogador_1.pop(0)
    else:
        print(f"\n> RESULTADO: {valor_vencedor}")

        # Esse bloco aqui basicamente faz o que eu falei: quanto dá empate, os dois jogadores deixam a carta de lado num mesmo monte
        monte_empate.append(jogador_1[0])
        monte_empate.append(jogador_2[0])
        # Aqui só remove as cartas da lista de ambos jogadores
        jogador_1.pop(0)
        jogador_2.pop(0)

        # E isso aqui: eu tive a grande sorte de testar uma vez e, nessa brincadeira, conseguir empatar TODAS as cartas, o que significa que o jogo, em teoria, acabou? Já que todas as cartas ficaram de lado? Então só resolvi que, se isso acontecer, basicamente tem que embaralhar as cartas de novo e continuar (resetar o jogo sem anunciar um vencedor)
        if (len(monte_empate) == 12):
            random.shuffle(monte_empate)
            meio = len(monte_empate) // 2

            jogador_1 = monte_empate[meio:]
            jogador_2 = monte_empate[:meio]

# A função que determina o vencedor (o jogo acaba quando um dos jogadores pegar todas as cartas do adversário pra ele mesmo)
def determinar_vencedor():
    if (len(jogador_1) == 0):
        print("\nVENCEDOR: JOGADOR 1!")
    elif (len(jogador_2) == 0):
        print("\nVENCEDOR: JOGADOR 2!")

# Isso aqui é >> SÓ UM EXEMPLO << de duas coisas: como pegar os valores de um item específico de uma carta específica (então, nesse caso, por exemplo, no "Elemento", você tá acessando a primeira carta (jogador[0]) E ENTÃO o atributo 1 dela (jogador[0][1]) + como poderia ficar a visualização dos jogadores 
def menu(jogador):
    print(f"""\n -- CARTA: {jogador[0][0]} -- 
          
1. Elemento: {jogador[0][1]}
2. Força: {jogador[0][2]}
3. Agilidade: {jogador[0][3]}
4. Intelecto: {jogador[0][4]}
5. Vigor: {jogador[0][5]}
6. Presença: {jogador[0][6]}
""")
    
int(input("\nQual atributo você escolhe? "))

# Enfim, é isso amigo, qualquer coisa, sabes onde me encontrar (emoji de piscadela safada)