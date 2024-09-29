import React from 'react';
import styles from "./Footer.module.scss";

const Nav: React.FC = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footer__container + " container"}>
                <div className={styles.footer__col} style={{textAlign: "center"}}>
                    <p>© 2024 JustCheckingHow.com</p>
                </div>
            </div>
        </footer>
    );
};

export default Nav;