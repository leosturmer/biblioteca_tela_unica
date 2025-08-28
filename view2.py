from textual.app import (App, SystemCommand, ComposeResult)
from textual.widgets import (
    Static,  Header, Footer, Button, TabbedContent, TabPane, Input, Label, Select)
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import (
    Container,  HorizontalGroup, VerticalGroup, ScrollableContainer, Grid, )

from textual import on

from model import biblioteca
from controller import controller_livros


class TelaInicial(Screen):
    def compose(self):
        yield Static("📚 Biblioteca 📚", id="titulo_inicial")

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Livros", id="bt_livros", classes="botoes_inicial", variant="primary")
            yield Button("Leitores", id="bt_leitores", classes="botoes_inicial", variant="success")
            yield Button("Empréstimos", id="bt_emprestimos", classes="botoes_inicial", variant="warning")
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_livros":
                self.app.switch_screen("tela_livros")
            case "bt_leitores":
                self.app.switch_screen("tela_leitores")
            case "bt_emprestimos":
                self.app.switch_screen("tela_emprestimos")
            case "bt_sair":
                self.app.exit()

class TelaLivros(Screen):

    def compose(self):
        
        yield Static("📖  Livros da biblioteca  📖", id="st_header_livros", classes="stt_header_telas")

        yield Select([
            ("Livros", "livros"),
            ("Leitores", "leitores"),
            ("Empréstimos", "emprestimos")
        ], id="sel_funcoes", allow_blank=True)


        yield Select([
            ("Cadastrar", "cadastrar"),
            ("Atualizar", "atualizar"),
            ("Pesquisar", "pesquisar"),
            ("Excluir", "excluir")
        ], id="sel_opcao", allow_blank=True)

    
        yield Label("Título do livro:", id="lbl_nome")
        yield Input(placeholder="digite aqui...", id="ip_titulo")
        yield Label("Código do livro:", id="lbl_cod")
        yield Input(placeholder="digite aqui...", id="ip_codigo")

        yield Static(f"Situação do livro", id="stt_situacao")

        with HorizontalGroup():
            yield Button("Ok", id="bt_executar")
            yield Button("Limpar", id="bt_limpar")

        with HorizontalGroup(id="container_botao"):
            yield Button("Voltar", variant="primary", id="bt_tela_inicial")

    def pegar_select(self):
        opcao = self.query_one("#sel_opcao", Select).value

        if opcao == Select.BLANK:
            self.notify("Selecione uma opção")
        else:
            return opcao

    def pegar_input(self):
        titulo = self.query_one("#ip_titulo", Input).value
        cod = self.query_one("#ip_codigo", Input).value

        if titulo == "" or cod == "":
            self.notify("Insira os dados do livro!")

        else:
            return titulo, cod

    def acao_cadastro_livro(self):
        titulo, cod = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if biblioteca.cadastrar_livro(cod, titulo) == True:
            stt_situacao.update(
                f"{biblioteca.get_titulo_livro(cod)} cadastrado com sucesso!")
        elif biblioteca.cadastrar_livro(cod, titulo) == False:
            stt_situacao.update(
                f"Código {cod} já cadastrado! Título: [i]{biblioteca.get_titulo_livro(cod)}[/]")
            
    def acao_atualizar_livro(self):
        titulo, cod = self.pegar_input()
        stt_situacao = self.query_one("#stt_situacao", Static)

        if biblioteca.atualizar_livro(cod, titulo) == False:
            stt_situacao.update(
                f"{biblioteca.get_titulo_livro(cod)} atualizado com sucesso!")
        elif biblioteca.atualizar_livro(cod, titulo) == True:
            stt_situacao.update(f"Não cadastrado")

    def acao_pesquisar_livro(self):
        titulo, cod = self.pegar_input()
        livro = biblioteca.consultar_livro(cod)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if livro:
            stt_situacao.update(
                f"Livro cadastrado: [i]{livro.titulo}[/], código {livro.cod}")
        else:
            stt_situacao.update(f"Código não cadastrado")

    def acao_excluir_livro(self):
        titulo, cod = self.pegar_input()
        livro = biblioteca.consultar_livro(cod)
        stt_situacao = self.query_one("#stt_situacao", Static)

        if livro:
            cod = self.query_one("#ip_codigo", Input).value
            biblioteca.excluir_livro(cod)
            stt_situacao.update("Livro excluído!")
        else:
            stt_situacao.update("Livro não encontrado!")

    def acao_limpar(self):
        self.query_one("#ip_titulo", Input).value = ""
        self.query_one("#ip_codigo", Input).value = ""
        self.query_one("#sel_opcao").focus()

    def on_select_changed(self, event: Select.Changed):
        
        match event.select.id:
            case "sel_funcoes":
                valor = self.query_one("#sel_funcoes", Select).value

                match valor:
                    case "livros":
                        self.query_one("#lbl_nome", Label)
                        self.query_one("#lbl_cod", Label)
                    case "leitores":
                        self.query_one("#lbl_nome", Label).update("Nome do leitor:")
                        self.query_one("#lbl_cod", Label).update("CPF do leitor:")
                    case "emprestimos":
                        self.query_one("#lbl_nome", Label).update("Código do livro:")
                        self.query_one("#lbl_cod", Label).update("CPF do leitor:")

            case "sel_opcao":
                opcao = self.query_one("#sel_opcao", Select).value

                match opcao:
                    case "cadastrar":
                        cadastrar = self.acao_cadastro_livro()
                        return cadastrar
                    case "atualizar":
                        self.acao_atualizar_livro()
                    case "pesquisar":
                        self.acao_pesquisar_livro()
                    case "excluir":
                        self.acao_excluir_livro()



    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_tela_inicial":
                self.app.switch_screen("tela_inicial")

            case "bt_executar":
                self.pegar_input()
                opcao = self.pegar_select()

                match opcao:
                    case "cadastrar":
                        self.acao_cadastro_livro()
                    case "atualizar":
                        self.acao_atualizar_livro()
                    case "pesquisar":
                        self.acao_pesquisar_livro()
                    case "excluir":
                        self.acao_excluir_livro()

            case "bt_limpar":
                self.acao_limpar()


