import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom'
import "./assets/styles/global.scss"
import Chat from './pages/chat'
import Admin from './pages/admin/Admin'  // Add this import
import { LanguageProvider } from './context/languageProvider'
import MobileUpload from './pages/mobileUpload/mobileUpload'


function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<Chat />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/mobileUpload/:id" element={<MobileUpload />} />
        <Route path="/admin" element={<Admin />} />
      </>
    )
  )
  
  return (
    <LanguageProvider>
      <RouterProvider router={router} />
    </LanguageProvider>
  )
}

export default App
