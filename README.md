# 🌎 Sentinel SOS

## Sistema Inteligente de Previsão de Riscos Climáticos com Dados Orbitais

O Sentinel SOS é uma solução desenvolvida para o desafio de Economia Espacial da Global Solution, utilizando Inteligência Artificial, Machine Learning e dados orbitais da NASA POWER API para prever riscos climáticos extremos, como enchentes, tempestades e alagamentos.

O sistema realiza consultas em tempo real a dados climáticos provenientes de satélites da NASA e utiliza um modelo de Machine Learning baseado em XGBoost para classificar o nível de risco climático de determinada região.

---

# 🚀 Objetivo do Projeto

O objetivo do Sentinel SOS é auxiliar na prevenção e monitoramento de eventos climáticos extremos por meio de:

- ingestão de dados orbitais;
- processamento de dados climáticos;
- engenharia de atributos;
- modelos de Machine Learning;
- interpretabilidade com SHAP;
- interface interativa com Streamlit.

---

# 🛰️ Tecnologias Utilizadas

## Dados Orbitais

- NASA POWER API

## Machine Learning

- XGBoost
- Random Forest
- SHAP

## Desenvolvimento

- Python
- Pandas
- Scikit-Learn
- Streamlit
- Requests
- Joblib
- Matplotlib
- Seaborn

---

# 📡 Fonte dos Dados

Os dados utilizados no projeto são provenientes da NASA POWER API.

## Variáveis Climáticas Utilizadas

| Variável          | Descrição           |
| ----------------- | ------------------- |
| PRECTOTCORR       | Precipitação        |
| T2M               | Temperatura média   |
| RH2M              | Umidade relativa    |
| WS2M              | Velocidade do vento |
| ALLSKY_SFC_SW_DWN | Radiação solar      |

---

# 🧠 Pipeline do Projeto

O projeto foi dividido nas seguintes etapas:

## 1. Coleta de Dados

Consulta dinâmica à NASA POWER API utilizando múltiplas cidades brasileiras.

---

## 2. Tratamento de Dados

- remoção de inconsistências;
- validação de tipos;
- análise exploratória;
- verificação de valores nulos.

---

## 3. Engenharia de Atributos

Criação de variáveis derivadas para melhorar a capacidade preditiva do modelo.

### Features Criadas

| Feature        | Descrição                      |
| -------------- | ------------------------------ |
| rain_intensity | Intensidade da chuva           |
| storm_index    | Índice de tempestade           |
| heat_index     | Índice térmico                 |
| extreme_rain   | Identificação de chuva extrema |

---

## 4. Machine Learning

Modelos treinados:

- Random Forest
- XGBoost

---

## 5. Avaliação dos Modelos

Métricas utilizadas:

- Accuracy
- Precision
- Recall
- F1-Score
- Matriz de Confusão

---

## 6. Interpretabilidade

Aplicação de SHAP para explicar as decisões dos modelos de IA.

---

## 7. Deploy

Aplicação interativa desenvolvida utilizando Streamlit.

---

# 📊 Dataset

O dataset foi construído utilizando dados de múltiplas cidades brasileiras:

- São Paulo
- Rio de Janeiro
- Curitiba
- Florianópolis
- Porto Alegre
- Belo Horizonte

## Informações do Dataset

- mais de 2000 registros;
- múltiplas variáveis climáticas;
- dados orbitais reais;
- features derivadas;
- classificação de risco climático.

---

# 🤖 Modelo Final

Após comparação entre os modelos Random Forest e XGBoost, o modelo XGBoost foi escolhido como modelo final do projeto devido à sua:

- maior capacidade preditiva;
- melhor captura de relações não lineares;
- melhor aproveitamento das features derivadas;
- maior sensibilidade a eventos climáticos extremos.

---

# 📈 SHAP

O SHAP foi utilizado para interpretar as previsões realizadas pelo modelo.

## Variáveis Mais Importantes

1. PRECTOTCORR
2. rain_intensity
3. RH2M
4. storm_index

Os resultados demonstraram que a precipitação e a intensidade climática são os principais fatores relacionados à previsão de risco climático.

---

# 🌐 Streamlit

A aplicação permite que o usuário:

- selecione uma cidade;
- escolha uma data;
- consulte dados orbitais reais da NASA;
- visualize métricas climáticas;
- obtenha previsões de risco climático em tempo real.

---

# 🛰️ Consulta Orbital em Tempo Real

O sistema realiza requisições diretamente à NASA POWER API, tornando o Sentinel SOS uma solução conectada ao contexto da Economia Espacial.

Fluxo da aplicação:

```text
Usuário → Streamlit → NASA POWER API → Feature Engineering → XGBoost → Previsão
```

---

# 📂 Estrutura do Projeto

```bash
SentinelSOS/

├── app.py
├── sentinel_sos_xgboost.pkl
├── sentinel_sos_features.csv
├── sentinel_sos_raw.csv
├── requirements.txt
├── README.md
├── notebooks/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
└── images/
```

---

# ⚙️ Como Executar Localmente

## 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/SentinelSOS.git
```

---

## 2. Acesse a pasta do projeto

```bash
cd SentinelSOS
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Execute o Streamlit

```bash
streamlit run app.py
```

---

# 📦 Requirements

```txt
streamlit
pandas
requests
scikit-learn
xgboost
joblib
shap
matplotlib
seaborn
```

---

# 📸 Funcionalidades da Aplicação

✅ Consulta dinâmica à NASA POWER API

✅ Dados orbitais em tempo real

✅ Feature Engineering automática

✅ Classificação de risco climático

✅ Visualização das probabilidades da IA

✅ Explicabilidade com SHAP

✅ Interface interativa com Streamlit

---

# 🌎 Economia Espacial

O Sentinel SOS se conecta diretamente ao conceito de Economia Espacial ao utilizar dados provenientes de satélites da NASA para solucionar problemas reais relacionados à prevenção de desastres naturais na Terra.

O projeto demonstra como tecnologias espaciais podem ser aplicadas em sistemas inteligentes de monitoramento climático e apoio à tomada de decisão.

---

# 👩‍💻 Autora

**Leticia Resina**

---

# 📅 Última Atualização

27 de Maio de 2026

---

# 📌 Observações Sobre o Deploy

O projeto foi desenvolvido inicialmente utilizando:

- Google Colab
- Streamlit
- ngrok

⚠️ Links gerados pelo ngrok são temporários e mudam a cada nova execução do notebook.

---

# 🔗 Exemplo de Deploy Temporário

```txt
https://nintendo-headpiece-conflict.ngrok-free.dev
```

---

# 🚀 Sugestões de Deploy Permanente

Para disponibilização permanente da aplicação, recomenda-se:

- Streamlit Community Cloud
- Render
- Hugging Face Spaces

---

# 📚 Referências

- NASA POWER API
- Scikit-Learn Documentation
- XGBoost Documentation
- SHAP Documentation
- Streamlit Documentation

---

# 📌 Projeto Acadêmico

Projeto desenvolvido para a disciplina de Global Solution com foco em Economia Espacial, Inteligência Artificial e Engenharia de Software.
