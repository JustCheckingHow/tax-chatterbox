import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';
import useChatterWS from '../../hooks/useChatterWS';
import Nav from '../../components/Nav/Nav';
import Footer from '../../components/Footer/Footer';
import styles from './Chat.module.scss';

import GridItem from "../../components/GridItem/GridItem.tsx";
import ChatDocUploader from "../../components/ChatDocUploader/ChatDocUploader.tsx";

import signIcon from "../../assets/icons/sign.svg";
// import chatIcon from "../../assets/icons/czatbot.svg";
import voiceIcon from "../../assets/icons/callcenter.svg";

import logo from "../../assets/image/logo.png"
import Checklist from "../../components/Checklist/Checklist.tsx"
import GovermentSelect from "../../components/GovermentSelect/GovermentSelect.tsx"
import FinalDocument from "../../components/FinalDocument/FinalDocument.tsx"


interface Message {
  message: string;
  sender: 'user' | 'ai' | 'system';
  hidden?: boolean;
}


const Message: React.FC<Message> = ({ message, sender, hidden }) => {
  if (hidden) {
    return null;
  }

  let senderName = 'AI';
  if (sender === 'user') {
    senderName = 'Ty';
  }
  else if (sender === 'system') {
    senderName = '';
  }

  return (
    <li className={styles.chat__message + " " + (sender === 'user' ? styles.chat__message__user : (sender === 'ai' ? styles.chat__message__ai : styles.chat__message__system))}>
      {senderName != '' && <div className={styles.chat__message__author}>
        {senderName === 'AI' && <img src={logo} alt="logo" />}
      </div> }
      <div className={styles.chat__message__content}>
        {message}
      </div>
    </li>
  )
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([{ message: "Witaj! Jak mogę Ci pomóc?", sender: 'ai' }]);
  const [newestMessage, setNewestMessage] = useState<Message | null>(null);
  const [isNecessary, setIsNecessary] = useState<boolean | "unknown">("unknown");
  const [view, setView] = useState("");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [requiredInfo, setRequiredInfo] = useState<any>([]);
  const [validatedInfo, setValidatedInfo] = useState<any>(false);
  const [obtainedInfo, setObtainedInfo] = useState<Record<string, string>>({});
  const [closestUrzad, setClosestUrzad] = useState<Array<any>>([]);
  const [allUrzedy, setAllUrzedy] = useState<Array<any>>([]);
  const [xmlFile, setXmlFile] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  useEffect(() => {
    try {
      console.log(validatedInfo);
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/xml_schema`)
        .then(response => response.json())
        .then(data => {
          setRequiredInfo(data.message);
        })
    } catch (error) {
      console.error(error);
    }
  }, [])

  useEffect(() => {
    setValidatedInfo(true);
    requiredInfo.forEach((info: string) => {
      if (!obtainedInfo[info]) {
        setValidatedInfo(false);
      }
    })
  }, [requiredInfo]);

  useEffect(() => {
    if (obtainedInfo.Ulica && obtainedInfo.NrDomu && obtainedInfo.Miejscowosc && obtainedInfo.KodPocztowy) {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/closestUrzad`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          location: `${obtainedInfo.Ulica} ${obtainedInfo.NrDomu} ${obtainedInfo.Miejscowosc} ${obtainedInfo.KodPocztowy}`
        })
      })
        .then(response => response.json())
        .then(data => {
          setClosestUrzad(data.closest);
          setAllUrzedy(data.all_urzedy);
        })
    }
    if(validatedInfo) {
      generateXml();
    }
  }, [validatedInfo, obtainedInfo]);


  const [input, setInput] = useState('');
  const { lastMessage, sendMessage } = useChatterWS('ws/v1/chat');

  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(JSON.stringify({ command: 'basicFlow', text: input, required_info: requiredInfo, obtained_info: obtainedInfo, history: messages, is_necessary: isNecessary }));

      setMessages([...messages, { message: input, sender: 'user' }]);
      setInput('');
      setIsLoading(true);
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
        setIsLoading(false);
      }
      else if (lastMessageData.command === 'basicFlowPartial') {
        setNewestMessage({ message: lastMessageData.message, sender: 'ai' });
        setIsLoading(false);
      }
      else if (lastMessageData.command === 'informationParsed') {
        const newestInfo = lastMessageData.message as Record<string, string>;
        const nonEmpty = Object.fromEntries(Object.entries(newestInfo).filter(([, v]) => v !== ''));
        setObtainedInfo(info => ({ ...info, ...nonEmpty }));

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

  const updateUrzad = (kod: string) => {
    setObtainedInfo(info => ({ ...info, UrzadSkarbowy: kod }));
  }

  const generateXml = () => {
    try {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/generate_xml`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          data: obtainedInfo
        })
      }).then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = 'formularz.xml';
          document.body.appendChild(a);
        })
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <Box sx={{ minHeight: "100vh", width: "100%", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div className="container" style={{ paddingTop: "2em", paddingBottom: "2em", flex: 1 }}>
        <div className={styles.chat__container}>
          {messages.length < 2 && (view != "uploadDoc" ? (
            <div
              className={styles.chat__grid}
            >
              <GridItem
                onClick={() => { setView("uploadDoc") }}
                icon={signIcon}
                heading={"Prześlij umowę"}
                content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
              />
              <GridItem
                onClick={() => { }}
                icon={voiceIcon}
                heading={"Porozmawiaj z asystentem"}
                content={"Porozmawiaj z asystentem i opisz mu swoją sytuację. JustCheckingTax Ci pomoże."}
              />
            </div>
          ) : <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <ChatDocUploader sendMessage={
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              (message: any) => {
                const msg = {
                  command: 'basicFlow',
                  text: message.text.replaceAll("\n", " "),
                  required_info: requiredInfo,
                  obtained_info: obtainedInfo,
                  history: messages,
                  is_necessary: isNecessary
                };
                setMessages(m => [...m, { message: message.text, sender: 'user', hidden: true }]);
                sendMessage(JSON.stringify(msg));
              }
            } />
            <p onClick={() => { setView('') }}>Wróć</p>
          </div>)}
          <ul className={styles.chat__message__container}>
            {messages.map((message, index) => (
              <React.Fragment key={index}>
                <Message {...message} />
              </React.Fragment>
            ))}
            {isLoading && <LoadingAnimation />}
            {newestMessage && <Message {...newestMessage} />}
          </ul>
          <form className={styles.chat__form}>
            <input
              className={styles.chat__input}
              placeholder="Wpisz swoją wiadomość..."
              value={input}
              type='text'
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSendMessage();
                }
              }} />
            <button className={"btn btn-primary"} onClick={handleSendMessage} type='button'>
              <span>Wyślij</span>
            </button>
          </form>
        </div>
        <Checklist required_info={requiredInfo} obtained_info={obtainedInfo} />
        {!validatedInfo && <GovermentSelect closestUrzad={closestUrzad} updateUrzad={updateUrzad} allUrzedy={allUrzedy} generateXml={generateXml} />}
      {xmlFile && <FinalDocument xmlFile={xmlFile} />}
      </div>
      <Footer />
    </Box>
  );
};

export default Chat;


const LoadingAnimation: React.FC = () => {
  return (
    <div className={styles.loading__animation}>
      <div className={styles.loading__animation__dot}></div>
      <div className={styles.loading__animation__dot}></div>
      <div className={styles.loading__animation__dot}></div>
    </div>
  );
};
