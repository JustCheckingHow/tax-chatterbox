import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import LangContext from './context/LangContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <LangContext.Provider value={"pl"}>
      <App />
    </LangContext.Provider>
  </StrictMode>,
)
