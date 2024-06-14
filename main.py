import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import numpy as np


# Simulando datos históricos para un hombre de 45 años con diabetes tipo 2
start_date = pd.to_datetime("today") - pd.DateOffset(months=6)
end_date = pd.to_datetime("today")
date_range = pd.date_range(start_date, end_date, freq='D')

# Crear un DataFrame simulado
data = {
    'Fecha': date_range,
    'Nombre': ['Juan Pérez']*len(date_range),
    'Edad': [45]*len(date_range),
    'Ocupación': ['Ingeniero']*len(date_range),
    'Sexo': ['Masculino']*len(date_range),
    'Peso': np.random.normal(85, 2.5, len(date_range)),  # Peso con menos variación
    'Talla': np.random.normal(1.75, 0.05, len(date_range)),
    'Frecuencia Cardíaca': np.random.normal(70, 5, len(date_range)),  # Simulación de ritmo cardíaco
    'Horas de Sueño': np.random.normal(7, 1, len(date_range)),  # Simulación de horas de sueño
    'Azúcar en la Sangre': np.random.normal(85, 5, len(date_range)),  # Valores típicos para diabetes tipo 2
    'Enfermedades': ['Diabetes tipo 2']*len(date_range),
    'Alergias': ['Polen']*len(date_range)
}
historico = pd.DataFrame(data)

def main():
    st.sidebar.title("Navegación")
    selection = st.sidebar.radio("Ir a", ["Formulario", "Historial", "Perfil del Paciente", "Recomendaciones"])

    if selection == "Formulario":
        formulario()
    elif selection == "Historial":
        historial()
    elif selection == "Perfil del Paciente":
        perfil_paciente()
    else:
        recomendaciones()

def formulario():
    st.title('Formulario de Registro de Salud del Paciente')
    enfermedades_opciones = ['Diabetes tipo 2', 'Hipertensión', 'Asma', 'Enfermedad coronaria', 'Artritis', 
                             'Depresión', 'Ansiedad', 'Obesidad', 'EPOC', 'Cáncer', 'Hipotiroidismo', 'Hipercolesterolemia', 
                             'Osteoporosis', 'Fibromialgia', 'Esclerosis múltiple']
    alergias_opciones = ['Polen', 'Ácaros del polvo', 'Nueces', 'Látex', 'Picaduras de insectos', 'Moldes', 'Pelo de animales',
                         'Alimentos marinos', 'Soja', 'Leche', 'Huevo', 'Gluten', 'Perfumes', 'Látex']
    tipos_de_sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    medicamentos_comunes = ['Penicilina', 'Aspirina', 'Ibuprofeno', 'Amoxicilina', 'Codeína', 'Acetaminofén', 'Naproxeno', 'Diclofenaco', 'Ciprofloxacino', 'Metformina']
    with st.form("health_form"):
        nombre = st.text_input('Nombre')
        edad = st.number_input('Edad', min_value=0, step=1)
        ocupacion = st.text_input('Ocupación')
        sexo = st.selectbox('Sexo', ['Masculino', 'Femenino', 'Otro'])
        tipo_sangre = st.selectbox('Tipo de Sangre', tipos_de_sangre)
        peso = st.number_input('Peso (kg)', min_value=0.0, step=0.1)
        talla = st.number_input('Talla (m)', min_value=0.0, step=0.01)
        enfermedades = st.multiselect('Enfermedades Diagnosticadas', enfermedades_opciones)
        alergias = st.multiselect('Alergias', alergias_opciones)
        alergia_medicamentos = st.multiselect('Alergia a Medicamentos', medicamentos_comunes)
        submitted = st.form_submit_button('Enviar')

        if submitted:
            st.session_state['nombre'] = nombre
            st.session_state['edad'] = edad
            st.session_state['ocupacion'] = ocupacion
            st.session_state['sexo'] = sexo
            st.session_state['tipo_sangre'] = tipo_sangre
            st.session_state['peso'] = peso
            st.session_state['talla'] = talla
            st.session_state['imc'] = round(peso / (talla ** 2), 2)
            st.session_state['enfermedades'] = enfermedades
            st.session_state['alergias'] = alergias
            st.session_state['alergia_medicamentos'] = alergia_medicamentos
            st.success("Datos enviados con éxito!")

