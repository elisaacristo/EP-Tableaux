# Testes do provador de tableaux
from implementa_tableaux import *

P, Q, R, S = vars('P', 'Q', 'R', 'S')

def testar(nome, sequente):
    print("Teste:", nome)
    print("Sequente:", sequente)

    valido, contraexemplo, historico = provador_tableaux(sequente.premises, sequente.conclusion)

    if valido:
        print("Resultado: VÁLIDO")
    else:
        print("Resultado: INVÁLIDO")
        print("Contraexemplo:", contraexemplo)

    print("Regras aplicadas:", historico)
    print("Pela tabela verdade é válido? (Código Professora):", sequente.is_valid_truth_table())
    print()

# Válidos
testar("Modus Ponens", ArgumentForm(P >> Q, P, conclusion=Q))
testar("Modus Tollens", ArgumentForm(P >> Q, ~Q, conclusion=~P))
testar("Silogismo disjuntivo", ArgumentForm(P | Q, ~P, conclusion=Q))
testar("Silogismo hipotético", ArgumentForm(P >> Q, Q >> R, conclusion=P >> R))
testar("De Morgan", ArgumentForm(~(P | Q), conclusion=~P & ~Q))
testar("P >> Q |- P >> (Q | R)", ArgumentForm(P >> Q, conclusion=P >> (Q | R)))
testar("Fórmula do demo (sem premissas)", ArgumentForm(conclusion=(P >> (Q >> R) | (Q >> (P | R)))))

# Inválidos
testar("Afirmação do consequente", ArgumentForm(P >> Q, Q, conclusion=P))
testar("Negação do antecedente", ArgumentForm(P >> Q, ~P, conclusion=~Q))
testar("Disjunção implica conjunção", ArgumentForm(P | Q, conclusion=P & Q))