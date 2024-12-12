from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from logger import logger
from  model import Base

import re

class Student(Base):
    __tablename__= 'student'

    id = Column("pk_produto",Integer, primary_key=True)
    name = Column(String(100))
    cpf = Column(String(11), unique = True)
    enrollment = Column(String(15), unique= True) 
    grade_level = Column(String(10))            
    grade_1 = Column(Float, default = 0)
    grade_2 = Column(Float, default = 0)
    grade_3 = Column(Float, default = 0)
    grade_4 = Column(Float, default = 0)
    final_average = Column(Float, default = 0)

    def __init__(self,name:str, cpf:str, grade_level:str):
        self.name = name
        self.cpf = cpf
        self.grade_level = grade_level
        self.enrollment = self.__create_enrollment(grade_level)
        self.grade_1 = 0
        self.grade_2 = 0
        self.grade_3 = 0
        self.grade_4 = 0
        self.final_average = 0

    def __create_enrollment(self, grade_level: str):
        from  model import Session
        """Cria uma matrícula única para o aluno."""
        this_year = datetime.now().year
        series = self.__transform_grade(grade_level)

        session = Session()
        try:
            # Buscar o maior número sequencial para o ano e série
            last_enrollment = (
                session.query(Student.enrollment)
                .filter(Student.enrollment.like(f"M.{this_year}.{series}.%"))
                .order_by(Student.enrollment.desc())
                .first()
            )
            
            if last_enrollment:
                # Extrair o número sequencial e incrementar
                last_sequence = int(last_enrollment[0].split(".")[-1])
                next_sequence = last_sequence + 1
            else:
                # Caso não exista nenhuma matrícula para o ano e série, começar em 1
                next_sequence = 1

            # Gerar a matrícula única
            return f"M.{this_year}.{series}.{next_sequence:03}"
        finally:
            session.close()  

    def __transform_grade(self, grade_str):
        # Extrai o número no início da string usando regex
        match = re.match(r'^(\d+)st grade$', grade_str.strip())
        if match:
            number = int(match.group(1))  # Converte para inteiro
            return f"{number:02}"  # Formata como dois dígitos com zero à esquerda
        return None  # Retorna None se o formato não for válido

    def calculate_final_average(self):
        self.final_average = (self.grade_1 + self.grade_2 + self.grade_3 + self.grade_4) / 4

