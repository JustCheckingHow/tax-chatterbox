/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';
import useChatterWS from '../../hooks/useChatterWS';
import Nav from '../../components/Nav/Nav';
import Footer from '../../components/Footer/Footer';
import styles from './Chat.module.scss';

import GridItem from "../../components/GridItem/GridItem.tsx";
import ChatDocUploader from "../../components/ChatDocUploader/ChatDocUploader.tsx";

import signIcon from "../../assets/icons/sign.svg";
import voiceIcon from "../../assets/icons/callcenter.svg";

import logo from "../../assets/image/logo.png"
import Checklist from "../../components/Checklist/Checklist.tsx"
import GovermentSelect from "../../components/GovermentSelect/GovermentSelect.tsx"
import FinalDocument from "../../components/FinalDocument/FinalDocument.tsx"
import { useLanguage } from '../../context/languageContext.ts';
import Form from '../../components/Form/Form.tsx';


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

  const renderMessage = (text: string) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);
    return parts.map((part, index) =>
      urlRegex.test(part) ? (
        <a key={index} href={part} target="_blank" rel="noopener noreferrer">
          {part}
        </a>
      ) : (
        part
      )
    );
  };

  return (
    <li className={styles.chat__message + " " + (sender === 'user' ? styles.chat__message__user : (sender === 'ai' ? styles.chat__message__ai : styles.chat__message__system))}>
      {senderName != '' && <div className={styles.chat__message__author}>
        {senderName === 'AI' && <img src={logo} alt="logo" />}
      </div>}
      <div className={styles.chat__message__content}>
        {renderMessage(message)}
      </div>
    </li>
  )
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([{ message: "Witaj! Jak mogę Ci pomóc?", sender: 'ai' }]);
  const [newestMessage, setNewestMessage] = useState<Message | null>(null);
  const [isNecessary, setIsNecessary] = useState<boolean | "unknown">("unknown");
  const [view, setView] = useState("");
  const [requiredInfo, setRequiredInfo] = useState<any>([]);
  const [validatedInfo, setValidatedInfo] = useState<any>(false);
  const [obtainedInfo, setObtainedInfo] = useState<Record<string, string>>({});
  const [closestUrzad, setClosestUrzad] = useState<Array<any>>([]);
  const [allUrzedy, setAllUrzedy] = useState<Array<any>>([]);
  const [xmlFile, _] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [conversationKey, setConversationKey] = useState<string | null>(null);
  const [requiredInfoLength, setRequiredInfoLength] = useState<number>(0);
  const [progress, setProgress] = useState<number>(0);
  const [multideviceIdx, setMultideviceIdx] = useState<string | null>(null);
  const [mobileImage, setMobileImage] = useState<string | null>(null);
  const [formType, setFormType] = useState<string | null>(null);
  const [formName, setFormName] = useState<string | null>(null);
  const [qrCode, setQrCode] = useState<any>(null);

  const { language } = useLanguage();

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/api/initialize_conversation`)
      .then(response => response.json())
      .then(data => {
        setMultideviceIdx(data.multidevice_idx);
        setQrCode(data.qr);
      })
  }, []);

  useEffect(() => {
    try {
      console.log(validatedInfo);
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/${formType}`)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          setRequiredInfo(data.message);
          let requiredInfoLength = 0;
          data.message.forEach((info: any) => {
            if (info.required) {
              requiredInfoLength++;
            }
          });
          setRequiredInfoLength(requiredInfoLength);
        })
    } catch (error) {
      console.error(error);
    }
  }, [formType])

  useEffect(() => {
    if (obtainedInfo.Ulica && obtainedInfo.NrDomu && obtainedInfo.Miejscowosc && obtainedInfo.KodPocztowy && obtainedInfo.UrzadSkarbowy == null) {
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
    else {
      setClosestUrzad([]);
      setAllUrzedy([]);
    }
    let isValid = true;
    let progress = 0;
    requiredInfo.forEach((info: string) => {
      if ((!obtainedInfo[info] || obtainedInfo[info] === '')) {
        isValid = false;
      }
      else {
        progress++;
      }
    });
    setProgress(progress);
    setValidatedInfo(isValid);

    if (validatedInfo) {
      generateXml();
    }
  }, [obtainedInfo]);

  const [input, setInput] = useState('');
  const { lastMessage, sendMessage } = useChatterWS(`ws/v1/chat/${multideviceIdx}`);

  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(JSON.stringify({
        command: 'basicFlow', text: input,
        required_info: requiredInfo,
        obtained_info: obtainedInfo,
        history: messages,
        is_necessary: isNecessary,
        language: language,
        conversation_key: conversationKey,
        form_name: formName
      }));

      setMessages([...messages, { message: input, sender: 'user' }]);
      setInput('');
      setIsLoading(true);
      // Here you would typically send the message to your backend
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/validate_infer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          data: obtainedInfo
        })
      }).then(response => response.json())
        .then(data => {
          console.log(data);
          // setObtainedInfo({...obtainedInfo, ...data.message});
        })
    }
  };

  React.useEffect(() => {
    if (lastMessage) {
      const lastMessageData = JSON.parse(lastMessage.data);
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
      else if (lastMessageData.command === 'connect') {
        setConversationKey(lastMessageData.messageId);
      }
      else if (lastMessageData.command === 'mobileMessage') {
        console.log("Setting mobile image");
        setMobileImage(lastMessageData.fileBase64);
      }
      else if (lastMessageData.command === 'formType') {
        console.log("Form type");
        console.log(lastMessageData.endpoint);
        setFormType(lastMessageData.endpoint);
        setFormName(lastMessageData.formName);
      }
    }
  }, [lastMessage]);


  useEffect(() => {
    if (mobileImage) {
      setIsLoading(true);
      console.log("Uploading mobile image");
      const formData = new FormData();

      // Convert base64 string to Blob
      console.log(mobileImage.slice(0, 100));
      const byteCharacters = atob(mobileImage.split(',')[1]);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'image/jpeg' });

      // Create File object from Blob
      const file = new File([blob], "image.jpg", { type: "image/jpeg" });
      formData.append('file', file);

      try {
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/upload`, {
          method: 'POST',
          body: formData,
        })
        .then(response => {
          if (response.ok) {
          console.log('Files uploaded');
          response.json().then(data => {
            if (data.responses) {
              if (!Array.isArray(data.responses)) {
                data.responses = [data.responses];
              }
            }
            if (data.responses && Array.isArray(data.responses)) {
              console.log(data.responses);
              const message = {
                command: 'basicFlow',
                text: "Oto treść umowy którą podpisałem. ```" + data.responses.join(' ') + "```",
                required_info: requiredInfo,
                history: [],
                is_necessary: "unknown",
                conversation_key: conversationKey,
                language: language,
                obtained_info: obtainedInfo,
                form_name: formName
              };
              sendMessage(JSON.stringify(message));
            }
            setProgress(100);
          });
        } else {
          console.error('Upload failed');
          setProgress(0);
          }
        })
        .catch(error => {
          console.error('Upload error:', error);
          setProgress(0);
        })
        .finally(() => {
          setIsLoading(false);
        });
      } finally {
        setIsLoading(false);
      }
    };
  }, [mobileImage]);

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
        // setXmlFile(url);
      })
  } catch (error) {
    console.error(error);
  }
}

return (
  <Box sx={{ minHeight: "100vh", width: "100%", display: "flex", flexDirection: "column" }}>
    <Nav />
    <div className={'container ' + styles.container__lg} style={{ paddingTop: "2em", paddingBottom: "2em", flex: 1 }}>
      <div className={styles.chat__progress}>
        <div
          className={styles.chat__progress__item}
          style={{ width: `${(progress / requiredInfoLength) * 100}%` }}
        >

        </div>
        <span className={styles.chat__progress__item__text}>
          {((progress / requiredInfoLength) * 100).toFixed(2)}%
        </span>
      </div>
      <div className={styles.chat__wrapper}>
        <Checklist required_info={requiredInfo} obtained_info={obtainedInfo} />
        <div className={styles.chat__container}>
          {messages.length < 2 && (view != "uploadDoc" ? (
            <div
              className={styles.chat__grid}
            >
              <GridItem
                onClick={() => { setView("uploadDoc") }}
                icon={signIcon}
                heading={"Prześlij umowę"}
                content={"System na bazie umowy sam uzupełni formularz. W przypadku braku informacji dopyta Cię o szczegóły."}
              />
              <GridItem
                onClick={() => { }}
                icon={voiceIcon}
                heading={"Wgraj umowę z telefonu"}
                content={"Zrób zdjęcie umowy i wgraj je tutaj."}
                qr={qrCode}
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
              (message: any) => {
                const msg = {
                  command: 'basicFlow',
                  text: message.text.replaceAll("\n", " "),
                  required_info: requiredInfo,
                  obtained_info: obtainedInfo,
                  history: messages,
                  is_necessary: isNecessary,
                  language: language,
                  conversation_key: conversationKey,
                  form_name: formName
                };
                setMessages(m => [...m, { message: message.text, sender: 'user', hidden: true }]);
                sendMessage(JSON.stringify(msg));
                setIsLoading(true);
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
      </div>
    </div>
    <div className="container" style={{ paddingTop: "2em", paddingBottom: "2em", flex: 1 }}>

      <Form required_info={requiredInfo} obtained_info={obtainedInfo} setObtainedInfo={setObtainedInfo} />

      {allUrzedy && <GovermentSelect closestUrzad={closestUrzad} updateUrzad={updateUrzad} allUrzedy={allUrzedy} generateXml={generateXml} />}
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
