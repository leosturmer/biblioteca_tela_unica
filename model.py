class Biblioteca():
    def __init__(self):
        self.livros = dict()
        self.leitores = dict()

    def cadastrar_livro(self, cod, titulo):
        livro = Livro()
        livro.set_cod(cod)
        livro.set_titulo(titulo)
        try:
            self.livros[cod]
        except KeyError:
            self.livros[livro.cod] = livro
            return True
        return False

    def consultar_livro(self, cod):
        try:
            return self.livros[cod]
        except KeyError:
            return False

    def excluir_livro(self, cod):
        try:
            del self.livros[cod]
            return True
        except KeyError:
            return False

    def get_titulo_livro(self, cod):
        titulo = str()
        try:
            titulo = self.livros[cod].titulo
        except KeyError:
            return ""

        return titulo

    def atualizar_livro(self, cod, titulo):
        try:
            self.livros[cod]
            self.excluir_livro(cod)
            self.cadastrar_livro(cod, titulo)
        except KeyError:
            return True
        return False

    def cadastrar_leitor(self, cpf, nome):
        leitor = Leitor()
        leitor.set_cpf(cpf)
        leitor.set_nome(nome)

        try:
            self.leitores[cpf]
        except KeyError:
            self.leitores[leitor.cpf] = leitor
            return True
        return False

    def consultar_leitor(self, cpf):
        try:
            return self.leitores[cpf]
        except KeyError:
            return False

    def excluir_leitor(self, cpf):
        try:
            del self.leitores[cpf]
            return True
        except KeyError:
            return False

    def atualizar_leitor(self, cpf, nome):
        try:
            self.leitores[cpf]
            self.excluir_leitor(cpf)
            self.cadastrar_leitor(cpf, nome)
        except KeyError:
            return True
        return False

    def get_nome_leitor(self, cpf):
        nome = str()
        try:
            nome = self.leitores[cpf].nome
        except KeyError:
            return ""

        return nome

    def calcular_data_devolucao(self):
        import datetime
        hoje = datetime.date.today()
        tempo_de_emprestimo = datetime.timedelta(weeks=1)
        data_de_devolucao = hoje + tempo_de_emprestimo

        return data_de_devolucao.strftime("%d-%m-%Y")

    def emprestar(self, livro, leitor):
        data_de_devolucao = self.calcular_data_devolucao()

        try:
            livro_emprestado = self.livros[livro]
            livro_emprestado.set_emprestado()
            return Emprestimo(livro, leitor, data_de_devolucao)
        except KeyError:
            return None

    def devolver(self, livro, leitor):
        try:
            livro_devolvido = self.livros[livro]
            leitor_devolvendo = self.leitores[leitor]
            livro_devolvido.set_devolvido()
            leitor_devolvendo.del_emprestimo(livro_devolvido)
        except KeyError:
            return None

    def teste_do_emprestimo(self, cod):
        try:
            emprestado = biblioteca.livros[cod].emprestado
        except KeyError:
            return ""
        return emprestado


class Livro():
    def __init__(self):
        self.emprestado = False

    def set_titulo(self, titulo):
        self.titulo = titulo

    def set_cod(self, cod):
        self.cod = cod

    def set_emprestado(self):
        self.emprestado = True

    def set_devolvido(self):
        self.emprestado = False


class Leitor():
    def __init__(self):
        self.emprestimos = list()

    def add_emprestimo(self, emprestimo):
        self.emprestimos.append(emprestimo)

    def del_emprestimo(self, emprestimo):
        for livro in self.emprestimos:
            if livro.cod == emprestimo:
                self.emprestimos.pop(emprestimo)

    def set_nome(self, nome):
        self.nome = nome

    def set_cpf(self, cpf):
        self.cpf = cpf


class Emprestimo():
    def __init__(self, livro, leitor, data_devolucao):
        self.livro = livro
        self.leitor = leitor
        self.data_devolucao = data_devolucao

# Inicializar a biblioteca / conectar à model da biblioteca


biblioteca = Biblioteca()