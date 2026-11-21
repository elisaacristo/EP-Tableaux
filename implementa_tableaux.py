# IMPLEMENTAÇÃO

# def: função. ex: def tipo_regra(marca, f):
# class: classe. criar objetos
# self: representa o próprio objeto criado
# __init__: roda no instante em que criamos um objeto
# __str__: como o objeto aparece como texto quando usamos print()

class Var:
    # Átomo proposicional: p, q
    def __init__(self, atomo):
        self.atomo = atomo
    def __str__(self):
        return self.atomo

# f = fórmula

class Nao:
    # Negação de uma fórmula: ~A
    def __init__(self, f):
        self.f = f
    def __str__(self):
        return f"~({self.f})"

# Nos conectivos binários (que ligam duas fórmulas), usamos e para o lado esquerdo e d para o lado direito

class E:
    # Conjunção: A & B
    def __init__(self, e, d):
        self.e = e
        self.d = d
    def __str__(self):
        return f"({self.e} & {self.d})"

class Ou:
    # Disjunção: A | B
    def __init__(self, e, d):
        self.e = e
        self.d = d
    def __str__(self):
        return f"({self.e} | {self.d})"

class Implica:
    # Implicação: A >> B
    def __init__(self, e, d):
        self.e = e
        self.d = d
    def __str__(self):
        return f"({self.e} >> {self.d})"

# Exemplo das classes acima: 
# Entrada: Implica(p, q) - guarda p na esquerda e q na direita
# Saída: (p >> q) - formatado com __str__ e printado

class Ramo:
    # Um tableau é uma árvore formada por vários ramos
    # Essa classe é um desses caminhos e guarda o estado dele até o momento
    def __init__(self):
        self.formulas = [] # Lista de fórmulas ('T'/'F', formula)
        self.atomos_T = set()
        self.atomos_F = set()
        self.historico = [] # Lista das regras aplicadas (regra_aplicada, formula)

    def copia(self):
        # Cria um clone do ramo atual (importante para regra beta que precisamos bifurcar)
        novo = Ramo()
        novo.formulas = list(self.formulas)
        novo.atomos_T = set(self.atomos_T)
        novo.atomos_F = set(self.atomos_F)
        novo.historico = list(self.historico)
        return novo

    def fechou(self):
        # Retorna True se há o mesmo átomo marcado como T e F
        return len(self.atomos_T.intersection(self.atomos_F)) > 0


def tipo_regra(marca, f):
    # Retorna se a expansão da fórmula será alfa, beta ou átomo.
    if isinstance(f, Var): return "átomo"
    if isinstance(f, Nao): return "alfa" # Não bifurca, então priorizamos junto com as alfas
    if isinstance(f, E): return "alfa" if marca == "T" else "beta"
    if isinstance(f, Ou): return "beta" if marca == "T" else "alfa"
    if isinstance(f, Implica): return "beta" if marca == "T" else "alfa"
    return "átomo"


