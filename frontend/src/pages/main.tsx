import React from 'react';
import { Box } from '@mui/material';
import Nav from '../components/Nav/Nav';
import Footer from "../components/Footer/Footer.tsx";
import Chat from "../components/Chat/Chat.tsx";


const Main: React.FC = () => {


  return (
    <Box sx={{ height: '100vh', width: "100%", display: "flex", flexDirection: "column"}}>
      <Nav/>
        <div className="container" style={{paddingTop: "2em", paddingBottom: "2em", flex: 1}}>
            <Chat/>
        </div>
      <Footer/>
    </Box>
  );
};

export default Main;
