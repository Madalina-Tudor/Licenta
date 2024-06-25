from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS

import DataFetchModule
import ImageModel
from ClusteringModule import HeartEventClusterer
from ModelGRU import EventPredictionModel

app = Flask(__name__)
CORS(app)


# Initialize the predictor


@app.route('/predict', methods=['POST'])
def predict():
    model = EventPredictionModel()
    data = request.json
    input_array = data['input']
    epochs = data['epochs']

    model.train_model(epochs=epochs)
    model.evaluate_model()

    try:
        # Ensure the input array is correctly shaped
        if len(input_array) != 26:
            raise ValueError("Input array must contain exactly 26 elements.")

        input_array = np.tile(input_array, 5).reshape((5, -1))  # Ensure input matches the window size
        predicted_event, probability, predicted_date = model.make_predictions(input_array)
        return jsonify({
            'predicted_event': str(predicted_event),
            'probability%': str(round(probability * 100, 2)) + '%',
            'predicted_date': predicted_date.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict_img', methods=['POST'])
def predict_img():
    data = request.json
    img_path = data['img_path']
    epochs = int(data['epochs'])

    # Initialize and train the model (this can be moved outside if training is done beforehand)
    img_model = ImageModel.ImageClassifier(epochs=epochs)
    img_model.train()

    # Predict the image
    top_predictions = img_model.predict_image(img_path)
    response = {
        'predictions': [
            {'Event': class_label, 'Probability%': round(probability * 100, 2)}
            for class_label, probability in top_predictions
        ]
    }
    return jsonify(response), 200


@app.get("/clusters")
def get_clusters():
    clusterer = HeartEventClusterer(DataFetchModule.session)
    cluster_info, centers = clusterer.get_cluster_info()
    plot_base64 = clusterer.plot()
    return {"cluster_info": cluster_info, "centers": centers,"cluster_plot": plot_base64}



if __name__ == '__main__':
    app.run(debug=True)
