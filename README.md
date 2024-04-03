# flask-auth-sample

Repositório criado para armazenar o código da API de autenticação com banco de dados.

Desenvolvido utilizando o framework Flask com utilização de banco de dados PostgreSQL em container.


## Inicialização do banco (temporário)
Executar o seguinte comando no terminal:
```
docker compose up -d
```

Iniciar o serviço e após isos, executar seguinte comando no terminal:
```
flask shell
```

Após a abertura do shell, executar os seguintes comandos:
```
db.create_all()
db.session.commit()
exit()
```
