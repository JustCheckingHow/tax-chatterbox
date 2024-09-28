import './App.css'
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom'
import Main from './pages/main'
import Chat from './pages/chat'

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<Main />} />
        <Route path="/chat" element={<Chat />} />
      </>
    )
  )
  
  return <RouterProvider router={router} />
}

export default App
