import React from 'react';
import styles from "./Nav.module.scss";
import logo from "../../assets/image/logo.png"
import { Link } from 'react-router-dom';

import { Language, useLanguage } from '../../context/languageContext';

const Nav: React.FC = () => {
    const { language, setLanguage } = useLanguage();

    return (
        <nav className={styles.nav}>
            <div className={styles.nav__container}>
                <Link to="/chat" className={styles.nav__logo}>
                    <img src={logo} alt="" />
                    <h1>JustCheckingTax</h1>
                </Link>
                <select name="lang" id="lang" style={{width: "90px"}} onChange={(e) => {
                    setLanguage(e.target.value as Language);
                }}>
                    <option value="pl" selected={language === "pl"}>PL </option>
                    <option value="en" selected={language === "en"}>EN </option>
                    <option value="uk" selected={language === "uk"}>UK </option>
                </select>
            </div>
        </nav>
    );
};

export default Nav;