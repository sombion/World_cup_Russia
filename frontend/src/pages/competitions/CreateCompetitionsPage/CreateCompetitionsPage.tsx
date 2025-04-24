import { Link } from "react-router-dom";
import CreateCompetitionForm from "../../../components/competitions/CreateCompetitionsForm";
import styles from './CreateCompetitionsPage.module.scss';

const CreateCompetitionPage =() => {
    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h1 className={styles.title}>Создание соревнования</h1>
                <CreateCompetitionForm/>
                <div className={styles.footer}>
                    <Link to="/competitions/all" className={styles.link}>
                    Вернуться к списку соревнований
                    </Link>
                </div>
            </div>
        </div>
    )
}

export default CreateCompetitionPage