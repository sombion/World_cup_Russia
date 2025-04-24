import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useAuth } from '../../lib/hooks/useAuth';
import axios from 'axios';
import { CompetitionsType, CompetitionsDiscipline } from '../../lib/types/competitions';
import * as Yup from 'yup';
import { useEffect, useState } from 'react';
import styles from './CreateCompetitionsForm.module.scss';

interface Region {
    id: number;
    region_name: string;
}

interface CompetitionFormValues {
    title: string;
    type: CompetitionsType;
    discipline: CompetitionsDiscipline;
    date_to_start: string;
    description: string;
    max_count_users: number;
    min_age_users: number;
    region_id_list: number[];
    is_published: boolean;
}


const competitionSchema = Yup.object().shape({
  title: Yup.string().required('Обязательное поле'),
  type: Yup.string()
    .oneOf(Object.values(CompetitionsType))
    .required('Обязательное поле'),
  discipline: Yup.string()
    .oneOf(Object.values(CompetitionsDiscipline))
    .required('Обязательное поле'),
  date_to_start: Yup.date()
    .min(new Date(), 'Дата должна быть в будущем')
    .required('Обязательное поле'), 
  description: Yup.string().required('Обязательное поле'),
  max_count_users: Yup.number()
    .min(1, 'Минимум 1 участник')
    .required('Обязательное поле'),
  min_age_users: Yup.number()
    .min(7, 'Минимальный возраст - 7 лет')
    .required('Обязательное поле'),
    region_id_list: Yup.array()
    .of(Yup.number().required())
    .when('type', {
      is: CompetitionsType.REGIONAL,
      then: schema => schema
        .min(1, 'Выберите хотя бы один регион')
        .required('Выберите регионы'),
      otherwise: schema => schema.notRequired().nullable()
    }),
  is_published: Yup.boolean()
});

const initialValues: CompetitionFormValues = {
    title: '',
    type: CompetitionsType.REGIONAL,
    discipline: CompetitionsDiscipline.ALGORITHMIC,
    date_to_start: '',
    description: '',
    max_count_users: 4,
    min_age_users: 7,
    region_id_list: [],
    is_published: false
  };

const CreateCompetitionForm = () => {
  const { user, createCompetition } = useAuth();
  const [regions, setRegions] = useState<Region[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadRegions = async () => {
        if (user?.role === 'Региональные представители') {
            try {
                const response = await axios.get<{ regions: Region[] }>('api/region/all');
                setRegions(response.data.regions || []);
            } catch (err) {
                console.error('Ошибка загрузки регионов:', err);
                setRegions([]);
            }
        }
    };
    loadRegions();
}, [user]);

  const getAvailableTypes = () => {
    switch(user?.role) {
      case 'Всероссийская Федерация спортивного программирования':
        return [CompetitionsType.FEDERAL, CompetitionsType.OPEN];
      case 'Региональные представители':
        return [CompetitionsType.REGIONAL];
      default:
        return [];
    }
  };

  const handleSubmit = async (values: CompetitionFormValues) => {
    try {
      await createCompetition({
        ...values,
        region_id_list: values.type === CompetitionsType.REGIONAL 
          ? values.region_id_list 
          : []
      });
      alert('Соревнование успешно создано!');
    } catch (error) {
        setError('Ошибка при создании соревнования');
      console.error('Ошибка создания:', error);
    }
  };

  const availableTypes = getAvailableTypes();

  if (availableTypes.length === 0) {
    return <div className={styles.error}>У вас нет прав для создания соревнований</div>;
  }

  return (
    <Formik<CompetitionFormValues>
      initialValues={{
        ...initialValues,
        type: availableTypes[0]
      }}
      validationSchema={competitionSchema}
      onSubmit={handleSubmit}
    >
      {({ values, isSubmitting, setFieldValue }) => (
        <Form className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="title">Название соревнования</label>
            <Field name="title" type="text" className={styles.input} />
            <ErrorMessage name="title" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="type">Тип соревнования</label>
            <Field as="select" name="type" className={styles.select}>
              {availableTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </Field>
          </div>

          <div className={styles.field}>
            <label htmlFor="discipline">Дисциплина</label>
            <Field as="select" name="discipline" className={styles.select}>
              {Object.values(CompetitionsDiscipline).map(discipline => (
                <option key={discipline} value={discipline}>{discipline}</option>
              ))}
            </Field>
          </div>

          <div className={styles.field}>
            <label htmlFor="date_to_start">Дата начала</label>
            <Field 
              name="date_to_start" 
              type="datetime-local" 
              className={styles.input} 
            />
            <ErrorMessage name="date_to_start" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="description">Описание</label>
            <Field 
              as="textarea" 
              name="description" 
              rows={4} 
              className={styles.textarea} 
            />
            <ErrorMessage name="description" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="max_count_users">Максимальное количество участников</label>
            <Field 
              name="max_count_users" 
              type="number" 
              min={4} 
              className={styles.input} 
            />
            <ErrorMessage name="max_count_users" component="div" className={styles.error} />
          </div>

          <div className={styles.field}>
            <label htmlFor="min_age_users">Минимальный возраст участников</label>
            <Field 
              name="min_age_users" 
              type="number" 
              min={7} 
              className={styles.input} 
            />
            <ErrorMessage name="min_age_users" component="div" className={styles.error} />
          </div>

          {values.type === CompetitionsType.REGIONAL && (
            <div className={styles.field}>
              <label>Регион</label>
              <select
                multiple
                value={values.region_id_list.map(String)} // Преобразуем числа в строки
                onChange={e => {
                  const options = e.target.options;
                  const selected: number[] = [];
                  for (let i = 0; i < options.length; i++) {
                    if (options[i].selected) {
                      selected.push(Number(options[i].value));
                    }
                  }
                  setFieldValue('region_id_list', selected);
                }}
                className={styles.select}
              >
                {regions.map(region => (
                  <option key={region.id} value={String(region.id)}>
                    {region.region_name}
                  </option>
                ))}
              </select>
              <small>Удерживайте Ctrl/Cmd для выбора</small>
              <ErrorMessage name="region_id_list" component="div" className={styles.error} />
            </div>
          )}

          <div className={styles.checkboxField}>
            <label>
              <Field name="is_published" type="checkbox" />
              Опубликовать сразу
            </label>
          </div>

          {error && <div className={styles.formError}>{error}</div>}

          <button
            type="submit"
            disabled={isSubmitting}
            className={styles.submitButton}
          >
            {isSubmitting ? 'Создание...' : 'Создать соревнование'}
          </button>
        </Form>
      )}
    </Formik>
  );
};

export default CreateCompetitionForm;