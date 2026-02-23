import math
def crear_tablero():
    return [' '] * 9

def mostrar_tablero(tablero):
    print("-------------")
    print(f"| {tablero[0]} | {tablero[1]} | {tablero[2]} |")
    print("-------------")
    print(f"| {tablero[3]} | {tablero[4]} | {tablero[5]} |")
    print("-------------")
    print(f"| {tablero[6]} | {tablero[7]} | {tablero[8]} |")
    print("-------------")

# prueba 
# tablero = crear_tablero()
# tablero[0] = 'X'
# tablero[4] = 'O'
# mostrar_tablero(tablero)



# =================================================================
# PARTE 2: SUCESORES Y HEURÍSTICA (Trabajo de tu compañero)
# =================================================================

def obtener_sucesores(tablero):
    """
    Retorna una lista de los índices (0-8) vacíos en el tablero.
    """
    # Tu compañero debe implementar esto
    pass

def evaluar_estado(tablero):
    """
    Evalúa el tablero actual.
    Retorna:
      +10 si gana MAX ('X')
      -10 si gana MIN ('O')
        0 si es empate o el juego no ha terminado
    """
    # Tu compañero debe implementar esto
    pass

def hay_ganador_o_empate(tablero):
    """
    Retorna True si el juego terminó (alguien ganó o no hay más movimientos).
    """
    # Tu compañero debe implementar esto
    pass

def hacer_movimiento(tablero, posicion, jugador):
    """
    Coloca la ficha del 'jugador' ('X' o 'O') en la 'posicion' (0-8).
    """
    tablero[posicion] = jugador

def deshacer_movimiento(tablero, posicion):
    """
    Quita la ficha de la 'posicion' (0-8), dejándola vacía.
    """
    tablero[posicion] = ' '

def minimax(tablero, profundidad, es_maximizador):
    # 1. Caso base: Verificar si el juego terminó
    if hay_ganador_o_empate(tablero):
        return evaluar_estado(tablero)

    # 2. Max: Se busca el valor más alto
    if es_maximizador:
        mejor_valor = -math.inf
        for sucesor in obtener_sucesores(tablero):
            hacer_movimiento(tablero, sucesor, 'X')
            valor = minimax(tablero, profundidad + 1, False)
            deshacer_movimiento(tablero, sucesor)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor

    # 3. Min: Se busca el valor más bajo
    else:
        mejor_valor = math.inf
        for sucesor in obtener_sucesores(tablero):
            hacer_movimiento(tablero, sucesor, 'O')
            valor = minimax(tablero, profundidad + 1, True)
            deshacer_movimiento(tablero, sucesor)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def obtener_mejor_movimiento(tablero):
    mejor_valor = -math.inf
    mejor_jugada = None

    for sucesor in obtener_sucesores(tablero):
        hacer_movimiento(tablero, sucesor, 'X')
        valor = minimax(tablero, 0, False)
        deshacer_movimiento(tablero, sucesor)
        
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_jugada = sucesor

    return mejor_jugada