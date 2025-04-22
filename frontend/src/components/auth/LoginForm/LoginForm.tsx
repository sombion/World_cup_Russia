import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useAuth } from '../../../lib/hooks/useAuth';
import styles from './LoginForm.module.scss';

const LoginSchema = Yup.object().shape({
  login: Yup.string().required('Введите логин'),
  password: Yup.string().required('Введите пароль'),
});

const LoginForm = () => {
  const { handleLogin } = useAuth();

  return (
    <Formik
      initialValues={{ login: '', password: '' }}
      validationSchema={LoginSchema}
      onSubmit={async (values, { setSubmitting, setErrors }) => {
        try {
          await handleLogin(values);
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (error) {
          setErrors({
            login: 'Неверный логин или пароль',
            password: 'Неверный логин или пароль',
          });
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="login" className={styles.label}>
              Логин
            </label>
            <Field
              name="login"
              type="text"
              className={styles.input}
            />
            <ErrorMessage name="login" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="password" className={styles.label}>
              Пароль
            </label>
            <Field
              name="password"
              type="password"
              className={styles.input}
            />
            <ErrorMessage name="password" component="div" className={styles.error} />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className={styles.loginButton}
          >
            {isSubmitting ? 'Вход...' : 'Войти'}
          </button>
        </Form>
      )}
    </Formik>
  );
};

export default LoginForm;