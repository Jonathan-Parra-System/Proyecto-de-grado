MODULOS = [
    {
        "curso": "informatica-basica",
        "titulo": "Módulo 1: Conociendo el computador",
        "descripcion": "Aprende a reconocer el equipo y a usar sus elementos principales.",
        "imagen": "computador.svg",
        "lecciones": [
            {
                "slug": "partes-computador",
                "titulo": "Partes del computador",
                "duracion": "5 min",
                "introduccion": "Un computador recibe datos, los procesa y muestra resultados. Sus partes trabajan juntas para ayudarte a estudiar, crear y comunicarte.",
                "objetivos": [
                    "Reconocer monitor, teclado, mouse y CPU.",
                    "Identificar para qué sirve cada componente.",
                    "Relacionar cada parte con una tarea cotidiana.",
                ],
                "pasos": [
                    {"titulo": "Monitor", "texto": "Muestra textos, imágenes y videos. Es la pantalla que permite ver lo que haces."},
                    {"titulo": "Teclado y mouse", "texto": "El teclado sirve para escribir; el mouse permite mover el puntero, seleccionar y abrir elementos."},
                    {"titulo": "CPU o torre", "texto": "Procesa instrucciones y coordina muchas de las tareas del computador. En un portátil sus componentes están integrados."},
                ],
                "actividad": {
                    "pregunta": "¿Qué componente usarías para escribir tu nombre en un documento?",
                    "opciones": [("monitor", "El monitor"), ("teclado", "El teclado"), ("parlantes", "Los parlantes")],
                    "respuesta": "teclado",
                },
            },
            {
                "slug": "teclado-mouse",
                "titulo": "Teclado y mouse",
                "duracion": "6 min",
                "introduccion": "El teclado y el mouse son dispositivos de entrada: permiten darle instrucciones al computador de forma sencilla.",
                "objetivos": [
                    "Ubicar letras, números y teclas especiales.",
                    "Practicar clic, doble clic y desplazamiento.",
                    "Usar ambos dispositivos con cuidado.",
                ],
                "pasos": [
                    {"titulo": "Escribe con el teclado", "texto": "Las letras forman palabras; Enter confirma o inicia una línea y Retroceso borra el carácter anterior."},
                    {"titulo": "Controla el puntero", "texto": "Mueve el mouse sobre una superficie plana. Un clic selecciona; un doble clic abre algunos elementos."},
                    {"titulo": "Desplázate", "texto": "La rueda del mouse permite recorrer una página. También puedes usar las flechas y las barras de desplazamiento."},
                ],
                "actividad": {
                    "pregunta": "¿Qué acción suele abrir un archivo desde el escritorio?",
                    "opciones": [("doble", "Hacer doble clic sobre el archivo"), ("rueda", "Girar la rueda del mouse"), ("mayus", "Presionar Mayús una vez")],
                    "respuesta": "doble",
                },
            },
            {
                "slug": "encender-apagar",
                "titulo": "Encender y apagar el computador",
                "duracion": "5 min",
                "introduccion": "Un inicio y apagado correctos ayudan a cuidar el equipo y a evitar que se pierdan tus trabajos.",
                "objetivos": [
                    "Encender el equipo con el botón de energía.",
                    "Guardar el trabajo antes de salir.",
                    "Apagar desde las opciones del sistema.",
                ],
                "pasos": [
                    {"titulo": "Antes de empezar", "texto": "Comprueba que el equipo esté conectado y que tus manos estén secas. Pulsa una vez el botón de encendido."},
                    {"titulo": "Guarda tus cambios", "texto": "Usa Guardar en tus aplicaciones antes de cerrar un documento para conservar el trabajo."},
                    {"titulo": "Apaga con seguridad", "texto": "Abre el menú del sistema y elige Apagar. Espera a que termine; no desconectes el equipo a la fuerza."},
                ],
                "actividad": {
                    "pregunta": "¿Cuál es la forma recomendada de apagar el computador?",
                    "opciones": [("cable", "Desconectar el cable inmediatamente"), ("menu", "Elegir Apagar desde el menú del sistema"), ("boton", "Mantener presionado el botón siempre")],
                    "respuesta": "menu",
                },
            },
        ],
    },
    {
        "curso": "informatica-basica",
        "titulo": "Módulo 2: Archivos y carpetas",
        "descripcion": "Crea, encuentra y organiza documentos en tu computador.",
        "imagen": "archivos.svg",
        "lecciones": [
            {
                "slug": "que-es-archivo",
                "titulo": "¿Qué es un archivo?",
                "duracion": "5 min",
                "introduccion": "Un archivo guarda información digital. Puede ser un texto, una fotografía, una canción o un video.",
                "objetivos": [
                    "Distinguir un archivo de una carpeta.",
                    "Reconocer que los archivos tienen nombre y tipo.",
                    "Identificar algunos formatos comunes.",
                ],
                "pasos": [
                    {"titulo": "Nombre", "texto": "Un nombre claro te ayuda a reconocer el contenido, por ejemplo: Tarea ciencias."},
                    {"titulo": "Tipo de archivo", "texto": "La extensión puede indicar su formato: .pdf para documentos, .jpg para imágenes y .mp3 para audio."},
                    {"titulo": "Ubicación", "texto": "Los archivos se guardan dentro de carpetas o en dispositivos como el disco del computador."},
                ],
                "actividad": {
                    "pregunta": "¿Cuál de estos nombres suele corresponder a una imagen?",
                    "opciones": [("jpg", "foto.jpg"), ("pdf", "informe.pdf"), ("mp3", "cancion.mp3")],
                    "respuesta": "jpg",
                },
            },
            {
                "slug": "crear-carpeta",
                "titulo": "Crear una carpeta",
                "duracion": "5 min",
                "introduccion": "Las carpetas agrupan archivos relacionados. Puedes crear una para cada materia, proyecto o tema.",
                "objetivos": [
                    "Crear una carpeta desde el explorador de archivos.",
                    "Elegir un nombre fácil de entender.",
                    "Guardar documentos en la ubicación correcta.",
                ],
                "pasos": [
                    {"titulo": "Elige dónde guardarla", "texto": "Abre el explorador de archivos y entra en Documentos o en la ubicación que prefieras."},
                    {"titulo": "Crea la carpeta", "texto": "Selecciona Nueva carpeta, escribe un nombre descriptivo y confirma con Enter."},
                    {"titulo": "Guarda contenido", "texto": "Abre la carpeta y guarda allí los documentos relacionados para encontrarlos juntos."},
                ],
                "actividad": {
                    "pregunta": "¿Qué nombre ayuda más a encontrar una carpeta con tareas de ciencias?",
                    "opciones": [("nuevo", "Nueva carpeta"), ("ciencias", "Tareas de ciencias"), ("cosas", "Cosas")],
                    "respuesta": "ciencias",
                },
            },
            {
                "slug": "organizar-archivos",
                "titulo": "Organizar archivos",
                "duracion": "6 min",
                "introduccion": "Una buena organización evita duplicados y facilita encontrar tus trabajos cuando los necesitas.",
                "objetivos": [
                    "Agrupar archivos por tema o proyecto.",
                    "Usar nombres descriptivos y fechas cuando ayuden.",
                    "Mover o copiar archivos con atención.",
                ],
                "pasos": [
                    {"titulo": "Agrupa por tema", "texto": "Crea carpetas como Matemáticas o Fotos familiares y guarda dentro los archivos relacionados."},
                    {"titulo": "Nombra claramente", "texto": "Usa títulos breves y únicos. Añade una fecha si guardas varias versiones de un mismo trabajo."},
                    {"titulo": "Revisa antes de borrar", "texto": "Comprueba que tienes una copia útil antes de eliminar un archivo. La papelera permite recuperarlo temporalmente."},
                ],
                "actividad": {
                    "pregunta": "¿Qué práctica facilita localizar un trabajo más adelante?",
                    "opciones": [("claro", "Usar nombres claros y carpetas por tema"), ("mezcla", "Guardar todo en una sola carpeta sin nombres"), ("borrar", "Eliminar archivos después de cada uso")],
                    "respuesta": "claro",
                },
            },
        ],
    },
    {
        "curso": "internet",
        "titulo": "Módulo 1: Navegación por Internet",
        "descripcion": "Conéctate, navega y busca información de manera responsable.",
        "imagen": "internet.svg",
        "lecciones": [
            {
                "slug": "que-es-internet",
                "titulo": "¿Qué es Internet?",
                "duracion": "5 min",
                "introduccion": "Internet conecta computadores y otros dispositivos para compartir información y comunicarse en todo el mundo.",
                "objetivos": [
                    "Comprender que Internet es una red de redes.",
                    "Distinguir Internet de una página web.",
                    "Reconocer usos cotidianos de la conexión.",
                ],
                "pasos": [
                    {"titulo": "Una red mundial", "texto": "Los dispositivos conectados intercambian datos mediante redes y servicios."},
                    {"titulo": "Servicios diferentes", "texto": "La web, el correo y las videollamadas son servicios que pueden funcionar a través de Internet."},
                    {"titulo": "Conexión", "texto": "Puedes conectarte mediante Wi-Fi o una red móvil. Algunas funciones del computador también trabajan sin conexión."},
                ],
                "actividad": {
                    "pregunta": "¿Cuál afirmación describe mejor Internet?",
                    "opciones": [("red", "Una red mundial que conecta dispositivos"), ("pantalla", "La pantalla del computador"), ("programa", "Un único programa para escribir")],
                    "respuesta": "red",
                },
            },
            {
                "slug": "navegadores-web",
                "titulo": "Navegadores web",
                "duracion": "5 min",
                "introduccion": "Un navegador es una aplicación que permite visitar sitios web, abrir enlaces y volver a páginas que ya consultaste.",
                "objetivos": [
                    "Reconocer la barra de direcciones.",
                    "Abrir y recorrer páginas web.",
                    "Usar pestañas y controles de navegación.",
                ],
                "pasos": [
                    {"titulo": "Escribe una dirección", "texto": "La barra de direcciones está en la parte superior. Allí puedes escribir el sitio que quieres visitar."},
                    {"titulo": "Usa enlaces", "texto": "Los enlaces te llevan a otras páginas. Puedes volver a la página anterior con el botón Atrás."},
                    {"titulo": "Organiza pestañas", "texto": "Las pestañas permiten tener varias páginas abiertas en una misma ventana. Ciérralas cuando ya no las necesites."},
                ],
                "actividad": {
                    "pregunta": "¿Dónde escribes la dirección de un sitio web?",
                    "opciones": [("direccion", "En la barra de direcciones del navegador"), ("documento", "En el nombre de un archivo"), ("papelera", "En la papelera")],
                    "respuesta": "direccion",
                },
            },
            {
                "slug": "buscar-informacion",
                "titulo": "Buscar información",
                "duracion": "6 min",
                "introduccion": "Una búsqueda efectiva usa palabras clave claras y compara fuentes antes de confiar en la información encontrada.",
                "objetivos": [
                    "Escribir una búsqueda específica.",
                    "Comparar quién publica la información y cuándo.",
                    "Evitar compartir datos personales innecesarios.",
                ],
                "pasos": [
                    {"titulo": "Elige palabras clave", "texto": "En lugar de una pregunta muy larga, prueba términos concretos que describan lo que quieres aprender."},
                    {"titulo": "Evalúa la fuente", "texto": "Revisa quién publicó el contenido, la fecha y si coincide con otras fuentes confiables."},
                    {"titulo": "Navega con cuidado", "texto": "No abras enlaces sospechosos ni escribas contraseñas o datos personales en sitios que no conoces."},
                ],
                "actividad": {
                    "pregunta": "¿Qué conviene hacer antes de confiar en un resultado de búsqueda?",
                    "opciones": [("comparar", "Revisar la fuente y comparar con otras fuentes confiables"), ("compartir", "Compartirlo de inmediato sin leer"), ("contrasena", "Escribir la contraseña para ver más información")],
                    "respuesta": "comparar",
                },
            },
        ],
    },
    {
        "curso": "herramientas-digitales",
        "titulo": "Módulo 1: Herramientas para aprender y comunicarte",
        "descripcion": "Practica con documentos, correo electrónico y reuniones virtuales.",
        "imagen": "herramientas.svg",
        "lecciones": [
            {
                "slug": "documentos-digitales",
                "titulo": "Crear documentos digitales",
                "duracion": "6 min",
                "introduccion": "Un procesador de texto permite redactar, corregir y presentar trabajos desde un computador o dispositivo móvil.",
                "objetivos": [
                    "Crear un documento y darle un nombre.",
                    "Aplicar formato básico a un texto.",
                    "Guardar los cambios en una ubicación fácil de encontrar.",
                ],
                "pasos": [
                    {"titulo": "Empieza un documento", "texto": "Abre una aplicación de escritura y crea un documento en blanco. Escribe un título que describa tu trabajo."},
                    {"titulo": "Da formato con intención", "texto": "Usa tamaño, negrita y alineación para ordenar la información. Mantén un estilo sencillo que facilite la lectura."},
                    {"titulo": "Guarda tu trabajo", "texto": "Selecciona Guardar, elige una carpeta y pon un nombre claro. Guarda de nuevo mientras avanzas."},
                ],
                "actividad": {
                    "pregunta": "¿Qué debes hacer para conservar los cambios de un documento?",
                    "opciones": [("guardar", "Guardar el archivo en una ubicación conocida"), ("cerrar", "Cerrar la aplicación sin guardar"), ("renombrar", "Cambiar el color de la ventana")],
                    "respuesta": "guardar",
                },
            },
            {
                "slug": "correo-electronico",
                "titulo": "Usar el correo electrónico",
                "duracion": "6 min",
                "introduccion": "El correo electrónico permite enviar mensajes y archivos a otras personas. Conviene escribir con claridad y revisar los destinatarios antes de enviar.",
                "objetivos": [
                    "Identificar destinatario, asunto y mensaje.",
                    "Escribir un asunto breve y claro.",
                    "Adjuntar archivos con cuidado.",
                ],
                "pasos": [
                    {"titulo": "Completa los campos", "texto": "Escribe la dirección de la persona en Para y resume el propósito del mensaje en el asunto."},
                    {"titulo": "Redacta con claridad", "texto": "Saluda, explica lo necesario y despídete cordialmente. Revisa la ortografía y confirma que elegiste el destinatario correcto."},
                    {"titulo": "Adjunta y revisa", "texto": "Usa Adjuntar archivo si necesitas enviar un documento. Comprueba el archivo y el mensaje antes de pulsar Enviar."},
                ],
                "actividad": {
                    "pregunta": "¿Qué conviene revisar antes de enviar un correo?",
                    "opciones": [("destinatario", "El destinatario, el asunto y el archivo adjunto"), ("fondo", "El color de fondo de la pantalla"), ("borrar", "Borrar el asunto y enviar sin revisar")],
                    "respuesta": "destinatario",
                },
            },
            {
                "slug": "videollamadas",
                "titulo": "Videollamadas y colaboración",
                "duracion": "6 min",
                "introduccion": "Las videollamadas ayudan a conversar y trabajar en grupo a distancia. Preparar el equipo y respetar turnos mejora la experiencia.",
                "objetivos": [
                    "Comprobar cámara, micrófono y conexión.",
                    "Participar respetando los turnos.",
                    "Compartir únicamente lo necesario.",
                ],
                "pasos": [
                    {"titulo": "Prepárate", "texto": "Busca un lugar tranquilo y comprueba el micrófono, la cámara y la conexión antes de entrar."},
                    {"titulo": "Participa con respeto", "texto": "Silencia el micrófono cuando no hables, escucha a las demás personas y usa el chat para compartir comentarios breves."},
                    {"titulo": "Cuida tu privacidad", "texto": "Comparte pantalla solo cuando sea necesario y cierra documentos privados antes de mostrarla."},
                ],
                "actividad": {
                    "pregunta": "¿Qué práctica ayuda a cuidar la privacidad al compartir pantalla?",
                    "opciones": [("cerrar", "Cerrar documentos privados antes de compartir"), ("mostrar", "Mostrar todas las ventanas abiertas"), ("enlace", "Publicar el enlace de la reunión para cualquiera")],
                    "respuesta": "cerrar",
                },
            },
        ],
    },
]

CURSOS = {
    "informatica-basica": {
        "titulo": "Informática básica",
        "descripcion": "Aprende los conceptos básicos del uso del computador.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "informatica-basica"],
    },
    "internet": {
        "titulo": "Internet",
        "descripcion": "Aprende a navegar, comunicarte y buscar información de forma segura.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "internet"],
    },
    "herramientas-digitales": {
        "titulo": "Herramientas digitales",
        "descripcion": "Crea documentos, envía correos y colabora con herramientas digitales.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "herramientas-digitales"],
    },
}

LECCIONES = {}
ORDENES_CURSO = {}
for curso_slug, curso in CURSOS.items():
    orden = []
    for modulo in curso["modulos"]:
        for leccion in modulo["lecciones"]:
            LECCIONES[leccion["slug"]] = {
                **leccion,
                "curso": curso_slug,
                "curso_titulo": curso["titulo"],
                "modulo": modulo["titulo"],
                "imagen": modulo["imagen"],
            }
            orden.append(leccion["slug"])
    ORDENES_CURSO[curso_slug] = orden

ORDEN_LECCIONES = [
    slug
    for orden in ORDENES_CURSO.values()
    for slug in orden
]
