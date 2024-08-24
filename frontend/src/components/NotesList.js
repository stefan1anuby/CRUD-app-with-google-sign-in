import React from 'react';
import { Box, VStack, Input, Button, Flex, Text, Heading } from '@chakra-ui/react';

const NotesList = ({ userData, newNote, setNewNote, handleAddNote, handleDeleteNote, noteLoading, noteError }) => {
  const handleNoteChange = (e) => {
    setNewNote(e.target.value);
  };

  return (
    <Box mt={6}>
      <Heading size="md">Your Notes</Heading>
      <VStack spacing={4} mt={4}>
        {userData.notes && userData.notes.map(note => (
          <Box key={note.id} p={4} borderWidth={1} borderRadius={8} boxShadow="md" w="100%">
            <Text>{note.content}</Text>
            <Button
              mt={2}
              colorScheme="red"
              size="sm"
              onClick={() => handleDeleteNote(note.id)}
              isLoading={noteLoading}
            >
              Delete Note
            </Button>
          </Box>
        ))}
      </VStack>

      <Flex align="center" justify="center" direction="column" mt={4}>
        <Input
          placeholder="Enter new note (at least 10 characters)"
          value={newNote}
          onChange={handleNoteChange}
          mb={2}
        />
        <Button
          colorScheme="teal"
          onClick={handleAddNote}
          isLoading={noteLoading}
          isDisabled={newNote.length < 10} // Disable button if note content is too short
        >
          Add Note
        </Button>
        {newNote.length > 0 && newNote.length < 10 && (
          <Text color="red.500" mt={2}>
            Note content must be at least 10 characters long.
          </Text>
        )}
        {noteError && <Text color="red.500" mt={2}>{noteError}</Text>}
      </Flex>
    </Box>
  );
};

export default NotesList;
