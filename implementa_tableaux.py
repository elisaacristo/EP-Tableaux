# Usa as classes do code_base da professora (Variable, Not, And, Or, Implies)
from code_base_EP1 import *


def expandir(marca, f):
    
    # Devolve o tipo da regra (alfa ou beta), o nome da regra e as fórmulas novas:
    # (Na alfa todas fórmulas vão para o mesmo ramo, na beta cada uma abre um ramo)
    
    filhos = f.children
    
    if isinstance(f, Not):
        if marca == "T":
            return "alfa", "α¬", [("F", filhos[0])]
        else:
            return "alfa", "β¬", [("T", filhos[0])]
    
    if isinstance(f, And):
        if marca == "T":
            return "alfa", "α∧", [("T", c) for c in filhos]
        else:
            return "beta", "β∧", [("F", c) for c in filhos]
    
    if isinstance(f, Or):
        if marca == "F":
            return "alfa", "α∨", [("F", c) for c in filhos]
        else:
            return "beta", "β∨", [("T", c) for c in filhos]
    
    if isinstance(f, Implies):
        if marca == "F":
            return "alfa", "α→", [("T", filhos[0]), ("F", filhos[1])]
        else:
            return "beta", "β→", [("F", filhos[0]), ("T", filhos[1])]


def fechou(ramo):
    # O ramo fecha se tem o mesmo átomo com T e com F
    for marca1, f1 in ramo:
        for marca2, f2 in ramo:
            if isinstance(f1, Variable) and isinstance(f2, Variable):
                if f1.name == f2.name and marca1 != marca2:
                    return True
    return False


def provador_tableaux(premissas, conclusao):
    # Premissas com T e conclusão com F
    ramo = []
    for p in premissas:
        ramo.append(("T", p))
    ramo.append(("F", conclusao))

    pilha_ramos = [ramo]
    historico = []

    while len(pilha_ramos) > 0:
        ramo = pilha_ramos.pop()

        if fechou(ramo):
            continue

        # Escolhe a fórmula pra expandir, isto é, alfa primeiro, para não bifurcar antes da hora
        escolhida = -1
        for i in range(len(ramo)):
            marca, f = ramo[i]
            if isinstance(f, Variable):
                continue
            if expandir(marca, f)[0] == "alfa":
                escolhida = i
                break
            if escolhida == -1:
                escolhida = i

        # Caso não sobre nada para expandir e o ramo esteja aberto, achamos um contraexemplo
        if escolhida == -1:
            contraexemplo = {}
            for marca, f in ramo:
                contraexemplo[f.name] = (marca == "T")
            return False, contraexemplo, historico

        marca, f = ramo.pop(escolhida)
        tipo, regra, novas = expandir(marca, f)
        historico.append((regra, marca + " " + str(f)))

        if tipo == "alfa":
            pilha_ramos.append(ramo + novas)
        else:
            # Empilha ao contrário pra expandir o ramo da esquerda primeiro
            for nova in reversed(novas):
                pilha_ramos.append(ramo + [nova])

    # Caso todos os ramos se fechem
    return True, None, historico