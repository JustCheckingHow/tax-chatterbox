import React, { useContext, useEffect, useState } from 'react';
import styles from "./Nav.module.scss";
import logo from "../../assets/image/logo.png"
import { Link } from 'react-router-dom';

import chatIcon from "../../assets/icons/czatbot.svg";
import knowledgeIcon from "../../assets/icons/bazawiedzy.svg";
import homeIcon from "../../assets/icons/home.svg";
import LangContext from '../../context/LangContext';

const Nav: React.FC = () => {
    const [lang, setLang] = useState("pl");
    let langContext = useContext(LangContext);

    useEffect(() => {
        langContext = lang;
        // window.location.reload();
    }, [lang]);

    return (
        <nav className={styles.nav}>
            <div className={styles.nav__container}>
                <Link to="/chat" className={styles.nav__logo}>
                    <img src={logo} alt="" />
                    <h1>JustCheckingTax</h1>
                </Link>
                <select name="lang" id="lang" style={{width: "90px"}} onChange={(e) => {
                    setLang(e.target.value);
                }}>
                    <option value="pl" selected={lang === "pl"}>PL </option>
                    <option value="en" selected={lang === "en"}>EN </option>
                    <option value="uk" selected={lang === "uk"}>UK </option>
                </select>
                <ul className={styles.nav__ul}>
                    <li>
                        <Link to="/">
                            <img src={homeIcon} alt="homeIcon" />
                            <p>Strona Główna</p>
                        </Link>
                    </li>
                    <li>
                        <Link to="/chat">
                            <img src={chatIcon} alt="chatIcon" />
                            <p>Chat</p>
                        </Link>
                    </li>
                    <li>
                        <Link to="/chat">
                            <img src={knowledgeIcon} alt="knowledgeIcon" />
                            <p>Jak wysłać PCC-3?</p>
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Nav;