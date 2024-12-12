from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect,Flask
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Student
from logger import logger
from schemas import StudentSchema, StudentUpdateSchema, StudentSearchSchema, StudentViewSchema, StudentListSchema, StudentDelSchema,\
                            show_students, show_student, show_students
from schemas.error import ErrorSchema
from flask_cors import CORS



info = Info(title="API-Stdent", version="0.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
student_tag = Tag(name="Student", description="Tela de cadastro, visualização e consulta do Aluno. Também é possível definir as notas de cada bimestre")

@app.get('/', tags=[home_tag])
def home():
    """"Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/student', tags=[student_tag],
          responses={"200":StudentViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_student(form: StudentSchema):
    """Adiciona um novo Aluno à base de dados

    Retorna uma representação dos students e comentários associados.
    """

    logger.info(form)

    student = Student(
        name = form.name,
        cpf = form.cpf,
        grade_level = form.grade_level
    )
    logger.info(f"Recebido: name={form.name}, cpf={form.cpf}, grade_level={form.grade_level}")

    logger.warning(f"Adicionando estudante de nome: '{student.name}'")

    try:
        # criando conexão com a base
        session = Session()
        logger.warning(session)
        # adicionando student
        session.add(student)
        logger.warning(student)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.warning(f"Adicionado estudante de nome: '{student.name}'")
        return show_student(student), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "estudante de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar estudante '{student.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo estudante :/"
        logger.warning(f"Erro ao adicionar estudante '{student.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/students', tags=[student_tag],
          responses={"200":StudentListSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_students():
    """Faz a busca por todos os Students cadastrados

    Retorna uma representação da listagem de students.
    """
    logger.debug(f"Coletando students")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    students = session.query(Student).all()

    if not students:
        # se não há produtos cadastrados
        return {"students": []}, 200
    else:
        logger.debug(f"%d estudantes econtrados" % len(students))
        # retorna a representação de produto
        print(students)
        return show_students(students), 200
    
@app.get('/student', tags=[student_tag],
         responses={"200": StudentViewSchema, "404": ErrorSchema})
def get_student(query: StudentSearchSchema):
    """Faz a busca por um Student a partir do id do student

    Retorna uma representação dos students e comentários associados.
    """
    student_name = query.name
    logger.debug(f"Coletando dados sobre student #{student_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    student = session.query(Student).filter(Student.name == student_name).first()

    if not student:
        # se o student não foi encontrado
        error_msg = "Student não encontrado na base :/"
        logger.warning(f"Erro ao buscar student '{student_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Student econtrado: '{student.name}'")
        # retorna a representação de student
        return show_student(student), 200
    
@app.delete('/student', tags=[student_tag],
            responses={"200": StudentViewSchema,"404": ErrorSchema})    
def del_student(query: StudentSearchSchema):
    """Deleta um estudante a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    student_name = unquote(unquote(query.name))
    print(student_name)
    logger.debug(f"Deletando dados sobre student #{student_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Student).filter(Student.name == student_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado student #{student_name}")
        return {"message": "Student removido", "name": student_name}
    else:
        # se o produto não foi encontrado
        error_msg = "Student não encontrado na base :/"
        logger.warning(f"Erro ao deletar student #'{student_name}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/student', tags=[student_tag],
         responses={"200": StudentViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_student(query: StudentSearchSchema, form: StudentUpdateSchema):
    """Atualiza as informações de um estudante existente na base de dados

    Retorna a representação do estudante atualizado.
    """
    logger.info("")
    logger.info(query)
    logger.info(form)
    logger.info("")
    student_name = query.name
    logger.debug(f"Atualizando dados do student #{student_name}")
    
    # criando conexão com a base
    session = Session()
    try:

        # buscando o estudante pelo nome
        student = session.query(Student).filter(Student.name == student_name).first()
        
        if not student:
            # se o estudante não for encontrado
            error_msg = "Student não encontrado na base :/"
            logger.warning(f"Erro ao atualizar student '{student_name}', {error_msg}")
            return {"message": error_msg}, 404
        

        # atualizando os campos
        student.grade_1 = form.grade_1
        student.grade_2 = form.grade_2
        student.grade_3 = form.grade_3
        student.grade_4 = form.grade_4
        student.calculate_final_average()
        
        # confirmando as alterações no banco
        session.commit()
        logger.debug(f"Student atualizado: '{student.name}'")
        
        # retorna a representação do estudante atualizado
        return show_student(student), 200
    
    except Exception as e:
        # caso ocorra um erro inesperado
        error_msg = "Não foi possível atualizar o estudante :/"
        logger.error(f"Erro ao atualizar student '{student_name}', {error_msg}: {str(e)}")
        return {"message": error_msg}, 400
    finally:
        # encerrando a sessão
        session.close()

