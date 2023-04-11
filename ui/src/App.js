import { useState, useEffect, useMemo } from 'react';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import routes from './routes';
import Navbar from './components/Navbar';
import Spinner from './components/Spinner/Spinner';
import { useTokenValidation } from './hooks/useTokenValidation';

const App = () => {
  const { pathname } = useLocation();
  const { isLoading, isError, isValid: isValidToken } = useTokenValidation();

  const shouldShowNavbar = useMemo(() => {
    return routes.some(route => route.isPrivate && route.path === pathname);
  }, [pathname]);

  if (isLoading) {
    return <Spinner />;
  }

  if (isError) {
    // Handle the error case, e.g. redirect to login page
    return <Navigate to="/ui/" />;
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
