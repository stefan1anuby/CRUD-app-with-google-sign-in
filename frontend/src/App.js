import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';

function AuthSuccessHandler({ setIsAuth }) {
  const navigate = useNavigate();
  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const accessToken = queryParams.get('access_token');
  const refreshToken = queryParams.get('refresh_token');

  if (accessToken && refreshToken) {
    // TODO: I should store them in cookies but I already lost too much time working on this
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);

    setIsAuth(true);

    navigate('/home');
  } else {
    
    alert('Failed to retrieve authentication tokens.');
    navigate('/');
  }

  return null; // Or return a loading spinner
}

function App() {
  const [isAuth, setIsAuth] = React.useState(!!localStorage.getItem('access_token'));

  return (
    
      <Router>
        <Routes>
          {!isAuth ? (
            <>
              {/* Login Page */}
              <Route path="/" element={<Login />} />
              {/* Route to handle auth success and store tokens */}
              <Route path="/auth-success" element={<AuthSuccessHandler setIsAuth={setIsAuth} />} />
              {/* Redirect to login if not authenticated */}
              <Route path="*" element={<Navigate to="/" />} />
            </>
          ) : (
            <>
              {/* Home Page after login */}
              <Route path="/home" element={<Home />} />
              {/* Redirect to home if authenticated */}
              <Route path="*" element={<Navigate to="/home" />} />
            </>
          )}
        </Routes>
      </Router>
  );
}

export default App;
