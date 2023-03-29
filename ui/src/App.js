import { useState, useEffect, useMemo, useCallback } from 'react';
import { Route, Routes, useLocation, Navigate, useNavigate } from 'react-router-dom';
import routes from './routes';
import Navbar from './components/Navbar';
import Spinner from './components/Spinner/Spinner';
import { validateToken } from './helpers/auth';

const App = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isValidToken, setIsValidToken] = useState(false);

  const { pathname } = useLocation();
  const navigate = useNavigate();

  const handleValidateToken = useCallback(async () => {
    const tokenValid = await validateToken();
    setIsValidToken(tokenValid);

    if (tokenValid && (pathname === '/ui' || pathname === '/' || pathname === '/ui/')) {
      navigate('/ui/campaigns');
    }

    setIsLoading(false);
  }, [pathname, navigate]);

  useEffect(() => {
    handleValidateToken();
  }, [handleValidateToken]);

  const shouldShowNavbar = useMemo(() => {
    return routes.some(route => route.isPrivate && route.path === pathname);
  }, [pathname]);

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <>
      {shouldShowNavbar && <Navbar />}
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
    </>
  );
}

export default App;