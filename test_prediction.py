from src.models.predict_model import FitnessTrackerPredictor
import pandas as pd

# Usage Example
acc_path = 'data/raw/MetaMotion/E-squat-heavy_MetaWear_2019-01-15T20.14.03.633_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv'
gyr_path = 'data/raw/MetaMotion/E-squat-heavy_MetaWear_2019-01-15T20.14.03.633_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv'

acc_df = pd.read_csv(acc_path)
gyr_df = pd.read_csv(gyr_path)


model_path = 'models/final_model.pkl'
cluster_model_path = 'models/Clustering_model.pkl'

tracker_predictor = FitnessTrackerPredictor(acc_path, gyr_path, model_path, cluster_model_path)
# data_frame = tracker_predictor.read_data()

print(tracker_predictor.remove_outliers())

# df = tracker_predictor.apply_feature_engineering()



label = tracker_predictor.predict_activity()

print(label)

print(tracker_predictor.count_repetitions(label))