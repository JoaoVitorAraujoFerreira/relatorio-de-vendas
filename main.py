import sqlite3
import customtkinter as ctk
import tkinter.ttk as ttk
#import pandas as pd
#import mathplotlib

# banco de dados
conn = sqlite3.connect('database.db')
c = conn.cursor()

# tabelas
c.execute("""CREATE TABLE IF NOT EXISTS users 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    login TEXT NOT NULL,
    senha TEXT NOT NULL,
    admin TEXT NOT NULL)
    """)

c.execute("""CREATE TABLE IF NOT EXISTS products 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    ean TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    tipo TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS vendidos 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    ean TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT,
    quantidade INTEGER NOT NULL,
    data_venda TEXT NOT NULL)""")

# FILTRO DE DADOS
def so_texto(texto):
    texto = texto.lower()
    return texto.strip()
    #função para retornar apenas texto

def so_numero(numeros):
    aprovado=True
    for i in numeros:
        if type(i) != int:
            aprovado=False
    if aprovado:
        return #normal codigo continua
    return #mensagem de erro
    #função para retornar apenas valores numericos



# lançar vendas

# exportar relatorio

# editar banco de dados de vendas

# editar banco de dados de produtos

# editar usuarios

users = c.execute("SELECT * FROM users").fetchall()

if not users:
    c.execute("INSERT INTO users (nome, login, senha, admin) VALUES (?,?,?,?)",
              ("joao","admin",1509,"sim"))
    conn.commit()
for user in users:
    if user[4] == "sim":
        tem_adm = True
        continue
    if not tem_adm:
        c.execute("INSERT INTO users (nome, login, senha, admin) VALUES (?,?,?,?)",
                  ("joao", "admin", 1509, "sim"))
        conn.commit()
        continue

def add_users(nome,login, senha, admin, callback=None):
    # ID NOME LOGIN SENHA ADMIN(sim/nao)
    c.execute("INSERT INTO users (nome, login, senha, admin) VALUES (?,?,?,?)",
              (nome,login, senha, admin))
    conn.commit()
    if callback:
        callback()

def edit_users(id,nome,login, senha, admin, callback=None):
    c.execute("""UPDATE users SET nome = ?, login = ?, senha = ?, admin = ? WHERE id = ?""",
              (nome,login,senha,admin,id))
    conn.commit()
    if callback:
        callback()

def atualizar_tabela(tree):
    for i in tree.get_children():
        tree.delete(i)
    c.execute("SELECT * FROM users")
    for row in c.fetchall():
        tree.insert("", "end", values=row)

def delet_users(id, callback=None):
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    if callback:
        callback()


#---_edit----GUI----------------------GUI-----------------------GUI----------------------GUI----------------------GUI--------

app = ctk.CTk()
app.title("Controle de vendas")
app.geometry("865x820")
app.grid_columnconfigure(1, weight=1)  # Col1 (conteúdo) cresce!
app.grid_rowconfigure(0, weight=1)     # Linha 0 cresce!
app.grid_columnconfigure(0, weight=0)  # Sidebar fixa!

ctk.set_appearance_mode("dark")


#coluna 1 frames e seus conteudos
tela_app = ctk.CTkFrame(app)
tela_app.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
tela_app.grid_columnconfigure(0, weight=1)
tela_app.grid_rowconfigure(0, weight=1)

def show_frame(name):  # name = STRING!
    for frame_name, f in frames.items():
        if frame_name != name:  # ✅ STRING == STRING
            f.grid_remove()
        else:
            f.grid()


