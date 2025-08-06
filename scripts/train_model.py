from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

# Constants
IMG_SIZE = 128
LEARNING_RATE = 0.00001

def build_vgg16_model_unfreeze_2(img_size=IMG_SIZE, learning_rate=LEARNING_RATE):
    base_model = VGG16(
        include_top=False,
        weights='imagenet',
        input_tensor=Input(shape=(img_size, img_size, 3))
    )

    # Freeze all layers, then unfreeze block5
    for layer in base_model.layers:
        layer.trainable = False
    for layer in base_model.layers:
        if 'block5' in layer.name:
            layer.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.2)(x)
    output = Dense(2, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy', Precision(name="precision"), Recall(name='recall')]
    )
    return model

def train_model(X_train, y_train, X_val, y_val, output_path="best_model.keras"):
    model = build_vgg16_model_unfreeze_2()

    callbacks = [
        ModelCheckpoint(output_path, save_best_only=True, monitor='val_loss', mode='min'),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, verbose=1),
        EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)
    ]

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=32,
        callbacks=callbacks
    )

    return model, history
