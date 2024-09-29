import styles from "./GridItem.module.scss"

interface GridItemProps {
    onClick: () => void;
    heading: string;
    content: string;
    icon: string;
    qr?: string;
}

const GridItem = ({ onClick, icon, heading, content, qr }: GridItemProps) => {
    // parse qr from base64
    const qrCode = qr ? `data:image/png;base64,${qr}` : null;

    return (
        <div onClick={onClick} className={styles.gridItem__wrapper}>
            <header className={styles.gridItem__header}>
                <div className={styles.gridItem__icon}>
                    <img src={icon} alt={heading}/>
                </div>
                <span>{heading}</span>
            </header>
            {qrCode && <img src={qrCode} alt="QR Code" style={{ width: "128px", height: "128px", alignSelf: "center" }} />}
            <div className={styles.gridItem__content}>
                <p>{content}</p>
            </div>
        </div>
    )
}

export default GridItem;