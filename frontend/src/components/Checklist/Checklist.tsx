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
                    value !== "" && (
                        <li key={index}>
                            <strong>{key}:</strong> {value}
                        </li>
                    )
                ))}
                <li className={styles.checked}>Imię</li>
            </ul>
        </aside>
    );
};

export default Checklist;