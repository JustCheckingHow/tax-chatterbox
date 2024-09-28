import React from 'react';
import { Container, Grid, Paper, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Home, Settings, Help } from '@mui/icons-material';

const AppContainer: React.FC = ({ children }) => {
  return (
    <Container maxWidth="lg">
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ height: '100%' }}>
            <List component="nav">
              <ListItem>
                <ListItemIcon>
                  <Home />
                </ListItemIcon>
                <ListItemText primary="Home" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Settings />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Help />
                </ListItemIcon>
                <ListItemText primary="Help" />
              </ListItem>
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={9}>
          {children}
        </Grid>
      </Grid>
    </Container>
  );
};

export default AppContainer;
