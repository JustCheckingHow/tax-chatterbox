import styles from "./GridItem.module.scss"

const GridItem = (props) => {
    return (
        <div onClick={props.onClick} className={styles.gridItem__wrapper}>
            <header className={styles.gridItem__header}>
                <div className={styles.gridItem__icon}>
                    <img src={props.icon} alt={props.heading}/>
                </div>
                <span>{props.heading}</span>
            </header>
            <div className={styles.gridItem__content}>
                <p>{props.content}</p>
            </div>
        </div>
    )
}

export default GridItem;