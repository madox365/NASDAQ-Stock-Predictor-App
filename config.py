# Configuración de la aplicación
# Debe coincidir con config.yaml del entrenamiento

# Modelo
MODEL_PATH = 'models/tcn_best.h5'
FEATURE_SCALER_PATH = 'models/feature_scaler.pkl'
TARGET_SCALER_PATH = 'models/target_scaler.pkl'

# Parámetros del modelo (deben coincidir con config.yaml)
LOOKBACK_WINDOW = 30  # De config.yaml: features.lookback_window
PREDICTION_HORIZON = 1  # De config.yaml: features.prediction_horizon

# Features técnicos (deben coincidir EXACTAMENTE con config.yaml)
TECHNICAL_INDICATORS = [
    'SMA_20',
    'SMA_50',
    'EMA_12',
    'RSI_14',
    'MACD',
    'MACD_signal'  # MACD genera 2 columnas: MACD y MACD_signal
]

# Features base
BASE_FEATURES = ['Open', 'High', 'Low', 'Close']

# Todas las features en orden
ALL_FEATURES = BASE_FEATURES + TECHNICAL_INDICATORS

# Tickers probados en entrenamiento (los 50 de config.yaml)
TESTED_TICKERS = [
    # Tech - Semiconductors
    "NVDA", "AVGO", "KLAC", "LRCX", "AMAT", "TXN", "QCOM", 
    "ADI", "NXPI", "MPWR", "MCHP", "AMD", "SBUX",
    
    # Tech - Software & Cloud
    "MSFT", "ADBE", "INTU", "PANW", "CRWD", "ZS", "DDOG", 
    "MDB", "WDAY", "TEAM",
    
    # Tech - Consumer & Platforms
    "AAPL", "GOOGL", "AMZN", "META", "NFLX", "TSLA", 
    "ROKU", "DOCU",
    
    # Healthcare & Biotech
    "ISRG", "VRTX", "REGN", "IDXX", "DXCM", "ALGN", "BMRN",
    
    # Industrial & Services
    "LIN", "CTAS", "ODFL", "POOL", "ROP", "VRSK",
    
    # Consumer Discretionary
    "LULU", "TSCO", "ULTA", "EXPE", "HON", "PEP"
]

# Configuración de la UI
APP_TITLE = "📈NASDAQ - Stock Price Predictor"
APP_SUBTITLE = "Predicción de precios de acciones usando Temporal Convolutional Network"

# Valores por defecto para la UI
DEFAULT_TICKER = "AAPL"
DEFAULT_PERIOD = "1y"
DEFAULT_HORIZON = 5

# Límites
MIN_HORIZON = 1
MAX_HORIZON = 30
MIN_DATA_DAYS = 50  # Necesitamos más que lookback por los indicadores (SMA_50)

# Colores para gráficos
COLOR_REAL = '#3498db'
COLOR_PREDICTION = '#e74c3c'