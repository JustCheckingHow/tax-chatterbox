import styles from './Checklist.module.scss';

interface ChecklistProps {
    required_info: { [key: string]: { description: string, required: boolean, label: string, pattern: string, type: string } }[];
    obtained_info: { [key: string]: any };
}


const Checklist: React.FC<ChecklistProps> = ({ required_info, obtained_info }) => {
    return (
        <aside className={styles.checklist__aside}>
            <h3>Dane</h3>
            <ul className={styles.checklist__ul}>

                {Object.entries(required_info).map(([_, value], index) => {
                    const label = Object.values(value)[0].label;
                    const name = Object.keys(value)[0];
                    const val = obtained_info[name];
                    
                    let isChecked = true;

                    Object.values(value)[0].content.forEach((item) => {
                        const itemName = Object.keys(item)[0];
                        const itemVal = obtained_info[itemName];
                        if (itemVal === '' || itemVal === undefined) {
                            isChecked = false;
                        }
                    });

                    return (
                        <li key={index} className={isChecked ? styles.checked : ""}>
                            <a href={"#" + label}>{label}</a>
                        </li>
                    );
                })}
            </ul>
        </aside>
    )
}

export default Checklist;
