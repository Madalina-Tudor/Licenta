import keras
import pandas as pd
from keras import Model
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import GRU, Dense, Input
from sklearn.model_selection import train_test_split
import DataFetchModule
from datetime import datetime


class EventPredictionModel:
    def __init__(self, session=DataFetchModule.session, window_size=5, test_size=0.2, random_state=42):
        self.scaler = MinMaxScaler()
        self.label_encoder = LabelEncoder()
        self.window_size = window_size
        self.test_size = test_size
        self.random_state = random_state

        self.df = DataFetchModule.fetch_data(session)
        self.model = None
        self.history = None
        self.time_scaler = MinMaxScaler()

    def preprocess_data(self):
        numerical_features = ['abnormal_beat_percent', 'af_beat_percent', 'asystole_rr_period_count',
                              'atrial_beat_count', 'atrial_bigeminy_count', 'atrial_permature_beat_count',
                              'atrial_tachycardia_count', 'atrial_trigeminy_count', 'average_heart_rate',
                              'couple_atrial_permature_count', 'couple_ventricular_permature_count',
                              'long_rr_period_count', 'longest_atrial_tachycardia_duration',
                              'longest_ventricular_tachycardia_duration', 'max_heart_rate', 'max_long_rr_period',
                              'min_heart_rate', 'total_duration', 'valid_duration', 'ventricular_beat_count',
                              'ventricular_bigeminy_count', 'ventricular_permature_beat_count',
                              'ventricular_tachycardia_count', 'ventricular_trigeminy_count', 'abnormal_beat_count',
                              'beat_count']
        self.df[numerical_features] = self.scaler.fit_transform(self.df[numerical_features])
        self.df['event_name'] = self.label_encoder.fit_transform(self.df['event_name'])
        self.df['event_time'] = pd.to_datetime(self.df['event_time'])
        self.df['hour'] = self.df['event_time'].dt.hour
        self.df['minute'] = self.df['event_time'].dt.minute
        self.df['day'] = self.df['event_time'].dt.day
        self.df['month'] = self.df['event_time'].dt.month
        self.df['year'] = self.df['event_time'].dt.year

        # Normalize time components
        time_components = self.df[['hour', 'minute', 'day', 'month', 'year']]
        self.time_scaler.fit(time_components)
        self.df[['hour', 'minute', 'day', 'month', 'year']] = self.time_scaler.transform(time_components)
        self.df.drop('event_time', axis=1, inplace=True)

    def create_sequences(self, data, target):
        sequences = []
        labels = []
        for i in range(len(data) - self.window_size):
            sequences.append(data.iloc[i:(i + self.window_size)].values)
            labels.append(target.iloc[i + self.window_size])
        return np.array(sequences), np.array(labels)

    def prepare_data(self):
        self.preprocess_data()
        x, y = self.create_sequences(self.df.drop(['event_name', 'hour', 'minute', 'day', 'month', 'year'], axis=1),
                                     self.df[['event_name', 'hour', 'minute', 'day', 'month', 'year']])
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=self.test_size,
                                                                                random_state=self.random_state)

    def build_model(self):
        input_layer = Input(shape=(self.x_train.shape[1], self.x_train.shape[2]))
        gru_layer = GRU(128)(input_layer)
        dense1 = Dense(64, activation='relu')(gru_layer)
        dense2 = Dense(64, activation='relu')(dense1)
        dense3 = Dense(64, activation='relu')(dense2)

        event_output = Dense(len(set(self.y_train[:, 0])), activation='softmax', name='event_output')(dense3)
        time_output = Dense(5, activation='linear', name='time_output')(dense3)

        self.model = Model(inputs=input_layer, outputs=[event_output, time_output])
        self.model.compile(optimizer='adam',
                           loss={'event_output': 'sparse_categorical_crossentropy', 'time_output': 'mse'},
                           metrics={'event_output': 'accuracy'})

    def train_model(self, epochs=2, batch_size=32, validation_split=0.2):
        self.prepare_data()
        self.build_model()
        self.history = self.model.fit(self.x_train,
                                      {'event_output': self.y_train[:, 0], 'time_output': self.y_train[:, 1:]},
                                      epochs=epochs, batch_size=batch_size, validation_split=validation_split)

    def evaluate_model(self):
        results = self.model.evaluate(self.x_test,
                                      {'event_output': self.y_test[:, 0], 'time_output': self.y_test[:, 1:]})
        print("Evaluation results:", results)
        test_accuracy = results[1]  # Adjust this index based on the printed structure
        print(f"Test Accuracy: {test_accuracy:.4f}")

    def denormalize_time(self, normalized_time):
        # Reshape for the scaler
        normalized_time = normalized_time.reshape(1, -1)
        denormalized_time = self.time_scaler.inverse_transform(normalized_time)
        return denormalized_time.flatten()

    def make_predictions(self, input):
        input = np.array(input)
        input = input.reshape((1, self.window_size, -1))
        predictions = self.model.predict(input)
        event_probabilities = predictions[0]
        time_predictions = predictions[1]
        predicted_event = np.argmax(event_probabilities, axis=1)
        predicted_event_name = self.label_encoder.inverse_transform(predicted_event)
        denormalized_time = self.denormalize_time(time_predictions[0])

        year = int(denormalized_time[4])
        month = max(1, min(12, int(denormalized_time[3])))
        day = max(1, min(31, int(denormalized_time[2])))
        hour = max(0, min(23, int(denormalized_time[0])))
        minute = max(0, min(59, int(denormalized_time[1])))

        predicted_date = datetime(year + 1 if year < 2024 else year, month + 1 if month <= 6 and year==2024 else month, day, hour, minute)

        return predicted_event_name[0], np.max(event_probabilities, axis=1)[0], predicted_date


# Usage example
if __name__ == '__main__':
    input = [0.0, 0.0, 0, 4, 0, 4, 0, 0, 71.0, 0, 0, 0, 0.0, 0.0, 131.0, 0.0, 50.0, 24780.0, 24780.0, 4, 0, 4, 0, 0, 8,
             29482]
    input = np.tile(input, 5).reshape((5, -1))  # Ensure input matches the window size
    model = EventPredictionModel()
    model.train_model(epochs=1)
    model.evaluate_model()
    event, probability, predicted_date = model.make_predictions(input)
    print(f"Predicted Event: {event}, Probability: {round(probability * 100,2)}%, Predicted Date: {predicted_date}")
