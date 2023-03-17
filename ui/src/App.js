import { Route, Routes, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CampaignsPage from './pages/CampaignsPage';
import CreativesPage from './pages/CreativesPage';
import ConfiguresPage from './pages/ConfiguresPage';
import Navbar from './components/Navbar';

function App() {
  // const navigate = useNavigate();
  const location = useLocation();

  // useEffect(() => {
  //   const csrfToken = localStorage.getItem('csrfToken');
  //   if (csrfToken === 'true' && location.pathname === '/') {
  //     navigate('/campaigns')
  //   } else if (csrfToken === 'false') {
  //     navigate('/')
  //   }
  // }, [location.pathname, navigate]);

  const pages = [
    {
      path: "/campaigns",
      element: <CampaignsPage />,
    },
    {
      path: "/creatives",
      element: <CreativesPage />,
    },
    {
      path: "/configure",
      element: <ConfiguresPage />,
    },
  ];

  return (
    <>
      {location.pathname !== '/' && <Navbar />}
      <Routes>
        <Route path="/" element={<LoginPage />} />
        {pages.map(({ path, element }) => <Route key={path} path={path} element={element} />)}
      </Routes>
    </>
  );
}

export default App;
