import React, { useState } from 'react';
import styles from "./ChatDocUploader.module.scss"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const ChatDocUploader = ({sendMessage}: {sendMessage: (message: any) => void}) => {
    const [files, setFiles] = useState<File[]>([]);
    const [progress, setProgress] = useState<number>(0);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files;
        if (selectedFiles) {
            setFiles([...selectedFiles]);
        }
    };

    const handleUpload = async () => {
        setIsLoading(true);
        const formData = new FormData();
        files.forEach((file) => {
            formData.append('file', file);
        });

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/upload`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                console.log('Files uploaded');
                const data = await response.json();
                if (data.responses && Array.isArray(data.responses)) {
                    const message = {
                        command: 'basicFlow',
                        text: data.responses.join(' '),
                        required_info: {},
                        history: [],
                        is_necessary: "unknown"
                    };
                    sendMessage(message);
                    console.log("Wysłałem wiadomość");
                    console.log(message);
                }
                setProgress(100);
            } else {
                console.error('Upload failed');
                setProgress(0);
            }
        } catch (error) {
            console.error('Upload error:', error);
            setProgress(0);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={styles.uploader__container}>
            <div className="gov-file-uploader ">
                <div className="gov-file-uploader__header">
                    <h3>Dodaj umowę</h3>
                </div>
                <div className="gov-file-uploader__input">
                    <input
                        name="files"
                        type="file"
                        accept=".pdf,.jpg,.jpeg,.png"
                        tabIndex={-1}
                        onChange={handleFileChange}
                        disabled={files.length > 0}
                    />
                    <p>Przeciągnij i upuść umowę na to pole<br/>
                        albo załaduj z dysku.</p>
                    <button
                        className="btn btn-secondary"
                        onClick={handleUpload}
                    >
                        <span>Dodaj plik</span>
                    </button>
                    <p className="info">Dopuszczalna liczba plików: 1<br/>
                        Dopuszczalne formaty plików: .pdf, .jpg, .png<br/>
                        Maksymalny rozmiar 500 kb</p>
                </div>
                <div className="gov-file-uploader__files-list">
                    <ul>
                        {files.map((file, index) => (
                            <li key={index}>
                                {file.name}<br/>
                                <div className="gov-progress gov-progress--small">
                                    <div className="gov-progress__progress-bar" style={{ width: `${progress}%` }}>
                                    </div>
                                </div>
                                <div className="gov-progress__label">{progress}%</div>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default ChatDocUploader;