def perfil_paciente():
    st.title('Perfil del Paciente')
    if 'nombre' in st.session_state:
        st.subheader(f"Nombre: {st.session_state['nombre']}")
        st.write(f"Edad: {st.session_state['edad']}")
        st.write(f"Ocupación: {st.session_state['ocupacion']}")
        st.write(f"Sexo: {st.session_state['sexo']}")
        st.write(f"Tipo de Sangre: {st.session_state['tipo_sangre']}")
        st.write(f"Peso: {st.session_state['peso']} kg")
        st.write(f"Talla: {st.session_state['talla']} m")
        if 'imc' in st.session_state:
            st.write(f"IMC: {st.session_state['imc']}")
        st.write(f"Enfermedades Diagnosticadas: {', '.join(st.session_state['enfermedades'])}")
        st.write(f"Alergias: {', '.join(st.session_state['alergias'])}")
        if st.session_state['alergia_medicamentos']:
            st.write(f"Alergia a Medicamentos: {', '.join(st.session_state['alergia_medicamentos'])}")

def recomendaciones():
    st.title('Recomendaciones Basadas en su Salud')
    if 'enfermedades' in st.session_state:
        for enfermedad in st.session_state['enfermedades']:
            st.write(recomendacion_enfermedad(enfermedad))
    if 'alergias' in st.session_state:
        for alergia in st.session_state['alergias']:
            st.write(recomendacion_alergia(alergia))
    if 'imc' in st.session_state:
        imc = st.session_state['imc']
        categoria = clasificar_imc(imc)
        st.subheader(f"Su IMC es {imc}, lo que le clasifica en la categoría: {categoria}")
        st.write(recomendacion_imc(categoria))

def clasificar_imc(imc):
    if imc < 18.5:
        return 'Bajo peso'
    elif 18.5 <= imc < 25:
        return 'Normal'
    elif 25 <= imc < 30:
        return 'Sobrepeso'
    elif 30 <= imc < 35:
        return 'Obesidad grado I'
    elif 35 <= imc < 40:
        return 'Obesidad grado II'
    else:
        return 'Obesidad grado III'
    
def recomendacion_imc(categoria):
    recomendaciones_imc = {
        'Bajo peso': "Es importante aumentar la ingesta calórica de forma saludable e incrementar la actividad física.",
        'Normal': "Mantener una dieta equilibrada y continuar con ejercicio regular para conservar un peso saludable.",
        'Sobrepeso': "Es recomendable ajustar la dieta para reducir calorías y aumentar la actividad física.",
        'Obesidad grado I': "Considerar una consulta con un nutricionista para realizar cambios dietéticos significativos y un plan de ejercicio.",
        'Obesidad grado II': "Es crucial buscar asesoramiento médico para abordar esta condición con un enfoque multidisciplinario.",
        'Obesidad grado III': "Se recomienda un manejo intensivo que puede incluir medicación, dieta supervisada o cirugía bariátrica."
    }
    return recomendaciones_imc[categoria]

