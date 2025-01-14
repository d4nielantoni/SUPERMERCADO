# SUPERMERCADO

## Descrição
O projeto SUPERMERCADO é uma aplicação web desenvolvida em Django, destinada a gerenciar listas de compras. Os usuários podem criar, editar e visualizar suas listas de compras, além de adicionar itens com detalhes como quantidade e preço.

## Tecnologias Utilizadas
- **Django**: Framework web utilizado para o desenvolvimento da aplicação.
- **Python**: Linguagem de programação utilizada.
- **SQLite**: Banco de dados padrão utilizado para armazenar as informações.

## Como Usar
1. Clone o repositório:
   ```bash
   git clone https://github.com/d4nielantoni/SUPERMERCADO.git
   cd SUPERMERCADO
   ```
2. Ative o ambiente virtual:
   ```bash
   source venv/Scripts/activate  # Para Git Bash
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```
5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
6. Acesse a aplicação em seu navegador através de `http://127.0.0.1:8000/`.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests.
