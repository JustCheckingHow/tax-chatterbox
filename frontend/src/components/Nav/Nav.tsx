import React from 'react';
import styles from "./Nav.module.scss";
import logo from "../../assets/image/logo.png"
import { Link } from 'react-router-dom';

const Nav: React.FC = () => {
    return (
        <nav className={styles.nav}>
            <div className={styles.nav__container}>
                <Link to="/chat" className={styles.nav__logo}>
                    <img src={logo} alt="" />
                    <h1>JustCheckingTax</h1>
                </Link>
            
            </div>
        </nav>
    );
};

export default Nav;