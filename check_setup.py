"""
Script para verificar que todo está configurado correctamente
antes de ejecutar la aplicación.

Uso: python check_setup.py
"""

import os
import sys

def check_file_exists(path, description):
    """Verifica si un archivo existe"""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} NO encontrado: {path}")
        return False

def check_directory_exists(path, description):
    """Verifica si un directorio existe"""
    if os.path.isdir(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} NO encontrado: {path}")
        return False

def check_imports():
    """Verifica que las librerías necesarias estén instaladas"""
    print("\n📦 Verificando librerías...\n")
    
    required_packages = {
        'streamlit': 'streamlit',
        'tensorflow': 'tensorflow',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'ta': 'ta (technical analysis)',
        'yfinance': 'yfinance',
        'plotly': 'plotly',
        'sklearn': 'scikit-learn'
    }
    
    all_installed = True
    
    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} NO instalado")
            all_installed = False
    
    return all_installed

def main():
    print("="*70)
    print("VERIFICACIÓN DE CONFIGURACIÓN - Stock Predictor App")
    print("="*70)
    
    all_checks_passed = True
    
    # 1. Verificar estructura de directorios
    print("\n📁 Verificando estructura de directorios...\n")
    
    if not check_directory_exists('models', 'Carpeta models'):
        all_checks_passed = False
        print("   ⚠️  Crea la carpeta: mkdir models")
    
    if not check_directory_exists('utils', 'Carpeta utils'):
        all_checks_passed = False
        print("   ⚠️  Crea la carpeta: mkdir utils")
    
    # 2. Verificar archivos del modelo
    print("\n🤖 Verificando archivos del modelo...\n")
    
    model_files = [
        ('models/tcn_best.h5', 'Modelo TCN'),
        ('models/feature_scaler.pkl', 'Feature Scaler'),
        ('models/target_scaler.pkl', 'Target Scaler')
    ]
    
    for file_path, description in model_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
            print(f"   ⚠️  Copia desde tu proyecto de entrenamiento:")
            print(f"      cp ../NASDAQ_Stock_Prediction_Project/results/models/{os.path.basename(file_path)} {file_path}")
    
    # 3. Verificar archivos de código
    print("\n📝 Verificando archivos de código...\n")
    
    code_files = [
        ('app.py', 'Aplicación principal'),
        ('config.py', 'Configuración'),
        ('utils/predictor.py', 'Predictor'),
        ('utils/data_fetcher.py', 'Data fetcher'),
        ('requirements.txt', 'Requirements')
    ]
    
    for file_path, description in code_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # 4. Verificar librerías
    if not check_imports():
        all_checks_passed = False
        print("\n   ⚠️  Instala las librerías faltantes:")
        print("      pip install -r requirements.txt")
    
    # 5. Resumen final
    print("\n" + "="*70)
    if all_checks_passed:
        print("✅ TODO LISTO - Puedes ejecutar la aplicación")
        print("\nEjecuta: streamlit run app.py")
    else:
        print("❌ HAY ERRORES - Revisa los puntos marcados arriba")
        print("\nPasos sugeridos:")
        print("1. Copia los archivos del modelo desde tu proyecto de entrenamiento")
        print("2. Instala las dependencias: pip install -r requirements.txt")
        print("3. Ejecuta este script nuevamente: python check_setup.py")
    print("="*70)
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)