from datetime import datetime


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hola", "buenas", "qué tal", "cómo van"):
        return "hola compa"

    if user_message in ("qué es eso?", "quién es ud?", "quién es usted?"):
        return "Soy CompaBot, un bot para telegram programado en Python para https://t.me/grupodeprogramacionun"

    if user_message in ("mejor lenguaje", "qué lenguaje recomiendan", "qué lenguaje aprender primero", "python"):
        return "Python, mira la documentación https://docs.python.org/3.9/index.html"

    if user_message in ("github", "código del compabot"):
        return "Hola, mira mi código en https://github.com/SkyRedCorp/compaBotUNAL"

    if user_message in ("lo sacó el bot", "no completó el captcha"):
        return "XD"

    if user_message in ("hola mundo", "compabot"):
        return "Hola, a la orden"

    if user_message in ("f"):
        return "F"

    if user_message in ("x2", "X2"):
        return "X3"

    if user_message in ("hora", "hora?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")

        return str(date_time)

    # return "no entiendo"
