import { Route, Routes, useLocation, Navigate, useNavigate } from 'react-router-dom';
import { useState, useEffect, useMemo } from 'react';
import jwt_decode from 'jwt-decode';
import Navbar from './components/Navbar';
import routes from './routes';
import Spinner from './components/Spinner/Spinner';

function App() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(true);
  const [isValidToken, setIsValidToken] = useState(false);
  const [shouldRenderRoutes, setShouldRenderRoutes] = useState(false);

  const validateToken = async () => {
    const token = localStorage.getItem('token');

    if (!token) {
      setIsValidToken(false);
      setIsLoading(false);
      return Promise.resolve(false);
    }

    try {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;

      if (decoded.exp && decoded.exp > currentTime) {
        setIsValidToken(true);
      } else {
        setIsValidToken(false);
        localStorage.removeItem('token');
      }
    } catch (error) {
      setIsValidToken(false);
      localStorage.removeItem('token');
    }

    setIsLoading(false);
    return Promise.resolve(true);
  };

  useEffect(() => {
    validateToken().then((isValidToken) => {
      if (isValidToken && (pathname === '/ui' || pathname === '/' || pathname === '/ui/')) {
        navigate('/ui/campaigns');
      }
      setShouldRenderRoutes(true);
    });
  }, [pathname, navigate]);

  const shouldShowNavbar = useMemo(() => {
    return routes.some(route => route.isPrivate && route.path === pathname);
  }, [pathname]);

  return (
    <>
      {shouldShowNavbar && <Navbar />}
      {shouldRenderRoutes && (
        <Routes>
          <Route path="/" element={<Navigate to="/ui/" />} />
          {routes.map(({ path, element, isPrivate }) => (
            <Route
              key={path}
              path={path}
              element={
                isPrivate && !isValidToken ? (
                  <Navigate to="/ui/" />
                ) : (
                  element
                )
              }
            />
          ))}
        </Routes>
      )}
      {isLoading && <Spinner />}
    </>
  );
}

export default App;
