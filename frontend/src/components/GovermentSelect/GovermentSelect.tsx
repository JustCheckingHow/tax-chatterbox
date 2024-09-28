import styles from "./GovermentSelect.module.scss"

interface GovermentSelectProps {
  closestUrzad: any[];
  updateUrzad: (code: string) => void;
  allUrzedy: any[];
}

function GovermentSelect(props: GovermentSelectProps) {
    return (
        <div className={styles.govermentSelect__container}>
            <h3>Wybierz swój urząd skarbowy</h3>
            
            <p>Najbliższe urzędy na bazie twojej lokalizacji:</p>

            {props.closestUrzad && props.closestUrzad.map((urzad) => (
                <div key={urzad.name} onClick={() => props.updateUrzad(urzad.code)}>
                    <p>{urzad.name}</p>
                    <p>{urzad.address}</p>
                </div>
            ))}

            <div className="label">Inne</div>
            
            <datalist id="urzady">
                {props.allUrzedy.map((urzad) => (
                    <option value={urzad.name}>{urzad.name}</option>
                ))}
            </datalist>

            <input type="text" id="another_urzad" list="urzady" onChange={(e) => props.updateUrzad(e.target.value)} />

            <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
                props.generateXml();
            }}
            
            ><span>Zatwierdź swój urząd</span></button>

        </div>
    )
}

export default GovermentSelect;

