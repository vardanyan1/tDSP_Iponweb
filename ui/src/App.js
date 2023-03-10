import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CampaignsPage from './pages/CampaignsPage';
import CreativesPage from './pages/CreativesPage';
import { useEffect } from 'react';

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const csrfToken = localStorage.getItem('csrfToken');
    if (csrfToken === 'true' && location.pathname === '/') {
      console.log(csrfToken);
      navigate('/campaigns')
    };
  }, [location.pathname, navigate]);

  return (
    <>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/campaigns" element={localStorage.getItem('csrfToken') ? <CampaignsPage /> : <LoginPage />} />
        <Route path="/creatives" element={localStorage.getItem('csrfToken') ? <CreativesPage /> : <LoginPage />} />
      </Routes>
    </>
  );
}

export default App;
