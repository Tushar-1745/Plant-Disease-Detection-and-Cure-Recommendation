from keras.models import Sequential # type: ignore
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from keras.optimizers import SGD # type: ignore
from keras_preprocessing.image import ImageDataGenerator # type: ignore
import matplotlib.pyplot as plt # type: ignore

def main():
    # Initialize the CNN
    classifier = Sequential()

    # Step 1 - Convolution Layer 
    classifier.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding second convolution layer
    classifier.add(Conv2D(64, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    classifier.add(Flatten())

    # Step 4 - Full Connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(20, activation='softmax'))  # Changed output neurons to 20 for 20 classes

    # Compile the CNN
    classifier.compile(
        optimizer=SGD(learning_rate=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    # Data Augmentation and Preprocessing
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    # Load training data
    training_set = train_datagen.flow_from_directory(
        'E:\\BE_Project\\training_dataset',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical')
    
    # Load testing data
    test_set = test_datagen.flow_from_directory(
        'E:\\BE_Project\\testing_dataset',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical')

    # Train the model
    history = classifier.fit(
        training_set,
        steps_per_epoch=len(training_set),  # Adjusted steps per epoch
        epochs=75,
        # validation_data=test_set,
        # validation_steps=len(test_set)  # Validation steps may not be necessary
    )

    # Evaluate the model
    scores = classifier.evaluate(test_set, verbose=1)
    print("Testing Accuracy: %.2f%%" % (scores[1] * 100))

    scores = classifier.evaluate(training_set, verbose=1)
    print("Training Accuracy: %.2f%%" % (scores[1] * 100))

    # Plot training history
    print(history.history.keys())  # Print keys of history dictionary

    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    plt.plot(history.history['loss'], label='Training Loss')
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Save the trained model
    classifier.save('plant_model.h5')

    return "Training and model saving completed successfully!"

if __name__ == "__main__":
    main()
