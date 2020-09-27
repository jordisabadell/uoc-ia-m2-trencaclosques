import sys
import random
sys.setrecursionlimit(1000000)


################################################################################
## FUNCIONS DE SISTEMA

def gensym ():
    """
    Genera un identificador únic. 
    Format: 'symb' + 7 dígits.
    Per exemple, symb8754986
    """
    return 'symb' + str(int(10000000*random.random())).rjust(7,'0')

def car(lst): 
    """
    Donada una llista, retorna el primer element.
    Per exemple: [1,2,3,4] retorna 1
    """
    return ([] if not lst else lst[0])

def cdr(lst): 
    """
    Donada una llista, retorna tots els elements excepte el primer.
    Per exemple: [1,2,3,4] retorna [2,3,4]
    """
    return ([] if not lst else lst[1:]) 

def caar(lst): 
    """
    Donada una llista de llistes, retorna el primer element de la primera
    llista. 
    Per exemple: [[1,2,3,4],[5,6,7,8],[9,10,11,12]] retorna 1
    """
    return car(car(lst))

def cadr(lst): 
    """
    Donada una llista, retorna el segon element.
    Per exemple: [1,2,3,4] retorna 2
    """
    return car(cdr(lst))

def cdar(lst): 
    """
    Donada una llista de llistes, retorna tots els elements de la primera
    llista excepte el primer. 
    Per exemple, [[1,2,3,4],[5,6,7,8],[9,10,11,12]] retorna [2,3,4]
    """
    return cdr(car(lst))

def cddr(lst): 
    """
    Donada una llista, retorna tots els elements excepte el primer i el segon.
    Per exemple: [1,2,3,4] retorna [3,4]
    """
    return cdr(cdr(lst))

def caddr(lst): 
    """
    Donada una llista, retorna el tercer element.
    Per exemple: [1,2,3,4] retorna 3
    """
    return car(cdr(cdr(lst)))

def cdddr(lst): 
    """
    Donada una llista, retorna tots els elements excepte el primer, el segon i
    el tercer.
    Per exemple: [1,2,3,4,5,6] retorna [4,5,6]
    """
    return cdr(cdr(cdr(lst)))

def caadr(lst): 
    """
    Donada una llista de llistes, retorna el primer element de la segona
    llista. 
    Per exemple: [[1,2,3,4],[5,6,7,8],[9,10,11,12]] retorna 5
    """
    return car(car(cdr(lst)))

def cadadr(lst): 
    """
    Donada una llista de llistes, retorna el segon element de la segona
    llista. 
    Per exemple: [[1,2,3,4],[5,6,7,8],[9,10,11,12]] retorna 6
    """
    return car(cdr(car(cdr(lst))))

def cadddr(lst): 
    """
    Donada una llista, retorna el quart element.
    Per exemple: [1,2,3,4,5,6,7,8] retorna 4
    """
    return car(cdr(cdr(cdr(lst))))

def cons(elem, lst):
    tmp = lst.copy()
    tmp.insert(0,elem)
    return tmp

def member_if (prd, lst):
    ll = lst.copy()
    leng = len(lst)
    while (leng > 0):
        elem = ll[0]
        if prd(elem):
            return ll
        ll.pop(0)
        leng -= 1
    return []

def find_if (prd, lst):
    for elem in lst:
        if prd(elem):
            return elem
    return []

def remove_if (prd, lst):
    results = []
    for elem in lst:
        if not prd(elem):
            results.append(elem)
    return results

def mapcar (f, lst):
    return list(map(f,lst))

################################################################################
## ALGORITME DE CERCA

# Funció que a partir del problema i la estratègia, crea l'arbre incial
def fer_cerca (problema, estrategia):
    return cerca(
            problema, 
            estrategia, 
            arbre_inicial(
                estat_inicial(problema), 
                info_inicial(problema)
            )
        )

# Funció recursiva de cerca
def cerca (problema, estrategia, arbre):
    
    # Comprovar si hi ha nodes a expendir dins l'arbre de cerca.
    # En cas de no haver-n'hi retorna fals ('no_hi_ha_solucio')
    if (not candidats(arbre)):
        return ['no_hi_ha_solucio']
    else:
        # Seleccionar node a expendir
        node = selecciona_node(arbre)
        # Eliminar node a expendir de l'arbre
        nou_arbre = elimina_seleccio(arbre)
    
    # Comprovar si el node a expendir seleccionat és la solució.
    if solucio(problema, node):
        # Retornar camí fins a la solució
        return cami(arbre,node)
    else:
        # Cerca recursiva incorporant els nous nodes a l'arbre
        return cerca(problema, estrategia, 
            expandeix_arbre(problema, estrategia, nou_arbre, node))

# Mira si hi ha nodes a expendir dins l'arbre de cerca. En cas de no haver-n'hi, 
# retorna fals.
def candidats(arbre):
    return bool(nodes_a_expandir(arbre))

