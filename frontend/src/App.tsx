
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/auth/LoginPage/LoginPage';
import RegisterPage from './pages/auth/RegisterPage/RegisterPage';
import CreateCompetitionPage from './pages/competitions/CreateCompetitionsPage/CreateCompetitionsPage';
import { useAuth } from './lib/hooks/useAuth';
import './styles/global.scss';

const App = () => {
  const { isLoading } = useAuth();

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="*" element={<LoginPage />} />
      <Route path="/competitions" element={<CreateCompetitionPage/>}/>
    </Routes>
  );
};

export default App;
