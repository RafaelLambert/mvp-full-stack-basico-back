
# MVP Back-end - PUC-Rio

Este repositório contém o back-end do projeto MVP proposto pela PUC-Rio. A solução foi desenvolvida utilizando Python com Flask para modelagem do banco de dados e criação das rotas HTTP. O foco do projeto é oferecer um sistema para gerenciar informações de estudantes, incluindo cadastro, atualização de notas, listagem e remoção.

O objetivo deste projeto é demonstrar habilidades de como criar uma API REST, já documentada para o Swagger, para que esta possa ser consumida quando integrada com o Front

---



## Funcionalidades Principais

* **Cadastro de Estudantes:** Possibilidade de adicionar estudantes com informações como nome, CPF e série.
* **Atualização de Notas:** Permite atualizar as notas dos estudantes cadastrados.
* **Consulta de Estudantes:** Listagem e busca individual de estudantes por nome.
* **Remoção de Estudantes:** Deleta registros de estudantes com base no nome informado.
* **Geração de Matrículas:** Gera matrículas únicas baseadas no ano, série e um contador sequencial.
* **Cálculo da média final de cada Estudante:** Calcúla a média aritimética das 4 notas bimestrais de um estudante sempre que uma nota é atualizada.

---



## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** Flask
* **Banco de Dados:** SQLite (SQLAlchemy)
* **Validação de Dados:** Pydantic
* **Documentação da API:** flask-openapi3
* **Controle de CORS:** Flask-CORS

---



## Endpoints da API

### 1. **Documentação**

* **Rota:**`<span>/</span>`
* **Método:**`<span>GET</span>`
* **Descrição:** Redireciona para a interface de documentação (Swagger, Redoc ou RapiDoc).

### 2. **Cadastro de Estudantes**

* **Rota:**`<span>/student</span>`
* **Método:**`<span>POST</span>`
* **Descrição:** Adiciona um novo estudante à base de dados.
* **Exemplo de Corpo:**
  ```
  {
    "name": "João Silva",
    "cpf": "12345678901",
    "grade_level": "1st grade"
  }
  ```

### 3. **Listagem de Estudantes**

* **Rota:**`<span>/students</span>`
* **Método:**`<span>GET</span>`
* **Descrição:** Retorna a lista de estudantes cadastrados (com paginação).
* **Exemplo da response:**
  ```
  {
    "students": [
      {
        "cpf": "600.366.330-89",
        "enrollment": "M.2024.09.001",
        "final_average": 0,
        "grade_1": 0,
        "grade_2": 0,
        "grade_3": 0,
        "grade_4": 0,
        "grade_level": "9st grade",
        "id": 2,
        "name": "Bernardo"
      },
      {
        "cpf": "166.538.310-00",
        "enrollment": "M.2024.07.001",
        "final_average": 2.5,
        "grade_1": 10,
        "grade_2": 0,
        "grade_3": 0,
        "grade_4": 0,
        "grade_level": "7st grade",
        "id": 3,
        "name": "Ana"
      }
    ]
  }
  ```

### 4. **Busca Individual de Estudantes**

* **Rota:**`<span>/student</span>`
* **Método:**`<span>GET</span>`
* **Descrição:** Busca um estudante pelo nome.
* **Parâmetros de Query:**
  * `<span>name</span>`: Nome do estudante.

### 5. **Atualização de Notas**

* **Rota:**`<span>/student</span>`
* **Método:**`<span>PUT</span>`
* **Descrição:** Atualiza as notas de um estudante cadastrado.
* **Exemplo de Corpo:**
  ```
  {
    "grade_1": 8.0,
    "grade_2": 7.5,
    "grade_3": 9.0,
    "grade_4": 8.5
  }
  ```
* **Parâmetros de Query:**
  * `<span>name</span>`: Nome do estudante.

### 6. **Remoção de Estudantes**

* **Rota:**`<span>/student</span>`
* **Método:**`<span>DELETE</span>`
* **Descrição:** Remove um estudante da base de dados.
* **Parâmetros de Query:**
  * `<span>name</span>`: Nome do estudante.

---




## Como Executar o Projeto

### Requisitos Pré-requisitos:

* Python 3.10+
* pip (Python Package Installer)

### Passos:

1. Certifiqui-se que o python esta intalado:

   ```
   python --version
   ```

   1. Caso não esteja instale o python seguindo o passo a passo de acordo com o seu sistema operacional
2. Certifique-se que o pip esta intalado:

   ```
   pip --version
   ```

   1. Caso não esteja instale o python seguindo digitanto o prompt de comado de acordo com o seu sistema operacional
3. Clone este repositório:

   ```
   git clone <https://github.com/RafaelLambert/mvp-full-stack-basico-back>
   ```
4. Crie e ative um ambiente virtual:

   ```
   python -m venv env
   source env/bin/activate # No Windows: .env\Scripts\activate
   ```
5. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```
6. Inicie o banco de dados:

   ```
   python
   >>> from model.config import Base, engine
   >>> Base.metadata.create_all(engine)
   >>> exit()
   ```
7. Execute a aplicação:

   ```
   flask run --host 0.0.0.0 --port 5000
   ```

A aplicação estará disponível em [http://127.0.0.1:5000]().

---



## Licença

Este projeto foi desenvolvido como parte de um MVP para a PUC-Rio e é de uso educacional.
