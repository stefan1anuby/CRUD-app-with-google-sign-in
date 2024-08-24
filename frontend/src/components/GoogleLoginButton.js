import React from 'react';
import { Button } from '@chakra-ui/react';

const GoogleSignInButton = ({ onClick }) => {
  return (
    <Button colorScheme="teal" onClick={onClick}>
      Sign in with Google
    </Button>
  );
};

export default GoogleSignInButton;
