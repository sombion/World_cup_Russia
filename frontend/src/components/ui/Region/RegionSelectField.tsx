import { Field, useField, useFormikContext } from 'formik';
import { UserRole, Region } from '../../../lib/types/auth';
import styles from './Region.module.scss'

interface RegionSelectFieldProps {
  name: string;
  label: string;
  regions: Region[];
  userRole: UserRole;
}

export const RegionSelectField = ({
  name,
  label,
  regions,
  userRole
}: RegionSelectFieldProps) => {
  const { setFieldValue } = useFormikContext();
  const [field] = useField(name);

  if (userRole === 'Всероссийская Федерация спортивного программирования') {
    return null; // Для ФСП не показываем выбор региона
  }

  return (
    <div className={styles.field}>
      <label htmlFor={name}>{label}</label>
      <Field
        as="select"
        name={name}
        className={styles.select}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
          const value = e.target.value ? Number(e.target.value): null;
          setFieldValue(name, value);
        }}
        value={field.value || ''}
      >
        {/* <option value="">Не выбрано</option> */}
        {regions.map(region => (
          <option 
            key={region.id} 
            value={region.id}
          >
            {region.region_name}
          </option>
        ))}
      </Field>
      {/* <small className={styles.hint}>
        {userRole === 'Региональные представители' 
          ? 'Удерживайте Ctrl/Cmd для выбора нескольких регионов'
          : 'Выберите один регион'}
      </small> */}
    </div>
  );
};