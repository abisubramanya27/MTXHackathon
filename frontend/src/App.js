import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import HomePage from './views/HomePage.js';
import Dashboard from './views/Dashboard.js';
import NotFoundPage from './views/404.js';
import Loading from './components/Loading.js';
import {
    Routes,
    Navigate,
    Route
} from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

function App() {
    const { isAuthenticated } = useAuth0();
    const { isLoading } = useAuth0();

    if (isLoading) {
        return <Loading />;
    }

    return (
        <Routes>
        <Route path="/" element={ isAuthenticated ? <Navigate to={"/dashboard"} /> :
            <HomePage />  
        }/>
        <Route path="/dashboard" element={ <Dashboard /> } />
        <Route path="*" element={ <NotFoundPage /> } />
        </Routes>
    );
}

export default App;