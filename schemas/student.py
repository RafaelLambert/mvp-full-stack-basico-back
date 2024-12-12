from pydantic import BaseModel
from typing import  List
from model.student import Student



class StudentSchema(BaseModel):
    """
    Define como um novo produto a ser inserido, deve ser representado
    """
    name:str = "Rafael Marçal"    
    cpf:str = "123.456.789-00"     
    grade_level:str = "1st grade"

class StudentUpdateSchema(BaseModel):
    """
    Define o schema para atualizar as notas de um estudante.
    """
    grade_1: float
    grade_2: float
    grade_3: float
    grade_4: float


class StudentSearchSchema(BaseModel):
    """
    define como deve ser a estrutura que representa a busca que será
    feita apenas com base no nome do produto    
    """
    name:str = "Rafael"
    



def show_students(students:List[Student]):
    """ 
    Retorna uma representação do produto seguindo o schema definido em
    ProdutoViewSchema.
    """
    result = []
    for student in students:
        result.append({
            "id":student.id,
            "name":student.name,
            "cpf":student.cpf,
            "enrollment":student.enrollment,
            "grade_level":student.grade_level,
            "grade_1":student.grade_1,
            "grade_2":student.grade_2,
            "grade_3":student.grade_3,
            "grade_4":student.grade_4,
            "final_average":student.final_average
        })
    return {"students":result}

class StudentViewSchema(BaseModel):
    """ Define como um Student será retornado
    """
    id: int = 1
    name:str = "Rafael"
    cpf:str = "12345678900"
    enrollment:str = "m.2024.1.1"
    grade_level:str = "1st grade"
    grade_1:float = "0"
    grade_2:float = "0"
    grade_3:float = "0"
    grade_4:float = "0"
    final_average:float = "0"

class StudentDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """

    message: str
    name: str
    
def show_student(student:Student):
    """
    Retorna uma representação do produto seguindo o schema definido em
    ProdutoViewSchema.        
    """
    return {
        "id": student.id,
        "name":student.name,
        "cpf":student.cpf,
        "enrollment":student.enrollment,
        "grade_level":student.grade_level,
        "grade_1":student.grade_1,
        "grade_2":student.grade_2,
        "grade_3":student.grade_3,
        "grade_4":student.grade_4,
        "final_average":student.final_average
    }
            

class StudentListSchema(BaseModel):
    """
    Define como uma listagem de produtos será retornada.
    """
    studentsList:List[StudentViewSchema]