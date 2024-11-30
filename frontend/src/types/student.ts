export interface Student {
    id: number;
    last_name: string;
    first_name: string;
    middle_name: string;
    course: number;
    group: string;
    faculty: string;
    created_at: string;
    updated_at: string | null;
  }
  
  export interface StudentCreate {
    last_name: string;
    first_name: string;
    middle_name: string;
    course: number;
    group: string;
    faculty: string;
  }
  
  export interface PaginatedResponse {
    items: Student[];
    total: number;
    page: number;
    size: number;
    pages: number;
  }