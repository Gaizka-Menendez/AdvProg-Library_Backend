Práctica del Módulo de Programación Avanzada de Gaizka Menéndez Hernández

**Gestión de una Biblioteca de forma digital**.

La idea de esta práctica es desarrollar lo que podría ser una web online de una Biblioteca donde se llevane a cabo la gestión de los usuarios y de los libros de la misma. Es decir, que los usuarios puedan interactuar con la web de forma que puedan pedir préstamos o devolver libros y que todo esto quede registrado. Esta es la funcionalidad que busco conseguir.

A continuación voy a detallar un poco que es lo que ocurre en cada una de las clases del "source_code", cada clase representa una funcionalidad o parte de la aplicación y así cumplimos el principio de Separación de Responsabilidades.



1. **database.py (BBDD de la app)**
    * Aquí se encuentra todo aquello relativo a la creación de la base de datos. Usamos la librería SQLAlchemy para definir la url de conexión a la BBDD, crear el engine, definimos la forma de crear las sesiones para operar sobre la BBDD y lo necesario para añadir tablas a nuestra BBDD.







1.  **Claridad en los Objetos/Entidades:**
    * Puedes definir claramente objetos como `Libro`, `Autor`, `Usuario`, `Préstamo`, `Género`, `Editorial`. Cada uno con sus propios atributos y métodos.
    * **POO Pura:** Permite aplicar conceptos como **herencia** (ej. `LibroFisico` y `LibroDigital` heredando de `LibroBase`), **polimorfismo** (diferentes formas de manejar préstamos para libros físicos vs. digitales), **encapsulamiento** (métodos para añadir o quitar stock de libros, gestionar el estado de un préstamo).

2.  **Operaciones CRUD Complejas:**
    * Necesitarás APIs para:
        * Crear, leer, actualizar y eliminar (`CRUD`) libros, autores, usuarios.
        * Registrar nuevos usuarios.
        * Realizar préstamos y devoluciones de libros.
        * Gestionar el stock de libros.

3.  **Lógica de Negocio y Validaciones:**
    * **Validaciones:** Un usuario no puede pedir prestado más de X libros. Un libro solo puede ser prestado si hay stock disponible. Fechas de devolución, penalizaciones por retraso.
    * **Relaciones entre objetos:** Un `Libro` tiene un `Autor` (o varios). Un `Préstamo` relaciona un `Usuario` y un `Libro`.

4.  **Autenticación y Autorización:**
    * Los usuarios pueden iniciar sesión (autenticación).
    * Diferentes roles: `Lector` (puede ver libros, pedirlos prestados), `Bibliotecario` (puede gestionar stock, autores, usuarios), `Administrador` (superpoderes). Esto es perfecto para aplicar la autorización basada en roles de FastAPI.

5.  **Base de Datos y Persistencia:**
    * Necesitarás persistir los datos de tus objetos. FastAPI se integra muy bien con bases de datos SQL (SQLAlchemy, SQLite/PostgreSQL) o NoSQL.

6.  **APIs Restful:**
    * FastAPI es ideal para construir una API RESTful que permita a diferentes "clientes" (una interfaz web, una aplicación móvil, etc.) interactuar con la biblioteca.

**Posibles Funcionalidades a Implementar (para aplicar POO y FastAPI):**

* **Modelos de Datos:**
    * **`Libro`**: título, autor(es), ISBN, año de publicación, género, editorial, número de copias disponibles (stock), estado (disponible, prestado, en mantenimiento).
    * **`Autor`**: nombre, apellido, biografía, obras.
    * **`Usuario`**: nombre de usuario, contraseña (hashed), email, rol (Lector, Bibliotecario), lista de préstamos actuales.
    * **`Préstamo`**: usuario, libro, fecha de préstamo, fecha de devolución esperada, fecha de devolución real, estado (activo, devuelto, retrasado).
    * **`Género`**: nombre (Ficción, Ciencia Ficción, Historia, etc.).

* **Endpoints (API REST):**
    * `/books/`: Obtener todos los libros, crear nuevo libro.
    * `/books/{id}`: Obtener, actualizar, eliminar un libro específico.
    * `/authors/`: CRUD para autores.
    * `/users/`: CRUD para usuarios (solo por administradores/bibliotecarios).
    * `/auth/login`: Autenticación de usuarios.
    * `/loans/`: Ver préstamos, crear un nuevo préstamo.
    * `/loans/{id}/return`: Registrar una devolución.
    * `/users/{user_id}/loans`: Ver los préstamos de un usuario específico.
    * `/search/books`: Buscar libros por título, autor, ISBN, género.

**Consejos para la implementación con POO:**

* Define clases (`Book`, `Author`, `User`, `Loan`) que representen las entidades.
* Usa Pydantic para los esquemas de entrada y salida de tus APIs, lo que te permitirá validar datos y serializar/deserializar objetos.
* Aplica la inyección de dependencias de FastAPI para pasar objetos de bases de datos o servicios a tus *path operations*.
* Considera el patrón Repositorio para la interacción con la base de datos, separando la lógica de negocio de la lógica de persistencia.
