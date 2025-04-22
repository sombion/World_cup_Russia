export type UserRole = 'Спортсмены' | 'Региональные представители' | 'Всероссийская Федерация спортивного программирования';

export interface User{
    id: number;
    username: string;
    login: string;
    role: UserRole;
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
}

export interface LoginData{
    login: string;
    password: string;
}