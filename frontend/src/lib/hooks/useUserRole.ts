import { useAuth } from './useAuth';

export const useUserRole = () => {
  const { user } = useAuth();
  
  return {
    isCaptain: user?.role === 'Капитаны',
    isAthlete: user?.role === 'Спортсмены',
    isFederation: user?.role === 'Всероссийская Федерация спортивного программирования',
    userId: user?.id
  };
};