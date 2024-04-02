# flask-auth-sample

Repositório criado para armazenar o código da API de autenticação com banco de dados.

## Inicialização do banco (temporário)
Executar o seguinte comando no terminal:
```
flask shell
```

Após a abertura do shell, executar os seguintes comandos:
```
db.create_all()
db.session.commit()
exit()
```