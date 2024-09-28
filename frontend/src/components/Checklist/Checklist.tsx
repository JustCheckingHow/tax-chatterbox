import React from 'react';
import styles from "./Checklist.module.scss";

interface ChecklistProps {
    required_info: { [key: string]: { description: string, required: boolean } }[];
    obtained_info: { [key: string]: any };
}

const Checklist: React.FC<ChecklistProps> = ({ required_info, obtained_info }) => {
    return (
        <aside className={styles.checklist__aside}>
            <h3>Skompletowane dane</h3>
            <ul className={styles.checklist__ul}>
                {Object.entries(required_info).map(([key, value], index) => {
                    const description = Object.values(value)[0].description;
                    const name = Object.keys(value)[0];
                    const val = obtained_info[name];
                    const isChecked = val !== undefined;

                    console.log(value, val, description);
                    return (
                        <li key={index} className={isChecked ? styles.checked : ""}>
                            <strong>{description}:</strong> {val}
                        </li>
                    );
                }
                )}
            </ul>
        </aside>
    );
};

export default Checklist;