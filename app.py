import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Importar utilidades locales
from utils.predictor import StockPredictor
from utils.data_fetcher import fetch_stock_data
import config

# Configuración de la página
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="📈",
    layout="wide"
)

# Inicializar predictor (se carga una sola vez)
@st.cache_resource
def load_predictor():
    return StockPredictor(
        model_path=config.MODEL_PATH,
        feature_scaler_path=config.FEATURE_SCALER_PATH,
        target_scaler_path=config.TARGET_SCALER_PATH,
        lookback=config.LOOKBACK_WINDOW
    )

def plot_predictions(df, predictions, ticker):
    """Crea gráfico interactivo con Plotly"""
    fig = go.Figure()
    
    # Precio histórico
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        name='Precio Real',
        line=dict(color=config.COLOR_REAL, width=2)
    ))
    
    # Predicciones
    if predictions is not None and len(predictions) > 0:
        pred_dates = pd.date_range(
            start=df['Date'].iloc[-1] + timedelta(days=1),
            periods=len(predictions),
            freq='D'
        )
        
        fig.add_trace(go.Scatter(
            x=pred_dates,
            y=predictions,
            name='Predicción',
            line=dict(color=config.COLOR_PREDICTION, width=2, dash='dash'),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title=f'{ticker} - Precio y Predicción',
        xaxis_title='Fecha',
        yaxis_title='Precio ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def main():
    st.title(config.APP_TITLE)
    st.markdown(f"### {config.APP_SUBTITLE}")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Input del ticker
        ticker = st.text_input(
            "Ticker (ej: AAPL, GOOGL, MSFT)",
            value=config.DEFAULT_TICKER,
            help="Ingresa el símbolo de la acción"
        ).upper()
        
        # Período de datos históricos
        period = st.selectbox(
            "Período histórico",
            options=['6mo', '1y', '2y'],
            index=2,
            help="Cantidad de datos históricos a cargar"
        )
        
        # Horizonte de predicción
        horizon = st.slider(
            "Días a predecir",
            min_value=config.MIN_HORIZON,
            max_value=config.MAX_HORIZON,
            value=config.DEFAULT_HORIZON,
            help="Número de días hacia adelante"
        )
        
        # Botón de predicción
        predict_button = st.button("🚀 Predecir", type="primary", use_container_width=True)
        
        # Info sobre tickers probados
        with st.expander("ℹ️ Tickers probados"):
            st.markdown(f"""
            El modelo fue entrenado con **{len(config.TESTED_TICKERS)} tickers**.
            
            Algunos ejemplos:
            - **Tech**: {', '.join(config.TESTED_TICKERS[:5])}
            - **Healthcare**: ISRG, VRTX, REGN
            - **Consumer**: LULU, ULTA, TSCO
            
            Funciona mejor con estos tickers, pero puede predecir otros.
            """)
    
    # Área principal
    if predict_button:
        with st.spinner(f"Cargando datos de {ticker}..."):
            # Obtener datos
            df = fetch_stock_data(ticker, period=period)
            
            if df is None or len(df) == 0:
                st.error(f"❌ No se pudieron obtener datos para {ticker}")
                return
            
            st.success(f"✅ Datos cargados: {len(df)} días")
        
        with st.spinner("Realizando predicción..."):
            # Cargar predictor
            predictor = load_predictor()
            
            # Hacer predicción
            predictions = predictor.predict(df, horizon=horizon)
            
            if predictions is None:
                st.error("❌ Error en la predicción")
                return
        
        # Mostrar resultados
        st.success("✅ Predicción completada")
        
        # Métricas en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        last_price = df['Close'].iloc[-1]
        pred_price = predictions[-1]
        change = pred_price - last_price
        change_pct = (change / last_price) * 100
        
        col1.metric("Precio Actual", f"${last_price:.2f}")
        col2.metric("Predicción", f"${pred_price:.2f}")
        col3.metric("Cambio", f"${change:.2f}", f"{change_pct:.2f}%")
        col4.metric("Días", f"{horizon}")
        
        # Gráfico
        st.plotly_chart(plot_predictions(df, predictions, ticker), use_container_width=True)
        
        # Tabla de predicciones
        with st.expander("📊 Ver tabla de predicciones"):
            pred_df = pd.DataFrame({
                'Día': range(1, horizon + 1),
                'Fecha Estimada': pd.date_range(
                    start=df['Date'].iloc[-1] + timedelta(days=1),
                    periods=horizon,
                    freq='D'
                ).strftime('%Y-%m-%d'),
                'Precio Predicho': [f"${p:.2f}" for p in predictions]
            })
            st.dataframe(pred_df, use_container_width=True)
        
        # Datos históricos recientes
        with st.expander("📜 Datos históricos recientes"):
            recent = df.tail(10)[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            recent['Date'] = recent['Date'].dt.strftime('%Y-%m-%d')
            st.dataframe(recent, use_container_width=True)
    
    else:
        # Pantalla inicial
        st.info("👈 Selecciona un ticker y presiona **Predecir**")
        
        st.markdown("""
        ### 📋 Instrucciones:
        1. Ingresa el **ticker** de la acción (ej: AAPL, NVDA, MSFT)
        2. Selecciona el **período histórico** (mínimo 3 meses)
        3. Elige cuántos **días predecir** (1-30)
        4. Presiona **🚀 Predecir**
        
        ### 🎯 Características del Modelo:
        - ✅ Modelo **TCN** (Temporal Convolutional Network)
        - ✅ Ventana de contexto: **30 días**
        - ✅ Features: OHLC + SMA, EMA, RSI, MACD
        - ✅ Entrenado con **50 tickers** del NASDAQ
        - ✅ Datos en tiempo real de **Yahoo Finance**
        
        ### 📊 Indicadores Técnicos:
        - SMA (20, 50 días)
        - EMA (12 días)
        - RSI (14 días)
        - MACD + Signal
        """)
        
        # Ejemplo de tickers populares
        st.markdown("### 🔥 Prueba estos tickers:")
        cols = st.columns(3)
        sample_tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'META']
        for i, tick in enumerate(sample_tickers):
            cols[i % 3].button(tick, key=f"btn_{tick}", use_container_width=True)
    
    #Footer
    # === FOOTER: Created by ===
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; color: #888; font-size: 14px;">
            Created by <strong>Madox365</strong> • 
            <a href="https://github.com/madox365/" target="_blank" style="color: #00ff88; text-decoration: none;">GitHub</a> • 
            <a href="https://linkedin.com/in/tu-perfil" target="_blank" style="color: #00ff88; text-decoration: none;">LinkedIn</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()