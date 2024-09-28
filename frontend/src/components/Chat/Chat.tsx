import React, {useEffect, useState} from "react";
import {Button, Grid, Paper, TextField, Typography} from "@mui/material";
import GridItem from "../GridItem/GridItem.tsx";
import styles from "./Chat.module.scss";
import ChatDocUploader from "../ChatDocUploader/ChatDocUploader.tsx";

import signIcon from "../../assets/icons/sign.svg";
import chatIcon from "../../assets/icons/czatbot.svg";
import voiceIcon  from "../../assets/icons/callcenter.svg";


const Chat = () => {
    const [chatStarted, setChatStarted] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [chatHistory, setChatHistory] = useState<string[]>([]);

    const [view, setView] = useState("");

    useEffect(() => {
        console.log(view);
    }, [view]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (inputValue.trim()) {
            setChatHistory([...chatHistory, inputValue]);
            setInputValue('');
            setChatStarted(true);
        }
    };
    return(
        <div className={styles.chat__container}>
            {chatStarted && (
                <Grid item xs={12} md={6}>
                        {chatHistory.map((message, index) => (
                            <Typography key={index} paragraph>
                                {message}
                            </Typography>
                        ))}
                </Grid>
            )}
            {!chatStarted && (view != "uploadDoc" ? (
                <div
                    className={styles.chat__grid}
                >
                    <GridItem
                        icon={chatIcon}
                        heading={"Opisz swoją sprawę"}
                        content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
                    />
                    <GridItem
                        onClick={() => {setView("uploadDoc")}}
                        icon={signIcon}
                        heading={"Prześlij umowę"}
                        content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
                    />
                    <GridItem
                        icon={voiceIcon}
                        heading={"Porozmawiaj z asystentem"}
                        content={"System na bazie umowy sam uzupełni formularz w przypadku braku informacji dopyta Ciebie."}
                    />
                </div>
            ) : <ChatDocUploader/>)}
                    <form onSubmit={handleSubmit} className={styles.chat__form}>
                        <input
                            className={styles.chat__input}
                            placeholder="Tu wpisz wiadomość"
                            value={inputValue}
                            type="text"
                            onChange={(e) => setInputValue(e.target.value)}
                        />
                        <button type={"button"} className={"btn btn-secondary"}>
                            <svg version="1.1" id="Warstwa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                                 viewBox="0 0 54 54">
                                <title>brexit-mpit</title>
                                <line className="st0" x1="8.3" y1="13.5" x2="2.3" y2="13.5"/>
                                <path className="st0" d="M2.3,13.5v15.6c0.1,2.8,2.5,5,5.3,4.9h38.8c2.8,0.1,5.2-2.1,5.3-4.9v-26H8.3v23.4"/>
                                <path id="Path-43" className="st0" d="M38.2,9.8H13.9"/>
                                <path id="Path-43-2" className="st0" d="M28.3,17.3H13.9"/>
                                <path id="Path-43-3" className="st0" d="M25,24.8H13.9"/>
                                <path className="st1" d="M38.3,43.6L38.3,43.6c-3.6,0-6.6-3-6.6-6.6v-9.2c0-3.6,3-6.6,6.6-6.6l0,0c3.6,0,6.6,3,6.6,6.6V37
	C44.8,40.6,41.9,43.5,38.3,43.6z"/>
                                <line className="st0" x1="35.2" y1="28.1" x2="31.7" y2="28.1"/>
                                <line className="st0" x1="35.2" y1="32.4" x2="31.7" y2="32.4"/>
                                <line className="st0" x1="35.2" y1="36.7" x2="31.7" y2="36.7"/>
                                <line className="st0" x1="44.8" y1="28.1" x2="41.3" y2="28.1"/>
                                <line className="st0" x1="44.8" y1="32.4" x2="41.3" y2="32.4"/>
                                <line className="st0" x1="44.8" y1="36.7" x2="41.3" y2="36.7"/>
                                <path className="st0" d="M28.5,38c0.7,5.4,5.6,9.2,11.1,8.5c4.5-0.6,8-4.1,8.5-8.5"/>
                                <line className="st0" x1="38.3" y1="46.6" x2="38.3" y2="50.9"/>
                                <line className="st0" x1="33.1" y1="50.9" x2="43.8" y2="50.9"/>
                            </svg>
                        </button>
                        <button className={"btn btn-primary"}>
                            <span>Wyślij</span>
                        </button>
                    </form>
        </div>
    )
}

export default Chat;