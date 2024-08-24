import React from 'react';
import { Box, Input, Button, Flex, Text } from '@chakra-ui/react';

const EditName = ({ newName, setNewName, handleNameChange, updateLoading, updateError }) => {
	const handleChange = (e) => {
	  setNewName(e.target.value);
	};
  
	return (
	  <Box mt={6}>
		<Flex align="center" justify="center" direction="column">
		  <Input
			placeholder="Enter new name (at least 5 characters)"
			value={newName}
			onChange={handleChange}
			mb={2}
		  />
		  <Button
			colorScheme="teal"
			onClick={handleNameChange}
			isLoading={updateLoading}
			isDisabled={newName.length < 5} // Disable button if name is too short
		  >
			Update Name
		  </Button>
		  {newName.length > 0 && newName.length < 5 && (
			<Text color="red.500" mt={2}>
			  Name must be at least 5 characters long.
			</Text>
		  )}
		  {updateError && <Text color="red.500" mt={2}>{updateError}</Text>}
		</Flex>
	  </Box>
	);
  };
  
  export default EditName;
