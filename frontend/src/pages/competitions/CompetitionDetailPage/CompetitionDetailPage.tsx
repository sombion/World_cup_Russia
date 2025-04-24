import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios, {AxiosError} from 'axios';
import { CompetitionDetail, Team, User, CreateTeamData } from '../../../lib/types/competitions';
import CompetitionDetailForm from '../../../components/competitions/CompetitionDetailForm';
import TeamCreationModal from '../../../components/Team/TeamCreationModal';
import JoinTeamModal from '../../../components/Team/JoinTeamModal';
import {IndividualApplicationModal} from '../../../components/Team/IndividualApplicationModal';
import styles from './CompetitionDetailPage.module.scss';

const CompetitionDetailPage: React.FC = () => {
  const { competitionId } = useParams<{ competitionId: string }>();
  const [competition, setCompetition] = useState<CompetitionDetail | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [showIndividualModal, setShowIndividualModal] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [competitionResponse, teamsResponse, userResponse] = await Promise.all([
          axios.get(`/api/competitions/detail/${competitionId}`),
          axios.get(`/api/team/need-players/${competitionId}`),
          axios.get('/api/auth/me')
        ]);

        setCompetition(competitionResponse.data || null);
        setTeams(Array.isArray(teamsResponse.data) ? teamsResponse.data : teamsResponse.data?.teams || []);
        setCurrentUser(userResponse.data || null);
        setLoading(false);
      } catch (err) {
        const error = err as AxiosError<{message?: string}>
        setError(error.response?.data?.message || error.message);
        setLoading(false);
      }
    };

    if (competitionId) {
        fetchData();
      } else {
        setError('ID соревнования не указан');
        setLoading(false);
      }  }, [competitionId]);

  const handleCreateTeam = async (teamData: Omit<CreateTeamData, 'competitions_id' | 'status'>) => {
    try {
      const createTeamData: CreateTeamData = {
        ...teamData,
        competitions_id: Number(competitionId),
        status: 'Заполнена',
        captain_id: currentUser?.role === 'Капитаны' ? currentUser.id : undefined
      };

      const response = await axios.post('/api/team/create', createTeamData);
      setTeams([...teams, response.data]);
      setShowTeamModal(false);
    } catch (err) {
      const error = err as AxiosError<{message?: string}>
      alert(error.response?.data?.message || 'Ошибка при создании команды');
    }
  };

  const handleJoinTeam = async (teamId: number) => {
    try {
      await axios.post('/api/user-in-teams/accept-users', {
        users_in_teams_id: teamId
      });
      alert('Заявка на вступление подана!');
      setShowJoinModal(false);
      
      const response = await axios.get(`/api/competitions/${competitionId}/teams`);
      setTeams(Array.isArray(response.data) ? response.data : response.data?.teams || []);
    } catch (err) {
      const error = err as AxiosError<{message?: string}>
      alert(error.response?.data?.message || 'Ошибка при подаче заявки');
    }
  };

  const handleIndividualApplication = async () => {
    try {
      if (!currentUser) throw new Error('Пользователь не авторизован');
      if (!competitionId) throw new Error('ID соревнования не указан');

      await axios.post('/api/team/create', {
        name: `${currentUser.username} (индивидуально)`,
        description: 'Индивидуальная заявка',
        competitions_id: Number(competitionId),
        users_id_list: [currentUser.id],
        status: 'Заполнена'
      });

      alert('Индивидуальная заявка подана!');
      setShowIndividualModal(false);
      
      const response = await axios.get(`/api/competitions/${competitionId}/teams`);
      setTeams(response.data);
    } catch (err) {
      const error = err as AxiosError<{message?: string}>
      alert(error.response?.data?.message || 'Ошибка при подаче заявки');
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;
  if (!competition) return <div className={styles.notFound}>Соревнование не найдено</div>;

  return (
    <div className={styles.competitionDetailContainer}>
      <CompetitionDetailForm competition={competition} />

      <div className={styles.teamsSection}>
        <h2>Зарегистрированные команды</h2>
        {teams.length === 0 ? (
          <p>Пока нет зарегистрированных команд</p>
        ) : (
          <ul className={styles.teamsList}>
            {teams.map(team => (
              <li key={team.id} className={styles.teamItem}>
                <div className={styles.teamHeader}>
                  <h3>{team.name}</h3>
                  <span className={styles.teamStatus}>{team.status}</span>
                </div>
                <p className={styles.teamCaptain}>Капитан: {team.username} ({team.login})</p>
                {team.description && <p className={styles.teamDescription}>{team.description}</p>}
                
                <div className={styles.teamMembers}>
                  <h4>Участники ({team.members?.length || 0}/{competition.max_count_users}):</h4>
                  {team.members?.length ? (
                    <ul className={styles.membersList}>
                      {team.members.map(member => (
                        <li key={member.user_id} className={styles.memberItem}>
                          <div className={styles.memberInfo}>
                            <div className={styles.userName}>{member.username}</div>
                            <div className={styles.userLogin}>@{member.login}</div>
                          </div>
                          {member.status && (
                            <span className={`${styles.memberStatus} ${styles[member.status.toLowerCase()]}`}>
                              {member.status}
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>Нет участников</p>
                  )}
                </div>

                {currentUser?.role === 'Спортсмены' && (
                  <button 
                    onClick={() => {
                      setSelectedTeam(team);
                      setShowJoinModal(true);
                    }}
                    className={styles.joinButton}
                  >
                    Присоединиться
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className={styles.actionsSection}>
        {currentUser?.role === 'Капитаны' && (
          <button 
            onClick={() => setShowTeamModal(true)}
            className={styles.createTeamButton}
          >
            Создать команду
          </button>
        )}
        {currentUser?.role === 'Спортсмены' && (
          <button 
            onClick={() => setShowIndividualModal(true)}
            className={styles.individualApplicationButton}
          >
            Подать индивидуальную заявку
          </button>
        )}
      </div>

      {showTeamModal && competition && (
        <TeamCreationModal
          maxMembers={competition.max_count_users}
          onClose={() => setShowTeamModal(false)}
          onSubmit={handleCreateTeam}
        />
      )}

      {showJoinModal && selectedTeam && (
        <JoinTeamModal
          team={selectedTeam}
          onClose={() => setShowJoinModal(false)}
          onJoin={() => handleJoinTeam(selectedTeam.id)}
        />
      )}

      {showIndividualModal && (
        <IndividualApplicationModal
          onClose={() => setShowIndividualModal(false)}
          onSubmit={handleIndividualApplication}
        />
      )}
    </div>
  );
};

export default CompetitionDetailPage;