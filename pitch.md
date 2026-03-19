# Preparacion de Pitch

## 1. Pitch corto

Hola. Mi proyecto es una plataforma web desarrollada en Python que permite a analistas consultar bases de datos usando lenguaje natural. La herramienta traduce preguntas comunes a codigo SQL, pero con un enfoque central en la seguridad: valida que cada consulta sea segura de ejecutar y asegura que funcione correctamente en un entorno multi-tenant, garantizando de manera estricta que los usuarios solo puedan ver datos de su propia organizacion.

## 2. Pitch

Problema:
Actualmente, si un usuario de negocio necesita informacion cruzada sobre clientes o transacciones, muchas veces depende de que el equipo tecnico le arme un reporte a la medida. Esto hace que el acceso a datos sea lento y poco escalable.

Solucion:
Para resolver esto, cree una aplicacion local con Streamlit donde el usuario hace sus preguntas directamente en lenguaje natural.

Como funciona:
El sistema toma la pregunta y, usando un modelo de lenguaje, la traduce a codigo SQL. Para evitar riesgos y cruces de informacion, escribi un filtro que revisa esa consulta antes de que toque la base de datos. Este filtro asegura que el texto incluya obligatoriamente el identificador de la organizacion de la persona, y rechaza cualquier accion que no sea de consulta.

Valor:
Con esto le damos autonomia al analista para investigar sus metricas al instante de forma amigable, asegurando internamente que los datos esten siempre aislados y seguros por organizacion al mismo tiempo.

## 3. Explicacion tecnica

Multi-tenant:
Para asegurar que un usuario nunca cruce datos de otra empresa, cuando la persona inicia sesion yo guardo su 'organization_id' en la memoria de la aplicacion. Cada vez que el sistema arma o ejecuta un query, ese identificador es forzado directamente desde el backend en forma de un 'WHERE id_organizacion = X'. El usuario jamas puede alterar ese parametro desde la interfaz.

NL2SQL:
Para transformar la idea en SQL, le paso al modelo el esquema de la base de datos como contexto inicial y le sumo la pregunta del usuario. Instruyo al modelo para que no genere conversaciones, sino unicamente el script SQL valido de lectura.

Seguridad:
Implemente un modulo de "guardrails". La funcion principal de este modulo es leer el SQL generado. Si llega a detectar instrucciones como UPDATE, DROP, DELETE o INSERT, sencillamente devuelve un error de seguridad controlado y no ejecuta nada. El software esta forzado a ser exclusivamente de lectura (SELECT).

Monitoreo:
Elabore un archivo con reglas de negocio fijas escritas en consultas SQL parametrizadas, que son mas seguras contra inyeccion de datos. Estas consultas revisan todos los registros del cliente actual para buscar riesgos, por ejemplo transacciones excesivamente altas o personas con mas de tres alertas acumuladas.

## 4. Preguntas y respuestas tipicas

¿Como aseguras que un usuario no vea datos de otra organizacion?
Yo guardo el identificador de la organizacion en la sesion al momento del login. Cuando se procesa una consulta nueva, el sistema revisa si el filtro de esa organizacion exacta se encuentra dentro de la sintaxis. Si no detecta ese filtro especifico de seguridad, el sistema genera una excepcion interna y frena la consulta, devolviendo un aviso en pantalla de consulta invalida.

¿Que pasa si falla la IA?
Construi un mecanismo de contingencia. Si el servicio del modelo de lenguaje falla o si simplemente el usuario no coloco su clave externa, mi codigo atrapa ese problema e invoca una funcion alternativa ('fallback'). Esta funcion utiliza la busqueda de palabras como 'alertas' o 'asociados' en la frase que metio el usuario. Al detectar esas palabras devuelve consultas SQL locales prearmadas. De este modo, la aplicacion siempre entrega una tabla y el flujo no se interrumpe.

¿Como manejas consultas peligrosas?
Aparte de pedirle a la inteligencia artificial que restrinja su propio codigo, la verdadera seguridad la pongo del lado de la logica en Python. Parseo el string o texto que me llega, y busco la existencia de sentencias DML o DDL prohibidas. La base de datos no es tocada en absoluto si detecto alguna peticion manipuladora de informacion.
