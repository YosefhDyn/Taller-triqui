import tkinter as tk
from tkinter import messagebox
from funciones import (
    crear_tablero,
    evaluar_estado,
    hay_ganador_o_empate,
    hacer_movimiento,
    obtener_mejor_movimiento,
)


class TriquiGUI:
    """Interfaz gráfica para el juego de Triqui (Tic-Tac-Toe) con IA Minimax."""

    COLORES = {
        "fondo": "#1e1e2e",
        "celda": "#313244",
        "celda_hover": "#45475a",
        "X": "#f38ba8",
        "O": "#89b4fa",
        "linea": "#cdd6f4",
        "texto": "#cdd6f4",
        "boton": "#585b70",
        "boton_hover": "#6c7086",
    }

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Triqui – IA Minimax")
        self.ventana.configure(bg=self.COLORES["fondo"])
        self.ventana.resizable(False, False)

        self.tablero = crear_tablero()
        self.turno_humano = True  # El humano inicia
        self.juego_terminado = False

        self._crear_widgets()
        self._centrar_ventana()

    # ── Widgets ─────────────────────────────────────────────

    def _crear_widgets(self):
        # Título
        self.label_titulo = tk.Label(
            self.ventana,
            text="Triqui – IA Minimax",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
            pady=10,
        )
        self.label_titulo.pack()

        # Indicador de turno
        self.label_turno = tk.Label(
            self.ventana,
            text="Tu turno (O)",
            font=("Segoe UI", 13),
            bg=self.COLORES["fondo"],
            fg=self.COLORES["O"],
            pady=4,
        )
        self.label_turno.pack()

        # Tablero 3×3
        self.frame_tablero = tk.Frame(self.ventana, bg=self.COLORES["fondo"], padx=20, pady=10)
        self.frame_tablero.pack()

        self.botones: list[tk.Button] = []
        for i in range(9):
            fila, col = divmod(i, 3)
            btn = tk.Button(
                self.frame_tablero,
                text="",
                font=("Segoe UI", 32, "bold"),
                width=3,
                height=1,
                bg=self.COLORES["celda"],
                fg=self.COLORES["texto"],
                activebackground=self.COLORES["celda_hover"],
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda pos=i: self._click_celda(pos),
            )
            btn.grid(row=fila, column=col, padx=4, pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORES["celda_hover"]) if b["text"] == "" else None)
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORES["celda"]) if b["text"] == "" else None)
            self.botones.append(btn)

        # Botones inferiores
        self.frame_inferior = tk.Frame(self.ventana, bg=self.COLORES["fondo"], pady=10)
        self.frame_inferior.pack()

        self.btn_reiniciar = tk.Button(
            self.frame_inferior,
            text="🔄  Nueva partida",
            font=("Segoe UI", 12),
            bg=self.COLORES["boton"],
            fg=self.COLORES["texto"],
            activebackground=self.COLORES["boton_hover"],
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._reiniciar,
        )
        self.btn_reiniciar.pack(side=tk.LEFT, padx=8)

        self.btn_salir = tk.Button(
            self.frame_inferior,
            text="❌  Salir",
            font=("Segoe UI", 12),
            bg=self.COLORES["boton"],
            fg=self.COLORES["texto"],
            activebackground=self.COLORES["boton_hover"],
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.ventana.destroy,
        )
        self.btn_salir.pack(side=tk.LEFT, padx=8)

        # Marcador
        self.victorias_humano = 0
        self.victorias_ia = 0
        self.empates = 0

        self.label_marcador = tk.Label(
            self.ventana,
            text=self._texto_marcador(),
            font=("Segoe UI", 11),
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
            pady=8,
        )
        self.label_marcador.pack()

    # ── Lógica de juego ────────────────────────────────────

    def _click_celda(self, pos: int):
        if self.juego_terminado or not self.turno_humano:
            return
        if self.tablero[pos] != " ":
            return

        # Movimiento del humano (O)
        hacer_movimiento(self.tablero, pos, "O")
        self._actualizar_boton(pos, "O")

        if self._verificar_fin():
            return

        # Turno de la IA
        self.turno_humano = False
        self.label_turno.config(text="Turno de la IA (X)", fg=self.COLORES["X"])
        self.ventana.update_idletasks()

        self.ventana.after(300, self._turno_ia)

    def _turno_ia(self):
        mejor_mov = obtener_mejor_movimiento(self.tablero)
        if mejor_mov is not None:
            hacer_movimiento(self.tablero, mejor_mov, "X")
            self._actualizar_boton(mejor_mov, "X")

        if self._verificar_fin():
            return

        self.turno_humano = True
        self.label_turno.config(text="Tu turno (O)", fg=self.COLORES["O"])

    def _verificar_fin(self) -> bool:
        if not hay_ganador_o_empate(self.tablero):
            return False

        self.juego_terminado = True
        resultado = evaluar_estado(self.tablero)

        if resultado == 1:
            mensaje = "¡La IA gana! 🤖"
            self.victorias_ia += 1
            self.label_turno.config(text="La IA gana", fg=self.COLORES["X"])
        elif resultado == -1:
            mensaje = "¡Ganaste! 🎉"
            self.victorias_humano += 1
            self.label_turno.config(text="¡Ganaste!", fg=self.COLORES["O"])
        else:
            mensaje = "¡Empate! 🤝"
            self.empates += 1
            self.label_turno.config(text="Empate", fg=self.COLORES["texto"])

        self.label_marcador.config(text=self._texto_marcador())

        # Resaltar línea ganadora
        self._resaltar_ganador()

        messagebox.showinfo("Fin del juego", mensaje)
        return True

    def _resaltar_ganador(self):
        from funciones import LINEAS

        for linea in LINEAS:
            a, b, c = linea
            if self.tablero[a] == self.tablero[b] == self.tablero[c] != " ":
                color = self.COLORES["X"] if self.tablero[a] == "X" else self.COLORES["O"]
                for idx in linea:
                    self.botones[idx].config(bg=color, fg="#1e1e2e")
                break

    # ── Utilidades ──────────────────────────────────────────

    def _actualizar_boton(self, pos: int, jugador: str):
        color = self.COLORES["X"] if jugador == "X" else self.COLORES["O"]
        self.botones[pos].config(text=jugador, fg=color, cursor="arrow")

    def _texto_marcador(self) -> str:
        return f"Tú: {self.victorias_humano}   |   IA: {self.victorias_ia}   |   Empates: {self.empates}"

    def _reiniciar(self):
        self.tablero = crear_tablero()
        self.juego_terminado = False
        self.turno_humano = not self.turno_humano  # Alterna quién inicia

        for btn in self.botones:
            btn.config(text="", bg=self.COLORES["celda"], fg=self.COLORES["texto"], cursor="hand2")

        if self.turno_humano:
            self.label_turno.config(text="Tu turno (O)", fg=self.COLORES["O"])
        else:
            self.label_turno.config(text="Turno de la IA (X)", fg=self.COLORES["X"])
            self.ventana.after(400, self._turno_ia)

    def _centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"+{x}+{y}")

    def ejecutar(self):
        self.ventana.mainloop()


def iniciar_gui():
    """Punto de entrada para lanzar la interfaz gráfica."""
    app = TriquiGUI()
    app.ejecutar()


if __name__ == "__main__":
    iniciar_gui()
