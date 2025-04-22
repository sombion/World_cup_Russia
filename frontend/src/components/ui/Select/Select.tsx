import { FieldProps } from 'formik';

interface SelectProps extends FieldProps {
  options: Array<{ value: string; label: string }>;
  className?: string;
}

const Select = ({ field, form, options, className }: SelectProps) => {
  return (
    <select
      {...field}
      className={className}
      onChange={(e) => form.setFieldValue(field.name, e.target.value)}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default Select;