import React from 'react';
import styles from "./Footer.module.scss";

const Nav: React.FC = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footer__container + " container"}>
                <div className={styles.footer__col}>
                    <h3>JustCheckingTax</h3>
                    <p></p>
                </div>
            </div>
        </footer>
    );
};

export default Nav;