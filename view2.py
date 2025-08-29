from textual.app import (App, SystemCommand, ComposeResult)
from textual.widgets import (
    Static,  Header, Footer, Button, TabbedContent, TabPane, Input, Label, Select)
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import (
    Container,  HorizontalGroup, VerticalGroup, ScrollableContainer, Grid, )

from model import biblioteca

class TelaGeral(Screen):

    def compose(self):
        with VerticalGroup():

            with VerticalGroup():
                yield Static("📖  Biblioteca  📖", id="st_header_livros")

            with HorizontalGroup():
                yield Select([
                    ("Livros", "livros"),
                    ("Leitores", "leitores"),
                    ("Empréstimos", "emprestimos")
                ], id="sel_funcoes", allow_blank=False, value="livros")

                yield Select([
                    ("Cadastrar", "cadastrar"),
                    ("Atualizar", "atualizar"),
                    ("Pesquisar", "pesquisar"),
                    ("Excluir", "excluir")
                ], id="sel_opcao", allow_blank=False, value="cadastrar")

            yield Label("Título do livro:", id="lbl_nome")
            yield Input(placeholder="digite aqui...", id="ip_nome")
            yield Label("Código do livro:", id="lbl_cod")
            yield Input(placeholder="digite aqui...", id="ip_codigo")

            yield Static(f"Situação do livro", id="stt_situacao")

            with HorizontalGroup(id="grupo_botoes"):
                yield Button("Ok", variant="primary", id="bt_executar")
                yield Button("Limpar", variant="primary", id="bt_limpar")

            with VerticalGroup(id="botao_sair"):
                yield Button("Sair", id="bt_sair")

# Métodos gerais

    def pegar_select_funcao(self):
        funcao = self.query_one("#sel_funcoes", Select).value
        return funcao

    def pegar_select_operacao(self):
        opcao = self.query_one("#sel_opcao", Select).value
        return opcao

    def pegar_input(self):
        titulo = self.query_one("#ip_nome", Input).value
        cod = self.query_one("#ip_codigo", Input).value
        return titulo, cod

    def acao_limpar(self):
        self.query_one("#ip_nome", Input).value = ""
        self.query_one("#ip_codigo", Input).value = ""
        self.query_one("#sel_opcao").focus()

    def on_select_changed(self, event: Select.Changed):

        match event.select.id:
            case "sel_funcoes":
                valor = self.query_one("#sel_funcoes", Select).value

                match valor:
                    case "livros":
                        self.query_one("#lbl_nome", Label).update(
                            "Título do livro:")
                        self.query_one("#lbl_cod", Label).update(
                            "Código do livro:")
                    case "leitores":
                        self.query_one("#lbl_nome", Label).update(
                            "Nome do leitor:")
                        self.query_one("#lbl_cod", Label).update(
                            "CPF do leitor:")
                    case "emprestimos":
                        self.query_one("#lbl_nome", Label).update(
                            "Código do livro:")
                        self.query_one("#lbl_cod", Label).update(
                            "CPF do leitor:")

# Métodos livro

    def acao_cadastro_livro(self):
        titulo, cod = self.pegar_input()

        stt_situacao = self.query_one("#stt_situacao", Static)

        if titulo == "" or cod == "":
            self.notify("Ops! Preencha todos os campos!")
        elif biblioteca.cadastrar_livro(cod, titulo) == True:
            stt_situacao.update(
                f"{biblioteca.get_titulo_livro(cod)} cadastrado com sucesso!")
        elif biblioteca.cadastrar_livro(cod, titulo) == False:
            stt_situacao.update(
                f"Código {cod} já cadastrado! Título: [i]{biblioteca.get_titulo_livro(cod)}[/]")

    def acao_atualizar_livro(self):
        titulo, cod = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if titulo == "" or cod == "":
            self.notify("Ops! Preencha todos os campos!")
        elif biblioteca.atualizar_livro(cod, titulo) == False:
            stt_situacao.update(
                f"{biblioteca.get_titulo_livro(cod)} atualizado com sucesso!")
        elif biblioteca.atualizar_livro(cod, titulo) == True:
            stt_situacao.update(f"Não cadastrado")

    def acao_pesquisar_livro(self):
        titulo, cod = self.pegar_input()
        livro = biblioteca.consultar_livro(cod)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if titulo == "" or cod == "":
            self.notify("Ops! Preencha todos os campos!")
        elif livro:
            stt_situacao.update(
                f"Livro cadastrado: [i]{livro.titulo}[/], código {livro.cod}")
        else:
            stt_situacao.update(f"Código não cadastrado")

    def acao_excluir_livro(self):
        titulo, cod = self.pegar_input()
        livro = biblioteca.consultar_livro(cod)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if titulo == "" or cod == "":
            self.notify("Ops! Preencha todos os campos!")
        elif livro:
            cod = self.query_one("#ip_codigo", Input).value
            biblioteca.excluir_livro(cod)
            stt_situacao.update("Livro excluído!")
        else:
            stt_situacao.update("Livro não encontrado!")

