import styles from "./GridItem.module.scss"

interface GridItemProps {
    onClick: () => void;
    heading: string;
    content: string;
    icon: string;
}

const GridItem = ({ onClick, icon, heading, content }: GridItemProps) => {
    return (
        <div onClick={onClick} className={styles.gridItem__wrapper}>
            <header className={styles.gridItem__header}>
                <div className={styles.gridItem__icon}>
                    <img src={icon} alt={heading}/>
                </div>
                <span>{heading}</span>
            </header>
            <div className={styles.gridItem__content}>
                <p>{content}</p>
            </div>
        </div>
    )
}

export default GridItem;