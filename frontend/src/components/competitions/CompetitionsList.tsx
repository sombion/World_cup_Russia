import { useEffect, useState } from 'react';
import axios from 'axios';
import { Competition, CompetitionsType, CompetitionsDiscipline, Region } from '../../lib/types/competitions';
import styles from './CompetitionsList.module.scss';
import { useNavigate } from 'react-router-dom';

interface Filters {
  date: string;
  discipline: string; 
  type: string;
  region: string;
}

const CompetitionsList = ({ filters, onFiltersChange }: { filters: Filters, onFiltersChange: (filters: Filters) => void }) => {
  const [competitions, setCompetitions] = useState<Competition[]>([]);
  const [regions, setRegions] = useState<{id: number, region_name: string}[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Загрузка данных
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [compResponse, regionsResponse] = await Promise.all([
          axios.get<Competition[]>('/api/competitions/all'),
          axios.get<{regions: Region[]}>('/api/region/all')
        ]);
        
        setCompetitions(compResponse.data);
        setRegions(regionsResponse.data.regions || []);
      } catch (err) {
        setError('Ошибка загрузки данных');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDetailsClick = (competitionId: number) => {
    navigate(`/competitions/detail/${competitionId}`);
  };

  // Фильтрация
  const filteredCompetitions = competitions.filter(comp => {
    const matchesDate = !filters.date || 
      (comp.date_to_start && new Date(comp.date_to_start) >= new Date(filters.date));
    const matchesDiscipline = !filters.discipline || 
      comp.discipline === filters.discipline;
    const matchesType = !filters.type || 
      comp.type === filters.type;
    const matchesRegion = !filters.region || 
      (comp.region_id_list && comp.region_id_list.includes(Number(filters.region)));

    return matchesDate && matchesDiscipline && matchesType && matchesRegion;
  });


  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.formContainer}>
      {/* Фильтры */}
      <div className={styles.filtersSection}>
        <div className={styles.filterGroup}>
          <label>Дата:</label>
          <input
            type="date"
            value={filters.date}
            onChange={(e) => onFiltersChange({...filters, date: e.target.value})}
          />
        </div>

        <div className={styles.filterGroup}>
          <label>Дисциплина:</label>
          <select
            value={filters.discipline}
            onChange={(e) => onFiltersChange({...filters, discipline: e.target.value})}
          >
            <option value="">Все</option>
            {Object.values(CompetitionsDiscipline).map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label>Тип:</label>
          <select
            value={filters.type}
            onChange={(e) => onFiltersChange({...filters, type: e.target.value})}
          >
            <option value="">Все</option>
            {Object.values(CompetitionsType).map(t => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label>Регион:</label>
          <select
            value={filters.region}
            onChange={(e) => onFiltersChange({...filters, region: e.target.value})}
          >
            <option value="">Все</option>
            {regions.map(region => (
              <option key={region.id} value={String(region.id)}>
                {region.region_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Список соревнований */}
      <div className={styles.competitionsList}>
        {filteredCompetitions.map((comp: Competition) => (
          <div key={comp.id} className={styles.competitionCard}>
            <h3>{comp.title}</h3>
            <div className={styles.meta}>
              <span>{new Date(comp.date_to_start).toLocaleDateString()}</span>
              <span>{comp.type}</span>
              <span>{comp.discipline}</span>
            </div>
            <p>{comp.description.substring(0, 100)}...</p>
            <button className={styles.detailsButton}
            onClick={() => handleDetailsClick(comp.id)}>
              Подробнее
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CompetitionsList;