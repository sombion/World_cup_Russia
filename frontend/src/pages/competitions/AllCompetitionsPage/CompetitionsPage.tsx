import { useState } from 'react';
import CompetitionsList from '../../../components/competitions/CompetitionsList';
import styles from './CompetitionsPage.module.scss';

const CompetitionsPage = () => {
  const [filters, setFilters] = useState({
    date: '',
    discipline: '',
    type: '',
    region: ''
  });

  return (
    <div className={styles.pageContainer}>
      <h1 className={styles.pageTitle}>Все соревнования</h1>
      <CompetitionsList 
        filters={filters}
        onFiltersChange={setFilters}
      />
    </div>
  );
};

export default CompetitionsPage;