print("teste visual")

import tkinter as tk
from tkinter import messagebox
from database import criar_tabela, get_ou_criar_jogador, atualizar_resultado, top_5

criar_tabela()

# ===== tema =====
BG = "#121212"
BG_SEC = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#00bcd4"
BTN = "#2a2a2a"
HOVER = "#3a3a3a"
WIN = "#2e7d32"

jogador_x = ""
jogador_o = ""
id_x = None
id_o = None
turno = "X"
botoes = []

# ===== lógica =====
def venceu(simbolo):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in combos:
        if botoes[a]["text"] == botoes[b]["text"] == botoes[c]["text"] == simbolo:
            return True
    return False

def empate():
    return all(b["text"] != "" for b in botoes)

def destacar_vitoria():
    for b in botoes:
        b.config(bg=WIN)

def resetar():
    global turno
    for b in botoes:
        b.config(text="", bg=BTN)
    turno = "X"

# ===== ranking =====
def mostrar_ranking():
    j = tk.Toplevel(root)
    j.title("ranking")
    j.configure(bg=BG)

    tk.Label(
        j,
        text="top 5 jogadores",
        bg=BG,
        fg=ACCENT,
        font=("segoe ui", 14, "bold")
    ).pack(pady=10)

    for nome, v, d, e in top_5():
        tk.Label(
            j,
            text=f"{nome}  |  v:{v}  d:{d}  e:{e}",
            bg=BG,
            fg=FG,
            font=("segoe ui", 11)
        ).pack(anchor="w", padx=20)

# ===== animações =====
def hover_on(btn):
    btn.after(0, lambda: btn.config(bg=HOVER))

def hover_off(btn):
    btn.after(0, lambda: btn.config(bg=BTN))

# ===== jogo =====
def clique(botao):
    global turno

    if botao["text"] != "":
        return

    botao.config(text=turno, fg=ACCENT)

    if venceu(turno):
        vencedor = jogador_x if turno == "X" else jogador_o
        messagebox.showinfo("fim de jogo", f"{vencedor} venceu")

        if turno == "X":
            atualizar_resultado(id_x, "vitoria")
            atualizar_resultado(id_o, "derrota")
        else:
            atualizar_resultado(id_o, "vitoria")
            atualizar_resultado(id_x, "derrota")

        destacar_vitoria()
        root.after(1200, resetar)
        return

    if empate():
        messagebox.showinfo("fim de jogo", "empate")
        atualizar_resultado(id_x, "empate")
        atualizar_resultado(id_o, "empate")
        resetar()
        return

    turno = "O" if turno == "X" else "X"

def iniciar_jogo():
    global jogador_x, jogador_o, id_x, id_o

    jogador_x = entry_x.get()
    jogador_o = entry_o.get()

    if not jogador_x or not jogador_o:
        messagebox.showerror("erro", "preencha os dois nomes")
        return

    id_x = get_ou_criar_jogador(jogador_x)
    id_o = get_ou_criar_jogador(jogador_o)

    placar_x.set(f"{jogador_x} (X)")
    placar_o.set(f"{jogador_o} (O)")

    frame_inicio.pack_forget()
    frame_jogo.pack()

# ===== interface =====
root = tk.Tk()
root.title("jogo da velha")
root.configure(bg=BG)

placar_x = tk.StringVar()
placar_o = tk.StringVar()

frame_inicio = tk.Frame(root, bg=BG)
frame_inicio.pack(padx=20, pady=20)

tk.Label(frame_inicio, text="jogador X", bg=BG, fg=FG).pack()
entry_x = tk.Entry(frame_inicio, bg=BG_SEC, fg=FG, insertbackground=FG)
entry_x.pack(pady=5)

tk.Label(frame_inicio, text="jogador O", bg=BG, fg=FG).pack()
entry_o = tk.Entry(frame_inicio, bg=BG_SEC, fg=FG, insertbackground=FG)
entry_o.pack(pady=5)

btn_start = tk.Button(frame_inicio, text="iniciar", bg=ACCENT, fg="black", relief="flat", command=iniciar_jogo)
btn_start.pack(pady=10)

frame_jogo = tk.Frame(root, bg=BG)

tk.Label(frame_jogo, textvariable=placar_x, bg=BG, fg=FG).pack()
tk.Label(frame_jogo, textvariable=placar_o, bg=BG, fg=FG).pack()

grade = tk.Frame(frame_jogo, bg=BG)
grade.pack(pady=10)

for i in range(9):
    b = tk.Button(
        grade,
        text="",
        width=5,
        height=2,
        font=("segoe ui", 20, "bold"),
        bg=BTN,
        fg=FG,
        activebackground=ACCENT,
        relief="flat"
    )
    b.bind("<Enter>", lambda e, bt=b: hover_on(bt))
    b.bind("<Leave>", lambda e, bt=b: hover_off(bt))
    b.config(command=lambda bt=b: clique(bt))
    b.grid(row=i//3, column=i%3, padx=4, pady=4)
    botoes.append(b)

btn_reset = tk.Button(frame_jogo, text="reiniciar", bg=BTN, fg=FG, relief="flat", command=resetar)
btn_reset.pack(pady=4)

btn_rank = tk.Button(frame_jogo, text="ranking", bg=BTN, fg=FG, relief="flat", command=mostrar_ranking)
btn_rank.pack(pady=4)

for btn in [btn_start, btn_reset, btn_rank]:
    btn.bind("<Enter>", lambda e, b=btn: hover_on(b))
    btn.bind("<Leave>", lambda e, b=btn: hover_off(b))

root.mainloop()
