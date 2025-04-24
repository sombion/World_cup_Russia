export type UserRole = 'Спортсмены' | 'Региональные представители' | 'Всероссийская Федерация спортивного программирования';

export interface Region{
    id: number;
    region_name: string
}
export interface User{
    id: number;
    username: string;
    login: string;
    role: UserRole;
    region_id?: number | null;
    age?: number | null;
}

export interface AuthResponse{
    user: User;
    access_token: string;
}

export interface RegisterData{
    username: string;
    login: string;
    password: string;
    role: UserRole;
    age?: number | null;
    region_id?: number | null;
}

export interface LoginData{
    login: string;
    password: string;
}