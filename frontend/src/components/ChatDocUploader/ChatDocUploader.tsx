// import React, { useState } from 'react';
import {Simulate} from "react-dom/test-utils";
import progress = Simulate.progress;

const ChatDocUploader = () => {
    // const [files, setFiles] = useState<File[]>([]);

    // const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    //     const files = e.target.files;
    //     if (files) {
    //         setFiles([...files]);
    //     }
    // };

    // const handleUpload = async () => {
    //     const formData = new FormData();
    //     files.forEach((file) => {
    //         formData.append('files', file);
    //     });
    //     const response = await fetch('http://localhost:3000/upload', {
    //         method: 'POST',
    //         body: formData,
    //     });
    //     if (response.ok) {
    //         console.log('Files uploaded');
    //     }
    // };

    return (
        <form encType="multipart/form-data" noValidate>
            <div className="gov-file-uploader ">
                <div className="gov-file-uploader__header">
                    <h3>Dodaj pliki</h3>
                </div>
                <div className="gov-file-uploader__input">
                    <input
                        name="files"
                        type="file"
                        accept="image/png, image/jpeg, image/jpg"
                        tabIndex={-1}
                    />
                    <p>Przeciągnij i upuść pliki na to pole<br/>
                        albo załaduj z dysku.</p>
                    <button
                        className="btn btn-secondary"
                    >
                        <span>Dodaj plik</span>
                    </button>
                    <p className="info">Dopuszczalna liczba plików: 1<br/>
                        Dopuszczalne formaty plików: .jpg, .png, .pdf ,
                        .doc, .zip, .rar<br/>
                        Maksymalny rozmiar 500 kb</p>
                </div>
                <div className="gov-file-uploader__files-list">
                    <ul>
                        <li>
                            nazwa_pliku.pdf<br/>
                            <div className="gov-progress gov-progress--small">
                                <div className="gov-progress__progress-bar" style={{ width: progress + '%' }}>
                                </div>
                            </div>
                            <div className="gov-progress__label">50%</div>
                            <div className="error__message">
                                Błąd podczas dodawania pliku
                            </div>
                            <button
                                type="button"
                                aria-label="Zamknij">
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </form>
    )
}

export default ChatDocUploader;