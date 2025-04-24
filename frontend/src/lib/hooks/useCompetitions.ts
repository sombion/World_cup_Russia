import { useState, useEffect } from 'react';
import axios from 'axios';
import { Region } from '../types/competitions';
import { getCompetitions } from '../../lib/api/competitionService';

const useCompetitions = () => {
  const [competitions, setCompetitions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCompetitions = async () => {
      try {
        const data = await getCompetitions();
        setCompetitions(data);
      } catch (err) {
        if (err instanceof Error){
        setError(err.message);
        } else {
            setError('Произошла неизвестная ошибка');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCompetitions();
  }, []);

  return { competitions, loading, error };
};
export const useRegions = () => {
    const [regions, setRegions] = useState<Region[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
  
    useEffect(() => {
      const fetchRegions = async () => {
        try {
          const response = await axios.get<{ regions: Region[] }>('/api/region/all');
          setRegions(response.data.regions || []);
        } catch (err) {
          setError('Не удалось загрузить регионы');
          console.error('Ошибка загрузки регионов:', err);
        } finally {
          setLoading(false);
        }
      };
  
      fetchRegions();
    }, []);
  
    return { regions, loading, error };
  };
  
export default useCompetitions;