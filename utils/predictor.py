# utils/predictor.py

import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class StockPredictor:
    """Clase para predicción con modelo TCN entrenado (lookback=30)"""
    
    def __init__(self, model_path='models/tcn_best.h5', 
                 feature_scaler_path='models/feature_scaler.pkl',
                 target_scaler_path='models/target_scaler.pkl',
                 lookback=30):
        """
        Inicializa el predictor
        """
        self.lookback = lookback
        self.feature_cols = [
            'Open', 'High', 'Low', 'Close',
            'SMA_20', 'SMA_50', 'EMA_12',
            'RSI_14', 'MACD', 'MACD_signal'
        ]
        
        print(f"Cargando modelo desde {model_path}...")
        self.model = keras.models.load_model(
            model_path,
            custom_objects={
                'mse': tf.keras.losses.MeanSquaredError(),
                'mae': tf.keras.metrics.MeanAbsoluteError()
            }
        )
        print("Modelo cargado")
        
        # Cargar scalers
        try:
            with open(feature_scaler_path, 'rb') as f:
                self.feature_scaler = pickle.load(f)
            with open(target_scaler_path, 'rb') as f:
                self.target_scaler = pickle.load(f)
            print("Scalers cargados")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Scaler no encontrado: {e}")

    def add_technical_indicators(self, df):
        """
        Agrega indicadores técnicos (sin dropna global)
        """
        df = df.copy()
        
        # Verificar mínimo de datos
        min_required = 60  # 50 para SMA_50 + margen
        if len(df) < min_required:
            raise ValueError(f"Se necesitan al menos {min_required} días para calcular indicadores")

        close = df['Close']

        # Indicadores
        df['SMA_20'] = SMAIndicator(close, window=20).sma_indicator()
        df['SMA_50'] = SMAIndicator(close, window=50).sma_indicator()
        df['EMA_12'] = EMAIndicator(close, window=12).ema_indicator()
        df['RSI_14'] = RSIIndicator(close, window=14).rsi()
        
        macd = MACD(close)
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()

        return df  # NO hacer dropna() aquí

    def prepare_initial_sequence(self, df):
        """
        Prepara la secuencia inicial válida (últimos lookback días sin NaN)
        """
        # Añadir indicadores
        df_with_features = self.add_technical_indicators(df)
        
        # Tomar últimos lookback + buffer para NaN
        window = df_with_features[self.feature_cols].tail(self.lookback + 50)
        
        # Eliminar filas con NaN
        window_clean = window.dropna()
        
        if len(window_clean) < self.lookback:
            raise ValueError(f"No hay {self.lookback} días válidos después de indicadores. "
                           f"Disponibles: {len(window_clean)}")
        
        # Tomar últimos lookback días válidos
        sequence = window_clean[self.feature_cols].tail(self.lookback).values
        return sequence.astype(np.float32)

    def predict(self, df, horizon=5):
        """
        Predicción iterativa SIN recalcular indicadores en bucle
        """
        try:
            # 1. Preparar secuencia inicial
            sequence = self.prepare_initial_sequence(df)  # shape: (lookback, n_features)
            
            predictions = []
            
            for _ in range(horizon):
                # Normalizar
                X_scaled = self.feature_scaler.transform(sequence)
                X = X_scaled.reshape(1, self.lookback, len(self.feature_cols))
                
                # Predecir
                pred_normalized = self.model.predict(X, verbose=0)[0][0]
                pred_price = self.target_scaler.inverse_transform([[pred_normalized]])[0][0]
                predictions.append(pred_price)
                
                # Actualizar secuencia (shift + nueva fila)
                new_row = sequence[-1].copy()
                new_row[3] = pred_price   # Close
                new_row[0] = pred_price   # Open
                new_row[1] = pred_price * 1.01  # High
                new_row[2] = pred_price * 0.99  # Low
                
                # Shift: eliminar primera fila, añadir nueva
                sequence = np.vstack([sequence[1:], new_row])
            
            return np.array(predictions)
            
        except Exception as e:
            print(f"Error en predicción: {e}")
            import traceback
            traceback.print_exc()
            return None

    def predict_single(self, df):
        """Predicción de un solo día"""
        preds = self.predict(df, horizon=1)
        return preds[0] if preds is not None else None