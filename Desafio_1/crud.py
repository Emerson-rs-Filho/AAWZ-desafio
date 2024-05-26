import sqlite3

class Vendedor:
    def __init__(self, nome, cpf, nascimento, email, estado):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email
        self.estado = estado

class VendedorCRUD:
    def __init__(self, vendedor: str = "vendedores.db"):
        self.conexao = sqlite3.connect(vendedor)
        self.creat_table()

    # Criação da tabela
    def creat_table(self):
        self.conexao.execute('''CREATE TABLE IF NOT EXISTS vendedores
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                nascimento TEXT NOT NULL,
                email TEXT NOT NULL,
                estado TEXT NOT NULL) ''')
        self.conexao.commit()

    # Criação do vendedor
    def criar_vendedor(self, vendedor: Vendedor):
        self.conexao.execute('''
            INSERT INTO vendedores (nome, cpf, nascimento, email, estado) VALUES(?, ?, ?, ?, ?)
        ''', (vendedor.nome, vendedor.cpf, vendedor.nascimento, vendedor.email, vendedor.estado))
        self.conexao.commit()

    # Leitura da tabela
    def ler_tab(self, cpf: str):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT nome, cpf, nascimento, email, estado FROM vendedores WHERE cpf = ?', (cpf,))
        row = cursor.fetchone()
        if row:
            return Vendedor(*row)
        return None

    # Atualização do vendedor
    def update_vendedor(self, cpf: str, vendedor: Vendedor):
        self.conexao.execute('''
            UPDATE vendedores
            SET nome = ?, nascimento = ?, email = ?, estado = ?
            WHERE cpf = ?
        ''', (vendedor.nome, vendedor.nascimento, vendedor.email, vendedor.estado, cpf))
        self.conexao.commit()

    # Delet do vendedor
    def delete_vendedor(self, cpf: str):
        self.conexao.execute('DELETE FROM vendedores WHERE cpf = ?', (cpf,))
        self.conexao.commit()

    # Listagem dos vendedores
    def listar_vendedores(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT nome, cpf, nascimento, email, estado FROM vendedores')
        vendedores = cursor.fetchall()
        return [Vendedor(*vendedor) for vendedor in vendedores]

    def close(self):
        self.conexao.close()

    # Menu
    def menu(self):
        print("\n1. Adicionar vendedor")
        print("2. Listar vendedores")
        print("3. Atualizar vendedor")
        print("4. Deletar vendedor")
        print("5. Sair")

    def criar_tabela(self):
        while True:
            self.menu()
            selecao = input("Escolha uma opção: ")

            if selecao == '1':
                nome = input("Digite o nome do vendedor: ")
                cpf = input("Digite o CPF do vendedor: ")
                nascimento = input("Digite a data de nascimento : ")
                email = input("Digite o email do vendedor: ")
                estado = input("Digite o estado do vendedor: ")
                vendedor = Vendedor(nome, cpf, nascimento, email, estado)
                self.criar_vendedor(vendedor)
                print("Vendedor adicionado com sucesso!")

            elif selecao == '2':
                print("\nTodos os vendedores:")
                vendedores = self.listar_vendedores()
                for vendedor in vendedores:
                    print(f'Nome: {vendedor.nome}, CPF: {vendedor.cpf}, Nascimento: {vendedor.nascimento}, Email: {vendedor.email}, Estado: {vendedor.estado}')
                
            elif selecao == '3':
                cpf = input("Digite o CPF do vendedor a ser atualizado: ")
                nome = input("Digite o novo nome do vendedor: ")
                nascimento = input("Digite a nova data de nascimento: ")
                email = input("Digite o novo email do vendedor: ")
                estado = input("Digite o novo estado do vendedor: ")
                vendedor = Vendedor(nome, cpf, nascimento, email, estado)
                self.update_vendedor(cpf, vendedor)
                print("Vendedor atualizado com sucesso!")

            elif selecao == '4':
                cpf = input("Digite o CPF do vendedor a ser deletado: ")
                self.delete_vendedor(cpf)
                print("Vendedor deletado com sucesso!")

            elif selecao == '5':
                print("Saindo do programa...")
                break

            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

        self.close()


if __name__ == "__main__":
    crud = VendedorCRUD()
    crud.criar_tabela()
