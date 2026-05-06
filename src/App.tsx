import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Inicial from './pages/PaginaInicial';
import Cadastro from './pages/HomePage'; 

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
  
        <Route path="/" element={<Inicial />} />

        <Route path="/cadastro/" element={<Cadastro />} />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;