import React from 'react';
import { Team } from '../../lib/types/competitions';
import styles from './JoinTeamModal.module.scss';

interface JoinTeamModalProps {
  team: Team;
  onClose: () => void;
  onJoin: () => void;
}

const JoinTeamModal: React.FC<JoinTeamModalProps> = ({ team, onClose, onJoin }) => {
  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <button className={styles.closeButton} onClick={onClose}>×</button>
        <h2>Присоединиться к команде</h2>
        <div className={styles.teamInfo}>
          <h3>{team.name}</h3>
          <p className={styles.teamMeta}>
            <span>Капитан: {team.username} ({team.login})</span>
            <span className={styles.teamStatus}>{team.status}</span>
          </p>
          {team.description && <p className={styles.teamDescription}>{team.description}</p>}
          
          <div className={styles.teamMembers}>
            <h4>Участники:</h4>
            <ul>
              {team.members.map(member => (
                <li key={member.user_id} className={styles.memberItem}>
                  <div className={styles.memberInfo}>
                    <div className={styles.userName}>{member.username}</div>
                    <div className={styles.userLogin}>@{member.login}</div>
                  </div>
                  <span className={`${styles.memberStatus} ${styles[member.status.toLowerCase()]}`}>
                    {member.status}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className={styles.modalActions}>
          <button onClick={onJoin} className={styles.joinButton}>Подать заявку</button>
          <button onClick={onClose} className={styles.cancelButton}>Отмена</button>
        </div>
      </div>
    </div>
  );
};

export default JoinTeamModal;