def recomendacion_enfermedad(enfermedad):
    recomendaciones_dict = {
        'Diabetes tipo 2': "Mantener una dieta baja en azúcares y carbohidratos, ejercitar regularmente.",
        'Hipertensión': "Reducir la ingesta de sal, evitar alimentos altos en grasa, realizar ejercicio regularmente.",
        'Asma': "Evitar alérgenos conocidos, mantener un entorno limpio y libre de polvo, tener un plan de acción para ataques de asma.",
        'Enfermedad coronaria': "Seguir una dieta saludable para el corazón, realizar actividad física regular, gestionar el estrés.",
        'Artritis': "Mantener una actividad física moderada, usar terapias de calor o frío, considerar la fisioterapia.",
        'Depresión': "Mantener una rutina regular, buscar apoyo psicológico, considerar la terapia cognitivo-conductual.",
        'Ansiedad': "Practicar técnicas de relajación como la meditación, mantener un estilo de vida activo, buscar terapia profesional.",
        'Obesidad': "Adoptar una dieta equilibrada, incrementar la actividad física, considerar asesoramiento nutricional.",
        'EPOC': "Evitar el humo de cigarrillos y otros irritantes pulmonares, realizar ejercicios de rehabilitación pulmonar.",
        'Cáncer': "Seguir las indicaciones del oncólogo, mantener una nutrición adecuada, explorar grupos de apoyo.",
        'Hipotiroidismo': "Tomar la medicación según lo prescrito, controlar regularmente los niveles de tiroides.",
        'Hipercolesterolemia': "Adoptar una dieta baja en grasas saturadas y colesterol, realizar ejercicio, considerar medicación si es necesario.",
        'Osteoporosis': "Incrementar la ingesta de calcio y vitamina D, realizar ejercicio de soporte de peso.",
        'Fibromialgia': "Implementar estrategias de manejo del dolor, mantener un sueño saludable, realizar ejercicios de bajo impacto.",
        'Esclerosis múltiple': "Adaptar las actividades diarias según la energía disponible, buscar apoyo fisioterapéutico, considerar medicación."
    }
    return recomendaciones_dict.get(enfermedad, "Consulte a un especialista para obtener recomendaciones personalizadas.")

def recomendacion_alergia(alergia):
    alergias_dict = {
        'Polen': "Utilizar purificadores de aire y evitar salir los días de alto conteo de polen.",
        'Ácaros del polvo': "Mantener una limpieza regular en el hogar, especialmente de ropa de cama y alfombras.",
        'Nueces': "Evitar el consumo de nueces y productos que puedan contener trazas de nueces.",
        'Látex': "Utilizar alternativas al látex en productos como guantes y preservativos.",
        'Picaduras de insectos': "Utilizar repelentes de insectos, evitar aguas estancadas y zonas con alta vegetación.",
        'Moldes': "Mantener los espacios bien ventilados y secos para evitar la acumulación de moho.",
        'Pelo de animales': "Evitar el contacto con animales, mantener una buena higiene en las mascotas y limpiar los hogares regularmente.",
        'Alimentos marinos': "Evitar el consumo de mariscos y peces si se es alérgico, prestar atención a etiquetas en alimentos procesados.",
        'Soja': "Evitar alimentos que contengan soja, leer etiquetas cuidadosamente.",
        'Leche': "Evitar la leche y sus derivados, considerar alternativas no lácteas.",
        'Huevo': "Evitar alimentos que contengan huevo, buscar alternativas para cocinar.",
        'Gluten': "Adoptar una dieta libre de gluten, ser cauteloso con la contaminación cruzada en alimentos.",
        'Perfumes': "Evitar perfumes y productos con fragancias fuertes, optar por productos sin aroma.",
        'Látex (repetido)': "Revisar productos médicos y personales para asegurar que no contengan látex."
    }
    return alergias_dict.get(alergia, "Consulte a un alergólogo para manejo específico.")



def historial():
    st.title('Historial de Salud')
    # Gráfico de Peso
    fig = px.line(historico, x='Fecha', y='Peso', title='Historial de Peso')
    st.plotly_chart(fig)
    # Gráfico de Frecuencia Cardíaca
    fig2 = px.line(historico, x='Fecha', y='Frecuencia Cardíaca', title='Historial de Frecuencia Cardíaca')
    st.plotly_chart(fig2)
    # Gráfico de Horas de Sueño
    fig3 = px.line(historico, x='Fecha', y='Horas de Sueño', title='Historial de Horas de Sueño')
    st.plotly_chart(fig3)
    # Gráfico de Azúcar en la Sangre
    fig4 = px.line(historico, x='Fecha', y='Azúcar en la Sangre', title='Historial de Azúcar en la Sangre')
    st.plotly_chart(fig4)
    # Gráfico de IMC
    historico['IMC'] = historico['Peso'] / (historico['Talla'] ** 2)
    fig5 = px.line(historico, x='Fecha', y='IMC', title='Historial de IMC')
    st.plotly_chart(fig5)

if __name__ == "__main__":
    main()
