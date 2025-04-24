import React from 'react';
import styles from './IndividualApplicationModal.module.scss';

interface IndividualApplicationModalProps {
  onClose: () => void;
  onSubmit: () => void;
}

export const IndividualApplicationModal: React.FC<IndividualApplicationModalProps> = ({ onClose, onSubmit }) => {
  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <button className={styles.closeButton} onClick={onClose}>×</button>
        <h2>Подать индивидуальную заявку</h2>
        <div className={styles.modalBody}>
          <p>Вы уверены, что хотите подать индивидуальную заявку на участие в соревновании?</p>
          <p>После подачи заявки вы сможете присоединиться к команде или создать свою.</p>
        </div>
        <div className={styles.modalActions}>
          <button onClick={onSubmit} className={styles.submitButton}>Подать заявку</button>
          <button onClick={onClose} className={styles.cancelButton}>Отмена</button>
        </div>
      </div>
    </div>
  );
};
