import sqlite3

def conectar():
    return sqlite3.connect("jogo.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists jogadores (
            id integer primary key autoincrement,
            nome text unique,
            vitorias integer default 0,
            derrotas integer default 0,
            empates integer default 0
        )
    """)
    conn.commit()
    conn.close()

def get_ou_criar_jogador(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("select id from jogadores where nome = ?", (nome,))
    res = cursor.fetchone()

    if res:
        conn.close()
        return res[0]

    cursor.execute("insert into jogadores (nome) values (?)", (nome,))
    conn.commit()
    jid = cursor.lastrowid
    conn.close()
    return jid

def atualizar_resultado(jogador_id, resultado):
    conn = conectar()
    cursor = conn.cursor()

    if resultado == "vitoria":
        cursor.execute("update jogadores set vitorias = vitorias + 1 where id = ?", (jogador_id,))
    elif resultado == "derrota":
        cursor.execute("update jogadores set derrotas = derrotas + 1 where id = ?", (jogador_id,))
    elif resultado == "empate":
        cursor.execute("update jogadores set empates = empates + 1 where id = ?", (jogador_id,))

    conn.commit()
    conn.close()

def top_5():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        select nome, vitorias, derrotas, empates
        from jogadores
        order by vitorias desc
        limit 5
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados
