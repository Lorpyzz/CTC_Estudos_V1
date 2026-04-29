import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import LandingPage from './pages/PaginaInicial';
import HomePage from './pages/HomePage'; 
import DisciplinasPage from './pages/DisciplinasPage';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
  
        <Route path="/" element={<LandingPage />} />

        <Route path="/auth" element={<HomePage />} />

        <Route path="/disciplinas" element={<DisciplinasPage />} />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;