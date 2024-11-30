from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Student, StudentCreate


class StudentRepository(ABC):
    @abstractmethod
    async def get_students(self, page: int, size: int) -> tuple[List[Student], int]:
        pass

    @abstractmethod
    async def get_student(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def create_student(self, student: StudentCreate) -> Student:
        pass

    @abstractmethod
    async def update_student(
        self, student_id: int, student: StudentCreate
    ) -> Optional[Student]:
        pass

    @abstractmethod
    async def delete_student(self, student_id: int) -> bool:
        pass

    @abstractmethod
    async def search_students(
        self,
        query: str,
        page: int,
        size: int,
        faculty: Optional[str] = None,
        course: Optional[int] = None,
    ) -> tuple[List[Student], int]:
        pass
