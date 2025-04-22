import { Link } from 'react-router-dom';
import LoginForm from '../../../components/auth/LoginForm/LoginForm';
import styles from './LoginPage.module.scss';

const LoginPage = () => {
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Вход в систему</h1>
        <LoginForm />
        <div className={styles.footer}>
          <span>Нет аккаунта?</span>
          <Link to="/register" className={styles.link}>
            Зарегистрируйтесь
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;