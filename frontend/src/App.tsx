import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom'
import "./assets/styles/global.scss"
import Chat from './pages/chat'
// import Admin from './pages/admin/Admin'  // Add this import
import { LanguageProvider } from './context/languageProvider'


function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<Chat />} />
        <Route path="/chat" element={<Chat />} />
        {/* <Route path="/admin" element={<Admin />} /> */}
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
