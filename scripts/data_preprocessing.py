import os
from tqdm import tqdm
from tensorflow.keras.utils import to_categorical
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

def load_Preprcess_data(loading_method, image_size=(128, 128), max_images_per_class =None, target_per_class=10000):
    """
    Loads and preprocesses a breast cancer histopathology image dataset for CNN models.

    The function:
        - Loads all images from benign and malignant folders
        - Resizes and normalizes images
        - Applies augmentation to classes until each has `target_per_class` samples
        - One-hot encodes labels
        - Shuffles and splits into train/val/test sets

    Parameters
    ----------
    loading_method : str
        Either 'colab' or 'direct'.
    image_size : tuple of int
        Target size (H, W) for resizing images.
    max_images_per_class : int or None
        Maximum number of images to load per class. Useful for limiting dataset size during testing.
    target_per_class : int
        Number of images to have per class after augmentation.

    Returns
    -------
    X_train : np.ndarray
    y_train : np.ndarray
    X_val : np.ndarray
    y_val : np.ndarray
    X_test : np.ndarray
    y_test : np.ndarray
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

    # Define augmentation pipeline
    augmenter = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.2),
        tf.keras.layers.Lambda(lambda x: tf.clip_by_value(x + tf.random.uniform([], -0.1, 0.1), 0.0, 1.0)),  # brightness
    ])

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

        original_images = []

        # Iterate over each image file in this class
        for img_name in tqdm(images_path, desc=f"Loading {cl} images"):
            img_path = os.path.join(class_dir, img_name)

            try:
                img = Image.open(img_path).convert('RGB').resize(image_size)
                original_images.append(np.array(img) / 255.0)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")


        # Augment until we reach target_per_class
        current_count = len(original_images)
        augmented_images = []

        if current_count < target_per_class:
            needed = target_per_class - current_count
            print(f"Augmenting {classes}: Need {needed} more images...")

            # Convert to tensor
            base_imgs = tf.convert_to_tensor(original_images)
            base_imgs = tf.image.resize(base_imgs, image_size)

            i = 0
            while len(augmented_images) < needed:
                batch = augmenter(base_imgs, training=True).numpy()
                for idx, img in enumerate(batch):
                    augmented_images.append(img)

                    # Save the augmented image
                    #save_augmented_image(img, class_dir, cl, len(original_images) + len(augmented_images))

                    if len(augmented_images) >= needed:
                        break


        # Combine original and augmented
        total_class_imgs = np.concatenate([original_images, augmented_images], axis=0)
        total_class_labels = np.full((target_per_class,), label)

        imgs.extend(total_class_imgs)
        labels.extend(total_class_labels)

    # Convert to arrays
    X = np.array(imgs, dtype=np.float32)
    y = to_categorical(np.array(labels), num_classes=2)

    # Shuffle
    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]

    # Split
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=1/6, stratify=y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, stratify=np.argmax(y_temp, axis=1), random_state=42)

    return X_train, y_train, X_val, y_val, X_test, y_test, 2

X_train, y_train, X_val, y_val, X_test, y_test, num_classes = load_Preprcess_data('colab')
