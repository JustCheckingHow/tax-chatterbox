import styles from "./FinalDocument.module.scss";

import docsIcon from "../../assets/icons/docs.svg";

import knowledgeIcon from "../../assets/icons/bazawiedzy.svg";
import { Link } from "react-router-dom";

const FinalDocument = (props: any) => {
    console.log(props.xmlFile);
    return (
        <div className={styles.finalDocument + " box"}>
            <h3 style={{textAlign: "center"}}>Twój dokument PCC-3 jest gotowy!</h3> 

            <div className={styles.finalDocument__download + " gov-file-uploader__input"}>
                <img src={docsIcon} alt="docsIcon" />
                <button className={styles.finalDocument__button + " btn btn-primary"}>
                    <span>Pobierz dokument</span>
                </button>
            </div>

            <Link to="/" className={styles.finalDocument__info}>
                <img src={knowledgeIcon} alt="knowledgeIcon" />
                <p>Co należy zrobić dalej?</p>
            </Link>
        </div>
    )
}

export default FinalDocument;

