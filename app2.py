from textual.app import App, SystemCommand
from textual.widgets import Static,  Header, Footer
from textual.binding import Binding

from view2 import (TelaGeral)


class AppBiblioteca(App):
    CSS_PATH = "biblioteca2.tcss"

    SCREENS = {"tela_livros": TelaGeral}

    def on_mount(self):
        self.theme = "gruvbox"
        self.push_screen("tela_livros")


if __name__ == "__main__":
    app = AppBiblioteca()
    app.run()