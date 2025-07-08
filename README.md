# SUPERMERCADO

## Descrição
O projeto **SUPERMERCADO** é uma aplicação web desenvolvida em Django, destinada a gerenciar listas de compras. Ele foi criado para solucionar um problema comum dentro de casa: a perda constante do papel com a lista de compras ou o esquecimento desse papel em casa. Com essa aplicação, os usuários podem criar, editar e visualizar suas listas de compras digitalmente, além de adicionar itens com detalhes como quantidade e preço.

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
   python -m venv venv
   source venv/bin/activate  # Linux
   venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o arquivo .env:
   ```bash
   # Crie um arquivo .env na raiz do projeto com as seguintes variáveis
   # (Substitua os valores conforme necessário)
   cp .env.example .env
   # Edite o arquivo .env com um editor de texto
   # Gere uma nova SECRET_KEY com o comando:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
5. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```
6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
7. Acesse a aplicação em seu navegador através de `http://127.0.0.1:8000/`.

## Segurança
Este projeto implementa as seguintes práticas de segurança:

1. **Variáveis de Ambiente**: Informações sensíveis como SECRET_KEY são armazenadas em variáveis de ambiente.
2. **Validação de Senhas**: Implementação de validadores de senha para garantir senhas fortes.
3. **Proteção contra Ataques de Força Bruta**: Limitação de tentativas de login por IP.
4. **Configurações HTTPS**: Em produção, o site força conexões HTTPS.
5. **Proteção contra XSS e CSRF**: Implementação de cabeçalhos de segurança e tokens CSRF.
6. **Cookies Seguros**: Cookies de sessão configurados com flags de segurança.
7. **Expiração de Sessão**: Sessões expiram após um período de inatividade.

## Configurações para Produção
Antes de implantar em produção, certifique-se de:

1. Definir `DEBUG=False` no arquivo .env
2. Configurar um servidor web adequado (Nginx, Apache)
3. Usar um banco de dados mais robusto (PostgreSQL, MySQL)
4. Configurar HTTPS com certificados válidos
5. Atualizar regularmente as dependências

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests.

## Projeto hospedado no pythonanywhere (https://d4nielantoni.pythonanywhere.com/)
