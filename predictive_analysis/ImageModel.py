from keras import Sequential
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np
from keras.api.preprocessing import image
import tensorflow as tf

class ImageClassifier:
    def __init__(self, img_height=300, img_width=300, batch_size=2, train_data_dir='./data', epochs=100):
        self.img_height = img_height
        self.img_width = img_width
        self.batch_size = batch_size
        self.train_data_dir = train_data_dir
        self.epochs = epochs
        self.model = None
        self.train_dataset = None
        self.validation_dataset = None
        self.train_generator = None
        self.validation_generator = None
        self._prepare_data()
        self._build_model()

    def _prepare_data(self):
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.1
        )

        self.train_generator = train_datagen.flow_from_directory(
            self.train_data_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )

        self.validation_generator = train_datagen.flow_from_directory(
            self.train_data_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )

        # Convert to tf.data.Dataset
        self.train_dataset = tf.data.Dataset.from_generator(
            lambda: self.train_generator,
            output_signature=(
                tf.TensorSpec(shape=(None, self.img_height, self.img_width, 3), dtype=tf.float32),
                tf.TensorSpec(shape=(None, self.train_generator.num_classes), dtype=tf.float32)
            )
        ).repeat()

        self.validation_dataset = tf.data.Dataset.from_generator(
            lambda: self.validation_generator,
            output_signature=(
                tf.TensorSpec(shape=(None, self.img_height, self.img_width, 3), dtype=tf.float32),
                tf.TensorSpec(shape=(None, self.validation_generator.num_classes), dtype=tf.float32)
            )
        ).repeat()

    def _build_model(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(self.train_generator.num_classes, activation='softmax')
        ])

        self.model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.summary()

    def train(self):
        self.model.fit(
            self.train_dataset,
            steps_per_epoch=self.train_generator.samples // self.batch_size,
            validation_data=self.validation_dataset,
            validation_steps=self.validation_generator.samples // self.batch_size,
            epochs=self.epochs
        )

    def evaluate(self):
        loss, accuracy = self.model.evaluate(self.validation_dataset, steps=self.validation_generator.samples // self.batch_size)
        print(f'Validation Accuracy: {accuracy:.4f}')
        return accuracy

    def predict_image(self, img_path):
        img = image.load_img(img_path, target_size=(self.img_height, self.img_width))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        predictions = self.model.predict(img_array)[0]
        top_indices = predictions.argsort()[-3:][::-1]
        class_labels = list(self.train_generator.class_indices.keys())
        top_predictions = [(class_labels[i], predictions[i]) for i in top_indices]
        return top_predictions

if __name__ == '__main__':
    classifier = ImageClassifier(epochs=10)
    classifier.train()
    classifier.evaluate()
    predictions = classifier.predict_image('./data/supraventricular_tachycardia/madalina_puia.png')
    print(predictions)