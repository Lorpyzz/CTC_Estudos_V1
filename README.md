CTC-Estudo é uma plataforma de estudos feita por alunos do Centro Técnico-Científico (CTC) da PUC-Rio. A plataforma foi desenvolvida com o proposito de ajudar alunos a estudarem com o conteúdo da própria disciplina, por exemplo, testes e provas antigas, listas de exercicios, mas também é possível personalizar com o uso de flashcards, e tirar dúvidas por meio da aba comentários/dúvidas.

Desenvolvedores responsáveis pela plataforma:
- Gabriel Novais
- Heloysa Aguiar
- Isabele Viana
- João Lopes

Algumas páginas foram feitas em REACT e outras em HTML, então foi necessário conectar todas essas páginas soltas com o framework Django.

Para buildar o projeto:
- É preciso clonar o repositório (git clone >colocar o link do repositorio<) via terminal;

* Caso utilize Windows:
- O comando para ativar o ambiente virtual é: .\venv\Scripts\activate;
caso nao queira digitar todo esse caminho, basta fazer: 
.\aa, o arquivo aa.ps1 possui o comando de ativar o ambiente virtual, reduzindo esse processo de digitação.

* Caso utilize Linux ou MacOS:
- O comando para ativar o ambiente virtual é: source venv/bin/activate;

Para saber se o ambiente virtual está ativo, basta verificar no terminal se aparece (venv) ao lado do caminho. 
- Após ativar o venv, é necessário buildar com o seguinte comando: 
python manage.py runserver 
vai aparecer o localhost no terminal.

O arquivo requirements.txt é responsável por todas as dependências que o projeto necessita para funcionar. Logo, é importante que usuários utilizem as mesmas versões para que não ocorra eventuais erros por incompatibilidade de versões.

* Banco de Dados
- As entidades presente no models.py serão nossas tabelas no banco de dados. Para que seja mais intuitivo, será interessante imaginar, por exemplo, a entidade Aluno como uma tabela, a entidade Disciplinas como uma tabela que possui relacionamentos, por exemplo, cada disciplina possui N tópicos/temas a serem estudados. Álgebra possui alguns dos seguintes tópicos: espaços vetoriais, matriz, autovetor e autovalor; Todos esses tópicos estão relacionados com a disciplina. Cada tópico possui uma relação com a disciplina (relacionamento: 1:1), mas no nosso exemplo, algebra possui relacionamento 1:3, 3 tópicos.

Relacionamento 1:N - Uma disciplina tem vários tópicos
--Criando o banco de dados--
Como mencionado, o models.py é responsável por criar as entidades. Após definir todas as entidades e seus atributos, é necessário criar o banco, e o comando responsável por essa função é python manage.py migrate, ou seja, migra os dados da models para o BD.

