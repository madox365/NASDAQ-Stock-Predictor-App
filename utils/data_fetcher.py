import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='1y', interval='1d'):
    """
    Descarga datos históricos de Yahoo Finance
    
    Args:
        ticker: Símbolo de la acción (ej: 'AAPL')
        period: Período de datos ('1mo', '3mo', '6mo', '1y', '2y', etc.)
        interval: Intervalo ('1d', '1h', etc.)
        
    Returns:
        DataFrame con columnas: Date, Open, High, Low, Close, Volume
    """
    try:
        print(f"Descargando datos de {ticker}...")
        
        # Descargar datos
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            print(f"⚠️  No se encontraron datos para {ticker}")
            return None
        
        # Resetear índice para tener Date como columna
        df = df.reset_index()
        
        # Renombrar columnas si es necesario
        if 'Date' not in df.columns and 'Datetime' in df.columns:
            df = df.rename(columns={'Datetime': 'Date'})
        
        # Seleccionar columnas relevantes
        columns_needed = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df[columns_needed]
        
        # Convertir Date a datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Ordenar por fecha
        df = df.sort_values('Date').reset_index(drop=True)
        
        print(f"✅ Datos descargados: {len(df)} días")
        print(f"   Rango: {df['Date'].min().date()} a {df['Date'].max().date()}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error descargando datos: {e}")
        return None

def get_latest_price(ticker):
    """
    Obtiene el precio más reciente de una acción
    
    Args:
        ticker: Símbolo de la acción
        
    Returns:
        float: Precio más reciente
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except:
        return None

def get_stock_info(ticker):
    """
    Obtiene información general de la acción
    
    Args:
        ticker: Símbolo de la acción
        
    Returns:
        dict: Información de la empresa
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0)
        }
    except:
        return {'name': ticker}

def validate_ticker(ticker):
    """
    Valida si un ticker existe
    
    Args:
        ticker: Símbolo de la acción
        
    Returns:
        bool: True si existe, False si no
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='5d')
        return not data.empty
    except:
        return False