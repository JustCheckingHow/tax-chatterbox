import { useState, useCallback } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const useChatterWS = (path: string) => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [messages, setMessages] = useState<any[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(`${import.meta.env.VITE_BACKEND_URL}/${path}`, {
    onOpen: () => console.log(`WebSocket connected to ${path}`),
    onClose: () => console.log('WebSocket disconnected'),
    onMessage: (event) => {
      const data = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, data]);
    },
    shouldReconnect: () => true,
  });

  const isConnected = readyState === ReadyState.OPEN;

  const sendMessageCallback = useCallback((message: string) => {
    if (isConnected) {
      sendMessage(message);
    } else {
      console.error('WebSocket is not connected');
    }
  }, [sendMessage, isConnected]);

  return { messages, lastMessage, sendMessage: sendMessageCallback, isConnected };
};

export default useChatterWS;
