import React from 'react';
import styles from "./Checklist.module.scss";

interface ChecklistProps {
    required_info: { [key: string]: string };
}

const Checklist: React.FC<ChecklistProps> = ({ required_info }) => {

    return (
        <aside className={styles.checklist__aside}>
            <h3>Skompletowane dane</h3>
            <ul className={styles.checklist__ul}>
                {Object.entries(required_info).map(([key, value], index) => (
                        <li key={index} className={value !== "" ? styles.checked : ""}>
                            <strong>{key}:</strong> {value}
                        </li>
                    
                ))}
            </ul>
        </aside>
    );
};

export default Checklist;