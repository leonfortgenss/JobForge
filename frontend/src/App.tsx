import {Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import AppLayout from './components/AppLayout'
import Home from './pages/Home'

function App() {

  return (
    <Router>
        <AppLayout>
          <Routes>
            <Route path='app/home' element={<Home />} />
          </Routes>
        </AppLayout>
    </Router>
  )
}

export default App
