import streamlit as st
import pandas as pd
import requests
import joblib
from datetime import date, timedelta

# =========================
# CONFIGURAÇÃO
# =========================

st.set_page_config(
    page_title="Sentinel SOS",
    page_icon="🛰️",
    layout="wide"
)

MODEL_PATH = "sentinel_sos_xgboost.pkl"

FEATURES = [
    "PRECTOTCORR",
    "T2M",
    "RH2M",
    "WS2M",
    "ALLSKY_SFC_SW_DWN",
    "month",
    "rain_intensity",
    "storm_index",
    "heat_index",
    "extreme_rain"
]

RISK_LABELS = {
    0: "Baixo Risco Climático",
    1: "Médio Risco Climático",
    2: "Alto Risco Climático"
}

CITIES = {
    "São Paulo": (-23.5505, -46.6333),
    "Rio de Janeiro": (-22.9068, -43.1729),
    "Curitiba": (-25.4284, -49.2733),
    "Florianópolis": (-27.5949, -48.5482),
    "Porto Alegre": (-30.0346, -51.2177),
    "Belo Horizonte": (-19.9167, -43.9345)
}

# =========================
# FUNÇÕES
# =========================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data(ttl=3600)
def get_nasa_power_data(latitude, longitude, selected_date):
    date_str = selected_date.strftime("%Y%m%d")

    parameters = ",".join([
        "PRECTOTCORR",
        "T2M",
        "RH2M",
        "WS2M",
        "ALLSKY_SFC_SW_DWN"
    ])

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={parameters}"
        "&community=AG"
        f"&longitude={longitude}"
        f"&latitude={latitude}"
        f"&start={date_str}"
        f"&end={date_str}"
        "&format=JSON"
    )

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Erro na NASA API: status {response.status_code}")

    data = response.json()
    parameters_data = data["properties"]["parameter"]

    return {
        "PRECTOTCORR": float(parameters_data["PRECTOTCORR"][date_str]),
        "T2M": float(parameters_data["T2M"][date_str]),
        "RH2M": float(parameters_data["RH2M"][date_str]),
        "WS2M": float(parameters_data["WS2M"][date_str]),
        "ALLSKY_SFC_SW_DWN": float(parameters_data["ALLSKY_SFC_SW_DWN"][date_str]),
        "month": selected_date.month
    }


def build_features(base_data):
    precipitation = base_data["PRECTOTCORR"]
    temperature = base_data["T2M"]
    humidity = base_data["RH2M"]
    wind_speed = base_data["WS2M"]

    features = {
        **base_data,
        "rain_intensity": precipitation * humidity,
        "storm_index": precipitation * wind_speed,
        "heat_index": temperature * (humidity / 100),
        "extreme_rain": int(precipitation > 40)
    }

    return pd.DataFrame([features])[FEATURES]


def predict_risk(model, input_data):
    prediction = int(model.predict(input_data)[0])
    probabilities = model.predict_proba(input_data)[0]

    return prediction, probabilities


# =========================
# APP
# =========================

model = load_model()

st.title("🛰️ Sentinel SOS")
st.markdown(
    "Sistema inteligente de previsão de risco climático usando **dados orbitais da NASA POWER API** e **XGBoost**."
)

st.sidebar.title("Sentinel SOS")
st.sidebar.markdown("""
**Modo dinâmico:** consulta a NASA API em tempo real.

**Modo manual:** permite simular cenários climáticos.

Classes:
- 🟢 Baixo risco
- 🟠 Médio risco
- 🔴 Alto risco
""")

mode = st.sidebar.radio(
    "Modo de uso",
    ["Consultar NASA API", "Simulação manual"]
)

st.divider()

# =========================
# MODO NASA
# =========================

