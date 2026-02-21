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
tablero = crear_tablero()
tablero[0] = 'X'
tablero[4] = 'O'
mostrar_tablero(tablero)