class TelaLeitores(Screen):
    def compose(self):

        yield Static("🙇‍♂️🙋  Leitores da biblioteca  🧏‍♀️💁‍♂️", id="st_header_emprestimos", classes="stt_header_telas")

        yield Select([
            ("Cadastrar", "cadastrar"),
            ("Atualizar", "atualizar"),
            ("Pesquisar", "pesquisar"),
            ("Excluir", "excluir")
        ], id="sel_opcao", allow_blank=True)

    
        yield Label("Nome do leitor:")
        yield Input(placeholder="digite aqui...", id="ip_nome")
        yield Label("CPF do leitor:")
        yield Input(placeholder="digite aqui...", id="ip_cpf")

        yield Static(f"Situação do livro", id="stt_situacao")

        with HorizontalGroup():
            yield Button("Ok", id="bt_executar")
            yield Button("Limpar", id="bt_limpar")

        with HorizontalGroup(id="container_botao"):
            yield Button("Voltar", variant="primary", id="bt_tela_inicial")
            


    

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_tela_inicial":
                self.app.switch_screen("tela_inicial")

            case "bt_cadastro_leitor":
                nome = self.query_one("#ip_cadastro_nome", Input).value
                cpf = self.query_one("#ip_cadastro_cpf", Input).value

                if nome == "" or cpf == "":
                    self.notify("Insira os dados do leitor!")
                elif biblioteca.cadastrar_leitor(cpf, nome) == True:
                    self.notify(
                        f"{biblioteca.get_nome_leitor(cpf)} cadastrado com sucesso!")
                elif biblioteca.cadastrar_leitor(cpf, nome) == False:
                    self.notify(
                        f"CPF {cpf} já cadastrado! Usuário: {biblioteca.get_nome_leitor(cpf)}")

            case "bt_atualizar_leitor":
                nome = self.query_one("#ip_atualizar_nome", Input).value
                cpf = self.query_one("#ip_atualizar_cpf", Input).value

                if nome == "" or cpf == "":
                    self.notify("Insira os dados do leitor!")
                else:
                    if biblioteca.atualizar_leitor(cpf, nome) == False:
                        self.notify(
                            f"{biblioteca.get_nome_leitor(cpf)} atualizado com sucesso!")
                    elif biblioteca.atualizar_livro(cpf, nome) == True:
                        self.notify(f"Não cadastrado")

            case "bt_consultar_leitor":
                cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                leitor = biblioteca.consultar_leitor(cpf)
                stt_situacao = self.query_one("#stt_situacao", Static)

                if cpf == "":
                    self.notify("Insira o CPF do leitor!")
                elif leitor:
                    stt_situacao.update(
                        f"Leitor cadastrado: [i]{leitor.nome}[/], CPF {leitor.cpf}")
                else:
                    stt_situacao.update(f"CPF não cadastrado")

            case "bt_excluir_leitor":
                cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                leitor = biblioteca.consultar_leitor(cpf)

                if cpf == "":
                    self.notify("Insira o CPF do leitor!")
                elif leitor:
                    cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                    biblioteca.excluir_leitor(cpf)
                    self.notify("Leitor excluído!")
                else:
                    self.notify("Leitor não encontrado!")


class TelaEmprestimos(Screen):
    def compose(self):
        with HorizontalGroup(id="container_botao"):
            yield Button("Voltar", variant="warning", id="bt_tela_inicial")

        yield Static("🔄📗  Empréstimos da biblioteca  📗🔄", id="st_header_emprestimos", classes="stt_header_telas")

        with TabbedContent(initial="tab_emprestimos"):
            with TabPane("Visualizar empréstimos", id="tab_emprestimos"):
                with HorizontalGroup():
                    yield Label("Código do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_cod_emprestimo")

                with HorizontalGroup():
                    yield Label("CPF do leitor:")
                    yield Input(placeholder="digite aqui...", id="ip_cpf_emprestimo")

                yield Static("""
Digite o código do livro e CPF para consultar a situação

Nome do leitor:
Título do livro: 
Situação:
""", id="stt_situacao")

                with HorizontalGroup():
                    yield Button("Emprestar", id="bt_emprestar", classes="grupo_botoes_pesquisa")
                    yield Button("Devolver", id="bt_devolver", classes="grupo_botoes_pesquisa")

    def dados_input_emprestimos(self):
        cpf = self.query_one("#ip_cpf_emprestimo", Input).value
        cod = self.query_one("#ip_cod_emprestimo", Input).value

        return cpf, cod

    def on_button_pressed(self, event: Button.Pressed):
        cpf, cod = self.dados_input_emprestimos()

        stt_situacao = self.query_one("#stt_situacao", Static)

        match event.button.id:
            case "bt_tela_inicial":
                self.app.switch_screen("tela_inicial")

            case "bt_emprestar":
                if cpf == "" or cod == "":
                    self.notify("Insira os dados do empréstimo!")
                else:
                    biblioteca.emprestar(cod, cpf)
                    stt_situacao.update(self.texto_do_emprestimo())

            case "bt_devolver":
                if cpf == "" or cod == "":
                    self.notify("Insira os dados do empréstimo!")
                else:
                    biblioteca.devolver(cod, cpf)
                    stt_situacao.update(self.texto_do_emprestimo())

    def texto_do_emprestimo(self):
        cpf, cod = self.dados_input_emprestimos()
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
