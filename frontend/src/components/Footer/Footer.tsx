import React from 'react';
import styles from "./Footer.module.scss";

const Nav: React.FC = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footer__container + " container"}>
                <div className={styles.footer__col}>
                    <h3>JustCheckingTax</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ex excepturi labore neque?</p>
                </div>
            </div>
        </footer>
    );
};

export default Nav;