#tela de login
def tela_login(tela):

    nome_frame = [name for name, f in frames.items() if f == tela][0] #seleciona um objeto
    show_frame(nome_frame)


    for widget in tela.winfo_children(): #limpa a tela
        widget.destroy()

    ctk.CTkLabel(tela, text="Login", font=ctk.CTkFont(size=28)).pack(padx=20, pady=50)

    ctk.CTkLabel(tela, text="Login", font=ctk.CTkFont(size=24)).pack()
    entry_login = ctk.CTkEntry(tela, width=300, height=40, font=ctk.CTkFont(size=16), show="*")
    entry_login.pack(pady=(5,30))
    ctk.CTkLabel(tela, text="Senha", font=ctk.CTkFont(size=24) ).pack()
    entry_senha = ctk.CTkEntry(tela, width=300, height=40, font=ctk.CTkFont(size=16), show="*")
    entry_senha.pack(pady=(5,30))

    def verificar_login():
        login = entry_login.get()
        senha = entry_senha.get()
        c.execute("SELECT * FROM users WHERE login = ? AND senha = ?", (login, senha))
        usuario = c.fetchone()

        nome_aba = [name for name, f in frames.items() if f == tela][0]
        frame_destino = frames[nome_aba]

        if usuario and usuario[4] == "sim" and nome_aba == "Editar Usuários":
            editar_usuarios_frame(frames[nome_aba])
            return
        elif usuario and usuario[4] != "sim" and nome_aba == "Editar Usuários":
            mensagem_nao_admin = ctk.CTkLabel(
                tela,
                text="O usuario não possui permissões de administrador",
                font=ctk.CTkFont(size=20),
                text_color="red"
            )
            mensagem_nao_admin.pack()
            tela.after(2500, mensagem_nao_admin.destroy)
        elif usuario:
            # Limpa e carrega
            for widget in frame_destino.winfo_children():
                widget.destroy()
            match nome_aba:
                case "Editar Produtos":
                    editar_produtos_frame(frames[nome_aba])
                case "Editar Vendas":
                    editar_vendas_frame(frames[nome_aba])
            return
        else:
            mensagem_login_incorreto = ctk.CTkLabel(tela, text="Login ou senha incorretos",
                                                    font=ctk.CTkFont(size=20), text_color="red" )
            mensagem_login_incorreto.pack()
            tela.after(2500, mensagem_login_incorreto.destroy)

    ctk.CTkButton(tela, text="Entrar", command=verificar_login, height=40, fg_color="green").pack(pady=30)


#lancar vendas
def vendas_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(frame, text= "Lancar vendas",font=ctk.CTkFont(size=28)).pack()
    show_frame("Lançar Vendas")
#relatorios
def relatorios_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(frame, text="Relatórios", font=ctk.CTkFont(size=28)).pack()
    show_frame("Relatórios")
#editar vendas
def editar_vendas_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(frame, text="Editar Vendas", font=ctk.CTkFont(size=28)).pack()
    show_frame("Editar Vendas")
#editar produtos
def editar_produtos_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(frame, text="Editar Produtos", font=ctk.CTkFont(size=28)).pack()
    show_frame("Editar Produtos")
