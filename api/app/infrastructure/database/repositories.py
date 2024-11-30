from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import List, Optional, Tuple
from fastapi import Depends

from ...domain.repositories import StudentRepository
from ...domain.models import Student, StudentCreate
from .models import StudentModel
from .database import get_session


TRANSLIT_DICT = {
    "a": "а",
    "b": "б",
    "v": "в",
    "g": "г",
    "d": "д",
    "e": "е",
    "yo": "ё",
    "zh": "ж",
    "z": "з",
    "i": "и",
    "j": "й",
    "k": "к",
    "l": "л",
    "m": "м",
    "n": "н",
    "o": "о",
    "p": "п",
    "r": "р",
    "s": "с",
    "t": "т",
    "u": "у",
    "f": "ф",
    "h": "х",
    "ts": "ц",
    "ch": "ч",
    "sh": "ш",
    "sch": "щ",
    "y": "ы",
    "e": "э",
    "yu": "ю",
    "ya": "я",
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


class PostgresStudentRepository(StudentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_search_variants(self, text: str) -> List[str]:
        text = text.lower().strip()
        variants = [text]

        translit_text = ""
        for char in text:
            translit_text += TRANSLIT_DICT.get(char, char)
        if translit_text != text:
            variants.append(translit_text)

        return variants

    async def get_students(self, page: int, size: int) -> Tuple[List[Student], int]:
        query = select(StudentModel).offset((page - 1) * size).limit(size)
        count_query = select(func.count(StudentModel.id))

        result = await self.session.execute(query)
        total = await self.session.execute(count_query)

        students = result.scalars().all()
        return [Student.model_validate(student) for student in students], total.scalar()

    async def get_student(self, student_id: int) -> Optional[Student]:
        query = select(StudentModel).where(StudentModel.id == student_id)
        result = await self.session.execute(query)
        student = result.scalar_one_or_none()
        return Student.model_validate(student) if student else None

    async def create_student(self, student: StudentCreate) -> Student:
        db_student = StudentModel(**student.model_dump())
        self.session.add(db_student)
        await self.session.commit()
        await self.session.refresh(db_student)
        return Student.model_validate(db_student)

    async def update_student(
        self, student_id: int, student: StudentCreate
    ) -> Optional[Student]:
        db_student = await self.get_student(student_id)
        if not db_student:
            return None

        query = select(StudentModel).where(StudentModel.id == student_id)
        result = await self.session.execute(query)
        db_student = result.scalar_one()

        for key, value in student.model_dump().items():
            setattr(db_student, key, value)

        await self.session.commit()
        await self.session.refresh(db_student)
        return Student.model_validate(db_student)

    async def delete_student(self, student_id: int) -> bool:
        db_student = await self.get_student(student_id)
        if not db_student:
            return False

        query = select(StudentModel).where(StudentModel.id == student_id)
        result = await self.session.execute(query)
        db_student = result.scalar_one()

        await self.session.delete(db_student)
        await self.session.commit()
        return True

    async def search_students(
        self,
        query: str,
        page: int,
        size: int,
        faculty: Optional[str] = None,
        course: Optional[int] = None,
    ) -> Tuple[List[Student], int]:
        stmt = select(StudentModel)
        conditions = []

        if query:
            search_terms = query.strip().split()
            if any(char.isdigit() for char in query):
                conditions.append(StudentModel.group.ilike(f"%{query}%"))
            else:
                if len(search_terms) >= 1:
                    name_conditions = []
                    for i, term in enumerate(search_terms):
                        term_conditions = or_(
                            (
                                StudentModel.last_name.ilike(f"%{term}%")
                                if i == 0
                                else False
                            ),
                            (
                                StudentModel.first_name.ilike(f"%{term}%")
                                if i == 1
                                else False
                            ),
                            (
                                StudentModel.middle_name.ilike(f"%{term}%")
                                if i == 2
                                else False
                            ),
                            StudentModel.group.ilike(f"%{term}%"),
                        )
                        name_conditions.append(term_conditions)
                    conditions.append(and_(*name_conditions))

        if faculty:
            faculty = faculty.strip()
            if faculty and not any(char.isdigit() for char in faculty):
                faculty_variants = self._get_search_variants(faculty)
                faculty_conditions = []
                for variant in faculty_variants:
                    faculty_conditions.append(
                        func.lower(StudentModel.faculty).contains(func.lower(variant))
                    )
                conditions.append(or_(*faculty_conditions))

        if course:
            course_condition = StudentModel.course == course
            conditions.append(course_condition)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(
            StudentModel.last_name, StudentModel.first_name, StudentModel.middle_name
        )

        count_query = select(func.count()).select_from(stmt)
        stmt = stmt.offset((page - 1) * size).limit(size)

        result = await self.session.execute(stmt)
        total = await self.session.execute(count_query)

        students = result.scalars().all()
        return [Student.model_validate(student) for student in students], total.scalar()


async def get_student_repository(
    session: AsyncSession = Depends(get_session),
) -> StudentRepository:
    return PostgresStudentRepository(session)
