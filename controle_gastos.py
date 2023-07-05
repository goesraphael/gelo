from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import json

# Variável para armazenar a referência da imagem do logo
logo_image = None

# Dados iniciais do estoque
estoque = []

# Arquivo JSON para armazenar o estoque
estoque_file = "estoque.json"

def adicionar_compra():
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Criar widgets para a página de adicionar compra
    lbl_instrucoes = Label(conteudo_frame, text="Digite o valor da compra:")
    lbl_instrucoes.pack()

    entry_valor = Entry(conteudo_frame)
    entry_valor.pack()

    # Aqui você pode adicionar outros widgets necessários

def registrar_venda():
    # Aqui você adiciona a lógica para registrar uma venda
    # por exemplo, exibir uma janela para inserir a quantidade vendida
    pass

def voltar_pagina_inicial():
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Adicionar a imagem do logo da empresa novamente
    logo_label = Label(conteudo_frame, image=logo_image)
    logo_label.pack()

def exibir_estoque():
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Criar o rótulo do título "Estoque de Produção"
    lbl_titulo = Label(conteudo_frame, text="Estoque de Produção", font=("Arial", 16, "bold"))
    lbl_titulo.pack(pady=10)

    # Exibir os itens do estoque
    for item in estoque:
        lbl_item = Label(conteudo_frame, text=f"{item['nome']} - {item['quantidade']} pacote(s)")
        lbl_item.pack()

    # Criar um botão para adicionar estoque
    btn_adicionar_estoque = Button(conteudo_frame, text="Adicionar Estoque", command=adicionar_estoque)
    btn_adicionar_estoque.pack(pady=10)

    # Criar um botão para corrigir estoque
    btn_corrigir_estoque = Button(conteudo_frame, text="Corrigir Estoque", command=corrigir_estoque)
    btn_corrigir_estoque.pack(pady=10)

def adicionar_estoque():
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Criar campos para digitar nome e quantidade do novo item
    lbl_nome_item = Label(conteudo_frame, text="Novo nome do item:")
    lbl_quantidade_item = Label(conteudo_frame, text="Quantidade:")

    # Declarar as variáveis como globais
    global entry_nome_item, entry_quantidade_item

    entry_nome_item = Entry(conteudo_frame)
    entry_quantidade_item = Entry(conteudo_frame)

    # Criar um rótulo para o dropdown
    lbl_selecionar_item = Label(conteudo_frame, text="Selecione um item existente ou digite um novo item:")
    lbl_selecionar_item.pack(pady=10)

    # Criar um menu dropdown com as opções de estoque
    opcoes_estoque = [item['nome'] for item in estoque]
    opcoes_estoque.append("Novo Item")

    selecionar_item = StringVar(conteudo_frame)
    selecionar_item.set(opcoes_estoque[0])  # Definir a primeira opção como padrão

    # Função para verificar a seleção do menu dropdown e exibir/ocultar a linha de nome do novo item
    def verificar_selecao(*args):
        opcao = selecionar_item.get()
        if opcao == "Novo Item":
            lbl_nome_item.pack()
            entry_nome_item.pack()
        else:
            lbl_nome_item.pack_forget()
            entry_nome_item.pack_forget()

            # Verificar se é um item existente e exibir campo de quantidade
            if opcao in opcoes_estoque[:-1]:
                lbl_quantidade_item.pack()
                entry_quantidade_item.pack()
            else:
                lbl_quantidade_item.pack_forget()
                entry_quantidade_item.pack_forget()

    # Chamar a função verificar_selecao sempre que a opção selecionada no menu dropdown mudar
    selecionar_item.trace_add("write", verificar_selecao)

    dropdown_estoque = OptionMenu(conteudo_frame, selecionar_item, *opcoes_estoque)
    dropdown_estoque.pack()

    verificar_selecao()  # Verificar a seleção inicial do menu dropdown

    # Criar botão para adicionar item
    btn_adicionar_item = Button(conteudo_frame, text="Adicionar Item", command=lambda: adicionar_item(selecionar_item.get(), entry_nome_item.get(), entry_quantidade_item.get()))
    btn_adicionar_item.pack(pady=10)

