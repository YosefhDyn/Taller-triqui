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



LINEAS = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8], 
    [0,4,8], [2,4,6]          
]
# Combinaciones para ganar

def obtener_sucesores(tablero):
    sucesores = []
    for i in range(9):
        if tablero[i] == ' ':
            sucesores.append(i)
    return sucesores
# Casillas vacias

def evaluar_estado(tablero):
    for linea in LINEAS:
        a, b, c = linea
        
        if tablero[a] == tablero[b] == tablero[c] != ' ':
            if tablero[a] == 'X':
                return 1
            else:
                return -1
    
    return 0

def hay_ganador_o_empate(tablero):
    if evaluar_estado(tablero) != 0:
        return True
    
    if ' ' not in tablero:
        return True
    
    return False

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


def jugar(inicia_humano):
    tablero = crear_tablero()
    turno_humano = inicia_humano

    while True:

        mostrar_tablero(tablero)

        if turno_humano:
            try:
                movimiento = int(input("Ingresa tu movimiento (0-8): "))
                
                if 0 <= movimiento <= 8 and tablero[movimiento] == ' ':
                    hacer_movimiento(tablero, movimiento, 'O')
                    turno_humano = False
                else:
                    print("Movimiento inválido.")
                    continue

            except:
                print("Ingresa un número válido.")
                continue

        else:
            print("Turno de la IA")
            mejor_mov = obtener_mejor_movimiento(tablero)
            hacer_movimiento(tablero, mejor_mov, 'X')
            turno_humano = True

        if hay_ganador_o_empate(tablero):
            break

    mostrar_tablero(tablero)

    resultado = evaluar_estado(tablero)

    if resultado == 1:
        print("La IA gana")
    elif resultado == -1:
        print("Tu ganaste")
    else:
        print("Hay un empate")

def main():
    print("=== TRIQUI – IA Minimax ===")
    print("1. Jugar en consola")
    print("2. Jugar con interfaz gráfica")
    opcion = input("Selecciona una opción (1/2): ").strip()

    if opcion == "2":
        from gui import iniciar_gui
        iniciar_gui()
    else:
        inicia_humano = True
        while True:
            jugar(inicia_humano)

            respuesta = input("¿Quieres jugar otra vez? (s/n): ").lower()

            if respuesta != 's':
                print("Gracias por jugar")
                break

            inicia_humano = not inicia_humano

if __name__ == "__main__":
    main()