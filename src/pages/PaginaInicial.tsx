import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PaginaInicial.css'; 

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-wrapper">
      <nav className="navbar">
        <div className="logo-container">
          <img src="/ctc-estudos.png" alt="Logo" className="logo-img" />
          <span className="logo-text">CTC Estudos</span>
        </div>
        
        <div className="nav-links">
          <a href="#" className="nav-link active">Início</a>
          <a href="#" className="nav-link">Disciplinas</a>
          <a href="#" className="nav-link">Flashcards</a>
          <a href="#" className="nav-link">Central de Dúvidas</a>
          <a href="#" className="nav-link">Chat</a>
          <button className="btn-entrar-nav" onClick={() => navigate('/auth')}>
            Entrar
          </button>
        </div>
      </nav>

      <header className="hero-section">
        <h1>
          Seu portal de estudos <br /> 
          do CTC – PUC-Rio
        </h1>
        <p>
          Materiais, resumos e uma comunidade colaborativa para você ir mais longe nas suas disciplinas.
        </p>

        <div className="hero-buttons">
          <button className="btn-primary" onClick={() => navigate('/disciplinas')}>
            Explorar Disciplinas &rarr;
          </button>
          <button className="btn-secondary" onClick={() => navigate('/auth')}>
            Fazer Login
          </button>
        </div>
      </header>
    </div>
  );
};

export default LandingPage;