import { ButtonHTMLAttributes } from 'react';
import styles from './Button.module.scss';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

const Button = ({ variant = 'primary', className = '', ...props }: ButtonProps) => {
  const variantClass = variant === 'primary' ? styles.primary : styles.secondary;
  return (
    <button
      className={`${styles.button} ${variantClass} ${className}`}
      {...props}
    />
  );
};

export default Button;