# Selecciona el node a expendir.
def selecciona_node(arbre):
    return car(nodes_a_expandir(arbre))

# Elimina el node a expendir.
def elimina_seleccio (arbre):
    return cons(cdr(nodes_a_expandir(arbre)), cdr(arbre))

# Comprova si el node seleccionat és la solució.
def solucio(problema, node):
    ff = funcio_objectiu(problema)
    return ff(estat(node))

# Retorna el camí fins al node solució
def cami(arbre,node):
    if not id_pare(node):
        return []
    lp = cami(arbre, node_arbre(id_pare(node), arbre))
    return lp + [operador(node)]

# Calcula l’expansió del node incorporant els nous nodes a l’arbre
def expandeix_arbre (problema, estrategia, arbre, node):
    nous_nodes_a_expandir = expandeix_node(node,
    operadors(problema),
        funcio_info_addicional(problema))
    return construeix_arbre(arbre, estrategia, node, nous_nodes_a_expandir)

def expandeix_node (node, operadors, funcio):
    def elimina_estats_buits (llista_nodes):
        return remove_if(lambda node: estat(node) == 'buit', llista_nodes)
        
    st = estat(node)
    id_node = ident(node)
    info_node = info(node)
    aux = []
    for op in operadors:
        nou_simbol = gensym()
        ff = cadr(op)
        ffapp = ff(st,info_node)
        aux.append(construeix_node(nou_simbol, ffapp, id_node, car(op), 
                    funcio([st, info_node], ffapp, car(op))))
    return elimina_estats_buits(aux)

def construeix_arbre (arbre, estrategia, node_expandit, nous_nodes_a_expandir):
    elm = estrategia(car(arbre), nous_nodes_a_expandir)
    return cons(elm, [cons(node_expandit, cadr(arbre))])

def arbre_inicial (estat, info):
    infres = info(estat)
    node = construeix_node(gensym(), estat, [], [], [])
    tmp = [node + infres]
    return [tmp]

def nodes_a_expandir (arbre):
    return car(arbre)

def nodes_expandits (arbre):
    return cadr(arbre)

def node_arbre (id_node, arbre):
    check_node = lambda node: ident(node) == id_node
    a_expandir = member_if(check_node, nodes_a_expandir(arbre))
    if bool(a_expandir):
        return car(a_expandir)
    
    return find_if(check_node, nodes_expandits(arbre))

def construeix_node (ident, estat, id_pare, op, info):
    return [ident, estat, id_pare, op] + info

def ident (node): return car(node)

def estat (node): return cadr(node)
def id_pare (node): return caddr(node)
def operador (node): return car(cdddr(node))
def info (node): return cdr(cdddr(node))

def operadors (problema): return car(problema)
def funcio_info_addicional (problema): return cadr(problema)
def estat_inicial (problema): return caddr(problema)
def funcio_objectiu (problema): return car(cdddr(problema))
def info_inicial (problema): return car(cdr(cdddr(problema)))

################################################################################
## TRENCACLOSQUES

# Operador IE: intercanviar esquerra [1,2,3,4] => [2,1,3,4]
def mov_ie (estat, info):
    return [cadr(estat), car(estat), caddr(estat), cadddr(estat)]

# Operador IC: intercanviar centre [1,2,3,4] => [1,3,2,4]
def mov_ic (estat, info):
    return [car(estat), caddr(estat), cadr(estat), cadddr(estat)]

# Operador ID: intercanviar dreta [1,2,3,4] => [1,2,4,3]
def mov_id (estat, info):
    return [car(estat), cadr(estat), cadddr(estat), caddr(estat)]

def tl_operadors_trencaclosques():
    return [['ie', mov_ie], ['ic', mov_ic], ['id', mov_id]]

def problema_trencaclosques(estat_ini, funcio_obj):
    return [tl_operadors_trencaclosques(), #operadors
            (lambda info_node_pare, estat, nom_operador: []), #funció info. ini.
            estat_ini, #estat inicial
            (lambda estat: estat == funcio_obj), #funció objectiu
            (lambda estat: [])] #informació inicial

################################################################################
## CERCA PER AMPLADA / PROFUNDITAT

def tl_estrategia_amplada (nodes_a_expandir, nous_nodes_a_expandir):
    return nodes_a_expandir + nous_nodes_a_expandir

def cerca_amplada (problema):
    return fer_cerca(problema, tl_estrategia_amplada)

def tl_estrategia_profunditat (nodes_a_expandir, nous_nodes_a_expandir):
    return nous_nodes_a_expandir + nodes_a_expandir

def cerca_profunditat (problema):
    return fer_cerca(problema, tl_estrategia_profunditat)

################################################################################
## EXECUCIÓ

print(cerca_amplada(problema_trencaclosques([4,2,1,3], [1,2,3,4])))
#print(cerca_profunditat(problema_trencaclosques([4,2,1,3], [1,2,3,4])))