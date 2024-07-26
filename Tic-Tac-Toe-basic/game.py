# Implementación muy básica del algoritmo MINIMAX para TicTacToe

import random
import math
import os

class Juego:
    def __init__(self):
        self.tablero = ['-' for i in range(9)]
        if random.randint(0, 1) == 1:
            self.humano = 'X'
            self.ia = 'O'
        else:
            self.humano = 'O'
            self.ia = 'X'
    
    def imprimir_tablero(self):
        for i in range(0, 9, 3): #Saltos de 3 en 3, rango 0-9
            print(f"{self.tablero[i]} | {self.tablero[i+1]} | {self.tablero[i+2]}")
    
    def esta_lleno(self, tablero):
        return not '-' in tablero
    
    def buscar_tercia(self, tablero, jugador):
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]               # Diagonales
        ]
        return any(all(tablero[i] == jugador for i in comb) for comb in combinaciones)

    def imprimir_ganador(self):
        if self.buscar_tercia(self.tablero, self.humano):
            os.system("cls")
            print(f"\Jugador {self.humano} ganó el juego")
            return True
        
        if self.buscar_tercia(self.tablero, self.ia):
            os.system("cls")
            print(f"\Jugador {self.ia} ganó el juego")
            return True

        if self.esta_lleno(self.tablero):
            os.system("cls")
            print("Empate!")
            return True
        
        return False
    
    def iniciar(self):
        #Instancias de los jugadores
        humano = Humano(self.humano)
        maquina = Maquina(self.ia)

        while True:
            os.system("cls")
            print(f"Turno de {self.humano}")
            self.imprimir_tablero()

            # Humano
            casilla = humano.movimiento(self.tablero)
            self.tablero[casilla] = self.humano
            if self.imprimir_ganador():
                break
            
            # Maquina
            casilla = maquina.movimiento(self.tablero)
            self.tablero[casilla] = self.ia
            if self.imprimir_ganador():
                break


class Humano:
    def __init__(self, letra):
        self.letra = letra
    
    def movimiento(self, tablero):
        while True:
            casilla = int(input("Digita el número de casilla donde quieres jugar (1-9): "))
            print()
            if tablero[casilla-1] == "-":
                break

        return casilla-1
        
class Maquina(Juego):
    def __init__(self, letra):
        self.max_jugador = letra
        self.min_jugador = "X" if letra == "O" else "O"

    def casillas_disponibles(self, tablero):
        return [i for i, x in enumerate(tablero) if x == "-"]

    def tablero_prueba(self, tablero, casilla, jugador):
        nuevoTablero = tablero.copy()
        nuevoTablero[casilla] = jugador
        return nuevoTablero

    # Método para saber si es momento de terminar la recursividad porque hubo una tercia por cualquier jugador
    def final(self, tablero):
        return self.buscar_tercia(tablero, "X") or self.buscar_tercia(tablero, "O")

    # Método recursivo para obtener el mejor movimiento
    def minimax(self, tablero, jugador):
        max_jugador = self.max_jugador
        min_jugador = self.min_jugador

        # Si se encuentra con una posición ganadora retorna un valor negativo si el jugador ganador es min, positivo si el ganador es max
        # Para optimizar un poco, el valor retornado es mayor o menor si hay más casillas vacías (es decir, la tercia se alcanza más pronto)
        if self.final(tablero):
            return {'posicion': None, 'puntuacion': 1 * (len(self.casillas_disponibles(tablero)) + 1) if jugador == min_jugador else -1 * (len(self.casillas_disponibles(tablero)) + 1)}
        elif self.esta_lleno(tablero):
            return {'posicion': None, 'puntuacion': 0}
        
        if jugador == max_jugador:
            mejor_jugada = {'posicion': None, 'puntuacion': -math.inf}
        else:
            mejor_jugada = {'posicion': None, 'puntuacion': math.inf}
        
        for posible_movimiento in self.casillas_disponibles(tablero):
            nuevoTablero = self.tablero_prueba(tablero, posible_movimiento, jugador)
            oponente = min_jugador if jugador == max_jugador else max_jugador
            intentar_jugada = self.minimax(nuevoTablero, oponente)
        
            intentar_jugada['posicion'] = posible_movimiento

            if jugador == max_jugador:
                if intentar_jugada['puntuacion'] > mejor_jugada['puntuacion']:
                    mejor_jugada = intentar_jugada
            else:
                if intentar_jugada['puntuacion'] < mejor_jugada['puntuacion']:
                    mejor_jugada = intentar_jugada

        return mejor_jugada

    def movimiento(self, tablero):
        casilla = self.minimax(tablero, self.max_jugador)['posicion']
        return casilla


nuevoJuego = Juego()
nuevoJuego.iniciar()
