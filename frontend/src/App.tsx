import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppLayout from './components/AppLayout';
import Home from './pages/Home';
import SignIn from './pages/SignIn';

const queryClient = new QueryClient();

function App() {
  return (
    <Router>
      <QueryClientProvider client={queryClient}>
        <Routes>
          <Route path='/' element={<SignIn />} />
          <Route
            path='/home'
            element={
              <AppLayout>
                <Home />
              </AppLayout>
            }
          />
        </Routes>
      </QueryClientProvider>
    </Router>
  );
}

export default App;
