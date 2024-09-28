import React from 'react';
import styles from "./Nav.module.scss";
import logo from "../../assets/image/logo.png"
import { Link } from 'react-router-dom';

import chatIcon from "../../assets/icons/czatbot.svg";
import knowledgeIcon from "../../assets/icons/bazawiedzy.svg";
import homeIcon from "../../assets/icons/home.svg";

const Nav: React.FC = () => {
    return (
        <nav className={styles.nav}>
            <div className={styles.nav__container}>
                <Link to="/chat" className={styles.nav__logo}>
                    <img src={logo} alt="" />
                    <h1>JustCheckingTax</h1>
                </Link>
                <select name="" id="" style={{width: "90px"}}>
                    <option value="pl">PL </option>
                    <option value="en">EN </option>
                    <option value="uk">UK </option>
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