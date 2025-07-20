from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras.optimizers import Adam

IMG_SIZE = 256  # same as preprocessing

def build_model():
    """
    Builds and compiles CNN model the binary classification.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(2, 2),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax') #  changed it to 2 outputs and softmax
    ])

    model.compile(optimizer=Adam(learning_rate = 1e-4), loss='categorical_crossentropy', metrics=['accuracy', 'precision']) # changed loss to 'categorical_crossentropy'
    return model
