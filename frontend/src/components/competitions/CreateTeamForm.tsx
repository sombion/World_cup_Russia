// import { useState } from 'react';
// import styles from './CompetitionDetailForm.module.scss';

// interface Props {
//   competitionId: number;
//   onSubmit: (data: { name: string; description: string; users_id_list: number[] }) => void;
//   onClose: () => void;
// }

// export const CreateTeamForm = ({ competitionId, onSubmit, onClose }: Props) => {
//   const [name, setName] = useState('');
//   const [description, setDescription] = useState('');
//   const [members, setMembers] = useState('');

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();
//     onSubmit({
//       name,
//       description,
//       users_id_list: members.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id))
//     });
//   };

//   return (
//     <div className={styles.modalOverlay}>
//       <div className={styles.modalContent}>
//         <h2>Создать команду</h2>
//         <form onSubmit={handleSubmit}>
//           <div className={styles.formGroup}>
//             <label>Название команды:</label>
//             <input
//               type="text"
//               value={name}
//               onChange={(e) => setName(e.target.value)}
//               required
//             />
//           </div>

//           <div className={styles.formGroup}>
//             <label>Описание:</label>
//             <textarea
//               value={description}
//               onChange={(e) => setDescription(e.target.value)}
//             />
//           </div>

//           <div className={styles.formGroup}>
//             <label>ID участников (через запятую):</label>
//             <input
//               type="text"
//               value={members}
//               onChange={(e) => setMembers(e.target.value)}
//               placeholder="Например: 1, 2, 3"
//             />
//           </div>

//           <div className={styles.formActions}>
//             <button type="button" onClick={onClose} className={styles.cancelButton}>
//               Отмена
//             </button>
//             <button type="submit" className={styles.submitButton}>
//               Отправить на модерацию
//             </button>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// };