import { Formik, Form, Field, ErrorMessage } from 'formik';
import { RegisterData, UserRole, Region } from '../../../lib/types/auth';
import * as Yup from 'yup';
import { useAuth } from '../../../lib/hooks/useAuth';
import styles from './RegisterForm.module.scss';
import { useEffect, useState } from 'react';
import axios from 'axios';

const roleOptions = [
  { value: 'Спортсмены', label: 'Спортсмены' },
  { value: 'Региональные представители', label: 'Региональные представители' },
  { value: 'Всероссийская Федерация спортивного программирования', label: 'Всероссийская Федерация спортивного программирования' },
];

const RegisterSchema = Yup.object().shape({
  username: Yup.string()
    .min(1, 'Минимум 1 символ')
    .max(50, 'Максимум 50 символов')
    .required('Обязательное поле'),
  login: Yup.string()
    .min(4, 'Минимум 4 символа')
    .max(20, 'Максимум 20 символов')
    .matches(/^[a-zA-Z0-9]+$/, 'Только латинские буквы и цифры')
    .required('Обязательное поле'),
  password: Yup.string()
    .min(1, 'Минимум 1 символ')
    .required('Обязательное поле'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Пароли должны совпадать')
    .required('Обязательное поле'),
  role: Yup.string()
    .oneOf(['Спортсмены', 'Региональные представители', 'Всероссийская Федерация спортивного программирования'], 'Неверная роль' as const)
    .required('Обязательное поле'),
  age: Yup.number()
    .when('role', {
      is: (role: string) => role === 'Спортсмены',
      then: (schema) => schema
        .required('Укажите возраст')
        .min(10, 'Минимальный возраст - 10 лет')
        .integer('Введите целое число'),
      otherwise: (schema) => schema.nullable()
    }),
    region_id: Yup.number()
  .when('role', {
    is: 'Региональные представители',
    then: schema => schema
      .required('Выберите регион')
      .typeError('Выберите регион'),
    otherwise: schema => schema.nullable()
  })
});

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const RegionSelect = ({ regions, role, field, form }: any) => {
  if (role === 'Всероссийская Федерация спортивного программирования') {
    return null;
  }

  return (
    <div className={styles.field}>
      <label htmlFor="region_id" className={styles.label}>
        Регион
      </label>
      <select
        {...field}
        className={styles.select}
        onChange={(e) => {
          const value = e.target.value ? Number(e.target.value) : null;
          form.setFieldValue(field.name, value);
        }}
        value={field.value || ''}
      >
        <option value="">Выберите регион</option>
        {regions.map((region: Region) => (
          <option key={region.id} value={region.id}>
            {region.region_name}
          </option>
        ))}
      </select>
      <ErrorMessage name="region_id" component="div" className={styles.error} />
    </div>
  );
};

const RegisterForm = () => {
  const { handleRegister } = useAuth();
  const [regions, setRegions] = useState<Region[]>([]);
  const [loadingRegions, setLoadingRegions] = useState(false);

  useEffect(() => {
    const fetchRegions = async () => {
      setLoadingRegions(true);
      try {
        const response = await axios.get<{ regions: Region[] }>('/api/region/all');
        setRegions(response.data.regions);
      } catch (error) {
        console.error('Ошибка загрузки регионов:', error);
      } finally {
        setLoadingRegions(false);
      }
    };
    fetchRegions();
  }, []);

  return (
    <Formik
      initialValues={{
        username: '',
        login: '',
        password: '',
        confirmPassword: '',
        role: 'Спортсмены' as UserRole,
        age: null,
        region_id: null
      }}
      validationSchema={RegisterSchema}
      onSubmit={async (values, { setSubmitting, setErrors }) => {
        try {
          const registerData: RegisterData = {
            username: values.username,
            login: values.login,
            password: values.password,
            role: values.role,
            ...(values.role === 'Спортсмены' && { age: values.age }),
            region_id: values.role === 'Всероссийская Федерация спортивного программирования' 
              ? null
              : values.region_id
          };
          await handleRegister(registerData);
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (error) {
          setErrors({
            login: 'Ошибка регистрации',
            password: 'Ошибка регистрации',
            ...(values.role === 'Спортсмены' && { age: 'Ошибка в возрасте' }),
            ...(values.role === 'Региональные представители' && { region_id: 'Ошибка в выборе региона' })
          });
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting, values }) => (
        <Form className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="username" className={styles.label}>
              ФИО
            </label>
            <Field
              name="username"
              type="text"
              className={styles.input}
            />
            <ErrorMessage name="username" component="div" className={styles.error} />
          </div>

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

          <div className={styles.field}>
            <label htmlFor="confirmPassword" className={styles.label}>
              Подтвердите пароль
            </label>
            <Field
              name="confirmPassword"
              type="password"
              className={styles.input}
            />
            <ErrorMessage name="confirmPassword" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="role" className={styles.label}>
              Роль
            </label>
            <Field
              as="select"
              name="role"
              className={styles.select}
            >
              {roleOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Field>
          </div>

          {values.role === 'Спортсмены' && (
            <div className={values.role === 'Спортсмены' ? styles.field : styles.hidden}>
            <label htmlFor="age" className={styles.label}>
              Возраст *
            </label>
            <Field
              name="age"
              type="number"
              min="10"
              max="99"
              className={styles.input}
            />
            <ErrorMessage name="age" component="div" className={styles.error} />
          </div>
          )}
          {values.role !== 'Всероссийская Федерация спортивного программирования' && !loadingRegions && regions.length > 0 && (
            <Field
              name="region_id"
              component={RegionSelect}
              regions={regions}
              role={values.role}
            />
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className={styles.registerButton}
          >
            {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </Form>
      )}
    </Formik>
  );
};
export default RegisterForm;