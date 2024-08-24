import React, { useEffect, useState } from 'react';
import { Container, Heading, Box, Spinner, Text, Button } from '@chakra-ui/react';
import { fetchUserData, updateUserName, addNote, deleteNote } from '../utils/api'; 
import UserInfo from '../components/UserInfo';
import EditName from '../components/EditName';
import NotesList from '../components/NotesList'
import axios from 'axios';
import { BACKEND_URL } from '../config';

const Home = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newName, setNewName] = useState('');
  const [updateLoading, setUpdateLoading] = useState(false);
  const [updateError, setUpdateError] = useState(null);
  const [newNote, setNewNote] = useState('');
  const [noteLoading, setNoteLoading] = useState(false);
  const [noteError, setNoteError] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState(null);

  useEffect(() => {
    const loadUserData = async () => {
      try {
        const response = await fetchUserData();
        setUserData(response.data);
      } catch (err) {
        console.error('Error fetching user data:', err);
  
        if (err.response && err.response.status === 401) {
          // Unauthorized error: remove tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          
          window.location = "/";
          
        } else {
          setError('Failed to fetch user data');
        }
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  const handleNameChange = async () => {
    if (!newName.trim()) {
      setUpdateError('Name cannot be empty.');
      return;
    }

    if (newName.length < 5) {
      setUpdateError('Name must be at least 5 characters long.');
      return;
    }

    setUpdateLoading(true);
    setUpdateError(null);

    try {
      const response = await updateUserName(newName);
      setUserData((prevData) => ({
        ...prevData,
        name: response.data.name,
      }));

      setNewName('');
    } catch (err) {
      console.error('Error updating user name:', err);
      setUpdateError('Failed to update name');
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleAddNote = async () => {
    if (!newNote.trim()) {
      setNoteError('Note content cannot be empty.');
      return;
    }

    if (newNote.length < 10) {
      setNoteError('Note content must be at least 10 characters long.');
      return;
    }

    setNoteLoading(true);
    setNoteError(null);

    try {
      const response = await addNote(newNote);
      setUserData((prevData) => ({
        ...prevData,
        notes: [...prevData.notes, response.data],
      }));

      setNewNote('');
    } catch (err) {
      console.error('Error adding note:', err);
      setNoteError('Failed to add note');
    } finally {
      setNoteLoading(false);
    }
  };

  const handleDeleteNote = async (noteId) => {
    setNoteLoading(true);
    setNoteError(null);

    try {
      await deleteNote(noteId);
      setUserData((prevData) => ({
        ...prevData,
        notes: prevData.notes.filter(note => note.id !== noteId),
      }));
    } catch (err) {
      console.error('Error deleting note:', err);
      setNoteError('Failed to delete note');
    } finally {
      setNoteLoading(false);
    }
  };

  const handleLogout = () => {
    // Remove tokens from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location = "/"; // Redirect to login page
  };

  if (loading) {
    return <Spinner size="xl" />;
  }

  if (error) {
    return <Text color="red.500">{error}</Text>;
  }

  const handleDeleteAccount = async () => {
    setDeleteLoading(true);
    setDeleteError(null);

    try {
      const token = localStorage.getItem('access_token');
      await axios.delete(`${BACKEND_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location = "/";
    } catch (err) {
      console.error('Error deleting account:', err);
      setDeleteError('Failed to delete account');
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <Container centerContent>
      <Box p={8} borderWidth={1} borderRadius={8} boxShadow="lg" textAlign="center">
        <Heading>Welcome to the Home Page!</Heading>
        {userData && (
          <>
            <UserInfo userData={userData} />
            <EditName
              newName={newName}
              setNewName={setNewName}
              handleNameChange={handleNameChange}
              updateLoading={updateLoading}
              updateError={updateError}
            />
            <NotesList
              userData={userData}
              newNote={newNote}
              setNewNote={setNewNote}
              handleAddNote={handleAddNote}
              handleDeleteNote={handleDeleteNote}
              noteLoading={noteLoading}
              noteError={noteError}
            />
            <Box mt={10}>
              <Button colorScheme="red" onClick={handleLogout} m={2}>
                Logout
              </Button>
              <Button colorScheme="red" onClick={handleDeleteAccount} m={2} isLoading={deleteLoading}>
                Delete Account
              </Button>
              {deleteError && <Text color="red.500" mt={2}>{deleteError}</Text>}
            </Box>
          </>
        )}
      </Box>
    </Container>
  );
};

export default Home;
