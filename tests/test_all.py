import sys
import pandas as pd
import numpy as np

try:
    from src.preprocessing import clean_data
    from src.feature_engineering import prepare_sales_time_series, create_forecasting_features, encode_categorical_features, split_features_target
    from src.modeling import train_models, select_best_model
    from src.restock import create_stock_summary, calculate_recommended_restock, determine_restock_priority, generate_restock_reason
    
    print("1. Loading raw data...")
    df = pd.read_csv("data/dataset.csv")
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    
    print("2. Cleaning data...")
    df_clean = clean_data(df)
    
    print("3. Stock Summary...")
    stock_summary = create_stock_summary(df_clean)
    
    print("4. Forecasting...")
    df_ts = prepare_sales_time_series(df_clean)
    df_features = create_forecasting_features(df_ts)
    df_encoded = encode_categorical_features(df_features)
    X, y = split_features_target(df_encoded)
    
    trained_models = train_models(X, y)
    from src.modeling import predict_models
    from src.evaluation import evaluate_predictions
    predictions = predict_models(trained_models, X)
    eval_df = evaluate_predictions(y, predictions)
    best_model_name, best_model = select_best_model(eval_df, trained_models)
    
    print("Best model selected:", best_model_name)
    print("Pipeline executed successfully without errors.")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
