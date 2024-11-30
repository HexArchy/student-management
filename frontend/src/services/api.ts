import axios from 'axios';
import { API_BASE_URL, API_PREFIX } from '../config/api';
import { PaginatedResponse, Student, StudentCreate } from '../types/student';

const api = axios.create({
  baseURL: `${API_BASE_URL}${API_PREFIX}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const studentApi = {
    getStudents: async (
        page: number = 1,
        size: number = 10,
        search?: string,
        course?: number
    ): Promise<PaginatedResponse> => {
        const params = new URLSearchParams();
        
        params.append('page', Math.max(1, page).toString());
        params.append('size', size.toString());

        if (search?.trim()) {
            params.append('search', search.trim());
        }

        if (course !== undefined) {
            params.append('course', course.toString());
        }

        const { data } = await api.get<PaginatedResponse>(`/students?${params}`);
        return {
            ...data,
            pages: Math.max(1, data.pages),  
            page: Math.min(Math.max(1, data.page), data.pages)  
        };
    },

  getStudent: async (id: number): Promise<Student> => {
    const { data } = await api.get<Student>(`/students/${id}`);
    return data;
  },

  createStudent: async (student: StudentCreate): Promise<Student> => {
    const { data } = await api.post<Student>('/students', student);
    return data;
  },

  updateStudent: async (id: number, student: StudentCreate): Promise<Student> => {
    const { data } = await api.patch<Student>(`/students/${id}`, student);
    return data;
  },

  deleteStudent: async (id: number): Promise<void> => {
    await api.delete(`/students/${id}`);
  },
};