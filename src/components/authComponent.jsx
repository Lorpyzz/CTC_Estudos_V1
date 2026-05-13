import React, { useState } from 'react';
import axios from 'axios';

const AuthComponent = () => {
  // 1. Gerenciamento de Estado Único (Mais limpo e escalável)
  const [formData, setFormData] = useState({
    username: '', // Matrícula (conforme seu forms.html)
    email: '',
    password: '',
    first_name: ''
  });

  
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  
  const handleAuth = async (e, type) => {
    e.preventDefault();
    
    
    const baseUrl = "http://127.0.0.1:8000/api/";
    const endpoint = type === 'login' ? 'token/' : 'usuarios/';

    try {
      const response = await axios.post(`${baseUrl}${endpoint}`, formData);
      
      if (type === 'login') {
        localStorage.setItem('token', response.data.token);
        alert("Login realizado! Redirecionando para Disciplinas...");
      } else {
        alert("Cadastro criado com sucesso! Agora você pode fazer login.");
      }
    } catch (error) {
      
      const errorMsg = error.response?.data?.detail || "Erro na conexão com o servidor.";
      alert(errorMsg);
    }
  };

  return (
    <div className="auth-container">
      <h2>{}</h2>
      <form>
        
        <input name="username" placeholder="Matrícula" onChange={handleChange} />
        <input name="email" type="email" placeholder="E-mail" onChange={handleChange} />
        <input name="password" type="password" placeholder="Senha" onChange={handleChange} />
        
        <div className="button-group">
          <button onClick={(e) => handleAuth(e, 'login')}>Fazer Login</button>
          <button onClick={(e) => handleAuth(e, 'register')}>Cadastrar-se</button>
        </div>
      </form>
    </div>
  );
};

export default AuthComponent;