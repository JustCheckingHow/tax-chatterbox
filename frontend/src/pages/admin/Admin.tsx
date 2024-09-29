import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Nav from '../../components/Nav/Nav';
import { Box, Typography, Container, Stack } from '@mui/material';
import { BarChart, LineChart, PieChart } from '@mui/x-charts';

interface Conversation {
  id: number;
  user: string;
  messageCount: number;
  lastActive: string;
}

const Admin: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const url = `${import.meta.env.VITE_BACKEND_URL}/api/admin/conversations`;
        console.log(url);
        const response = await axios.get(url);
        console.log(response.data);
        setConversations(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch conversations');
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;


  return (
    <Box sx={{ minHeight: "100vh", width: "100%", display: "flex", flexDirection: "column" }}>
      <Nav />
      <Container maxWidth="lg">
        <Stack direction="column" spacing={2}>
          <Typography variant="h4" component="h1" gutterBottom>Admin Panel</Typography>

          <Stack direction="row" spacing={2}>
            <Box>
              <Typography variant="h6" gutterBottom>Message Count per Conversation</Typography>
              <BarChart
                xAxis={[{ scaleType: 'band', data: conversations.map(conv => conv.id.toString()) }]}
                series={[{ data: conversations.map(conv => conv.messageCount) }]}
                width={600}
                height={300}
              />
            </Box>
            <Box>
              <Typography variant="h6" gutterBottom>Message Distribution</Typography>
              <LineChart
                xAxis={[{ 
                  scaleType: 'time', 
                  data: conversations
                    .filter(conv => conv.lastActive !== null)
                    .map(conv => new Date(conv.lastActive))
                }]}
                series={[{ 
                  data: conversations
                    .filter(conv => conv.lastActive !== null)
                    .map((_, index) => index + 1),
                  label: 'Number of Conversations'
                }]}
                width={600}
                height={300}
              />
            </Box>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
};

export default Admin;