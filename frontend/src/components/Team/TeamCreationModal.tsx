import React, { useState } from 'react';
import axios from 'axios';
import styles from './TeamCreationModal.module.scss';

interface UserSearchResult {
  id: number;
  login: string;
  username: string;
}

interface TeamCreationModalProps {
  maxMembers: number;
  onClose: () => void;
  onSubmit: (data: {
    name: string;
    description: string;
    users_id_list: number[];
  }) => void;
}

const TeamCreationModal: React.FC<TeamCreationModalProps> = ({ 
  maxMembers,
  onClose, 
  onSubmit 
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<UserSearchResult[]>([]);
  const [selectedUsers, setSelectedUsers] = useState<UserSearchResult[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);

  const handleSearch = async (query: string) => {
    if (query.length < 3) {
      setSearchResults([]);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await axios.get(`/api/users/search?query=${query}`);
      setSearchResults(response.data);
    } catch (err) {
      console.error('Ошибка поиска:', err);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedUsers.length === 0) {
      alert('Добавьте хотя бы одного участника');
      return;
    }

    onSubmit({
      name,
      description,
      users_id_list: selectedUsers.map(user => user.id)
    });
  };

  const addUser = (user: UserSearchResult) => {
    if (selectedUsers.length >= maxMembers) {
      alert(`Максимальное количество участников: ${maxMembers}`);
      return;
    }
    if (!selectedUsers.some(u => u.id === user.id)) {
      setSelectedUsers([...selectedUsers, user]);
    }
  };

  const removeUser = (userId: number) => {
    setSelectedUsers(selectedUsers.filter(user => user.id !== userId));
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <button className={styles.closeButton} onClick={onClose}>×</button>
        <h2>Создать новую команду</h2>
        
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label>Название команды *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              maxLength={100}
            />
          </div>

          <div className={styles.formGroup}>
            <label>Описание</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={500}
            />
          </div>

          <div className={styles.formGroup}>
            <label>Добавить участников (макс. {maxMembers}) *</label>
            <div className={styles.searchContainer}>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  handleSearch(e.target.value);
                }}
                placeholder="Поиск по логину или имени..."
              />
              {searchLoading && <div className={styles.searchLoading}>Поиск...</div>}
            </div>

            {searchResults.length > 0 && (
              <div className={styles.searchResultsContainer}>
                <div className={styles.searchResultsHeader}>Найдено:</div>
                <ul className={styles.searchResults}>
                  {searchResults.map(user => (
                    <li key={user.id} className={styles.searchResultItem}>
                      <div className={styles.userInfo}>
                        <div className={styles.userName}>{user.username}</div>
                        <div className={styles.userLogin}>@{user.login}</div>
                      </div>
                      <button
                        type="button"
                        className={styles.addUserButton}
                        onClick={() => addUser(user)}
                        disabled={selectedUsers.some(u => u.id === user.id)}
                      >
                        {selectedUsers.some(u => u.id === user.id) ? 'Добавлен' : 'Добавить'}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {selectedUsers.length > 0 && (
            <div className={styles.selectedUsersContainer}>
              <div className={styles.selectedUsersHeader}>
                Выбранные участники: {selectedUsers.length}/{maxMembers}
              </div>
              <ul className={styles.selectedUsers}>
                {selectedUsers.map(user => (
                  <li key={user.id} className={styles.selectedUserItem}>
                    <div className={styles.userInfo}>
                      <div className={styles.userName}>{user.username}</div>
                      <div className={styles.userLogin}>@{user.login}</div>
                    </div>
                    <button
                      type="button"
                      className={styles.removeUserButton}
                      onClick={() => removeUser(user.id)}
                    >
                      ×
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className={styles.formActions}>
            <button type="button" className={styles.cancelButton} onClick={onClose}>
              Отмена
            </button>
            <button type="submit" className={styles.submitButton}>
              Создать команду
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TeamCreationModal;