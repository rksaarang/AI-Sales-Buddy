import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  IconButton,
} from '@mui/material';
import { Add, Delete } from '@mui/icons-material';
import axios from 'axios';

export function Notes({ user }) {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({
    title: '',
    content: '',
    client_name: '',
    sales_estimated: '',
    proposal_given: false,
  });

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/notes');
      setNotes(response.data);
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewNote((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/notes', newNote);
      setNewNote({
        title: '',
        content: '',
        client_name: '',
        sales_estimated: '',
        proposal_given: false,
      });
      fetchNotes();
    } catch (error) {
      console.error('Error creating note:', error);
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Client Notes
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <TextField
          fullWidth
          label="Title"
          name="title"
          value={newNote.title}
          onChange={handleInputChange}
          sx={{ mb: 2 }}
        />
        <TextField
          fullWidth
          label="Client Name"
          name="client_name"
          value={newNote.client_name}
          onChange={handleInputChange}
          sx={{ mb: 2 }}
        />
        <TextField
          fullWidth
          label="Sales Estimated"
          name="sales_estimated"
          type="number"
          value={newNote.sales_estimated}
          onChange={handleInputChange}
          sx={{ mb: 2 }}
        />
        <TextField
          fullWidth
          label="Content"
          name="content"
          multiline
          rows={4}
          value={newNote.content}
          onChange={handleInputChange}
          sx={{ mb: 2 }}
        />
        <FormControlLabel
          control={
            <Checkbox
              name="proposal_given"
              checked={newNote.proposal_given}
              onChange={handleInputChange}
            />
          }
          label="Proposal Given"
        />
        <Button
          type="submit"
          variant="contained"
          startIcon={<Add />}
          sx={{ mt: 2 }}
        >
          Add Note
        </Button>
      </Box>

      <Grid container spacing={2}>
        {notes.map((note) => (
          <Grid item xs={12} sm={6} md={4} key={note.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {note.title}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Client: {note.client_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {note.content}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Sales Estimated: ${note.sales_estimated}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {note.created_at}
                </Typography>
                <IconButton
                  color="error"
                  onClick={() => handleDelete(note.id)}
                >
                  <Delete />
                </IconButton>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
