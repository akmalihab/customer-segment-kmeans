import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Model paths
MODELS_DIR = PROJECT_ROOT / 'models'

# Output paths
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'

# File paths
MALL_CUSTOMERS_CSV = RAW_DATA_DIR / 'Mall_Customers.csv'
CUSTOMER_SEGMENTS_CSV = PROCESSED_DATA_DIR / 'customer_segments.csv'

KMEANS_MODEL_PKL = MODELS_DIR / 'kmeans_model.pkl'
SCALER_PKL = MODELS_DIR / 'scaler.pkl'
LABEL_ENCODER_PKL = MODELS_DIR / 'label_encoder.pkl'

# Visualization outputs
EDA_VISUALIZATION_PNG = OUTPUTS_DIR / 'eda_visualization.png'
CORRELATION_HEATMAP_PNG = OUTPUTS_DIR / 'correlation_heatmap.png'
ELBOW_SILHOUETTE_PNG = OUTPUTS_DIR / 'elbow_silhouette.png'
CLUSTER_VISUALIZATION_PNG = OUTPUTS_DIR / 'cluster_visualization.png'
CLUSTER_3D_PNG = OUTPUTS_DIR / 'cluster_3d.png'