# Métodos leitor

    def acao_cadastro_leitor(self):
        nome, cpf = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if nome == "" or cpf == "":
            self.notify("Ops! Preencha todos os campos!")
        elif biblioteca.cadastrar_leitor(cpf, nome) == True:
            stt_situacao.update(
                f"Leitor {biblioteca.get_nome_leitor(cpf)} cadastrado com sucesso!")
        elif biblioteca.cadastrar_leitor(cpf, nome) == False:
            stt_situacao.update(
                f"CPF {cpf} já cadastrado! Leitor: [i]{biblioteca.get_titulo_livro(cpf)}[/]")

    def acao_atualizar_leitor(self):
        nome, cpf = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if nome == "" or cpf == "":
            self.notify("Ops! Preencha todos os campos!")
        elif biblioteca.atualizar_leitor(cpf, nome) == False:
            stt_situacao.update(
                f"{biblioteca.get_nome_leitor(cpf)} atualizado com sucesso!")
        elif biblioteca.atualizar_leitor(cpf, nome) == True:
            stt_situacao.update(f"Não cadastrado")

    def acao_pesquisar_leitor(self):
        nome, cpf = self.pegar_input()
        leitor = biblioteca.consultar_leitor(cpf)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if nome == "" or cpf == "":
            self.notify("Ops! Preencha todos os campos!")
        elif leitor:
            stt_situacao.update(
                f"Leitor cadastrado: [i]{leitor.nome}[/], CPF {leitor.cpf}")
        else:
            stt_situacao.update(f"Código não cadastrado")

    def acao_excluir_leitor(self):
        nome, cpf = self.pegar_input()
        leitor = biblioteca.consultar_leitor(cpf)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if nome == "" or cpf == "":
            self.notify("Ops! Preencha todos os campos!")
        elif leitor:
            cpf = self.query_one("#ip_codigo", Input).value
            biblioteca.excluir_livro(cpf)
            stt_situacao.update("Leitor excluído!")
        else:
            stt_situacao.update("Leitor não encontrado!")

# Métodos empréstimo

    def texto_do_emprestimo(self):
        cod, cpf = self.pegar_input()
        emprestado = biblioteca.teste_do_emprestimo(cod)

        leitor = biblioteca.get_nome_leitor(cpf)
        livro = biblioteca.get_titulo_livro(cod)

        if emprestado == True:
            emprestado = "emprestado"
        elif emprestado == False:
            emprestado = "na biblioteca"
        elif emprestado == "":
            self.notify("Dados não encontrados!")

        return f"""
Digite o código do livro e CPF para consultar a situação

Nome do leitor: {leitor}
Título do livro: {livro}
Situação: {emprestado}
"""

    def acao_cadastrar_emprestimo(self):
        cod, cpf = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if cpf == "" or cod == "":
            self.notify("Insira os dados do empréstimo!")
        else:
            biblioteca.emprestar(cod, cpf)
            stt_situacao.update(self.texto_do_emprestimo())
            
    def acao_atualizar_emprestimo(self):
        cod, cpf = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if cpf == "" or cod == "":
            self.notify("Insira os dados do empréstimo!")
        else:
            biblioteca.devolver(cod, cpf)
            stt_situacao.update(self.texto_do_emprestimo())

# Ações controller


    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_sair":
                self.app.exit()

            case "bt_limpar":
                self.acao_limpar()

            case "bt_executar":
                funcao = self.pegar_select_funcao()
                operacao = self.pegar_select_operacao()

                match funcao:
                    case "livros":
                        match operacao:
                            case "cadastrar":
                                self.acao_cadastro_livro()
                            case "atualizar":
                                self.acao_atualizar_livro()
                            case "pesquisar":
                                self.acao_pesquisar_livro()
                            case "excluir":
                                self.acao_excluir_livro()

                    case "leitores":
                        match operacao:
                            case "cadastrar":
                                self.acao_cadastro_leitor()
                            case "atualizar":
                                self.acao_atualizar_leitor()
                            case "pesquisar":
                                self.acao_pesquisar_leitor()
                            case "excluir":
                                self.acao_excluir_leitor()

                    case "emprestimos":
                        match operacao:
                            case "cadastrar":
                                self.acao_cadastrar_emprestimo()
                            case "atualizar":
                                self.acao_atualizar_emprestimo()
                            case "pesquisar":
                                self.notify("Operação não disponível")
                            case "excluir":
                                self.notify("Operação não disponível")