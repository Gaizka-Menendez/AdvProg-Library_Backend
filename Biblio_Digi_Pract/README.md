Práctica del Módulo de Programación Avanzada de Gaizka Menéndez Hernández

**Gestión de una Biblioteca de forma digital**.

La idea de esta práctica es desarrollar lo que podría ser una web online de una Biblioteca donde se llevane a cabo la gestión de los usuarios y de los libros de la misma. Es decir, que los usuarios puedan interactuar con la web de forma que puedan pedir préstamos o devolver libros y que todo esto quede registrado. Esta es la funcionalidad que busco conseguir.

A continuación voy a detallar un poco que es lo que ocurre en cada una de las clases del "source_code". Cada clase representa una funcionalidad o parte de la aplicación y así cumplimos el principio de Separación de Responsabilidades.



1. **database.py (BBDD de la app)**
    * Aquí se encuentra todo aquello relativo a la creación de la base de datos. Usamos la librería SQLAlchemy para definir la url de conexión a la BBDD, crear el engine, definimos la forma de crear las sesiones para operar sobre la BBDD y lo necesario para añadir tablas a nuestra BBDD.


2. **validators.py (schema class para la app)**

    * Esta clase es la que gestiona las validaciones pertinentes a los diferentes parámetros y variables creadas en cada una de las clases que componen la app. A continuación voy a explicar un poco las decisiones tomadas y el porque de las mismas.

        * Para la clase `Book` que representa los libros de la bilbioteca se validan los campos de nombre, autor y el género al que pertenece. Sus métodos validadores comprueban que el nombre de los mismos contienen vocales (reutilizando un poco lo visto en clase) y para los autores nos aseguramos que se especifiquen con un String compuesto de lo que sería 3 palabras, 1 para el nombre y otras dos para sus dos primeros apellidos. Para los tres campos se establece un número mínimo de caracteres y en el caso de géneros mínimo a 1 género tiene que pertenecer un libro.

        * La clase `Film`, donde se validan las películas que se pueden alquilar de nuestra biblioteca. Awui similar que para la clase libro se realizan las mismas validaciones de variables. 

        * La clase `Loan` hace referencia al préstamo de un libro y/o una película como máximo. He de reconocer que mi intención inicial era permitir que se pudiesen alquilar más de un item de cada tipo pero a la hora de la implementación vi que era más complejo y que debería de modificar algunos endpoints y clases ya definidas y por tema tiempos y planificación no me daría tiempo, por lo tanto lo dejo como una posible futura mejora.







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
