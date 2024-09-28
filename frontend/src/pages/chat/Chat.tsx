import React, { useState } from 'react';
import { Box, Button, Container, Paper, TextField, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import useChatterWS from '../../hooks/useChatterWS';

interface Message {
  message: string;
  sender: 'user' | 'ai';
}

const Message: React.FC<Message> = ({ message, sender }) => (
  <ListItem alignItems="flex-start">
    <ListItemText
      primary={sender === 'user' ? 'Ty' : 'AI'}
      secondary={message}
      sx={{ textAlign: sender === 'user' ? 'right' : 'left' }}
    />
  </ListItem>
);

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newestMessage, setNewestMessage] = useState<Message | null>(null);

  const [input, setInput] = useState('');
  const { lastMessage, sendMessage } = useChatterWS('ws/v1/chat');

  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(JSON.stringify({ command: 'basicFlow', text: input }));

      setMessages([...messages, { message: input, sender: 'user' }]);
      setInput('');
      // Here you would typically send the message to your backend
    }
  };

  React.useEffect(() => {
    if (lastMessage) {
      if (lastMessage.command === 'basicFlowComplete') {
        setMessages(m => [...m, { message: lastMessage.message, sender: 'ai' }]);
        setNewestMessage(null);
      }
      else if (lastMessage.command === 'basicFlowPartial') {
        setNewestMessage({ message: lastMessage.message, sender: 'ai' });
      }
    }
  }, [lastMessage]);

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 2, mt: 4, height: '80vh', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h4" gutterBottom>
          Czat Podatkowy
        </Typography>
        <List sx={{ flexGrow: 1, overflow: 'auto' }}>
          {messages.map((message, index) => (
            <React.Fragment key={index}>
              <Message {...message} />
              <Divider variant="inset" component="li" />
            </React.Fragment>
          ))}
          {newestMessage && <Message {...newestMessage} />}
        </List>
        <Box sx={{ display: 'flex', mt: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Wpisz swoją wiadomość..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <Button
            variant="contained"
            endIcon={<SendIcon />}
            onClick={handleSendMessage}
            sx={{ ml: 1 }}
          >
            Wyślij
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat;
