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
home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc, or RapiDoc")
student_tag = Tag(name="Student", description="Student registration, viewing, and querying screen. It is also possible to define grades for each term")

@app.get('/', tags=[home_tag])
def home():
    """"Redirects to /openapi, a screen that allows selecting the documentation style.
    """
    return redirect('/openapi')

@app.post('/student', tags=[student_tag],
          responses={"200":StudentViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_student(form: StudentSchema):
    """Adds a new Student to the database
    
       Returns a representation of the students.
    """

    logger.info(form)

    student = Student(
        name = form.name,
        cpf = form.cpf,
        grade_level = form.grade_level
    )
    logger.info(f"Received: name={form.name}, cpf={form.cpf}, grade_level={form.grade_level}")

    logger.warning(f"Adding student with name: '{student.name}'")

    try:
        # criando conexão com a base
        session = Session()
        logger.warning(session)
        # adicionando student
        session.add(student)
        logger.warning(student)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.warning(f"Added student with name: '{student.name}'")
        return show_student(student), 200

    except IntegrityError as e:
        # como a duplicidade do CPF é a provável razão do IntegrityError
        error_msg = "Student with the same name already exists in the database :/ "
        logger.warning(f"Error adding student '{student.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Could not save new student :/ "
        logger.warning(f"Error adding student '{student.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/students', tags=[student_tag],
          responses={"200":StudentListSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_students():
    """Fetches all registered Students
     
       Returns a representation of the student list.
    """
    logger.debug(f"Collecting students")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    students = session.query(Student).all()

    if not students:
        # se não há produtos cadastrados
        return {"students": []}, 200
    else:
        logger.debug(f"%d students found" % len(students))
        # retorna a representação de produto
        print(students)
        return show_students(students), 200
    
@app.get('/student', tags=[student_tag],
         responses={"200": StudentViewSchema, "404": ErrorSchema})
def get_student(query: StudentSearchSchema):
    """Fetches a Student based on the given student name
    
       Returns a representation of the students
    """
    student_name = query.name
    logger.debug(f"Collecting data about student #{student_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    student = session.query(Student).filter(Student.name == student_name).first()

    if not student:
        # se o student não foi encontrado
        error_msg = "Student not found in database :/"
        logger.warning(f"Error fetching student '{student_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Student found: '{student.name}'")
        # retorna a representação de student
        return show_student(student), 200
    
@app.delete('/student', tags=[student_tag],
            responses={"200": StudentViewSchema,"404": ErrorSchema})    
def del_student(query: StudentSearchSchema):
    """Deletes a Student based on the given student name

       Returns a representation of the students.
    """
    student_name = unquote(unquote(query.name))
    print(student_name)
    logger.debug(f"Deleting data about student #{student_name}")
    
    session = Session()
    # fazendo a remoção
    count = session.query(Student).filter(Student.name == student_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Student deleted #{student_name}")
        return {"message": "Student removed", "name": student_name}
    else:
        # se o produto não foi encontrado
        error_msg = "Student not found in database :/"
        logger.warning(f"Error deleting student #'{student_name}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/student', tags=[student_tag],
         responses={"200": StudentViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_student(query: StudentSearchSchema, form: StudentUpdateSchema):
    """Updates the information of an existing Student in the database 
    
    Returns the representation of the updated student.
    """
    logger.info("")
    logger.info(query)
    logger.info(form)
    logger.info("")
    student_name = query.name
    logger.debug(f"Updating data of student #{student_name}")
    
    # criando conexão com a base
    session = Session()
    try:

        # buscando o estudante pelo nome
        student = session.query(Student).filter(Student.name == student_name).first()
        
        if not student:
            # se o estudante não for encontrado
            error_msg = "Student not found in database:/"
            logger.warning(f"Error updating student '{student_name}', {error_msg}")
            return {"message": error_msg}, 404
        

        # atualizando os campos
        student.grade_1 = form.grade_1
        student.grade_2 = form.grade_2
        student.grade_3 = form.grade_3
        student.grade_4 = form.grade_4
        student.calculate_final_average()
        
        # confirmando as alterações no banco
        session.commit()
        logger.debug(f"Student updated: '{student.name}'")
        
        # retorna a representação do estudante atualizado
        return show_student(student), 200
    
    except Exception as e:
        # caso ocorra um erro inesperado
        error_msg = "Could not update the student :/"
        logger.error(f"Error updating student '{student_name}', {error_msg}: {str(e)}")
        return {"message": error_msg}, 400
    finally:
        # encerrando a sessão
        session.close()

