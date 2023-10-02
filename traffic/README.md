# Traffic Sign Recognition

This project involves the development of an AI model to identify which traffic sign appears in a photograph, utilizing the German Traffic Sign Recognition Benchmark (GTSRB) dataset. The project is implemented in Python, leveraging libraries such as TensorFlow, OpenCV, and scikit-learn.

## Skills Demonstrated
- **Image Processing:** Using OpenCV to load, resize, and preprocess images.
- **Machine Learning:** Employing scikit-learn for splitting data into training and testing sets.
- **Deep Learning:** Designing and training a Convolutional Neural Network (CNN) using TensorFlow.
- **Optimization:** Experimenting with different neural network architectures, optimizers, and loss functions to enhance model performance.

## Application Overview
The application reads images of traffic signs and classifies them into one of the 43 different traffic sign categories. It uses a neural network model trained on the GTSRB dataset, containing thousands of images of different kinds of road signs.

### Features
- Image Loading and Preprocessing
- Neural Network Model Training and Evaluation
- Model Optimization and Experimentation

## Experimentation and Observations
During the development of this project, extensive experimentation was conducted with different neural network architectures, activation functions, optimizers, and loss functions. The following observations were made:
- The RMSprop optimizer, coupled with the categorical cross-entropy loss function, yielded the best results.
- The ReLU activation function was found to be the most effective for the hidden layers, while the softmax activation function was used for the output layer.
- Experimentation with different metrics such as precision, recall, and AUC provided deeper insights into model performance.

## Getting Started
To run the project, follow the instructions below:

### Prerequisites
- Python 3.10
- Required Python libraries: `cv2`, `numpy`, `tensorflow`, `sklearn`
- You will also need the German Traffic Sign Recognition Benchmark (GTSRB) dataset

## Results of RMSprop optimizer:

Epoch 1/10
500/500 [==============================] - 3s 6ms/step - loss: 6.4174 - accuracy: 0.0532 - precision: 0.0260 - recall: 5.0050e-04 - auc: 0.6369
Epoch 2/10
500/500 [==============================] - 3s 6ms/step - loss: 3.5903 - accuracy: 0.0664 - precision: 0.8073 - recall: 0.0097 - auc: 0.6987    
Epoch 3/10
500/500 [==============================] - 3s 6ms/step - loss: 3.5131 - accuracy: 0.0848 - precision: 0.8296 - recall: 0.0253 - auc: 0.7131
Epoch 4/10
500/500 [==============================] - 3s 6ms/step - loss: 3.3606 - accuracy: 0.1342 - precision: 0.8473 - recall: 0.0656 - auc: 0.7406
Epoch 5/10
500/500 [==============================] - 3s 6ms/step - loss: 3.1965 - accuracy: 0.1844 - precision: 0.8409 - recall: 0.1114 - auc: 0.7701
Epoch 6/10
500/500 [==============================] - 3s 6ms/step - loss: 2.9875 - accuracy: 0.2255 - precision: 0.8539 - recall: 0.1587 - auc: 0.7980
Epoch 7/10
500/500 [==============================] - 3s 6ms/step - loss: 2.9009 - accuracy: 0.2489 - precision: 0.8581 - recall: 0.1809 - auc: 0.8135
Epoch 8/10
500/500 [==============================] - 3s 6ms/step - loss: 2.8316 - accuracy: 0.2624 - precision: 0.8831 - recall: 0.1975 - auc: 0.8236
Epoch 9/10
500/500 [==============================] - 3s 6ms/step - loss: 2.7701 - accuracy: 0.2725 - precision: 0.8999 - recall: 0.2087 - auc: 0.8306
Epoch 10/10
500/500 [==============================] - 3s 6ms/step - loss: 2.7311 - accuracy: 0.2799 - precision: 0.9038 - recall: 0.2123 - auc: 0.8387
333/333 - 1s - loss: 2.2914 - accuracy: 0.3853 - precision: 0.9327 - recall: 0.2954 - auc: 0.8991 - 829ms/epoch - 2ms/step
