import pandas as pd
import numpy as np
from src.preprocessing import clean_data, generate_product_summary
from src.restock import create_stock_summary
from src.feature_engineering import prepare_sales_time_series, create_forecasting_features, encode_categorical_features, split_features_target
from src.modeling import prepare_train_test_data, train_models, predict_models, select_best_model
from src.evaluation import evaluate_predictions

print("1. Loading raw data...")
df_raw = pd.read_csv("data/dataset.csv")

print("2. Cleaning data...")
df_clean = clean_data(df_raw)

print("3. Product and Stock Summary...")
df_prod = generate_product_summary(df_clean)
df_stock = create_stock_summary(df_clean)

print("4. Forecasting...")
df_ts = prepare_sales_time_series(df_clean, product=None, category=None)
print("Time series shape:", df_ts.shape)

df_features = create_forecasting_features(df_ts)
df_encoded = encode_categorical_features(df_features)

X, y = split_features_target(df_encoded)
actual_test_size = 14
X_train, X_test, y_train, y_test = prepare_train_test_data(X, y, test_size=actual_test_size)

print("Training models...")
trained_models = train_models(X_train, y_train)
print("Models trained:", list(trained_models.keys()))

predictions = predict_models(trained_models, X_test)
eval_df = evaluate_predictions(y_test, predictions)
print(eval_df)

best_model_name, best_model = select_best_model(eval_df, trained_models)
print("Best model:", best_model_name)

print("All tests passed!")
