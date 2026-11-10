# Guion aprobado (v3 + registro v4). Marcas: [tag]=direccion (solo en la version dirigida),
# *palabra*=enfasis (MAYUSCULA en la dirigida), {SuprNotes}=se pronuncia "Supr Nouts" en la dirigida.
import re

BLOQUES = [
("b01", "[warm] [upbeat] Te damos la bienvenida al curso de certificación de OneScreen {SuprNotes}. [short pause] Este es el módulo *uno*, la base de todo lo que vendrá después: [confident] aquí vas a entender qué es {SuprNotes}, qué puede hacer por ti y cómo entrar. [short pause] Al terminar el curso presentarás tu examen de certificación, directamente con OneScreen."),
("b02", "[thoughtful] Empecemos por una situación que seguro conoces. [short pause] Termina una clase, una capacitación o una sesión de estudio. Se explicó mucho, se dieron ejemplos, se resolvieron preguntas. [short pause] Y ahora toca convertir todo eso en algo que otras personas puedan repasar: un resumen, tarjetas, un cuestionario. [emphatic] Hacerlo a mano toma *horas*, y casi siempre se queda a medias. [short pause] [confident] {SuprNotes} existe para resolver *justo* eso."),
("b03", "[upbeat] {SuprNotes} es una aplicación web desarrollada por OneScreen que usa inteligencia artificial para convertir contenido educativo: documentos, audios y videos, en materiales de estudio *estructurados* y de alta calidad."),
("b04", "[curious] Piensa en una herramienta de notas tradicional: escucha y escribe lo que se dijo. [short pause] Nada más. [emphatic] {SuprNotes} da un paso adicional: *entiende*. [confident] Analiza lo que se escucha y también lo que se ve, como una diapositiva o un esquema dentro de un video, comprende el contexto y organiza la información como lo haría una persona que se tomó el tiempo de estudiarla."),
("b05", "[upbeat] Esto es posible por su capacidad *multimodal*: puede trabajar con texto, audio, imagen y video al mismo tiempo. [short pause] Le entregas un contenido y no hace una sola cosa: lanza varios procesos en *paralelo*, y cada uno produce una salida distinta. [short pause] Veámoslas."),
("b05a", "[confident] *Primero*, el resumen de guía: la versión corta y ordenada del contenido, para entender de qué trata sin volver a verlo completo."),
("b05b", "*Segundo*, las tarjetas didácticas: preguntas y respuestas breves para memorizar conceptos. [short pause] Son ideales para repasar en ratos libres."),
("b05c", "*Tercero*, el cuestionario: preguntas para comprobar si de verdad se entendió."),
("b05d", "*Cuarto*, la guía de repaso: un documento que reúne definiciones y puntos clave, pensado para el momento previo a una evaluación."),
("b05e", "[upbeat] Y *quinto*, el chat con inteligencia artificial: una conversación sobre ese mismo contenido, para preguntar lo que no quedó claro."),
("b06", "[thoughtful] Detrás hay dos tipos de modelos trabajando juntos. [short pause] Los modelos de *lenguaje* entienden y redactan el texto. Los modelos de *visión* interpretan las imágenes. [confident] Entre los dos analizan todo tu material al mismo tiempo."),
("b07a", "[serious] [emphatic] Ahora, lo más importante de todo el software de OneScreen: [short pause] la inteligencia artificial *solo* genera contenido a partir de las fuentes que tú le das."),
("b07b", "{SuprNotes} no investiga en internet ni usa información que no hayas aprobado. [confident] Todo lo que produce sale de *tu* material."),
("b07c", "[curious] ¿Y qué material puede ser? [short pause] La transcripción de una clase: así {SuprNotes} aprende qué se dijo, qué ejemplos se usaron, cómo se explicó el tema y qué preguntas se hicieron. [short pause] Notas de estudio o una presentación, si el contenido está escrito en algún lugar. [short pause] O un video de YouTube, o cualquier fuente que se te ocurra, siempre que la hayas elegido tú."),
("b07d", "[warm] [emphatic] El resultado es material que suena a tu clase, a tu empresa, a tu curso. [short pause] No a un texto genérico."),
("b08", "[warm] Veamos cómo se ve esto en la práctica. Imagina una docente de biología que acaba de dar una clase sobre depredadores. Graba la sesión y le entrega la transcripción a {SuprNotes}. [short pause] En pocos minutos tiene un resumen con los conceptos de la clase, tarjetas con definiciones como ecosistema o especie en peligro, un cuestionario para la siguiente sesión y una guía de repaso para compartir con todo el curso. [upbeat] Y lo mejor: está construido con sus ejemplos y con su forma de explicar, porque ella fue la fuente. [confident] Ya no pasa la noche armando material; revisa, ajusta y comparte."),
("b09", "[warm] Ahora ponte en el lugar de un estudiante, a una semana del parcial. Tiene sus apuntes, la presentación del profesor y la grabación de la clase. [short pause] Los sube como fuentes, y obtiene tarjetas para repasar en el trayecto a casa, un cuestionario para probarse y descubrir qué todavía no domina, [curious] y un chat donde puede preguntar: «¿cuál es la diferencia entre estos dos conceptos?» [confident] y recibir una respuesta basada en su propio material, no en lo primero que aparezca en internet."),
("b10", "[confident] Y en el ámbito corporativo funciona igual. Un equipo de recursos humanos graba la sesión de inducción, o toma el manual de procesos. [short pause] Con eso genera una guía de repaso para cada persona nueva, un cuestionario para verificar que entendió los procedimientos y un chat para resolver dudas rápidas. [emphatic] Y como solo usa los documentos que la empresa *aprobó*, la información es consistente para todos y no se mezcla con fuentes externas."),
("b11a", "[upbeat] Ahora vamos a crear tu cuenta, paso a paso. [short pause] *Paso uno.* Entra a la página principal de {SuprNotes}. Arriba a la derecha vas a ver tres opciones: Precios, Iniciar sesión y Registrarse. [confident] Haz clic en *Registrarse*. También puedes usar el botón Comienza gratis, que está debajo del título."),
("b11b", "*Paso dos.* Elige cómo quieres crear tu cuenta. Tienes tres caminos. [short pause] Con tu correo electrónico, completando este formulario. O, más abajo, con Continuar con Google o Continuar con Microsoft: son los más rápidos, porque usas una cuenta que ya tienes y no tienes que inventar otra contraseña. [confident] Las tres son completamente válidas; elige la que uses a diario."),
("b11c", "Si eliges Google o Microsoft, selecciona tu cuenta, acepta, y entras directo. [short pause] Si prefieres el correo, completa el formulario: tu nombre, tu apellido, tu correo electrónico, una contraseña y su confirmación. La barra que aparece debajo te indica qué tan segura es: elige una contraseña *fuerte*, que puedas recordar."),
("b11d", "*Paso tres.* Marca la casilla «No soy un robot», para confirmar que eres una persona."),
("b11e", "*Paso cuatro.* Haz clic en *Crear cuenta*. [short pause] [upbeat] Y listo, ya estás dentro. Esta es tu pantalla de inicio: arriba, el espacio para importar contenido; abajo, tus resúmenes recientes, donde irán apareciendo todas las guías que vayas creando."),
("b11f", "[warm] Un consejo: usa el correo con el que vas a trabajar siempre en {SuprNotes}. Y si ya tienes cuenta, en lugar de Registrarse haz clic en Iniciar sesión."),
("b12", "[thoughtful] Quedémonos con tres ideas. {SuprNotes} convierte tu contenido en material de estudio. [short pause] Lo hace en paralelo: resumen, tarjetas, cuestionario, guía de repaso y chat. [emphatic] Y solo usa las fuentes que tú le das. [short pause] [warm] En el siguiente módulo vamos a aprender a importar contenido desde distintas fuentes y a crear tu primera clase. Nos vemos allí."),
]


def limpio(t):
    t = re.sub(r"\[[^\]]*\]\s*", "", t)
    t = t.replace("{SuprNotes}", "SuprNotes")
    return re.sub(r"\*([^*]+)\*", r"\1", t).strip()


def dirigido(t):
    t = t.replace("{SuprNotes}", "Supr Nouts")
    return re.sub(r"\*([^*]+)\*", lambda m: m.group(1).upper(), t).strip()
