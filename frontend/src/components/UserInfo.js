import React from 'react';
import { Text } from '@chakra-ui/react';

const UserInfo = ({ userData }) => (
  <>
    <Text mt={4}>Name: {userData.name}</Text>
    <Text>Email: {userData.email}</Text>
    <Text>Registered on: {userData.created_date}</Text>
    <Text>Last Login Date: {userData.last_login_date}</Text>
  </>
);

export default UserInfo;
