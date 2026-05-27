 import streamlit as st
import pandas as pd
import joblib

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Sentinel SOS",
    page_icon="🌎",
    layout="centered"
)

# =========================
# CARREGAR MODELO
# =========================

model = joblib.load(
    "sentinel_sos_xgboost.pkl"
)

# =========================
# TÍTULO
# =========================

st.title("🌎 Sentinel SOS")

st.subheader(
    "Sistema Inteligente de Previsão de Riscos Climáticos"
)

st.markdown("""
O Sentinel SOS utiliza Inteligência Artificial e dados orbitais
da NASA POWER API para prever riscos climáticos extremos.
""")

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Sobre o Projeto")

st.sidebar.markdown("""
### Tecnologias Utilizadas

- NASA POWER API
- Machine Learning
- XGBoost
- SHAP
- Streamlit

### Objetivo

Auxiliar na prevenção de:

- enchentes
- tempestades
- alagamentos
- eventos extremos
""")

# =========================
# INPUTS
# =========================

st.header("📡 Dados Climáticos")

precipitation = st.number_input(
    "Precipitação (mm)",
    min_value=0.0,
    max_value=500.0,
    value=10.0
)

temperature = st.number_input(
    "Temperatura Média (°C)",
    min_value=-10.0,
    max_value=50.0,
    value=25.0
)

humidity = st.number_input(
    "Umidade Relativa (%)",
    min_value=0.0,
    max_value=100.0,
    value=70.0
)

wind_speed = st.number_input(
    "Velocidade do Vento (m/s)",
    min_value=0.0,
    max_value=100.0,
    value=5.0
)

solar_radiation = st.number_input(
    "Radiação Solar",
    min_value=0.0,
    max_value=50.0,
    value=15.0
)

month = st.slider(
    "Mês",
    min_value=1,
    max_value=12,
    value=1
)

# =========================
# FEATURE ENGINEERING
# =========================

rain_intensity = (
    precipitation * humidity
)

storm_index = (
    precipitation * wind_speed
)

heat_index = (
    temperature * (humidity / 100)
)

extreme_rain = int(
    precipitation > 40
)

# =========================
# DATAFRAME FINAL
# =========================

input_data = pd.DataFrame([{
    "PRECTOTCORR": precipitation,
    "T2M": temperature,
    "RH2M": humidity,
    "WS2M": wind_speed,
    "ALLSKY_SFC_SW_DWN": solar_radiation,
    "month": month,
    "rain_intensity": rain_intensity,
    "storm_index": storm_index,
    "heat_index": heat_index,
    "extreme_rain": extreme_rain
}])

# =========================
# BOTÃO DE PREVISÃO
# =========================

if st.button("🔍 Analisar Risco Climático"):

    prediction = model.predict(
        input_data
    )[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    st.divider()

    st.header("📊 Resultado da Análise")

    # =========================
    # CLASSIFICAÇÃO
    # =========================

    if prediction == 0:

        st.success(
            "🟢 Baixo Risco Climático"
        )

    elif prediction == 1:

        st.warning(
            "🟠 Médio Risco Climático"
        )

    else:

        st.error(
            "🔴 Alto Risco Climático"
        )

    # =========================
    # PROBABILIDADES
    # =========================

    st.subheader(
        "Probabilidade por Classe"
    )

    st.write(
        f"🟢 Baixo Risco: {probabilities[0]*100:.2f}%"
    )

    st.write(
        f"🟠 Médio Risco: {probabilities[1]*100:.2f}%"
    )

    st.write(
        f"🔴 Alto Risco: {probabilities[2]*100:.2f}%"
    )

    # =========================
    # FEATURES GERADAS
    # =========================

    st.subheader(
        "📈 Indicadores Gerados"
    )

    st.write(
        f"Rain Intensity: {rain_intensity:.2f}"
    )

    st.write(
        f"Storm Index: {storm_index:.2f}"
    )

    st.write(
        f"Heat Index: {heat_index:.2f}"
    )

    st.write(
        f"Extreme Rain: {extreme_rain}"
    )

# =========================
# RODAPÉ
# =========================

st.divider()

st.caption("""
Sentinel SOS • Global Solution • Economia Espacial

Projeto acadêmico utilizando Machine Learning
e dados orbitais da NASA POWER API.
""")