import React, { useState } from 'react';
import { Box, TextField, Button, Grid, Paper, Typography, Fade, Grow } from '@mui/material';

const Main: React.FC = () => {
  const [chatStarted, setChatStarted] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [chatHistory, setChatHistory] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      setChatHistory([...chatHistory, inputValue]);
      setInputValue('');
      setChatStarted(true);
    }
  };

  return (
    <Box sx={{ width: "100%", padding: 2 }}>
      <Grid container spacing={2} justifyContent="center">
        <Grow in={chatStarted} mountOnEnter unmountOnExit>
          <Grid item xs={12} md={6}>
            <Fade in={chatStarted}>
              <Paper elevation={3} sx={{ p: 2, height: '100%', overflowY: 'auto' }}>
                <Typography variant="h6" gutterBottom>
                  Chat History
                </Typography>
                {chatHistory.map((message, index) => (
                  <Typography key={index} paragraph>
                    {message}
                  </Typography>
                ))}
              </Paper>
            </Fade>
          </Grid>
        </Grow>
        <Grid item xs={12} md={chatStarted ? 6 : 5}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', transition: 'all 0.3s ease-in-out' }}>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Ask your tax question here..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                sx={{ mb: 2 }}
              />
              <Button type="submit" variant="contained" fullWidth>
                Submit
              </Button>
            </form>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Main;