if mode == "Consultar NASA API":
    st.header("📡 Consulta Orbital")

    with st.form("nasa_form"):
        col1, col2 = st.columns(2)

        with col1:
            city = st.selectbox("Cidade", list(CITIES.keys()))

        with col2:
            selected_date = st.date_input(
                "Data",
                value=date(2024, 1, 1),
                min_value=date(2020, 1, 1),
                max_value=date.today() - timedelta(days=2)
            )

        submitted = st.form_submit_button("🔍 Consultar e prever risco")

    if submitted:
        latitude, longitude = CITIES[city]

        try:
            with st.spinner("Consultando dados orbitais da NASA..."):
                base_data = get_nasa_power_data(
                    latitude,
                    longitude,
                    selected_date
                )

            input_data = build_features(base_data)
            prediction, probabilities = predict_risk(model, input_data)

            st.success("Dados consultados com sucesso!")

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Chuva", f"{base_data['PRECTOTCORR']:.2f} mm")
            col2.metric("Temperatura", f"{base_data['T2M']:.2f} °C")
            col3.metric("Umidade", f"{base_data['RH2M']:.2f}%")
            col4.metric("Vento", f"{base_data['WS2M']:.2f} m/s")
            col5.metric("Radiação", f"{base_data['ALLSKY_SFC_SW_DWN']:.2f}")

            st.subheader("📊 Resultado da IA")

            if prediction == 0:
                st.success(f"🟢 {RISK_LABELS[prediction]}")
            elif prediction == 1:
                st.warning(f"🟠 {RISK_LABELS[prediction]}")
            else:
                st.error(f"🔴 {RISK_LABELS[prediction]}")

            prob_df = pd.DataFrame({
                "Classe": ["Baixo", "Médio", "Alto"],
                "Probabilidade (%)": [
                    probabilities[0] * 100,
                    probabilities[1] * 100,
                    probabilities[2] * 100
                ]
            })

            st.bar_chart(
                prob_df.set_index("Classe")
            )

            with st.expander("Ver features enviadas ao modelo"):
                st.dataframe(input_data)

        except Exception as error:
            st.error("Não foi possível consultar a NASA API ou gerar a previsão.")
            st.code(str(error))

# =========================
# MODO MANUAL
# =========================

else:
    st.header("🧪 Simulação Manual")

    with st.form("manual_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            precipitation = st.number_input("Precipitação (mm)", 0.0, 500.0, 20.0)
            temperature = st.number_input("Temperatura média (°C)", -10.0, 50.0, 25.0)

        with col2:
            humidity = st.number_input("Umidade relativa (%)", 0.0, 100.0, 75.0)
            wind_speed = st.number_input("Velocidade do vento (m/s)", 0.0, 100.0, 5.0)

        with col3:
            solar_radiation = st.number_input("Radiação solar", 0.0, 50.0, 15.0)
            month = st.slider("Mês", 1, 12, 1)

        submitted = st.form_submit_button("🔍 Prever risco")

    if submitted:
        base_data = {
            "PRECTOTCORR": precipitation,
            "T2M": temperature,
            "RH2M": humidity,
            "WS2M": wind_speed,
            "ALLSKY_SFC_SW_DWN": solar_radiation,
            "month": month
        }

        input_data = build_features(base_data)
        prediction, probabilities = predict_risk(model, input_data)

        st.subheader("📊 Resultado da IA")

        if prediction == 0:
            st.success(f"🟢 {RISK_LABELS[prediction]}")
        elif prediction == 1:
            st.warning(f"🟠 {RISK_LABELS[prediction]}")
        else:
            st.error(f"🔴 {RISK_LABELS[prediction]}")

        prob_df = pd.DataFrame({
            "Classe": ["Baixo", "Médio", "Alto"],
            "Probabilidade (%)": [
                probabilities[0] * 100,
                probabilities[1] * 100,
                probabilities[2] * 100
            ]
        })

        st.bar_chart(prob_df.set_index("Classe"))

        with st.expander("Ver features enviadas ao modelo"):
            st.dataframe(input_data)

st.divider()
st.caption("Sentinel SOS • Global Solution • Economia Espacial • NASA POWER API + XGBoost + Streamlit")