def adicionar_item(opcao, novo_item, quantidade):
    # Verificar se foi selecionado um item existente
    if opcao.strip() == "Novo Item":
        if novo_item.strip() == "":
            messagebox.showerror("Erro", "Digite um nome para o item.")
            return

        # Verificar se o campo de quantidade está vazio
        if quantidade.strip() == "":
            messagebox.showerror("Erro", "Digite um valor para a quantidade.")
            return

        # Verificar se a quantidade é um número inteiro
        try:
            quantidade_int = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico para a quantidade.")
            return

        # Verificar se a quantidade é positiva
        if quantidade_int <= 0:
            messagebox.showerror("Erro", "Digite um valor igual ou maior que 1 para a quantidade.")
            return

        # Verificar se o novo item já existe no estoque
        item_existente = False
        for item in estoque:
            if item['nome'] == novo_item:
                item['quantidade'] += quantidade_int
                item_existente = True
                break

        # Se o item não existir, adicioná-lo ao estoque
        if not item_existente:
            estoque.append({"nome": novo_item, "quantidade": quantidade_int})

        messagebox.showinfo("Sucesso", f"{quantidade_int} pacote(s) de {novo_item} adicionado(s) ao estoque.")
    else:
        if opcao.strip() == "":
            messagebox.showerror("Erro", "Selecione ou digite um nome para o item.")
            return

        # Converter a quantidade para inteiro
        try:
            quantidade_int = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico para a quantidade.")
            return

        # Verificar se a quantidade é positiva
        if quantidade_int <= 0:
            messagebox.showerror("Erro", "Digite um valor igual ou maior que 1 para a quantidade.")
            return

        # Verificar se o item existe no estoque
        item_existente = False
        for item in estoque:
            if item['nome'] == opcao:
                item['quantidade'] += quantidade_int
                item_existente = True
                break

        # Se o item não existir, adicioná-lo ao estoque
        if not item_existente:
            estoque.append({"nome": opcao, "quantidade": quantidade_int})

        messagebox.showinfo("Sucesso", f"{quantidade_int} pacote(s) de {opcao} adicionado(s) ao estoque.")

    exibir_estoque()

def corrigir_estoque():
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Criar um rótulo para selecionar o item a ser corrigido
    lbl_selecionar_item = Label(conteudo_frame, text="Selecione um item para corrigir:")
    lbl_selecionar_item.pack(pady=10)

    # Criar um menu dropdown com as opções de estoque
    opcoes_estoque = [item['nome'] for item in estoque]

    selecionar_item = StringVar(conteudo_frame)
    selecionar_item.set(opcoes_estoque[0])  # Definir a primeira opção como padrão

    dropdown_estoque = OptionMenu(conteudo_frame, selecionar_item, *opcoes_estoque)
    dropdown_estoque.pack()

    # Criar botões para editar ou deletar o item selecionado
    btn_editar_item = Button(conteudo_frame, text="Editar Item", command=lambda: editar_item(selecionar_item.get()))
    btn_editar_item.pack(pady=10)

    btn_deletar_item = Button(conteudo_frame, text="Deletar Item", command=lambda: deletar_item(selecionar_item.get()))
    btn_deletar_item.pack(pady=10)

