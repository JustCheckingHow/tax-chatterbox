import React, { useState } from 'react';
import { Box, Button, Container, Paper, TextField, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import useChatterWS from '../../hooks/useChatterWS';

interface Message {
  message: string;
  sender: 'user' | 'ai' | 'system';
}

const Message: React.FC<Message> = ({ message, sender }) => {
  let senderName = 'AI';
  if (sender === 'user') {
    senderName = 'Ty';
  }
  else if (sender === 'system') {
    senderName = '';
  }
  let alignment = "left";
  if (sender === 'user') {
    alignment = "right";
  }

  return (
    <ListItem alignItems="flex-start">
      <ListItemText
        primary={senderName}
        secondary={message}
        sx={{ textAlign: alignment }}
      />
    </ListItem>
  )
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([{ message: "Witaj! Jak mogę Ci pomóc?", sender: 'ai' }]);
  const [newestMessage, setNewestMessage] = useState<Message | null>(null);
  const [isNecessary, setIsNecessary] = useState<boolean | "unknown">("unknown");
  const [requiredInfo, setRequiredInfo] = useState<{ [key: string]: string }>({
    // PCC-3
    "Imię": "",
    "Nazwisko": "",
    "Adres": "",
    "PESEL": "",
    "Numer telefonu": "",
    "Wartość przedmiotu": ""
  });

  const [input, setInput] = useState('');
  const { lastMessage, sendMessage } = useChatterWS('ws/v1/chat');

  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(JSON.stringify({ command: 'basicFlow', text: input, required_info: requiredInfo, history: messages, is_necessary: isNecessary }));

      setMessages([...messages, { message: input, sender: 'user' }]);
      setInput('');
      // Here you would typically send the message to your backend
    }
  };

  React.useEffect(() => {
    if (lastMessage) {
      const lastMessageData = JSON.parse(lastMessage.data);
      console.log(lastMessageData);
      if (lastMessageData.command === 'basicFlowComplete') {
        setMessages(m => [...m, { message: lastMessageData.message, sender: 'ai' }]);
        setNewestMessage(null);
      }
      else if (lastMessageData.command === 'basicFlowPartial') {
        setNewestMessage({ message: lastMessageData.message, sender: 'ai' });
      }
      else if (lastMessageData.command === 'informationParsed') {
        const newestInfo = lastMessageData.message as Record<string, string>;
        const nonEmpty = Object.fromEntries(Object.entries(newestInfo).filter(([, v]) => v !== ''));
        setRequiredInfo(info => ({ ...info, ...nonEmpty }));

        if (Object.keys(nonEmpty).length > 0) {
          const msg = `Nowe informacje. ${Object.entries(nonEmpty).map(([k, v]) => `${k}: ${v}`).join(', ')}`;
          setMessages(m => [...m, { message: msg, sender: 'system' }]);
        }
      }
      else if (lastMessageData.command === 'isNecessary') {
        console.log(lastMessageData.message);
        if (lastMessageData.message === "nie wiem") {
          setIsNecessary("unknown");
        }
        else if (lastMessageData.message === "nie musi") {
          setIsNecessary(false);
        }
        else {
          setIsNecessary(true);
        }
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
              {message.sender !== "system" && <Divider variant="inset" component="li" />}
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
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSendMessage();
              }
            }}
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
