import React from 'react';
import styles from "./Nav.module.scss";

const Nav: React.FC = () => {
    return (
        <nav className={styles.nav}>
            <div className={styles.nav__container}>
                <a href="" className={styles.nav__logo}>
                    <h1>Tax Chatter</h1>
                </a>
                <ul className={styles.nav__ul}>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
        </nav>
    );
};

export default Nav;