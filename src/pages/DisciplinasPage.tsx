import React from 'react';
import { useNavigate } from 'react-router-dom';
import './DisciplinasPage.css';

// Definindo o tipo para garantir a segurança do TypeScript
interface Disciplina {
  id: number;
  nome: string;
  professor: string;
  periodo: string;
}

const DisciplinasPage: React.FC = () => {
  const navigate = useNavigate();

  // Dados fictícios (Mock)
  const disciplinas: Disciplina[] = [
    { id: 1, nome: "Cálculo Diferencial e Integral I", professor: "Marcos Guimarães", periodo: "1º Período" },
    { id: 2, nome: "Algoritmos e Programação", professor: "Ana Beatriz", periodo: "1º Período" },
    { id: 3, nome: "Introdução à Engenharia", professor: "Roberto Silva", periodo: "1º Período" },
    { id: 4, nome: "Física Experimental I", professor: "Cláudio Ferreira", periodo: "2º Período" },
  ];

  return (
    <div className="disciplinas-wrapper">
      {/* Reutilizando a lógica da Navbar da Landing Page */}
      <nav className="disciplinas-nav">
        <span className="logo" onClick={() => navigate('/')}>CTC Estudos</span>
        <button className="btn-voltar" onClick={() => navigate(-1)}>Voltar</button>
      </nav>

      <main className="disciplinas-content">
        <header className="page-header">
          <h1>Minhas Disciplinas</h1>
          <p>Selecione uma matéria para acessar materiais e flashcards.</p>
        </header>

        <div className="grid-disciplinas">
          {disciplinas.map((disc) => (
            <div key={disc.id} className="card-disciplina">
              <div className="card-tag">{disc.periodo}</div>
              <h3>{disc.nome}</h3>
              <p>Prof. {disc.professor}</p>
              <button 
                className="btn-acessar" 
                onClick={() => navigate(`/disciplinas/${disc.id}`)}
              >
                Ver Conteúdo
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default DisciplinasPage;