# Ikusi backend user

Microservicio encargado del registro, loggeo y autenticación de usuarios de la aplicacion Ikusi.

## Endpoints

### Descripción de los endpoints

- `/register`: Permite registrar un usuario en la base de datos y retorna un JWT para poder autenticar peticiones.

- `/login`: Loggea a los usuarios por medio de su usuario y contraseña y retorna JWT para autenticacion de peticiones.

- `/validate-token`: Permite validar si un token es valido, tanto en la forma del JWT (header, payload y firma) como en el tiempo de expiración. Si la validacion es exitosa, retorna un objeto con la informacion basica del usuario al que pertenece ese token.

| Endpoint  | params  |  Body keys | HTTP method |
|:---:|:---:|:---:|:---:|
| `/register`  |   |  `username`, `password`, `email` |  POST |
| `/login`  |   | `username`, `password`  |  POST |
| `/validate-token`  | `token`  |   |  GET |


