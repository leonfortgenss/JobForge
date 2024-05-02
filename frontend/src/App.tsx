
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppLayout from './components/AppLayout';
import Home from './pages/Home';

const queryClient = new QueryClient();

function App() {
  return (
    <Router>
      <QueryClientProvider client={queryClient}>
        <AppLayout>
          <Routes>
            <Route path='app/home' element={<Home />} />
          </Routes>
        </AppLayout>
      </QueryClientProvider>
    </Router>
  );
}

export default App;
