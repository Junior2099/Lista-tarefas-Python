import tkinter as tk
from tkinter import ttk, font, messagebox

# Configurando janela
janela = tk.Tk()
janela.title("Minhas Tarefas")
janela.configure(bg="#F0F0F0")
janela.geometry("630x600")
font_size = font.Font(family="Arial", size=25, weight="bold")
cabecalho = tk.Label(janela, text="Tarefas", font=font_size, bg="#F0F0F0", fg="#333")
cabecalho.pack(pady=20)

# Chamando ícones (depois da janela ser criada)
try:
    icon_editar = tk.PhotoImage(file="editar.png").subsample(8,8)  # Ajuste o fator aqui
    icon_deletar = tk.PhotoImage(file="lixeira.png").subsample(6, 6)  # Ajuste o fator aqui
except tk.TclError as e:
    print(f"Erro ao carregar ícones: {e}")
    icon_editar = icon_deletar = None  # Definindo como None para evitar erros posteriores

# Configurando interações de usuário
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)
entrada_tarefa = tk.Entry(frame, font=("Arial", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)
botao_adicionar = tk.Button(frame, text="Adicionar Tarefas", bg="#4CAF50", fg="white", height=1, width=15, font=("Arial", 12), relief=tk.FLAT, command=lambda: adicionar_tarefa())
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criando lista
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.configure(yscrollcommand=scrollbar.set)

# Função para adicionar tarefas
frame_em_edicao = None

def adicionar_tarefa():
    global frame_em_edicao
    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            adicionar_item_tarefa(tarefa)
            entrada_tarefa.delete(0, tk.END)
    else: 
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma tarefa")

def adicionar_item_tarefa(tarefa):
    global frame_em_edicao
    
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)
    
    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Arial", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
    
    if icon_editar:
        botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
        botao_editar.pack(side=tk.RIGHT, padx=5)
    
    if icon_deletar:
        botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa: deletar_tarefa(f), bg="white", relief=tk.FLAT)
        botao_deletar.pack(side=tk.RIGHT, padx=5)
    
    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alterar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)
    
    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

def preparar_edicao(frame, label):
    global frame_em_edicao
    frame_em_edicao = frame
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label.cget("text"))

def atualizar_tarefa(tarefa):
    if frame_em_edicao:
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=tarefa)

def deletar_tarefa(frame):
    frame.destroy()

def alterar_sublinhado(label):
    if label.cget("font").find("underline") != -1:
        label.config(font=("Arial", 16))
    else:
        label.config(font=("Arial", 16, "underline"))

janela.mainloop()
