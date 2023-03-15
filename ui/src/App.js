import { useEffect } from 'react';
import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CampaignsPage from './pages/CampaignsPage';
import CreativesPage from './pages/CreativesPage';
import ConfiguresPage from './pages/ConfiguresPage';
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
      {location.pathname !== '/' && <Navbar />}
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/campaigns" element={<CampaignsPage />} />
        <Route path="/creatives" element={<CreativesPage />} />
        <Route path="/configure" element={<ConfiguresPage />} />
      </Routes>
    </>
  );
}

export default App;
