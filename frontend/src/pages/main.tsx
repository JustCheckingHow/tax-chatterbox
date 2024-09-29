import React from 'react';
import { Box } from '@mui/material';
import Nav from '../components/Nav/Nav';
import Footer from "../components/Footer/Footer.tsx";
// import Chat from "../components/Chat/ChatOld.tsx";
import { Link } from 'react-router-dom';


const Main: React.FC = () => {
  return (
    <Box sx={{ minHeight: '100vh', width: "100%", display: "flex", flexDirection: "column"}}>
      <Nav/>
        <div className="container" style={{paddingTop: "2em", paddingBottom: "2em", flex: 1}}>
            <div className="gov-banner-products">
              <div className="gov-banner-products__image">
                  <img src="./assets/images/local/banner-foto.png" />
              </div>
              <div className="gov-banner-products__content">
                  <h4>Platforma pomocy podatkowej</h4>
                  <p>Przejdź do funkcji czatu, aby móc zadawać pytania o formy podatkowe, 
                      ich wypełnianie. Nasz asystent zada Ci niezbędne pytania, by ustalić dane 
                      koeniczne do utworzenia odpowiedniego formularza podatkowego. 
                      Możesz też załadować plik umowy, by program automatycznie 
                      wypełnił formularz PCC-3.
                      Po zakończeniu rozmowy otrzymasz gotowy formularz xml.
                  </p>
                  <Link to={"/chat"} className="gov-banner-products__cta">Przejdź do czatu</Link>  
              </div>
          </div>
        </div>
      <Footer/>
    </Box>
  );
};

export default Main;
