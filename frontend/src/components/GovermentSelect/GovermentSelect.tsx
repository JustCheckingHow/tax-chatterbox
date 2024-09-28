import styles from "./GovermentSelect.module.scss"

import { govermentList } from "./govermentList"

const GovermentSelect = () => {
    

    return (
        <div className={styles.govermentSelect__container}>
            <h3>Wybierz swój urząd skarbowy</h3>
            
            <p>Najbliższe urzędy na bazie twojej lokalizacji</p>

            
            <div className="label">Inne</div>
            <select name="" id="">
                {Object.keys(govermentList).map((key) => (
                    <option value={key}>{key}</option>
                ))}
            </select>

            <select name="" id="">
                {Object.keys(govermentList).map((key) => (
                    <option value={key}>{key}</option>
                ))}
            </select>

            <button type="button" className="btn btn-primary"><span>Zatwierdź swój urząd</span></button>

        </div>
    )
}

export default GovermentSelect;

