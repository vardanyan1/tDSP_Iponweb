import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CampaignsPage from './pages/CampaignsPage';
import CreativesPage from './pages/CreativesPage';
import ConfigsPage from './pages/ConfigsPage';
import { useEffect } from 'react';
import Navbar from './components/Navbar';

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const csrfToken = localStorage.getItem('csrfToken');
    if (csrfToken === 'true' && location.pathname === '/') {
      navigate('/campaigns')
    } else if (csrfToken === 'false') {
      navigate('/')
    }
  }, [location.pathname, navigate]);

  return (
    <>
    {localStorage.getItem('csrfToken') === 'true' && <Navbar />}
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/campaigns" element={localStorage.getItem('csrfToken') === 'true' ? <CampaignsPage /> : <LoginPage />} />
        <Route path="/creatives" element={localStorage.getItem('csrfToken') === 'true' ? <CreativesPage /> : <LoginPage />} />
        <Route path="/config" element={localStorage.getItem('csrfToken') === 'true' ? <ConfigsPage /> : <LoginPage />} />
      </Routes>
    </>
  );
}

export default App;
