import React from 'react';
import { CompetitionDetail } from '../../lib/types/competitions';
import styles from './CompetitionDetailForm.module.scss';

interface CompetitionDetailFormProps {
  competition: CompetitionDetail;
}

const CompetitionDetailForm: React.FC<CompetitionDetailFormProps> = ({ competition }) => {
    const formatDate = (dateString: string) => {
      try {
        const date = new Date(dateString);
        return isNaN(date.getTime()) ? 'Дата не указана' : date.toLocaleDateString('ru-RU');
      } catch {
        return 'Дата не указана';
      }
    };

  const regions = competition.region || [];
  const hasRegions = regions.length > 0;

  return (
    <div className={styles.competitionInfo}>
      <h1>{competition.title || 'Название не указано'}</h1>
      
      <div className={styles.competitionMeta}>
        {/* <span className={styles.competitionType}>{competition.type}</span> */}
        <span className={styles.competitionDiscipline}>{competition.discipline || 'Дисциплина не указано'}</span>
      </div>

      <div className={styles.competitionDates}>
        <div>
          <span className={styles.dateLabel}>Дата создания:</span>
          <span>{formatDate(competition.date_to_create)}</span>
        </div>
        <div>
          <span className={styles.dateLabel}>Дата начала:</span>
          <span>{formatDate(competition.date_to_start)}</span>
        </div>
      </div>

      <div className={styles.competitionDescription}>
        <h3>Описание:</h3>
        <p>{competition.description || 'Описание не указано'}</p>
      </div>

      <div className={styles.competitionRestrictions}>
        <h3>Ограничения:</h3>
        <p>Максимальное количество участников: {competition.max_count_users || 'Не указано'}</p>
        <p>Минимальный возраст участников: {competition.min_age_users || 'Не указано'}</p>
      </div>

      {hasRegions && (
        <div className={styles.competitionRegions}>
          <h3>Регионы:</h3>
          <ul>
            {competition.region.map((region, index) => (
              <li key={index}>{region.region_name || 'Не указан'}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default CompetitionDetailForm;