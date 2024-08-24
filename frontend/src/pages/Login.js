import React from 'react';
import { Container, Heading, Box, Button } from '@chakra-ui/react';
import axios from 'axios';
import { BACKEND_URL } from '../config';

const Login = () => {
  const handleGoogleLogin = async () => {
    try {
      // Step 1: Initiate OAuth2 Login with Google
      const response = await axios.get(`${BACKEND_URL}/users/login/google`);
      const { authorization_url, state } = response.data;

      // Store the state in session storage to validate on callback
      sessionStorage.setItem('oauth_state', state);

      // Redirect user to the provider's authorization URL
      window.location.href = authorization_url;
    } catch (error) {
      console.error('Error initiating OAuth2 login', error);
      // Handle error (e.g., show a notification to the user)
    }
  };

  const handleTestLogin = async () => {
    try {
      
      const response = await fetch(`${BACKEND_URL}/users/auth/test/callback?code=test-code`, {
        method: 'GET'
      });
     
      if (response.status < 400) {
        const redirectUrl = response.url;

        window.location.href = redirectUrl;
      }
    } catch (error) {
      console.error('Error initiating Test provider login', error);
      
    }
  };

  return (
    <Container centerContent>
      <Box p={8} borderWidth={1} borderRadius={8} boxShadow="lg" textAlign="center">
        <Heading mb={4}>Login</Heading>
        <Button colorScheme="teal" onClick={handleGoogleLogin} m={4}>
          Sign in with Google
        </Button>
        <Button colorScheme="blue" onClick={handleTestLogin} m={4}> 
          Login with Test Provider
        </Button>
      </Box>
    </Container>
  );
};

export default Login;
