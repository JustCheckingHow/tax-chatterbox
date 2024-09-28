import React from 'react';
import { Box } from '@mui/material';
import Nav from '../components/Nav/Nav';
import Footer from "../components/Footer/Footer.tsx";
// import Chat from "../components/Chat/ChatOld.tsx";
import { Link } from 'react-router-dom';


const Main: React.FC = () => {


  return (
    <Box sx={{ height: '100vh', width: "100%", display: "flex", flexDirection: "column"}}>
      <Nav/>
        <div className="container" style={{paddingTop: "2em", paddingBottom: "2em", flex: 1}}>
            {/* <Chat/> */}
            <Link to="/chat">Czat</Link>
        </div>
      <Footer/>
    </Box>
  );
};

export default Main;
