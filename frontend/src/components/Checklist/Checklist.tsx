import React from 'react';
import styles from "./Checklist.module.scss";

interface ChecklistProps {
    required_info: { [key: string]: { description: string, required: boolean, label: string, pattern: string, type: string } }[];
    obtained_info: { [key: string]: any };
    setObtainedInfo: React.Dispatch<React.SetStateAction<{ [key: string]: any }>>;
}


const Checklist: React.FC<ChecklistProps> = ({ required_info, obtained_info, setObtainedInfo }) => {
    console.log(required_info);

    return (
        <aside className={styles.checklist__aside}>
            <h3>Skompletowane dane</h3>
            <ul className={styles.checklist__ul}>

                {Object.entries(required_info).map(([_, value], index) => {
                    const label = Object.values(value)[0].label;
                    const name = Object.keys(value)[0];
                    const val = obtained_info[name];
                    const isChecked = val !== undefined;
<<<<<<< HEAD
                    let isRequired = Object.values(value)[0].required;
                    const type = Object.values(value)[0].type != "string" ? Object.values(value)[0].type : "text";
=======
                    // const type = value.type ? value.type : "text";
                    const type = typeof value.type === 'string' ? value.type : "text";

>>>>>>> 4dad222b470c7942d400a98e601fc70afb14c043
                    return (
                        <li key={index} className={isChecked ? styles.checked : ""}>
                            <div className={(isRequired ? styles.label : "") + " label"}>{label}</div>
                            <input type={type} value={val} onChange={(e) => {
                                setObtainedInfo((prev) => ({ ...prev, [name]: e.target.value }));
                            }} />
                        </li>
                    );
                })}
            </ul>
        </aside>
    );
};

export default Checklist;