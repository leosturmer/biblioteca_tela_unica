from textual.widgets import (Select, Input, Static)
from textual.widget import Widget
from textual.app import App

from model import biblioteca

class ControllerLivros(App):
    def pegar_select(self):
        opcao = self.query_one("#sel_opcao", Select).value

        if opcao == Select.BLANK:
            self.notify("Selecione uma opção")
        else:
            return opcao

    def pegar_input(self):
        titulo = self.app.query_one("#ip_titulo", Input).value
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




controller_livros = ControllerLivros()