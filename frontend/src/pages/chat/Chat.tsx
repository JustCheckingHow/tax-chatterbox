import React, { useState } from 'react';
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
    <li className={styles.chat__message + " " + (sender === 'user' ? styles.chat__message__user : styles.chat__message__system)}>
      <div className={styles.chat__message__content}>
        {message}
      </div>
      <div className={styles.chat__message__author}>
        {senderName === 'AI' && <img src={logo} alt="logo" />}
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
  const [requiredInfo, setRequiredInfo] = useState<any>([
    { "Pesel": { "description": "Numer Pesel", "required": true } },
    { "P_4": { "description": "Data Dokonania czynności", "required": true } },
    { "DataZlozeniaDeklaracji": { "description": "Data złożenia deklaracji", "required": false } },
    { "Imie": { "description": "Imię", "required": true } },
    { "Nazwisko": { "description": "Nazwisko", "required": true } },
    { "ImieOjca": { "description": "Imię ojca", "required": true } },
    { "ImieMatki": { "description": "Imię matki", "required": true } },
    { "KodKraju": { "description": "Kod kraju", "required": true } },
    { "Wojewodztwo": { "description": "Województwo", "required": true } },
    { "Powiat": { "description": "Powiat", "required": true } },
    { "Gmina": { "description": "Gmina", "required": true } },
    { "Ulica": { "description": "Ulica", "required": true } },
    { "NrDomu": { "description": "Numer domu", "required": true } },
    { "NrLokalu": { "description": "Numer lokalu", "required": true } },
    { "Miejscowosc": { "description": "Miejscowość", "required": true } },
    { "KodPocztowy": { "description": "Kod pocztowy", "required": true } },
    { "P_6": { "description": "Cel złożenia deklaracji", "required": false } },
    {
      "P_7": {
        "description": "Podmiot składający deklarację. 1 - podmioty zobowiązane solidarnie do zapłaty podatku, w przeciwnym wypadku 5",
        "required": true,
      }
    },
    { "P_20": { "description": "Przedmiot opatkowania 1 - umowa", "required": true } },
    {
      "P_21": {
        "description": "Miejsce położenia rzeczy 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
        "required": false,
      }
    },
    {
      "P_22": {
        "description": "Miejsce położenia CWC 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
        "required": false,
      }
    },
    { "P_23": { "description": "Opis", "required": true } },
    {
      "P_26": {
        "description": "Podstawa opatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)",
        "required": true,
      }
    },
    { "P_62": { "description": "Liczba dodatkowych załączników", "required": true } },
  ]);

  const [obtainedInfo, setObtainedInfo] = useState<Record<string, string>>({});

  const [input, setInput] = useState('');
  const { lastMessage, sendMessage } = useChatterWS('ws/v1/chat');

  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(JSON.stringify({ command: 'basicFlow', text: input, required_info: requiredInfo, obtained_info: obtainedInfo, history: messages, is_necessary: isNecessary }));

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

  return (
    <Box sx={{ minHeight: "100vh", width: "100%", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div className="container" style={{ paddingTop: "2em", paddingBottom: "2em", flex: 1 }}>
        <div className={styles.chat__container}>
          {messages.length < 2 && (view != "uploadDoc" ? (
            <div
              className={styles.chat__grid}
            >
              {/* <GridItem
                    onClick={() => {}}
                        icon={chatIcon}
                        heading={"Opisz swoją sprawę"}
                        content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
                    /> */}
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
                content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
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
            <button type={"button"} className={"btn btn-secondary"}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M192 0C139 0 96 43 96 96l0 160c0 53 43 96 96 96s96-43 96-96l0-160c0-53-43-96-96-96zM64 216c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40z" /></svg>
            </button>
            <button className={"btn btn-primary"} onClick={handleSendMessage} type='button'>
              <span>Wyślij</span>
            </button>
          </form>
        </div>
        <Checklist required_info={requiredInfo} obtained_info={obtainedInfo} />
      </div>
      <GovermentSelect />
      <FinalDocument />
      <Footer />
    </Box>
  );
};

export default Chat;
