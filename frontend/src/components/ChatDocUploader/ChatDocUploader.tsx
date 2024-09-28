import React, { useState } from 'react';
import {Simulate} from "react-dom/test-utils";
import progress = Simulate.progress;
import styles from "./ChatDocUploader.module.scss"

const ChatDocUploader = () => {
    const [files, setFiles] = useState<File[]>([]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files;
        if (selectedFiles) {
            setFiles([...selectedFiles]);
        }
    };

    const handleUpload = async () => {
        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
        });
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/upload`, {
            method: 'POST',
            body: formData,
        });
        if (response.ok) {
            console.log('Files uploaded');
        }
    };

    return (
        <div className={styles.uploader__container}>
            <div className="gov-file-uploader ">
                <div className="gov-file-uploader__header">
                    <h3>Dodaj pliki</h3>
                </div>
                <div className="gov-file-uploader__input">
                    <input
                        name="files"
                        type="file"
                        accept=".pdf,.jpg,.jpeg,.png"
                        tabIndex={-1}
                        onChange={handleFileChange}
                    />
                    <p>Przeciągnij i upuść pliki na to pole<br/>
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
                                    <div className="gov-progress__progress-bar" style={{ width: progress + '%' }}>
                                    </div>
                                </div>
                                <div className="gov-progress__label">{String(progress)}%</div>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default ChatDocUploader;