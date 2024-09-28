import { useState, useEffect, useCallback } from 'react';


const useChatterWS = (path: string) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [messages, setMessages] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  const lastMessage = messages[messages.length - 1];
  useEffect(() => {
    const ws = new WebSocket(`${import.meta.env.VITE_BACKEND_URL}/${path}`);
    console.log(`${import.meta.env.VITE_BACKEND_URL}/${path}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [path]);

  const sendMessage = useCallback((message: string) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ message }));
    }
    else {
      console.error('WebSocket is not connected');
    }
  }, [socket]);

  return { messages, lastMessage, sendMessage, isConnected };
};

export default useChatterWS;
