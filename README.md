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
