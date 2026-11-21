# TESTES

from implementa_tableaux import Var, Nao, E, Ou, Implica, provador_tableaux

def rodar_teste(nome, premissas, conclusao):
    print(f"\n{'='*40}")
    print(f"Teste: {nome}")
    print(f"Sequente: {[str(p) for p in premissas]} |- {conclusao}")
    print(f"{'-'*40}")
    
    valido, contraexemplo, historico = provador_tableaux(premissas, conclusao)
    
    if valido:
        print("RESULTADO: Sequente VÁLIDO (Tautologia/Teorema)")
        print("Todos os ramos fecharam.")
        print("\nSequência de regras aplicadas [(regra, fórmula), ...]:")
        print(historico)
    else:
        print("RESULTADO: Sequente INVÁLIDO")
        print("Contraexemplo encontrado no ramo aberto e saturado:")
        for atomo, valor in contraexemplo.items():
            print(f"  {atomo} = {valor}")
        
        print("\nSequência de regras aplicadas até o ramo aberto [(regra, fórmula), ...]:")
        print(historico)

# TESTES ---------------------------------------------------------

p = Var("p")
q = Var("q")
r = Var("r")

# 1. Modus Ponens: p >> q, p |- q  (VÁLIDO)
premissas_1 = [Implica(p, q), p]
conclusao_1 = q
rodar_teste("Modus Ponens", premissas_1, conclusao_1)

# 2. Modus Erronens (Falácia da afirmação do consequente): p >> q, q |- p  (INVÁLIDO)
premissas_2 = [Implica(p, q), q]
conclusao_2 = p
rodar_teste("Falácia da Afirmação do Consequente", premissas_2, conclusao_2)

# 3. Lei de De Morgan 1: ~(p | q) |- ~p & ~q (VÁLIDO)
premissas_3 = [Nao(Ou(p, q))]
conclusao_3 = E(Nao(p), Nao(q))
rodar_teste("De Morgan 1", premissas_3, conclusao_3)

# 4. Exemplo aleatório inválido: p | q |- p & q (INVÁLIDO)
premissas_4 = [Ou(p, q)]
conclusao_4 = E(p, q)
rodar_teste("Disjunção implicando Conjunção", premissas_4, conclusao_4)

# 5. Teste extraído das notas: p -> q |- p -> (q V r) (VÁLIDO)
premissas_5 = [Implica(p, q)]
conclusao_5 = Implica(p, Ou(q, r))
rodar_teste("Exercício das Notas (p -> q |- p -> q V r)", premissas_5, conclusao_5)