def provador_tableaux(premissas, conclusao):
    """
    Tenta provar a validade do sequente.
    Retorna (True, None, historico) se válido.
    Retorna (False, contraexemplo, historico) se inválido.
    """
    ramo_inicial = Ramo()
    
    # 1. Coloca as premissas como "T" e a conclusão como "F" na raiz (refutação)
    for p in premissas:
        ramo_inicial.formulas.append(("T", p))
    ramo_inicial.formulas.append(("F", conclusao))
    
    pilha_ramos = [ramo_inicial]
    historico_geral = []

    while pilha_ramos:
        # Enquanto ainda existir algum ramo aberto na pilha, continua rodando
        ramo = pilha_ramos.pop()
        
        # Processa todos os átomos que caíram soltos na lista
        formulas_pendentes = []
        for marca, form in ramo.formulas:
            if isinstance(form, Var):
                if marca == "T": ramo.atomos_T.add(form.atomo)
                else: ramo.atomos_F.add(form.atomo)
            else:
                formulas_pendentes.append((marca, form))
        ramo.formulas = formulas_pendentes

        if ramo.fechou():
            continue # Ramo com contradição, podemos descartar e tentar o próximo

        if not ramo.formulas:
            # Se não tem mais fórmulas para expandir e não fechou, o ramo está saturado e aberto
            # Encontramos um contraexemplo
            contraexemplo = {a: "True" for a in ramo.atomos_T}
            contraexemplo.update({a: "False" for a in ramo.atomos_F})
            return False, contraexemplo, ramo.historico

        # Estratégia: Seleção alfa-primeiro, para evitar bifurcar antes da hora
        idx_alvo = 0
        for i, (m, f) in enumerate(ramo.formulas):
            if tipo_regra(m, f) == "alfa":
                idx_alvo = i
                break # Se achou alfa, para e usa ela
        
        marca, form = ramo.formulas.pop(idx_alvo)
        form_str = f"{marca} {form}"

        # REGRAS DE EXPANSÃO --------------------------------------------------
        
        if isinstance(form, Nao):
            # Regras de Negação (T~ é α¬, F~ é β¬, nenhuma bifurca)
            nova_marca = "F" if marca == "T" else "T"
            regra = "α¬" if marca == "T" else "β¬"
            ramo.formulas.append((nova_marca, form.f))
            ramo.historico.append((regra, form_str))
            historico_geral.append((regra, form_str))
            pilha_ramos.append(ramo)

        elif isinstance(form, E):
            if marca == "T":
                # Alfa: T(A & B) -> TA, TB
                ramo.formulas.append(("T", form.e))
                ramo.formulas.append(("T", form.d))
                ramo.historico.append(("α&", form_str))
                historico_geral.append(("α&", form_str))
                pilha_ramos.append(ramo)
            else:
                # Beta: F(A & B) -> FA | FB (bifurca)
                ramo_dir = ramo.copia()
                ramo.formulas.append(("F", form.e))
                ramo.historico.append(("β& (esq)", form_str))
                ramo_dir.formulas.append(("F", form.d))
                ramo_dir.historico.append(("β& (dir)", form_str))
                historico_geral.append(("β&", form_str))
                pilha_ramos.append(ramo_dir)
                pilha_ramos.append(ramo)

        elif isinstance(form, Ou):
            if marca == "F":
                # Alfa: F(A | B) -> FA, FB
                ramo.formulas.append(("F", form.e))
                ramo.formulas.append(("F", form.d))
                ramo.historico.append(("α|", form_str))
                historico_geral.append(("α|", form_str))
                pilha_ramos.append(ramo)
            else:
                # Beta: T(A | B) -> TA | TB (bifurca)
                ramo_dir = ramo.copia()
                ramo.formulas.append(("T", form.e))
                ramo.historico.append(("β| (esq)", form_str))
                ramo_dir.formulas.append(("T", form.d))
                ramo_dir.historico.append(("β| (dir)", form_str))
                historico_geral.append(("β|", form_str))
                pilha_ramos.append(ramo_dir)
                pilha_ramos.append(ramo)

        elif isinstance(form, Implica):
            if marca == "F":
                # Alfa: F(A >> B) -> TA, FB
                ramo.formulas.append(("T", form.e))
                ramo.formulas.append(("F", form.d))
                ramo.historico.append(("α>>", form_str))
                historico_geral.append(("α>>", form_str))
                pilha_ramos.append(ramo)
            else:
                # Beta: T(A >> B) -> FA | TB (bifurca)
                ramo_dir = ramo.copia()
                ramo.formulas.append(("F", form.e))
                ramo.historico.append(("β>> (esq)", form_str))
                ramo_dir.formulas.append(("T", form.d))
                ramo_dir.historico.append(("β>> (dir)", form_str))
                historico_geral.append(("β>>", form_str))
                pilha_ramos.append(ramo_dir)
                pilha_ramos.append(ramo)

    # Se a pilha esvaziar e a função não retornou False, é porque todos os ramos fecharam :)
    return True, None, historico_geral