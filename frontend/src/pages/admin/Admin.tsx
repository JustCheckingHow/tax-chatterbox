import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Nav from '../../components/Nav/Nav';
import { Box, Typography, Container, Stack, Grid2 } from '@mui/material';
import { BarChart, LineChart } from '@mui/x-charts';

interface IntentStats {
  [hour: string]: {
    [intent: string]: number;
  };
}

const Admin: React.FC = () => {
  const [intentStats, setIntentStats] = useState<IntentStats>({});
  const [messagesStats, setMessagesStats] = useState<IntentStats>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchIntentStats = async () => {
      try {
        const url = `${import.meta.env.VITE_BACKEND_URL}/api/admin/conversations`;
        console.log(url);
        const response = await axios.get(url);
        console.log(response.data);
        setIntentStats(response.data.stats);
        setMessagesStats(response.data.messages_stats);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch intent statistics');
        setLoading(false);
      }
    };

    fetchIntentStats();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  // Process data for charts
  const hours = Object.keys(intentStats).sort();
  const intents = Array.from(new Set(Object.values(intentStats).flatMap(Object.keys)));

  const chartData = intents.map(intent => ({
    intent,
    data: hours.map(hour => intentStats[hour][intent] || 0)
  }));

  // Calculate total conversations
  const totalConversations = Object.values(intentStats).reduce((acc, hourData) => {
    return acc + Object.values(hourData).reduce((sum, count) => sum + count, 0);
  }, 0);

  // Calculate most common intent
  const intentCounts = intents.map(intent => ({
    intent,
    count: hours.reduce((sum, hour) => sum + (intentStats[hour][intent] || 0), 0)
  }));
  const mostCommonIntent = intentCounts.reduce((max, current) =>
    current.count > max.count ? current : max
    , intentCounts[0]);

  // Calculate average intents per hour
  const avgIntentsPerHour = totalConversations / hours.length;

  return (
    <Box sx={{ minHeight: "100vh", width: "100%", display: "flex", flexDirection: "column" }}>
      <Nav />
      <Container maxWidth="lg" sx={{ mt: 5 }}>
        <Stack direction="column" spacing={2}>
          <Typography variant="h4" component="h1" gutterBottom>Panel statystyk</Typography>
          <Grid2 container spacing={2}>
            <Grid2 size={6}>
              <Typography variant="h6" gutterBottom>Rozkład intencji w czasie</Typography>
              <BarChart
                xAxis={[{ scaleType: 'band', data: hours }]}
                series={chartData.map(({ intent, data }) => ({
                  data,
                  label: intent,
                }))}
                height={500}
              />
              <Box justifyContent="center" sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography variant="h6" gutterBottom>Statystyki</Typography>
                <Typography>Łączna liczba konwersacji: {totalConversations}</Typography>
                <Typography>Najpopularniejsza intencja: {mostCommonIntent.intent} (Liczba: {mostCommonIntent.count})</Typography>
                <Typography>Średnia wiadomości na godzinę: {avgIntentsPerHour.toFixed(2)}</Typography>
              </Box>
            </Grid2>
            <Grid2 size={6}>
              <Typography variant="h6" gutterBottom>Liczba konwersacji na godzinę</Typography>
              <LineChart
                xAxis={[{ scaleType: 'band', data: hours }]}
                series={[{
                  data: hours.map(hour =>
                    Object.values(intentStats[hour]).reduce((sum, count) => sum + count, 0)
                  ),
                  label: 'Konwersacje',
                }]}
                height={300}
              />
              <Typography variant="h6" gutterBottom>Liczba wiadomości na godzinę</Typography>
              <LineChart
                xAxis={[{ scaleType: 'band', data: hours }]}
                series={[{
                  data: hours.map(hour => messagesStats[hour].messages || 0),
                  label: 'Wiadomości',
                }]}
                height={300}
              />
            </Grid2>
          </Grid2>
        </Stack>
      </Container>
    </Box>
  );
};

export default Admin;