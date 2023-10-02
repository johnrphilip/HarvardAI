import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images=[]
    labels=[]

    # iterating over categories
    for category in range(NUM_CATEGORIES):
        category_dir = os.path.join(data_dir, str(category))

        #iterate over images in the category directory
        for filename in os.listdir(category_dir):
            if filename.endswith(".ppm"):
                img = cv2.imread(os.path.join(category_dir, filename))

                # resivze the image and append it to image list
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                images.append(img)

                # append the category label to labels list
                labels.append(category)
    return images, labels



def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # this required a lot of fiddling to get good results

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(  # linear 2D layer model
            # canning the input image 3x3 dimensions as specified and 32 filters.
            # Uses ReLU rectified linear unit activation function* I tried a few different activations  for different layers to test for effectiveness and help with vanishing gradient problem
            # Swish and ELu(terrible) at first but relu with softmax worked best
            32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)

        ),
        # pooling layer 2x2
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        #flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with a dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # output layer for all categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # compiling
    model.compile(
        # I played around with a few optimizers until I found one that worked well. These seemed to have the greatest impact on my results. 
        optimizer="RMSprop",
        # I tried a few loss function but this one seemed to work best
        loss="categorical_crossentropy",
        # focused on accuracy at first then played around with additional metrics
        metrics=["accuracy", "Precision", "Recall", tf.keras.metrics.AUC(name='auc')]
    )

    return model


if __name__ == "__main__":
    main()


# python3 traffic.py /Users/jp/Documents/EdX/traffic/gtsrb
    """
    1: RMS prop: loss: 2.2914 - accuracy: 0.3853 - precision: 0.9327 - recall: 0.2954 - auc: 0.8991
    2: Nadam: loss: 0.4782 - accuracy: 0.8690 - 640ms/epoch
    3: SGD: loss: 3.4923 - accuracy: 0.0581 - 679ms/epoch

    
    RMS prop worked well. It maintaions a moving discounted average of the square of the gradients and divides the learning rate by the square root of this average
    """