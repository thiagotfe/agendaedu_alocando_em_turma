## Alocando alunos na Agenda Edu em turmas extras via consumo de API com Python

Em determinados períodos do ano existe a necessidade de criar turmas extras (turmas de futsal, natação, colônia de férias, integral, etc).

Geralmente, seria nececessário alocar aluno por aluno ou criar uma lista contendo o `legacy_id` dos alunos e solicitar que a Agenda inclua, o que nem sempre é tão simples.

O código deste repositório tem por objetivo mostrar como consumir a API da Agenda Edu com Python para alocar alunos.

Basta submeter um arquivo `.json` contendo o id da turma e o nome dos alunos.

A rotina "pega" os dados dos alunos da Agenda Edu e os compara com os dados do arquivo de entrada com o objetivo de retornar o `legacy_id` de cada aluno.

Em seguida, a rotina realiza a inclusão dos alunos por turma.

## Importante
Para que o código funcione será necessário ter credenciais de acesso à API da Agenda Edu.
