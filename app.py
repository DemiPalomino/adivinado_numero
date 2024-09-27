import random  # Importa el módulo random para generar números aleatorios
from flask import Flask, render_template, request, redirect, url_for, session  # Importa módulos de Flask para manejar la aplicación web
import numpy as np  # Importa NumPy para trabajar con arreglos y matrices
from sklearn.linear_model import LinearRegression  # Importa el modelo de regresión lineal de Scikit-learn

app = Flask(__name__)  # Crea una instancia de la clase Flask
app.secret_key = 'supersecretkey'  # Clave secreta para gestionar las sesiones (debería ser más robusta)

@app.route('/', methods=['GET', 'POST'])  # Define la ruta principal de la aplicación
def index():
    # Comprueba si 'numero_secreto' no está en la sesión
    if 'numero_secreto' not in session:
        session['numero_secreto'] = random.randint(1, 100)  # Genera un número secreto aleatorio entre 1 y 100
        session['intentos'] = []  # Inicializa la lista de intentos
        session['resultados'] = []  # Inicializa la lista de resultados

    # Maneja las solicitudes POST (cuando el usuario envía un intento)
    if request.method == 'POST':
        intento = request.form.get('intento')  # Obtiene el intento del formulario
        if intento:  # Comprueba si se recibió un intento
            intento = int(intento)  # Convierte el intento a un número entero
            session['intentos'].append(intento)  # Almacena el intento en la sesión

            # Compara el intento con el número secreto
            if intento < session['numero_secreto']:
                mensaje = "Demasiado bajo!"  # El intento es menor que el número secreto
                session['resultados'].append(1)  # Agrega un resultado positivo
            elif intento > session['numero_secreto']:
                mensaje = "Demasiado alto!"  # El intento es mayor que el número secreto
                session['resultados'].append(-1)  # Agrega un resultado negativo
            else:
                mensaje = "¡Correcto!"  # El intento es igual al número secreto
                session['resultados'].append(0)  # Agrega un resultado cero (acierto)
                return redirect(url_for('ganar'))  # Redirige a la página de ganar

            # Entrena el modelo de regresión solo si hay más de un intento
            if len(session['intentos']) > 1:
                # Prepara los datos para el modelo
                X = np.array(session['intentos'][:-1]).reshape(-1, 1)  # Usa todos los intentos menos el último como características
                y = np.array(session['resultados'][:-1])  # Usa todos los resultados menos el último como etiqueta
                model = LinearRegression().fit(X, y)  # Entrena el modelo de regresión lineal
                # Predecir el siguiente intento basado en la regresión
                prediccion = model.predict(np.array([[intento]]))  # Hace una predicción basado en el último intento
                siguiente_intento = int(prediccion[0])  # Convierte la predicción a un entero
                mensaje += f" Sugerencia para el siguiente intento: {siguiente_intento}"  # Agrega sugerencia al mensaje
                
            session.modified = True  # Indica que la sesión ha sido modificada
            return render_template('index2.html', mensaje=mensaje)  # Renderiza la página con el mensaje

    return render_template('index2.html')  # Renderiza la página inicial si no hay solicitudes POST

@app.route('/ganar')  # Define la ruta para la página de ganar
def ganar():
    session.clear()  # Limpia la sesión para reiniciar el juego
    return render_template('ganar.html')  # Renderiza la página de ganar

if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta la aplicación en modo de depuración
