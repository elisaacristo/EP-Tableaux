# Testes

# Teste: Modus Ponens
Sequente: P => Q, P, conclusion = Q

Resultado: VÁLIDO

Regras aplicadas: [('β→', 'T P => Q')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: Modus Tollens
Sequente: P => Q, ¬Q, conclusion = ¬P

Resultado: VÁLIDO

Regras aplicadas: [('α¬', 'T ¬Q'), ('β¬', 'F ¬P'), ('β→', 'T P => Q')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: Silogismo disjuntivo
Sequente: P v Q, ¬P, conclusion = Q

Resultado: VÁLIDO

Regras aplicadas: [('α¬', 'T ¬P'), ('β∨', 'T P v Q')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: Silogismo hipotético
Sequente: P => Q, Q => R, conclusion = P => R

Resultado: VÁLIDO

Regras aplicadas: [('α→', 'F P => R'), ('β→', 'T P => Q'), ('β→', 'T Q => R')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: De Morgan
Sequente: ¬(P v Q), conclusion = ¬P ^ ¬Q

Resultado: VÁLIDO

Regras aplicadas: [('α¬', 'T ¬(P v Q)'), ('α∨', 'F P v Q'), ('β∧', 'F ¬P ^ ¬Q'), ('β¬', 'F ¬P'), ('β¬', 'F ¬Q')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: P >> Q |- P >> (Q | R)
Sequente: P => Q, conclusion = P => (Q v R)

Resultado: VÁLIDO

Regras aplicadas: [('α→', 'F P => (Q v R)'), ('α∨', 'F Q v R'), ('β→', 'T P => Q')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: Fórmula do demo (sem premissas)
Sequente: conclusion = (P => (Q => R)) v (Q => (P v R))

Resultado: VÁLIDO

Regras aplicadas: [('α∨', 'F (P => (Q => R)) v (Q => (P v R))'), ('α→', 'F P => (Q => R)'), ('α→', 'F Q => (P v R)'), ('α→', 'F Q => R'), ('α∨', 'F P v R')]

Pela tabela verdade é válido? (Código Professora): True

# Teste: Afirmação do consequente
Sequente: P => Q, Q, conclusion = P

Resultado: INVÁLIDO

Contraexemplo: {'Q': True, 'P': False}

Regras aplicadas: [('β→', 'T P => Q')]

Pela tabela verdade é válido? (Código Professora): False

# Teste: Negação do antecedente
Sequente: P => Q, ¬P, conclusion = ¬Q

Resultado: INVÁLIDO

Contraexemplo: {'P': False, 'Q': True}

Regras aplicadas: [('α¬', 'T ¬P'), ('β¬', 'F ¬Q'), ('β→', 'T P => Q')]

Pela tabela verdade é válido? (Código Professora): False

# Teste: Disjunção implica conjunção
Sequente: P v Q, conclusion = P ^ Q

Resultado: INVÁLIDO

Contraexemplo: {'P': True, 'Q': False}

Regras aplicadas: [('β∨', 'T P v Q'), ('β∧', 'F P ^ Q')]

Pela tabela verdade é válido? (Código Professora): False
