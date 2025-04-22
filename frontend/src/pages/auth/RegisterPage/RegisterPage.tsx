import { Link } from 'react-router-dom';
import RegisterForm from '../../../components/auth/RegisterForm/RegisterForm';
import styles from './RegisterPage.module.scss';

const RegisterPage = () => {
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Регистрация</h1>
        <RegisterForm />
        <div className={styles.footer}>
          <span>Уже есть аккаунт?</span>
          <Link to="/login" className={styles.link}>
            Войдите
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;