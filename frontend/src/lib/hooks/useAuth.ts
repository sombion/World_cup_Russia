    import { useState, useEffect } from "react";
    import { useNavigate } from "react-router-dom";
    import { register, login, logout, getMe } from "../api/authService";
    import { User, RegisterData, LoginData } from "../types/auth";

    export const useAuth = () => {
        const [user, setUser] = useState<User | null>(null);
        const [isLoading, setIsLoading] = useState(true);
        const [error, setError] = useState<string | null>(null);
        const navigate = useNavigate();

        useEffect(() => {
            let isMounted = true;

            const checkAuth = async () => {
                try {
                    const userData = await getMe();
                    if (isMounted) {
                        setUser(userData);
                    }
                } catch (error) {
                    if (isMounted) {
                        setUser(null);
                        setError('Ошибка проверки аутентификации');
                        console.error('Auth check error:', error);
                    }
                } finally {
                    if (isMounted) {
                        setIsLoading(false);
                    }
                }
            };

            checkAuth();

            return () => {
                isMounted = false; // Очистка при размонтировании
            };
        }, []);

        const handleRegister = async (data: RegisterData) => {
            try {
                setIsLoading(true);
                const response = await register({
                    username: data.username,
                    login: data.login,
                    password: data.password,
                    role: data.role,
                    ...(data.role === 'Спортсмены' && {age: data.age})
                });
                if (!response?.user){
                    throw new Error('Регистрация не пройдена - нет информации о пользователе')
                }
                setUser(response.user);
                navigate('/');
            } catch (error) {
                setError('Ошибка регистрации');
                throw error;
            } finally {
                setIsLoading(false);
            }
        };

        const handleLogin = async (data: LoginData) => {
            try {
                setIsLoading(true);
                const response = await login(data);
                setUser(response.user);
                navigate('/');
            } catch (error) {
                setError('Ошибка входа');
                throw error;
            } finally {
                setIsLoading(false);
            }
        };

        const handleLogout = async () => {
            try {
                setIsLoading(true);
                await logout();
                setUser(null);
                navigate('/login');
            } catch (error) {
                setError('Ошибка выхода');
                throw error;
            } finally {
                setIsLoading(false);
            }
        };

        return { user, isLoading, error, handleRegister, handleLogin, handleLogout };
    };