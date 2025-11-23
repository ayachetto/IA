import nn
from backend import PerceptronDataset, RegressionDataset, DigitClassificationDataset


class PerceptronModel(object):
    def __init__(self, dimensions: int) -> None:
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self) -> nn.Parameter:
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x: nn.Constant) -> int:
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        score = self.run(x)
        score_value = nn.as_scalar(score)
        return 1 if score_value >= 0 else -1

    def train(self, dataset: PerceptronDataset) -> None:
        """
        Train the perceptron until convergence.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        all_correct = False
        while not all_correct:
            all_correct = True
            for x, y in dataset.iterate_once(1):
                true_label = nn.as_scalar(y)
                prediction = self.get_prediction(x)
                if prediction != true_label:
                    update_direction = nn.Constant(true_label * x.data)
                    self.w.update(update_direction, 1.0)
                    all_correct = False


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        self.hidden_size = 64

        self.w1 = nn.Parameter(1, self.hidden_size)
        self.b1 = nn.Parameter(1, self.hidden_size)

        self.w2 = nn.Parameter(self.hidden_size, self.hidden_size)
        self.b2 = nn.Parameter(1, self.hidden_size)

        self.w3 = nn.Parameter(self.hidden_size, 1)
        self.b3 = nn.Parameter(1, 1)

        self.parameters = [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3]

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        def affine(inp, weight, bias):
            return nn.AddBias(nn.Linear(inp, weight), bias)

        layer1 = nn.ReLU(affine(x, self.w1, self.b1))
        layer2 = nn.ReLU(affine(layer1, self.w2, self.b2))
        return affine(layer2, self.w3, self.b3)

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        predictions = self.run(x)
        return nn.SquareLoss(predictions, y)

    def train(self, dataset: RegressionDataset) -> None:
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        batch_size = 20
        learning_rate = 0.05
        target_loss = 0.02
        max_epochs = 2000

        for _ in range(max_epochs):
            for x_batch, y_batch in dataset.iterate_once(batch_size):
                loss = self.get_loss(x_batch, y_batch)
                grads = nn.gradients(loss, self.parameters)
                for parameter, grad in zip(self.parameters, grads):
                    parameter.update(grad, -learning_rate)

            full_loss = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))
            if nn.as_scalar(full_loss) <= target_loss:
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        # Hyperparamètres dans les intervalles recommandés
        self.hidden_size1 = 400   # [10, 400]
        self.hidden_size2 = 200   # [10, 400]
        self.learning_rate = 0.1  # [0.001, 1.0]
        self.batch_size = 100     # doit diviser la taille du dataset (dans leur setup c'est prévu)

        # Paramètres couche 1 : 784 -> hidden_size1
        self.W1 = nn.Parameter(784, self.hidden_size1)
        self.b1 = nn.Parameter(1, self.hidden_size1)

        # Paramètres couche 2 : hidden_size1 -> hidden_size2
        self.W2 = nn.Parameter(self.hidden_size1, self.hidden_size2)
        self.b2 = nn.Parameter(1, self.hidden_size2)

        # Paramètres sortie : hidden_size2 -> 10
        self.W3 = nn.Parameter(self.hidden_size2, 10)
        self.b3 = nn.Parameter(1, 10)

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        # Couche 1
        h1 = nn.Linear(x, self.W1)   # (batch_size x hidden_size1)
        h1 = nn.AddBias(h1, self.b1)
        h1 = nn.ReLU(h1)

        # Couche 2
        h2 = nn.Linear(h1, self.W2)  # (batch_size x hidden_size2)
        h2 = nn.AddBias(h2, self.b2)
        h2 = nn.ReLU(h2)

        # Couche de sortie
        out = nn.Linear(h2, self.W3)  # (batch_size x 10)
        out = nn.AddBias(out, self.b3)
        return out

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        logits = self.run(x)
        return nn.SoftmaxLoss(logits, y)

    def train(self, dataset: DigitClassificationDataset) -> None:
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        params = [self.W1, self.b1,
                  self.W2, self.b2,
                  self.W3, self.b3]

        max_steps = 20000          # assez long pour bien converger
        eval_every = 100           # fréquence d'évaluation sur la validation
        best_val = 0.0
        steps_since_improve = 0
        patience = 20              # nombre d'évaluations sans amélioration avant d'arrêter

        it = dataset.iterate_forever(self.batch_size)

        for step in range(max_steps):
            x_batch, y_batch = next(it)

            # Calcul loss + gradients
            loss = self.get_loss(x_batch, y_batch)
            grads = nn.gradients(loss, params)

            # Descente de gradient
            for p, g in zip(params, grads):
                p.update(g, -self.learning_rate)

            # On surveille la validation périodiquement
            if (step + 1) % eval_every == 0:
                val_acc = dataset.get_validation_accuracy()

                # Si amélioration, on met à jour
                if val_acc > best_val:
                    best_val = val_acc
                    steps_since_improve = 0
                else:
                    steps_since_improve += 1

                # Early stopping si plus d'amélioration depuis longtemps
                if steps_since_improve >= patience and best_val >= 0.97:
                    break
