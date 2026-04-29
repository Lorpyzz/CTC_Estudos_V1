import React from 'react';
// Importamos os componentes necessários para as rotas
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import LandingPage from './pages/PaginaInicial';
import HomePage from './pages/HomePage'; // Esta é a página de login que fizemos no estilo "Material"
import DisciplinasPage from './pages/DisciplinasPage';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* 1. A primeira página que o usuário vê (Landing Page) */}
        <Route path="/" element={<LandingPage />} />

        {/* 2. A rota para a página de Login (Auth) */}
        <Route path="/auth" element={<HomePage />} />

        {/* 3. A rota para a listagem de disciplinas */}
        <Route path="/disciplinas" element={<DisciplinasPage />} />

        {/* 4. Caso o usuário tente acessar qualquer outra rota inexistente, 
               ele é mandado de volta para a Landing Page */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;