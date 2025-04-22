import api from 'axios'
import { AuthResponse, LoginData, RegisterData, User } from '../types/auth';

export const register = async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/register', data, {
        withCredentials: true
    });
    return response.data;
};

export const login = async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/login', data);
    console.log("Login response headers:", response.headers);
    return response.data;
};

export const logout = async (): Promise<void> => {
    await api.post('/api/auth/logout');
}

export const getMe = async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
}