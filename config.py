# config.py

import os
import urllib.request

# === RUTAS LOCALES (para tu PC) ===
LOCAL_MODEL_DIR = "models"
LOCAL_MODEL_PATH = f"{LOCAL_MODEL_DIR}/tcn_best.h5"
LOCAL_FEATURE_SCALER = f"{LOCAL_MODEL_DIR}/feature_scaler.pkl"
LOCAL_TARGET_SCALER = f"{LOCAL_MODEL_DIR}/target_scaler.pkl"

# === URLs DE GOOGLE DRIVE (para GitHub / Streamlit Cloud) ===
DRIVE_MODEL_URL = "https://drive.google.com/uc?export=download&id=1Vd5OwEIIoLEF5YuFrWa98Tz6L4hoUVtn"
DRIVE_FEATURE_SCALER_URL = "https://drive.google.com/uc?export=download&id=1fn0X34x1_ngM4IVHNENcF2EY_38Y1Du-"
DRIVE_TARGET_SCALER_URL = "https://drive.google.com/uc?export=download&id=1QKmFi9Sm6esjp9WXbIPg611nmdn-5F0T"

# === FUNCIÓN: Descarga si no existe localmente ===
def ensure_file(local_path, drive_url, filename):
    if os.path.exists(local_path):
        return local_path  # Usa local si existe
    else:
        os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)
        local_file = os.path.join(LOCAL_MODEL_DIR, filename)
        if not os.path.exists(local_file):
            print(f"Descargando {filename} desde Google Drive...")
            try:
                urllib.request.urlretrieve(drive_url, local_file)
                print(f"Descargado: {local_file}")
            except Exception as e:
                raise RuntimeError(f"No se pudo descargar {filename}: {e}")
        return local_file

# === RUTAS FINALES (automáticas) ===
MODEL_PATH = ensure_file(LOCAL_MODEL_PATH, DRIVE_MODEL_URL, "tcn_best.h5")
FEATURE_SCALER_PATH = ensure_file(LOCAL_FEATURE_SCALER, DRIVE_FEATURE_SCALER_URL, "feature_scaler.pkl")
TARGET_SCALER_PATH = ensure_file(LOCAL_TARGET_SCALER, DRIVE_TARGET_SCALER_URL, "target_scaler.pkl")

# === TUS PARÁMETROS ORIGINALES (sin cambios) ===
LOOKBACK_WINDOW = 30
PREDICTION_HORIZON = 1

TECHNICAL_INDICATORS = [
    'SMA_20', 'SMA_50', 'EMA_12',
    'RSI_14', 'MACD', 'MACD_signal'
]

BASE_FEATURES = ['Open', 'High', 'Low', 'Close']
ALL_FEATURES = BASE_FEATURES + TECHNICAL_INDICATORS

TESTED_TICKERS = [
    "NVDA", "AVGO", "KLAC", "LRCX", "AMAT", "TXN", "QCOM", 
    "ADI", "NXPI", "MPWR", "MCHP", "AMD", "SBUX",
    "MSFT", "ADBE", "INTU", "PANW", "CRWD", "ZS", "DDOG", 
    "MDB", "WDAY", "TEAM",
    "AAPL", "GOOGL", "AMZN", "META", "NFLX", "TSLA", 
    "ROKU", "DOCU",
    "ISRG", "VRTX", "REGN", "IDXX", "DXCM", "ALGN", "BMRN",
    "LIN", "CTAS", "ODFL", "POOL", "ROP", "VRSK",
    "LULU", "TSCO", "ULTA", "EXPE", "HON", "PEP"
]

# === UI (sin cambios) ===
APP_TITLE = "NASDAQ - Stock Price Predictor"
APP_SUBTITLE = "Predicción de precios de acciones usando Temporal Convolutional Network"

DEFAULT_TICKER = "AAPL"
DEFAULT_PERIOD = "1y"
DEFAULT_HORIZON = 5

MIN_HORIZON = 1
MAX_HORIZON = 30
MIN_DATA_DAYS = 50

COLOR_REAL = '#3498db'
COLOR_PREDICTION = '#e74c3c'