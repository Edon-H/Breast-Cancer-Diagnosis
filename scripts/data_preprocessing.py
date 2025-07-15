import os
from tqdm import tqdm
from tensorflow.keras.utils import to_categorical
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

def load_Preprcess_data(loading_method, image_size=(256, 256), max_images_per_class=None, augment=True):
    """
    Loads and preprocesses a breast cancer histopathology image dataset for CNN models.

    The function:
        - loads images from disk
        - converts them to RGB
        - resizes them to a fixed shape
        - normalizes pixel values
        - one-hot encodes class labels
        - shuffles data
        - splits into training, validation, and test sets
        - optionally applies data augmentation

    Parameters
    ----------
    loading_method : str
        Either 'colab' or 'direct'. Determines dataset path depending on environment.
    image_size : tuple of int
        Target image size as (height, width) for resizing all images.
    max_images_per_class : int or None
        Maximum number of images to load per class. Useful for limiting dataset size during testing.
        If None, loads all images.
    augment : bool
        If True, applies data augmentation to training images.

    Returns
    -------
    X_train : np.ndarray
        Training images of shape (N, H, W, 3).
    y_train : np.ndarray
        One-hot encoded training labels of shape (N, num_classes).
    X_val : np.ndarray
        Validation images.
    y_val : np.ndarray
        One-hot encoded validation labels.
    X_test : np.ndarray
        Test images.
    y_test : np.ndarray
        One-hot encoded test labels.
    num_classes : int
        Number of distinct classes in the dataset.
    """

    # Select path to dataset depending on running environment
    if loading_method == 'colab':
        # Path for Google Colab
        data_path = "/content/drive/MyDrive/breast_project/breast_cancer_dataset"
    elif loading_method == 'direct':
        # Local or direct path
        data_path = "raw_data/breast_cancer/BreaKHis_Total_dataset"
    else:
        raise ValueError("loading_method must be either 'colab' or 'direct'.")

    imgs = []    # to store image arrays
    labels = []  # to store corresponding class labels

    # Dictionary mapping class names to numeric labels
    classes = {'benign': 0, 'malignant': 1}

    # Loop through each class (benign or malignant)
    for cl, label in classes.items():
        class_dir = os.path.join(data_path, cl)

        # List all image filenames in the class directory
        images_path = [
            f for f in os.listdir(class_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

        # If max_images_per_class is set, limit how many images to load
        if max_images_per_class:
            images_path = images_path[:max_images_per_class]

        # Iterate over each image file in this class
        for img_name in tqdm(images_path, desc=f"Loading {cl} images"):
            img_path = os.path.join(class_dir, img_name)

            if os.path.exists(img_path):
                try:
                    # Open the image and ensure it's in RGB
                    image = Image.open(img_path).convert('RGB')

                    # Resize to desired dimensions
                    image = image.resize(image_size)

                    # Convert image to NumPy array and scale pixel values to [0,1]
                    imgs.append(np.array(image) / 255.0)

                    # Save the class label
                    labels.append(label)

                except Exception as e:
                    # Catch and print errors for problematic files, so loading doesn't fail
                    print(f"Could not process image {img_path}: {e}")

    # Convert lists into NumPy arrays for ML processing
    X = np.array(imgs, dtype=np.float32)   # Shape → (N, H, W, 3)
    y = np.array(labels)                   # Shape → (N,)

    # Count number of classes
    num_classes = len(classes)

    # Convert labels from integer → one-hot encoding (e.g. 0 → [1,0])
    y = to_categorical(y, num_classes)

    # Shuffle the entire dataset randomly
    p = np.random.permutation(len(X))
    X, y = X[p], y[p]

    # First, split off ~16.7% of data as test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X,
        y,
        test_size=1/6,                   # i.e. ~16.7% test set
        random_state=42,
        stratify=y                       # maintain class balance
    )

    # Now split the remaining data into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp,
        y_temp,
        test_size=0.2,                    # 20% of remaining data as validation
        random_state=42,
        stratify=np.argmax(y_temp, axis=1)  # stratify using class labels
    )

    # Optionally apply data augmentation on the training set
    if augment:
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal_and_vertical"),
            tf.keras.layers.RandomRotation(0.2),
            tf.keras.layers.RandomZoom(0.1),
        ])

        # Note: we augment the entire training set in memory here
        # For large datasets, you’d instead create a data generator
        X_train = data_augmentation(X_train, training=True)

    return X_train, y_train, X_val, y_val, X_test, y_test, num_classes
