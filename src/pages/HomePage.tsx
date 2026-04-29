import React, { useState } from 'react';
import { FaLock } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import './HomePage.css'; // Importando o novo arquivo

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Login:', { email, password });
    navigate('/disciplinas');
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-box">
        <div className="login-header">
          <img src="/ctc-estudos.png" alt="Logo" className="logo-img" />
          <span className="logo-text" style={{"color":"black"}}>CTC Estudos</span>
          <h2>Entrar</h2>
        </div>

        <div className="input-group">
          <label htmlFor="email">E-mail *</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="seu@email.com"
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Senha *</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="********"
            required
          />
        </div>

        <button type="submit" className="btn-login">
          ENTRAR
        </button>

        <div className="login-footer">
          <a href="#">Esqueceu a senha?</a>
          <a href="#">Cadastre-se</a>
        </div>
      </form>
    </div>
  );
};

export default HomePage;