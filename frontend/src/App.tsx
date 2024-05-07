
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppLayout from './components/AppLayout';
import Home from './pages/Home';
import LandingPage from './pages/LandingPage';
import HistoricalData from './pages/HistoricalData';
import SignIn from './pages/SignIn';
import Register from './pages/Register';

const queryClient = new QueryClient();

function App() {
  return (
    <Router>
      <QueryClientProvider client={queryClient}>
        <Routes>
            <Route path='/' element={<LandingPage />} />
            <Route path='/signin' element={<SignIn />} />
            <Route path='/register' element={<Register />} />
        </Routes>
        <AppLayout>
          <Routes>
            <Route path='/home' element={<Home />} />
            <Route path='historical-data' element={<HistoricalData />} />
          </Routes>
        </AppLayout>
      </QueryClientProvider>
    </Router>
  );
}

export default App;
