from urllib.parse import quote_plus


MODULOS = [
    {
        "curso": "informatica-basica",
        "titulo": "Módulo 1: Conociendo el computador",
        "descripcion": "Identifica las partes del computador, elige el dispositivo adecuado y aprende a apagarlo sin perder tu trabajo.",
        "imagen": "computador.svg",
        "lecciones": [
            {
                "slug": "partes-computador",
                "titulo": "Partes del computador",
                "duracion": "8 min",
                "introduccion": "Un computador recibe información, la procesa y muestra resultados. En esta guía reconocerás cada pieza con ejemplos cotidianos y aprenderás a distinguir una torre de un equipo Todo en uno.",
                "objetivos": [
                    "Distinguir los dispositivos de entrada y de salida.",
                    "Reconocer el monitor, el teclado, el mouse y la torre.",
                    "Diferenciar el procesador (CPU) de la torre que lo contiene.",
                    "Identificar un computador Todo en uno y sus conexiones.",
                ],
                "pasos": [
                    {
                        "titulo": "Monitor: donde ves el resultado",
                        "texto": "Es un dispositivo de salida: muestra documentos, fotografías y mensajes. Si apagas el monitor pero la torre sigue encendida, el computador puede continuar funcionando.",
                        "imagen": "monitor-computador.svg",
                        "imagen_alt": "Ilustración de un monitor mostrando un documento y una fotografía",
                    },
                    {
                        "titulo": "Teclado y mouse: cómo das instrucciones",
                        "texto": "Son dispositivos de entrada. Con el teclado escribes; con el mouse mueves el puntero, haces clic para seleccionar y doble clic para abrir algunos elementos.",
                        "imagen": "teclado-mouse.svg",
                        "imagen_alt": "Ilustración de un teclado y un mouse",
                    },
                    {
                        "titulo": "Torre y procesador (CPU)",
                        "texto": "La torre o gabinete contiene componentes como la placa base, la memoria RAM, el almacenamiento y el procesador. Técnicamente, la CPU es el procesador dentro del equipo, no la torre completa.",
                        "imagen": "torre-computador.svg",
                        "imagen_alt": "Ilustración de una torre de computador abierta que muestra sus componentes",
                    },
                    {
                        "titulo": "Todo en uno: computador y pantalla integrados",
                        "texto": "En este modelo, la mayoría de los componentes está detrás de la pantalla, por eso necesita menos cables y ocupa menos espacio. El teclado y el mouse suelen ir aparte. Busca el botón de encendido y los puertos en los bordes o en la parte posterior.",
                        "imagen": "todo-en-uno.svg",
                        "imagen_alt": "Ilustración de un computador Todo en uno con teclado y mouse externos",
                    },
                ],
                "video": {
                    "titulo": "Video corto: partes del computador y Todo en uno",
                    "url": "https://www.youtube.com/results?search_query=shorts+partes+del+computador+todo+en+uno+espa%C3%B1ol",
                },
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
                "introduccion": "El teclado y el mouse son dispositivos de entrada: convierten tus acciones en instrucciones para el computador. Practica despacio; no hace falta memorizar todas las teclas para empezar.",
                "objetivos": [
                    "Ubicar letras, números y teclas especiales.",
                    "Practicar clic, doble clic y desplazamiento.",
                    "Usar ambos dispositivos con cuidado.",
                ],
                "pasos": [
                    {"titulo": "Escribe con el teclado", "texto": "Pulsa las letras como lo harías en una máquina de escribir. Enter inicia otra línea; Retroceso borra hacia atrás. Mantén Mayús mientras pulsas una letra para escribirla en mayúscula."},
                    {"titulo": "Mueve y selecciona con el mouse", "texto": "Apoya el mouse sobre la mesa y mueve el puntero por la pantalla. Un clic selecciona; el doble clic suele abrir archivos. Si tienes dificultad, aumenta el tamaño del puntero en la configuración."},
                    {"titulo": "Recorre la pantalla", "texto": "Gira la rueda del mouse para subir o bajar por una página. También puedes usar la barra lateral o las teclas de flecha; ambas opciones sirven para desplazarte."},
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
                "introduccion": "Encender desde el botón y apagar desde el sistema operativo permite que el equipo inicie y cierre sus programas en orden. Así reduces el riesgo de perder documentos.",
                "objetivos": [
                    "Encender el equipo con el botón de energía.",
                    "Guardar el trabajo antes de salir.",
                    "Apagar desde las opciones del sistema.",
                ],
                "pasos": [
                    {"titulo": "Enciende el equipo", "texto": "Comprueba que el cable esté firme y pulsa una sola vez el botón con el símbolo de encendido. Espera unos momentos mientras el sistema operativo inicia."},
                    {"titulo": "Guarda antes de salir", "texto": "Pulsa Guardar en cada documento y espera la confirmación. Si aparece una pregunta sobre los cambios, elige Guardar para conservarlos."},
                    {"titulo": "Elige Apagar en el menú", "texto": "Abre Inicio o el menú del sistema, selecciona Apagar y espera a que la pantalla se apague. No retires el cable ni mantengas el botón presionado salvo que el equipo esté bloqueado."},
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
        "descripcion": "Aprende a reconocer formatos, crear carpetas y encontrar tus documentos sin perderlos.",
        "imagen": "archivos.svg",
        "lecciones": [
            {
                "slug": "que-es-archivo",
                "titulo": "¿Qué es un archivo?",
                "duracion": "5 min",
                "introduccion": "Un archivo es información guardada con un nombre, como una carta, una fotografía o una canción. Las carpetas funcionan como separadores para tener esos archivos organizados.",
                "objetivos": [
                    "Distinguir un archivo de una carpeta.",
                    "Reconocer que los archivos tienen nombre y tipo.",
                    "Identificar algunos formatos comunes.",
                ],
                "pasos": [
                    {"titulo": "Ponle un nombre reconocible", "texto": "Un nombre como Receta de sopa o Foto cumpleaños ayuda más que Documento1. Es como escribir una etiqueta en una carpeta de papel."},
                    {"titulo": "Identifica el formato", "texto": "El final del nombre puede indicar el tipo: .pdf suele ser un documento, .jpg una imagen y .mp3 un audio. La extensión orienta, pero no garantiza que el archivo sea seguro."},
                    {"titulo": "Ubica dónde está guardado", "texto": "Un archivo se encuentra dentro de una carpeta y puede estar en el computador, una memoria USB o un servicio en la nube. Anota la carpeta si necesitas encontrarlo después."},
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
                "introduccion": "Una carpeta reúne archivos relacionados, igual que un archivador físico. Crear pocas carpetas con nombres claros hace más fácil guardar y encontrar documentos.",
                "objetivos": [
                    "Crear una carpeta desde el explorador de archivos.",
                    "Elegir un nombre fácil de entender.",
                    "Guardar documentos en la ubicación correcta.",
                ],
                "pasos": [
                    {"titulo": "Elige una ubicación sencilla", "texto": "Abre el Explorador de archivos y entra en Documentos. Allí tendrás tus trabajos en un lugar conocido, en vez de dejarlos repartidos por el escritorio."},
                    {"titulo": "Crea y nombra la carpeta", "texto": "Selecciona Nueva carpeta, escribe un nombre concreto —por ejemplo, Recibos 2026— y pulsa Enter. El nombre puede incluir espacios."},
                    {"titulo": "Comprueba que quedó guardada", "texto": "Abre la carpeta y guarda dentro un documento relacionado. La ruta que aparece en la parte superior del Explorador indica en qué lugar estás."},
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
                "introduccion": "Una organización sencilla reduce el tiempo de búsqueda y ayuda a evitar copias confusas. Usa una estructura que puedas recordar y revisa antes de mover o borrar información.",
                "objetivos": [
                    "Agrupar archivos por tema o proyecto.",
                    "Usar nombres descriptivos y fechas cuando ayuden.",
                    "Mover o copiar archivos con atención.",
                ],
                "pasos": [
                    {"titulo": "Agrupa por asunto", "texto": "Crea carpetas como Salud, Recibos o Fotos familiares. Guarda cada archivo en la carpeta que tenga sentido para ti."},
                    {"titulo": "Distingue las versiones", "texto": "Usa nombres como Presupuesto enero y Presupuesto febrero. Si necesitas varias versiones, añade una fecha para reconocer cuál es la más reciente."},
                    {"titulo": "Diferencia mover de copiar", "texto": "Mover cambia el archivo de lugar; copiar deja el original y crea otro. Antes de borrar, comprueba que no eliminas la única copia importante."},
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
        "descripcion": "Comprende la conexión, recorre sitios web y evalúa los resultados antes de confiar en ellos.",
        "imagen": "internet.svg",
        "lecciones": [
            {
                "slug": "que-es-internet",
                "titulo": "¿Qué es Internet?",
                "duracion": "5 min",
                "introduccion": "Internet es una red mundial que conecta computadores, teléfonos y otros dispositivos. Gracias a ella puedes consultar páginas, enviar mensajes y hacer videollamadas.",
                "objetivos": [
                    "Comprender que Internet es una red de redes.",
                    "Distinguir Internet de una página web.",
                    "Reconocer usos cotidianos de la conexión.",
                ],
                "pasos": [
                    {"titulo": "La conexión lleva información", "texto": "El router de casa conecta tus equipos por Wi-Fi o cable con el proveedor de Internet. Es parecido a una vía por la que viajan mensajes y páginas."},
                    {"titulo": "Internet no es lo mismo que la web", "texto": "Internet es la red; la web es uno de los servicios que funciona sobre ella. El correo y las videollamadas también usan Internet."},
                    {"titulo": "Wi-Fi y datos móviles", "texto": "El Wi-Fi conecta con una red cercana, como la de casa. Los datos móviles usan la red telefónica y pueden tener límites de consumo. Algunas tareas guardadas en el equipo funcionan sin conexión."},
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
                "introduccion": "Un navegador —como Chrome, Edge, Firefox o Safari— es la aplicación que abre sitios web. Aprender sus botones básicos ayuda a recorrer Internet sin perder la página que estabas viendo.",
                "objetivos": [
                    "Reconocer la barra de direcciones.",
                    "Abrir y recorrer páginas web.",
                    "Usar pestañas y controles de navegación.",
                ],
                "pasos": [
                    {"titulo": "Usa la barra de direcciones", "texto": "Haz clic en la barra larga de la parte superior, escribe la dirección o el tema que buscas y pulsa Enter. La dirección identifica el sitio que visitas."},
                    {"titulo": "Abre enlaces y vuelve atrás", "texto": "Un enlace suele tener texto coloreado o subrayado. Si te lleva a otro lugar, el botón Atrás regresa a la página anterior."},
                    {"titulo": "Mantén pocas pestañas abiertas", "texto": "Cada pestaña es una página distinta en la parte superior. Selecciona una para volver a ella y cierra las que ya no necesites."},
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
                "introduccion": "Un buscador ordena páginas que encuentra en Internet; no comprueba automáticamente que todo sea cierto. Una consulta clara y una revisión de la fuente ayudan a obtener información útil.",
                "objetivos": [
                    "Escribir una búsqueda específica.",
                    "Comparar quién publica la información y cuándo.",
                    "Evitar compartir datos personales innecesarios.",
                ],
                "pasos": [
                    {"titulo": "Escribe una búsqueda concreta", "texto": "Prueba con palabras específicas, como horario centro de salud Bucaramanga. Si los resultados no sirven, agrega un detalle o cambia las palabras."},
                    {"titulo": "Comprueba quién lo publica", "texto": "Mira el nombre de la entidad, la fecha y si ofrece fuentes. Para salud, trámites o dinero, confirma en una página oficial o consulta a una persona experta."},
                    {"titulo": "Reconoce señales de riesgo", "texto": "Desconfía de mensajes que presionan para pagar o compartir claves. No descargues archivos ni escribas datos personales en una página que no puedas identificar."},
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
        "descripcion": "Redacta documentos, envía correos con atención y participa en videollamadas de forma segura.",
        "imagen": "herramientas.svg",
        "lecciones": [
            {
                "slug": "documentos-digitales",
                "titulo": "Crear documentos digitales",
                "duracion": "6 min",
                "introduccion": "Un procesador de texto es una aplicación para redactar y corregir documentos. Puedes usarlo para cartas, listas, solicitudes o trabajos y guardar una copia con un nombre fácil de encontrar.",
                "objetivos": [
                    "Crear un documento y darle un nombre.",
                    "Aplicar formato básico a un texto.",
                    "Guardar los cambios en una ubicación fácil de encontrar.",
                ],
                "pasos": [
                    {"titulo": "Crea y escribe", "texto": "Abre una aplicación de escritura, elige Documento en blanco y escribe un título. Puedes corregir una palabra colocando el cursor sobre ella."},
                    {"titulo": "Haz el texto fácil de leer", "texto": "Usa títulos para separar temas, un tamaño de letra cómodo y negrita solo para destacar. El formato cambia la apariencia, no el contenido."},
                    {"titulo": "Guarda una copia", "texto": "Elige Guardar o Guardar como, selecciona una carpeta conocida y escribe un nombre como Carta al banco. Si trabajas en línea, verifica que indique Guardado."},
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
                "introduccion": "El correo electrónico envía mensajes a una dirección digital y permite adjuntar documentos o fotografías. Como el envío puede ser difícil de deshacer, revisa el destinatario y los archivos antes de confirmarlo.",
                "objetivos": [
                    "Identificar destinatario, asunto y mensaje.",
                    "Escribir un asunto breve y claro.",
                    "Adjuntar archivos con cuidado.",
                ],
                "pasos": [
                    {"titulo": "Revisa destinatario y asunto", "texto": "En Para escribe la dirección de quien debe recibir el mensaje. El asunto resume el tema, por ejemplo: Consulta sobre mi cita."},
                    {"titulo": "Escribe el mensaje", "texto": "Saluda y explica lo necesario con palabras claras. Revisa el nombre de la persona; no respondas a mensajes inesperados que pidan claves o códigos."},
                    {"titulo": "Comprueba el archivo adjunto", "texto": "Selecciona Adjuntar archivo y espera a que aparezca su nombre. Abre el adjunto correcto y revisa todo una vez más antes de pulsar Enviar."},
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
                "introduccion": "Una videollamada transmite sonido e imagen por Internet para conversar a distancia. Con una conexión estable y unos controles básicos puedes participar desde casa o el trabajo.",
                "objetivos": [
                    "Comprobar cámara, micrófono y conexión.",
                    "Participar respetando los turnos.",
                    "Compartir únicamente lo necesario.",
                ],
                "pasos": [
                    {"titulo": "Prueba sonido e imagen", "texto": "Busca los símbolos de micrófono y cámara. Entra unos minutos antes para comprobarlos; si no te oyen, confirma que el micrófono no esté silenciado."},
                    {"titulo": "Toma la palabra", "texto": "Activa el micrófono cuando vayas a hablar y siléncialo al terminar si hay ruido. Usa el chat si necesitas escribir un comentario o hacer una pregunta."},
                    {"titulo": "Comparte solo lo necesario", "texto": "Al compartir pantalla, otras personas pueden ver lo que está abierto. Cierra antes tus documentos y mensajes privados, y deja de compartir al terminar."},
                ],
                "actividad": {
                    "pregunta": "¿Qué práctica ayuda a cuidar la privacidad al compartir pantalla?",
                    "opciones": [("cerrar", "Cerrar documentos privados antes de compartir"), ("mostrar", "Mostrar todas las ventanas abiertas"), ("enlace", "Publicar el enlace de la reunión para cualquiera")],
                    "respuesta": "cerrar",
                },
            },
        ],
    },
    {
        "curso": "inteligencia-artificial",
        "titulo": "Módulo 1: Conoce la inteligencia artificial",
        "descripcion": "Comprende qué es la IA, conoce sus tipos más comunes y aprende qué puede y qué no puede hacer.",
        "imagen": "ia-conceptos.svg",
        "lecciones": [
            {
                "slug": "que-es-inteligencia-artificial",
                "titulo": "¿Qué es la inteligencia artificial?",
                "duracion": "7 min",
                "introduccion": "La inteligencia artificial (IA) es un conjunto de técnicas que permite a un programa encontrar patrones y producir respuestas a partir de datos. No piensa ni comprende como una persona: puede ayudar, pero sus resultados deben revisarse.",
                "objetivos": ["Explicar con palabras sencillas qué hace la IA.", "Distinguir una herramienta automática de una persona experta.", "Reconocer que una respuesta de IA puede contener errores."],
                "pasos": [
                    {"titulo": "Aprende con ejemplos", "texto": "Un sistema de IA analiza muchos ejemplos para reconocer patrones, como distinguir fotos de gatos y perros. Cuantos mejores ejemplos y reglas recibe, más útil puede ser.", "imagen": "ia-conceptos.svg", "imagen_alt": "Ilustración de un sistema que aprende patrones de datos"},
                    {"titulo": "Recibe una solicitud", "texto": "Cuando escribes una pregunta, el sistema procesa tus palabras y calcula una respuesta probable. No conoce tu situación personal si no se la explicas.", "imagen": "ia-prompt.svg", "imagen_alt": "Ilustración de una persona escribiendo una solicitud a una IA"},
                    {"titulo": "Revisa antes de usar", "texto": "La IA puede inventar datos o no entender el contexto. Comprueba fechas, cifras y consejos importantes con fuentes confiables o con una persona experta.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de una respuesta de IA siendo verificada"},
                ],
                "actividad": {"pregunta": "¿Qué conviene hacer con una respuesta importante de una IA?", "opciones": [("verificar", "Comprobarla con una fuente confiable"), ("creer", "Creerla sin revisarla"), ("clave", "Entregarle mi contraseña")], "respuesta": "verificar"},
            },
            {
                "slug": "tipos-de-inteligencia-artificial",
                "titulo": "Tipos de inteligencia artificial",
                "duracion": "8 min",
                "introduccion": "Hay herramientas de IA especializadas en distintas tareas: clasificar información, hacer predicciones, reconocer voz o crear contenido. La mayoría de las que usamos hoy resuelven tareas concretas; no son una inteligencia humana general.",
                "objetivos": ["Reconocer IA que clasifica y recomienda.", "Distinguir sistemas predictivos de IA generativa.", "Relacionar cada tipo con un ejemplo cotidiano."],
                "pasos": [
                    {"titulo": "Clasificar y reconocer", "texto": "Estos sistemas agrupan información o identifican patrones. Por ejemplo, pueden separar correo no deseado o convertir voz en texto.", "imagen": "ia-conceptos.svg", "imagen_alt": "Ilustración de datos agrupados por categorías"},
                    {"titulo": "Predecir o recomendar", "texto": "Un modelo predictivo estima qué podría ocurrir con base en datos anteriores. Una tienda puede recomendar productos, pero la recomendación no siempre coincide con lo que necesitas.", "imagen": "ia-recomendaciones.svg", "imagen_alt": "Ilustración de recomendaciones generadas a partir de preferencias"},
                    {"titulo": "Generar contenido", "texto": "La IA generativa crea texto, imágenes o audio nuevos a partir de una instrucción. El resultado puede parecer real aunque incluya errores.", "imagen": "ia-generativa.svg", "imagen_alt": "Ilustración de texto e imágenes creados con IA"},
                ],
                "actividad": {"pregunta": "¿Qué tipo de IA se usa para crear un borrador de texto desde una instrucción?", "opciones": [("generativa", "IA generativa"), ("teclado", "Teclado físico"), ("carpeta", "Carpeta digital")], "respuesta": "generativa"},
            },
            {
                "slug": "limites-de-la-ia",
                "titulo": "Lo que la IA puede y no puede hacer",
                "duracion": "7 min",
                "introduccion": "Una IA puede resumir, proponer ideas y reconocer patrones con rapidez. No tiene criterio humano, no siempre conoce información reciente y puede responder con seguridad aunque esté equivocada.",
                "objetivos": ["Elegir tareas apropiadas para una IA.", "Reconocer cuándo una respuesta requiere revisión humana.", "Evitar usar IA como reemplazo de asesoría profesional."],
                "pasos": [
                    {"titulo": "Úsala como apoyo", "texto": "Puedes pedirle un primer borrador, una lista de ideas o una explicación sencilla. Luego revisa y adapta el resultado a tu necesidad.", "imagen": "ia-generativa.svg", "imagen_alt": "Ilustración de una IA ofreciendo un borrador para revisar"},
                    {"titulo": "Ten en cuenta sus límites", "texto": "Puede confundir nombres, fechas y causas. Tampoco sabe automáticamente lo que ocurrió hoy; pregunta por la fecha de la información.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de una lupa comprobando información"},
                    {"titulo": "Pide ayuda en decisiones delicadas", "texto": "Para temas de salud, asuntos legales o dinero, consulta una fuente oficial o un profesional. No tomes una decisión importante solo por una respuesta automática.", "imagen": "ia-segura.svg", "imagen_alt": "Ilustración de una decisión importante protegida y revisada"},
                ],
                "actividad": {"pregunta": "¿Quién debe confirmar una recomendación de salud generada por IA?", "opciones": [("profesional", "Un profesional de salud"), ("nadie", "Nadie; la IA siempre tiene razón"), ("redes", "Cualquier publicación anónima")], "respuesta": "profesional"},
            },
        ],
    },
    {
        "curso": "inteligencia-artificial",
        "titulo": "Módulo 2: Usa la IA generativa",
        "descripcion": "Practica cómo pedir textos e imágenes, mejorar instrucciones y revisar los resultados.",
        "imagen": "ia-generativa.svg",
        "lecciones": [
            {
                "slug": "ia-generar-texto",
                "titulo": "Crear y resumir textos con IA",
                "duracion": "8 min",
                "introduccion": "Las herramientas generativas pueden resumir un texto, proponer ideas o preparar un borrador. El resultado es una sugerencia: tú decides qué conservar y verificas la información.",
                "objetivos": ["Pedir un resumen de un texto no confidencial.", "Solicitar un borrador con un propósito definido.", "Revisar y corregir el contenido antes de compartirlo."],
                "pasos": [
                    {"titulo": "Elige una tarea concreta", "texto": "Puedes pedir un resumen de un artículo público o ideas para una invitación. Evita incluir información privada de otras personas.", "imagen": "ia-generativa.svg", "imagen_alt": "Ilustración de un texto resumido por IA"},
                    {"titulo": "Indica cómo quieres el resultado", "texto": "Especifica el tema, para quién es y la extensión. Por ejemplo: Resume este texto en cinco puntos sencillos para alguien que comienza a usar correo.", "imagen": "ia-prompt.svg", "imagen_alt": "Ilustración de una instrucción para generar un resumen"},
                    {"titulo": "Lee, corrige y adapta", "texto": "Comprueba nombres, fechas y datos. Cambia el tono si hace falta y no presentes como propio un texto que aún no hayas revisado.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de edición y revisión de un texto generado"},
                ],
                "actividad": {"pregunta": "¿Qué debes hacer antes de enviar un texto generado por IA?", "opciones": [("revisar", "Leerlo, comprobar los datos y adaptarlo"), ("copiar", "Copiarlo sin leer"), ("privado", "Agregar datos confidenciales para mejorarlo")], "respuesta": "revisar"},
            },
            {
                "slug": "escribir-instrucciones-para-ia",
                "titulo": "Cómo dar instrucciones claras a una IA",
                "duracion": "8 min",
                "introduccion": "La instrucción que escribes se suele llamar prompt. Una petición con tarea, contexto y formato esperado suele producir una respuesta más útil; puedes ajustarla conversando por turnos.",
                "objetivos": ["Identificar las partes de una instrucción clara.", "Añadir contexto sin revelar información privada.", "Mejorar una respuesta con una segunda pregunta."],
                "pasos": [
                    {"titulo": "Explica la tarea", "texto": "Empieza con un verbo: explica, resume, compara o redacta. Así la herramienta entiende qué tipo de ayuda buscas.", "imagen": "ia-prompt.svg", "imagen_alt": "Ilustración de una instrucción clara para IA"},
                    {"titulo": "Añade contexto y formato", "texto": "Indica para quién es la respuesta y cómo la quieres. Ejemplo: Explica qué es una videollamada en tres pasos, con palabras sencillas para principiantes.", "imagen": "ia-conceptos.svg", "imagen_alt": "Ilustración de contexto y formato en una instrucción"},
                    {"titulo": "Ajusta con otra pregunta", "texto": "Si la respuesta es extensa, pide que la acorte o use un ejemplo. No compartas nombres, documentos, claves ni datos financieros.", "imagen": "ia-segura.svg", "imagen_alt": "Ilustración de una conversación privada y segura con IA"},
                ],
                "actividad": {"pregunta": "¿Qué hace más útil una instrucción para IA?", "opciones": [("contexto", "Explicar la tarea, el contexto y el formato deseado"), ("hola", "Escribir solamente hola"), ("clave", "Incluir una contraseña real")], "respuesta": "contexto"},
            },
            {
                "slug": "ia-imagenes-y-audio",
                "titulo": "Imágenes, voz y otros contenidos creados con IA",
                "duracion": "8 min",
                "introduccion": "Algunas herramientas generan o modifican imágenes, voces y audio desde una descripción. Estos contenidos pueden ser ficticios o imitar a una persona, así que conviene comprobar su origen antes de compartirlos.",
                "objetivos": ["Reconocer contenido creado o modificado por IA.", "Describir una imagen sin usar datos personales.", "Comprobar el origen antes de difundir un contenido."],
                "pasos": [
                    {"titulo": "Describe lo que necesitas", "texto": "Para crear una ilustración, describe el tema, los elementos y el estilo. No solicites usar la cara o la voz de otra persona sin permiso.", "imagen": "ia-generativa.svg", "imagen_alt": "Ilustración creada a partir de una descripción"},
                    {"titulo": "Diferencia creación de evidencia", "texto": "Una imagen o una voz generada puede parecer auténtica, pero no demuestra que el hecho ocurrió. Busca el origen y una fuente independiente.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de comprobación de una imagen generada"},
                    {"titulo": "Respeta permisos y privacidad", "texto": "No subas fotografías privadas ni compartas imitaciones de voz sin autorización. Revisa las condiciones de la herramienta y el permiso de uso.", "imagen": "ia-segura.svg", "imagen_alt": "Ilustración de privacidad y consentimiento para contenidos de IA"},
                ],
                "actividad": {"pregunta": "¿Qué conviene hacer al recibir un audio inesperado de un familiar pidiendo dinero?", "opciones": [("llamar", "Confirmar llamando a su número conocido"), ("enviar", "Enviar dinero de inmediato"), ("publicar", "Compartir el audio en redes")], "respuesta": "llamar"},
            },
        ],
    },
    {
        "curso": "inteligencia-artificial",
        "titulo": "Módulo 3: IA cotidiana, segura y responsable",
        "descripcion": "Identifica usos cercanos, verifica respuestas y protege tus datos y decisiones.",
        "imagen": "ia-segura.svg",
        "lecciones": [
            {
                "slug": "usos-cotidianos-de-ia",
                "titulo": "La IA en la vida cotidiana",
                "duracion": "7 min",
                "introduccion": "La IA ya aparece en filtros de correo, subtítulos automáticos, mapas y recomendaciones de contenido. Saber dónde interviene permite aprovecharla con criterio.",
                "objetivos": ["Identificar ejemplos cotidianos de IA.", "Distinguir una recomendación automática de una decisión personal.", "Ajustar las opciones de una aplicación cuando sea necesario."],
                "pasos": [
                    {"titulo": "Reconoce ayudas automáticas", "texto": "Un teléfono puede convertir voz en texto y un mapa estimar la ruta con menos tráfico. Son sugerencias calculadas a partir de datos.", "imagen": "ia-conceptos.svg", "imagen_alt": "Ilustración de funciones cotidianas apoyadas por IA"},
                    {"titulo": "Entiende las recomendaciones", "texto": "Una aplicación puede sugerir música o noticias según lo que has visto. Puedes ignorar la sugerencia, cambiar preferencias o revisar la configuración.", "imagen": "ia-recomendaciones.svg", "imagen_alt": "Ilustración de recomendaciones de contenido"},
                    {"titulo": "Mantén el control", "texto": "La automatización puede equivocarse. Confirma rutas, mensajes y acciones importantes antes de seguir la sugerencia.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de una persona confirmando una recomendación automática"},
                ],
                "actividad": {"pregunta": "¿Cómo debes tratar una ruta recomendada por una aplicación?", "opciones": [("confirmar", "Revisarla y confirmar que tenga sentido"), ("obedecer", "Seguirla siempre sin mirar"), ("clave", "Escribir la clave bancaria")], "respuesta": "confirmar"},
            },
            {
                "slug": "verificar-informacion-ia",
                "titulo": "Verifica lo que responde la IA",
                "duracion": "8 min",
                "introduccion": "Una respuesta bien redactada puede ser falsa o estar desactualizada. Verificar significa buscar el dato en una fuente independiente antes de confiar o compartirlo.",
                "objetivos": ["Comprobar afirmaciones importantes en otra fuente.", "Reconocer datos inventados o sin contexto.", "No difundir imágenes, audios o noticias sin confirmar."],
                "pasos": [
                    {"titulo": "Separa afirmaciones de opiniones", "texto": "Subraya fechas, cifras, nombres y consejos concretos. Esos datos se pueden contrastar; una opinión no funciona como prueba.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración que destaca datos para comprobar"},
                    {"titulo": "Consulta una fuente independiente", "texto": "Busca la información en una entidad oficial o una organización reconocida, revisa la fecha y compárala con otra fuente confiable.", "imagen": "buscar-seguro.svg", "imagen_alt": "Ilustración de consulta en fuentes confiables"},
                    {"titulo": "Detente si no puedes verificar", "texto": "No reenvíes el mensaje como cierto. Para salud, dinero o trámites, confirma directamente con la institución o una persona profesional.", "imagen": "ia-segura.svg", "imagen_alt": "Ilustración de una decisión prudente ante información no verificada"},
                ],
                "actividad": {"pregunta": "¿Qué es lo más prudente si la IA da una cifra sobre un trámite?", "opciones": [("oficial", "Comprobarla en la página oficial del trámite"), ("compartir", "Publicarla sin revisar"), ("asumir", "Suponer que es correcta por estar bien escrita")], "respuesta": "oficial"},
            },
            {
                "slug": "privacidad-y-seguridad-en-ia",
                "titulo": "Privacidad y seguridad al usar IA",
                "duracion": "8 min",
                "introduccion": "Lo que escribes o subes a un servicio de IA puede ser procesado por la empresa que lo ofrece. Protege los datos personales y entiende las reglas antes de cargar archivos.",
                "objetivos": ["Identificar información que no se debe compartir.", "Revisar controles y condiciones de privacidad.", "Reconocer intentos de fraude que imitan voces o imágenes."],
                "pasos": [
                    {"titulo": "No compartas datos sensibles", "texto": "No escribas contraseñas, códigos de verificación, números de tarjetas, documentos de identidad ni historias clínicas en un chat de IA.", "imagen": "ia-segura.svg", "imagen_alt": "Ilustración de datos personales protegidos"},
                    {"titulo": "Revisa la herramienta", "texto": "Usa el sitio o la aplicación oficial. Consulta qué datos guarda y cómo borrar conversaciones; no cargues un documento privado sin permiso.", "imagen": "ia-privacidad.svg", "imagen_alt": "Ilustración de controles de privacidad en una herramienta"},
                    {"titulo": "Confirma solicitudes urgentes", "texto": "Una voz o una imagen puede ser imitada. Si alguien pide dinero o un código con urgencia, comunícate por otro medio con el número que ya conoces.", "imagen": "ia-verificar.svg", "imagen_alt": "Ilustración de verificación de una identidad antes de responder"},
                ],
                "actividad": {"pregunta": "¿Qué debes hacer si un mensaje de voz desconocido pide un código de verificación?", "opciones": [("no", "No compartirlo y confirmar por un canal conocido"), ("enviar", "Enviar el código para ayudar"), ("ia", "Pegar el código en cualquier chat de IA")], "respuesta": "no"},
            },
        ],
    },
]


MEJORAS_PEDAGOGICAS = {
    "partes-computador": {
        "imagenes": ["monitor-computador.svg", "teclado-mouse.svg", "torre-computador.svg", "todo-en-uno.svg"],
    },
    "teclado-mouse": {
        "imagenes": ["teclado-mouse.svg", "mouse-puntero.svg", "navegador-web.svg"],
    },
    "encender-apagar": {
        "imagenes": ["computador.svg", "documento-digital.svg", "encendido-seguro.svg"],
    },
    "que-es-archivo": {
        "imagenes": ["archivo-tipos.svg", "archivo-tipos.svg", "carpetas.svg"],
    },
    "crear-carpeta": {
        "imagenes": ["carpetas.svg", "carpetas.svg", "archivo-tipos.svg"],
    },
    "organizar-archivos": {
        "imagenes": ["carpetas.svg", "archivo-tipos.svg", "organizar-archivos.svg"],
    },
    "que-es-internet": {
        "imagenes": ["internet.svg", "navegador-web.svg", "internet.svg"],
    },
    "navegadores-web": {
        "imagenes": ["navegador-web.svg", "navegador-web.svg", "navegador-web.svg"],
    },
    "buscar-informacion": {
        "imagenes": ["buscar-seguro.svg", "buscar-seguro.svg", "ia-segura.svg"],
    },
    "documentos-digitales": {
        "imagenes": ["documento-digital.svg", "documento-digital.svg", "archivo-tipos.svg"],
    },
    "correo-electronico": {
        "imagenes": ["correo-electronico.svg", "correo-electronico.svg", "ia-segura.svg"],
    },
    "videollamadas": {
        "imagenes": ["videollamada.svg", "videollamada.svg", "ia-segura.svg"],
    },
}

TEXTOS_ALTERNATIVOS = {
    "monitor-computador.svg": "Ilustración de un monitor mostrando información",
    "teclado-mouse.svg": "Ilustración de un teclado y un mouse",
    "torre-computador.svg": "Ilustración de una torre de computador y sus componentes",
    "todo-en-uno.svg": "Ilustración de un computador Todo en uno",
    "mouse-puntero.svg": "Ilustración de un mouse y el puntero en la pantalla",
    "navegador-web.svg": "Ilustración de una ventana de navegador web",
    "computador.svg": "Ilustración de un computador",
    "documento-digital.svg": "Ilustración de un documento digital",
    "encendido-seguro.svg": "Ilustración del botón de encendido de un computador",
    "archivo-tipos.svg": "Ilustración de varios archivos digitales",
    "carpetas.svg": "Ilustración de carpetas para organizar documentos",
    "organizar-archivos.svg": "Ilustración de archivos organizados en carpetas",
    "internet.svg": "Ilustración de dispositivos conectados a Internet",
    "buscar-seguro.svg": "Ilustración de una búsqueda de información verificada",
    "ia-conceptos.svg": "Ilustración de conceptos de inteligencia artificial",
    "ia-prompt.svg": "Ilustración de una instrucción escrita para una IA",
    "ia-generativa.svg": "Ilustración de contenido generado por inteligencia artificial",
    "ia-recomendaciones.svg": "Ilustración de recomendaciones automáticas",
    "ia-verificar.svg": "Ilustración de verificación de información generada por IA",
    "ia-segura.svg": "Ilustración de uso seguro de inteligencia artificial",
    "ia-privacidad.svg": "Ilustración de privacidad y protección de datos",
    "correo-electronico.svg": "Ilustración de un mensaje de correo electrónico",
    "videollamada.svg": "Ilustración de una videollamada",
}


def crear_recurso_video(titulo):
    busqueda = quote_plus(f"shorts {titulo} tutorial educativo español")
    return {
        "titulo": f"Videos cortos: {titulo}",
        "url": f"https://www.youtube.com/results?search_query={busqueda}",
    }


for modulo in MODULOS:
    for leccion in modulo["lecciones"]:
        recursos = MEJORAS_PEDAGOGICAS.get(leccion["slug"])
        if recursos:
            if len(recursos["imagenes"]) != len(leccion["pasos"]):
                raise ValueError(f"Cada paso necesita una imagen: {leccion['slug']}")
            for paso, imagen in zip(leccion["pasos"], recursos["imagenes"]):
                paso["imagen"] = imagen
                paso["imagen_alt"] = TEXTOS_ALTERNATIVOS[imagen]
        leccion.setdefault("video", crear_recurso_video(leccion["titulo"]))

CURSOS = {
    "informatica-basica": {
        "titulo": "Informática básica",
        "descripcion": "Aprende a usar el computador paso a paso: reconoce sus partes, escribe y organiza tus documentos.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "informatica-basica"],
    },
    "internet": {
        "titulo": "Internet",
        "descripcion": "Navega, busca información y comunícate por Internet con confianza y cuidado.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "internet"],
    },
    "herramientas-digitales": {
        "titulo": "Herramientas digitales",
        "descripcion": "Crea documentos, usa el correo y participa en videollamadas con instrucciones sencillas.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "herramientas-digitales"],
    },
    "inteligencia-artificial": {
        "titulo": "Inteligencia artificial para la vida diaria",
        "descripcion": "Conoce los tipos de IA, aprende a usar herramientas generativas y protege tus datos mientras verificas sus respuestas.",
        "modulos": [modulo for modulo in MODULOS if modulo["curso"] == "inteligencia-artificial"],
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
