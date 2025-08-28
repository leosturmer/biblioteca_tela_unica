from textual.app import App, SystemCommand
from textual.widgets import Static,  Header, Footer
from textual.binding import Binding

from view import (
    TelaInicial, TelaLeitores, TelaEmprestimos, TelaLivros)


class AppBiblioteca(App):
    CSS_PATH = "biblioteca.tcss"

    SCREENS = {
        "tela_inicial": TelaInicial,
        "tela_livros": TelaLivros,
        "tela_leitores": TelaLeitores,
        "tela_emprestimos": TelaEmprestimos
    }

    def on_mount(self):
        # self.theme = "solarized-light"
        self.push_screen("tela_inicial")


if __name__ == "__main__":
    app = AppBiblioteca()
    app.run()