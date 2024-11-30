from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from ...domain.models import Student, StudentCreate, PaginatedResponse
from ...domain.repositories import StudentRepository
from ...infrastructure.database.repositories import get_student_repository

router = APIRouter(prefix="/api/v1")


@router.get("/students", response_model=PaginatedResponse)
async def get_students(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    faculty: Optional[str] = None,
    course: Optional[int] = Query(None, ge=1, le=6),
    repo: StudentRepository = Depends(get_student_repository),
):
    if search or faculty or course:
        students, total = await repo.search_students(
            search or "", page, size, faculty, course
        )
    else:
        students, total = await repo.get_students(page, size)

    pages = (total + size - 1) // size
    return PaginatedResponse(
        items=students, total=total, page=page, size=size, pages=pages
    )


@router.post("/students", response_model=Student, status_code=201)
async def create_student(
    student: StudentCreate, repo: StudentRepository = Depends(get_student_repository)
):
    return await repo.create_student(student)


@router.get("/students/{student_id}", response_model=Student)
async def get_student(
    student_id: int, repo: StudentRepository = Depends(get_student_repository)
):
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentCreate,
    repo: StudentRepository = Depends(get_student_repository),
):
    updated = await repo.update_student(student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/students/{student_id}", status_code=204)
async def delete_student(
    student_id: int, repo: StudentRepository = Depends(get_student_repository)
):
    deleted = await repo.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
