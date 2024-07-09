### MagicMathNotebook

**MagicMathNotebook** is an application designed to solve mathematical problems drawn by users. The application allows users to draw mathematical tasks, and it automatically solves them using a neural network. The project utilizes deep learning techniques for digit and symbol recognition, making it an interactive tool for learning and practicing math.

#### Project Files:

1. **digit_recognizer.py**:
   This Python script defines the neural network model used for recognizing digits and mathematical symbols. The `DigitRecognizer` class inherits from `nn.Module` and includes convolutional layers, max-pooling layers, fully connected layers, and dropout for regularization. It also includes methods for forward propagation, probability to prediction conversion, and prediction to class conversion.

2. **Train.ipynb**:
   This Jupyter notebook is used to train the neural network model defined in `digit_recognizer.py`. It loads the dataset, applies necessary transformations, splits the data into training and testing sets, and trains the model using a specified loss function and optimizer. The training process includes logging the training and validation losses and accuracies for each epoch.

3. **paint.py**:
   This Python script provides the GUI for the MagicMathNotebook application. It uses `tkinter` for the graphical interface, allowing users to draw mathematical problems on a canvas. The script captures the drawings, processes them into images, and uses the trained neural network model to recognize the symbols. The recognized symbols are then used to form a mathematical expression, which is evaluated to provide the solution. The script includes classes for handling bounding boxes, lines, exercises, and the drawing application itself.

### How It Works:

- **Drawing and Recognition**: Users draw mathematical expressions on a canvas. The application captures the strokes and processes them into images.
- **Symbol Detection**: The images are fed into the neural network, which recognizes the digits and symbols.
- **Expression Evaluation**: The recognized symbols are combined to form a mathematical expression, which is then evaluated to provide the solution.
- **User Interaction**: The application displays the current task and the solved expression, providing an interactive and educational experience.

#### Key Enhancements

- **Regularization:** Adding regularization techniques significantly improved the performance of the `DigitRecognizer` model. Regularization helped in preventing overfitting and improving generalization on unseen data.

- **Line Thickness Adjustment:** Initially, symbols in the dataset were drawn with thin lines. Testing with symbols drawn using similarly thin lines yielded poor recognition results on real data. To address this, the drawing application was adjusted to use thicker lines, despite the training data remaining unchanged with thin lines. This adjustment markedly enhanced recognition accuracy.

These optimizations collectively enhance the usability and accuracy of the MagicMathNotebook application, making it a robust tool for interactive mathematical problem-solving.

The following video showcases the system in action

https://github.com/osipgas/MagicMathNotebook/assets/115102730/4e02fe89-b27f-433f-91ad-2d3780e4bcf0