def editar_item(item_atual):
    # Limpar o conteúdo do frame do conteúdo principal
    limpar_conteudo()

    # Criar campos para editar nome e quantidade do item selecionado
    lbl_novo_nome_item = Label(conteudo_frame, text="Novo nome do item:")
    lbl_nova_quantidade_item = Label(conteudo_frame, text="Nova quantidade:")

    entry_novo_nome_item = Entry(conteudo_frame)
    entry_nova_quantidade_item = Entry(conteudo_frame)

    # Função para atualizar o item com os novos valores
    def atualizar_item():
        novo_nome = entry_novo_nome_item.get()
        nova_quantidade = entry_nova_quantidade_item.get()

        # Verificar se o campo de nome está vazio
        if novo_nome.strip() == "":
            messagebox.showerror("Erro", "Digite um novo nome para o item.")
            return

        # Verificar se o campo de quantidade está vazio
        if nova_quantidade.strip() == "":
            messagebox.showerror("Erro", "Digite um valor para a nova quantidade.")
            return

        # Verificar se a quantidade é um número inteiro
        try:
            nova_quantidade_int = int(nova_quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico para a nova quantidade.")
            return

        # Verificar se a quantidade é positiva
        if nova_quantidade_int <= 0:
            messagebox.showerror("Erro", "Digite um valor igual ou maior que 1 para a nova quantidade.")
            return

        # Verificar se o item existe no estoque
        item_existente = False
        for item in estoque:
            if item['nome'] == item_atual:
                item['nome'] = novo_nome
                item['quantidade'] = nova_quantidade_int
                item_existente = True
                break

        if item_existente:
            messagebox.showinfo("Sucesso", f"Item '{item_atual}' corrigido para '{novo_nome}' com a nova quantidade de {nova_quantidade_int} pacote(s).")
        else:
            messagebox.showerror("Erro", f"O item '{item_atual}' não foi encontrado no estoque.")

        exibir_estoque()

    lbl_novo_nome_item.pack()
    entry_novo_nome_item.pack()
    lbl_nova_quantidade_item.pack()
    entry_nova_quantidade_item.pack()

    # Criar botão para confirmar a edição do item
    btn_atualizar_item = Button(conteudo_frame, text="Atualizar Item", command=atualizar_item)
    btn_atualizar_item.pack(pady=10)

def deletar_item(item_atual):
    # Verificar se o item existe no estoque
    item_existente = False
    for item in estoque:
        if item['nome'] == item_atual:
            estoque.remove(item)
            item_existente = True
            break

    if item_existente:
        messagebox.showinfo("Sucesso", f"Item '{item_atual}' deletado do estoque.")
    else:
        messagebox.showerror("Erro", f"O item '{item_atual}' não foi encontrado no estoque.")

    exibir_estoque()   

  # Chamar a função exibir_estoque() com a lista de estoque



def limpar_conteudo():
    # Limpar o conteúdo do frame do conteúdo principal
    for widget in conteudo_frame.winfo_children():
        widget.destroy()

def carregar_estoque():
    global estoque
    try:
        with open(estoque_file, "r") as file:
            estoque = json.load(file)
    except FileNotFoundError:
        estoque = []

def salvar_estoque():
    with open(estoque_file, "w") as file:
        json.dump(estoque, file)

def carregar_imagem_logo():
    global logo_image
    try:
        imagem_logo = Image.open("C:\\Users\\Home\\Desktop\\projeto software chat gpt\\imagens\\logo.png")
        imagem_logo = imagem_logo.resize((500, 293))  # Ajustar o tamanho da imagem
        logo_image = ImageTk.PhotoImage(imagem_logo)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Não foi possível carregar a imagem do logo.")

if __name__ == "__main__":
    # Criando a janela principal
    janela = Tk()
    janela.title("Controle de Gastos e Estoque")
    janela.geometry("1080x720")  # Definindo as dimensões da janela

    # Criando um Frame para o menu
    menu_frame = Frame(janela, bg="lightgray", padx=10, pady=10)
    menu_frame.pack(anchor=NW, fill=Y, side=LEFT)

    # Criando um Frame para a linha de separação
    separador_frame = Frame(janela, height=720, width=2, bg="gray")
    separador_frame.pack(anchor=NW, side=LEFT)

    # Criando um Frame para o conteúdo principal
    conteudo_frame = Frame(janela, padx=10, pady=10)
    conteudo_frame.pack(anchor=NW, fill=BOTH, expand=True, side=LEFT)

    # Carregar a imagem do logo
    carregar_imagem_logo()

    # Adicionar a imagem do logo da empresa
    logo_label = Label(conteudo_frame, image=logo_image)
    logo_label.pack()

    # Criando os botões do menu

    btn_voltar = Button(menu_frame, text="Voltar à Página Inicial", command=voltar_pagina_inicial)
    btn_voltar.pack(pady=10)

    btn_estoque = Button(menu_frame, text="Exibir Estoque", command=exibir_estoque)
    btn_estoque.pack(pady=10)
    
    btn_compra = Button(menu_frame, text="Adicionar Compra", command=adicionar_compra)
    btn_compra.pack(pady=10)

    btn_venda = Button(menu_frame, text="Registrar Venda", command=registrar_venda)
    btn_venda.pack(pady=10)

    # Carregar o estoque
    carregar_estoque()

    # Executar a janela principal
    janela.mainloop()

    # Salvar o estoque antes de fechar a aplicação
    salvar_estoque()
