import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom'
import Main from './pages/main'
import "./assets/styles/global.scss"

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<Main />} />
      </>
    )
  )
  
  return <RouterProvider router={router} />
}

export default App