#esitar usuarios
def editar_usuarios_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

    # VISUALISAÇÃO DE USUARIOS
    tree_frame = ctk.CTkFrame(tela_app)
    tree_frame.grid(row=0, column=3, rowspan=4, sticky="ns")
    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)

    arvore_users = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Login", "Senha", "Admin"), show="headings")
    arvore_users.heading("ID", text="ID")
    arvore_users.heading("Nome", text="Nome")
    arvore_users.heading("Login", text="Login")
    arvore_users.heading("Senha", text="Senha")
    arvore_users.heading("Admin", text="Admin")
    arvore_users.column("ID", width=50)
    arvore_users.column("Nome", width=60)
    arvore_users.column("Login", width=60)
    arvore_users.column("Senha", width=60)
    arvore_users.column("Admin", width=60)
    arvore_users.grid(row=0, column=0, sticky="nswe", padx=(10, 0), pady=10)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=arvore_users.yview)
    arvore_users.configure(yscrollcommand=scrollbar.set)

    scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

    atualizar_tabela(arvore_users)

    #MENU PARA ADCIONAR USUARIOS
    menu_add_users = ctk.CTkFrame(tela_app)
    menu_add_users.grid(row=0, column=0, padx=10, pady=10)
    menu_add_users.grid_columnconfigure((0,1), weight=1)
    menu_add_users.grid_rowconfigure(4, weight=1)

    ctk.CTkLabel(menu_add_users, text="ADD Usuários",
                 font=ctk.CTkFont(size=28)).grid(row=0, column=0, columnspan=2, pady=(5,15))

    entry_add_nome = ctk.CTkEntry(menu_add_users, placeholder_text="Digite o Nome")
    entry_add_nome.grid(row= 1, column= 0,padx=5, pady=10)
    entry_add_login = ctk.CTkEntry(menu_add_users, placeholder_text="Digite o Login")
    entry_add_login.grid(row= 1, column= 1,padx=5, pady=10)
    entry_add_senha = ctk.CTkEntry(menu_add_users, placeholder_text="Digite o Senha")
    entry_add_senha.grid(row= 2, column= 0,padx=5, pady=10)
    entry_add_adm = ctk.CTkEntry(menu_add_users, placeholder_text="Digite se é o administrador")
    entry_add_adm.grid(row= 2, column= 1,padx=5, pady=10)

    ctk.CTkButton(menu_add_users, text="Salvar Usuario",
                  command=lambda:
                  add_users(
                      entry_add_nome.get(),
                      entry_add_login.get(),
                      entry_add_senha.get(),
                      entry_add_adm.get(),
                      lambda: atualizar_tabela(arvore_users)),
                  height=40, fg_color="green").grid(row=3, column=0, columnspan=2, pady=30, sticky="ew")


    # MENU PARA EDITAR USUARIOS
    menu_edit_users = ctk.CTkFrame(tela_app)
    menu_edit_users.grid(row=1, column=0, padx=10, pady=10)
    menu_edit_users.grid_columnconfigure((0, 1), weight=1)
    menu_edit_users.grid_rowconfigure(4, weight=1)
    ctk.CTkLabel(menu_edit_users, text="Editar Usuário",
                 font=ctk.CTkFont(size=28)).grid(row=0, column=0, columnspan=2, pady=(5,15))

    entry_edit_id = ctk.CTkEntry(menu_edit_users, placeholder_text="Digite o ID")
    entry_edit_id.grid(row= 1, column= 0,padx=5, pady=10)
    entry_edit_nome = ctk.CTkEntry(menu_edit_users, placeholder_text="Novo Nome")
    entry_edit_nome.grid(row= 1, column= 1,padx=5, pady=10)
    entry_edit_login = ctk.CTkEntry(menu_edit_users, placeholder_text="Novo Login")
    entry_edit_login.grid(row= 2, column= 0,padx=5, pady=10)
    entry_edit_senha = ctk.CTkEntry(menu_edit_users, placeholder_text="Novo Senha")
    entry_edit_senha.grid(row= 2, column= 1,padx=5, pady=10)
    entry_edit_adm = ctk.CTkCheckBox(menu_edit_users, text="Usuario é administrador", onvalue="sim", offvalue="nao")
    entry_edit_adm.grid(row= 3, column= 0, columnspan=2,padx=5, pady=10)

    ctk.CTkButton(menu_edit_users, text="Salvar Edição",
                  command=lambda:
                  edit_users(
                      entry_edit_id.get(),
                      entry_edit_nome.get(),
                      entry_edit_login.get(),
                      entry_edit_senha.get(),
                      entry_edit_adm.get(),
                      lambda: atualizar_tabela(arvore_users)),
                  height=40, fg_color="green").grid(row=4, column=0, columnspan=2, pady=30, sticky="ew")

    #MENU PARA DELETAR USUARIOS
    menu_delet_users = ctk.CTkFrame(tela_app)
    menu_delet_users.grid(row=3, column=0, sticky="nswe", padx=10, pady=10)
    ctk.CTkLabel(menu_delet_users, text="Deletar Usuário", font=ctk.CTkFont(size=28)).pack(padx=5, pady=(5, 15))

    entry_delet_id = ctk.CTkEntry(menu_delet_users, placeholder_text="Digite o ID")
    entry_delet_id.pack(padx=5, pady=10)


    ctk.CTkButton(menu_delet_users, text="Deletar Usuario",
                  command=lambda:delet_users(entry_delet_id.get(), lambda: atualizar_tabela(arvore_users)),
                  height=40, fg_color="red").pack(pady=30)

    show_frame("Editar Usuários")

frames = {} #dicionario nome:frame
for name in ["Lançar Vendas", "Relatórios", "Editar Vendas", "Editar Produtos", "Editar Usuários"]:
    frame = ctk.CTkFrame(tela_app)
    frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    frames[name] = frame



#coluna 0

sidebar = ctk.CTkFrame(app, width=220)
sidebar.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
ctk.CTkLabel(sidebar, text="MENU", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

#botões
ctk.CTkButton(sidebar, text="Lançar Vendas",
              command=lambda: vendas_frame(frames["Lançar Vendas"]),
              height=40).pack(pady=10, padx=20, fill="x")
ctk.CTkButton(sidebar, text="Relatórios",
              command=lambda: relatorios_frame(frames["Relatórios"]),
              height=40).pack(pady=10, padx=20, fill="x")
ctk.CTkButton(sidebar, text="Editar Vendas",
              command=lambda: tela_login(frames["Editar Vendas"]),
              height=40).pack(pady=10, padx=20, fill="x")
ctk.CTkButton(sidebar, text="Editar Produtos",
              command=lambda: tela_login(frames["Editar Produtos"]),
              height=40).pack(pady=10, padx=20, fill="x")
ctk.CTkButton(sidebar, text="Editar Usuários",
              command=lambda: tela_login(frames["Editar Usuários"]),
              height=40).pack(pady=10, padx=20, fill="x")





# Inicia na primeira aba
vendas_frame(frames["Lançar Vendas"])
app.mainloop()
#-------GUI----------------------GUI-----------------------GUI----------------------GUI----------------------GUI--------

conn.commit()
conn.close()