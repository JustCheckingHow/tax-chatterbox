import React, { useState } from 'react';
import Nav from '../../components/Nav/Nav';
import { useParams } from 'react-router-dom';
import useWebSocket from 'react-use-websocket';


const MobileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { id } = useParams();

  const { sendMessage } = useWebSocket(`https://justcheckinghow.com/ws/v1/chat/${id}`);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('No file selected');
      return;
    }
    
    setUploading(true);
    
    const fileBase64 = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });

    sendMessage(JSON.stringify({
      type: 'mobileMessage',
      message: 'Hello, world!',
      fileBase64: fileBase64,
    }));
  };

  if (uploading) return <div>Uploading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
        <Nav />
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
        </div>
    </div>
  );
};

export default MobileUpload;