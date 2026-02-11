## CS37300 - Data Mining & Machine Learning
## Fall 2025
##### Instructor & Copyright: Bruno Ribeiro
----

# Deep Learning: Model Search via Backpropagation

## Announcement

- 48-hour extension of HW3. Please check Piazza for post regarding programming question clarification.
- Deadline updated on Gradescope
- Deadline will be updated soon on Brightspace

## What is Backpropagation?

- Backpropagation is an algorithm used for computing gradients of the parameters of a neural network with respect to a loss function. 
    - It computes the gradient of the loss function with respect to each weight by propagating the error backward through the network, using the chain rule to update the weights in proportion to the error's gradient.

## Feedforward Neural Network Recap

## Artificial neurons

The basic building block of a neural network is a *neuron* which is linked to $n$ input units
through a set of $n$ directed connections. This single function is characterized by 

1. a univariate (non-polynomial) activation function, denoted $\sigma : \mathbb{R} \to \mathbb{R}$, 
2. a (column) vector of weights, denoted ${\bf w} = (w_1, \ldots, w_n) \in \mathbb{R}^n$, and
3. a threshold (bias) value, denoted $b \in \mathbb{R}$.

Given an input vector ${\bf x} = (x_1, \ldots , x_n)$ is fed into the *neuron* through the input units, the neuron function computes $h({\bf x}) = \sigma({\bf w}^T {\bf x} + b)$. The value of this function is the neuron's output.

### Gradient Descent: General Recursive Gradient Computation (Backpropagation)

#### Recap: Feedforward neural network (FFNN a.k.a. MLP)

The general architecture of a feedforward neural network is:
- an input layer with $n$ input-units
- an output layer with $m$ outputs
- and one or more hidden layers consisting of intermediate neuron outputs.
    - the superscript $(k)$ in the parameters (weights) ${\bf W}^{(k)}$ will indicate they belong to layer $k$
    - if layer $k$ has $d_\text{in}$ inputs and $d_\text{out}$ outputs, then the neuron weights ${\bf W}^{(k)}\in \mathbb{R}^{n_\text{in} \times n_\text{out}}$ are a $n_\text{in} \times n_\text{out}$ matrix
    
<center><img src="MLP.png" height=400px></center>

### Maximum Likelihood Estimation (MLE)


Recap "is rich" task:
<center><img src="NNExample5.png" width=900px></center>

The maximum log-likelihood optimization will use gradient ascent:
<br>
Let ${\bf W} = ({\bf w}^{(1)},{\bf w}^{(2)},{\bf w}^{(3)})$.
Obtaining ${\bf W}$ via maximum likelihood estimation using gradient ascent.
Let $\text{Data} = \{({\bf x}(i),y(i))\}_{i=1}^n$
$$\begin{align*}
&\frac{\partial}{\partial {\bf W}} \text{log-likelihood(Data)} = \frac{\partial}{\partial {\bf W}} \sum_{i=1}^n \log p(y = y(i) | {\bf x}(i); {\bf w}^{(1)}, {\bf w}^{(2)}, {\bf w}^{(3)} ) \\
&=  \sum_{i=1}^n y(i) \frac{\partial}{\partial {\bf W}} \log \sigma(({\bf w}^{(3)})^T {\bf h}({\bf x}(i))) + (1 - y(i)) \frac{\partial}{\partial {\bf W}} \log (1-\sigma(({\bf w}^{(3)})^T {\bf h}({\bf x}(i))))  \\
\end{align*} 
$$
where $\sigma(x) = \frac{\exp(x)}{1 + \exp(x)}$, and ${\bf h}({\bf x}) = (1,\hat{h}_1({\bf x}),\hat{h}_2({\bf x}))$, 
$$
\hat{h}_1({\bf x}) = p(h_1 = 1 | {\bf x}) = \sigma(({\bf w}^{(1)})^T {\bf x})  
$$
and
$$
\hat{h}_2({\bf x}) = p(h_2 = 1 | {\bf x}) = \sigma(({\bf w}^{(2)})^T {\bf x})  
$$

How can we compute these gradients? Here, we will resort to the chain rule of **vector Calculus**. 

In a deep neural network each layer is a composition of previous layers, in our previous example the composition looks like: 
<img src="pathv2.png" width=700px>
defined as
$$\hat{h}_1({\bf x}) = f^1({\bf x};{\bf w}^{(1)}) = \sigma(({\bf w}^{(1)})^T {\bf x}),  $$
and
$$f^2({\bf h};{\bf w}^{(3)}) = \sigma(({\bf w}^{(3)})^T {\bf h})  ,$$
where ${\bf h} = (1,\hat{h}_1({\bf x}),\hat{h}_2({\bf x}))$.

The derivative of the composition $f^2(f^1(x;{\bf w}^{(1)});{\bf w}^{(3)})$ with respect to ${\bf w}^{(1)}_2$ is
$$
\frac{\partial f^2(f^1(x;{\bf w}^{(1)});{\bf w}^{(3)})}{\partial {\bf w}^{(1)}_2} = \frac{\partial f^2({\bf h})}{\partial {\bf h}} \bigg|_{h = f^1({\bf x};{\bf w}^{(1)})} \cdot \frac{\partial f^1({\bf x};{\bf w}^{(1)})}{\partial {\bf w}_2^{(1)}}.
$$

**General solution:** Consider having $K > 1$ hidden layers. The influence of a lower layer parameter in the final error can be recovered by the chain rule, which generally states:

$$\frac{\partial f^K(f^{K-1}(\cdots f^2(f^1(x;{\bf w}^{(1)}))\cdots))}{\partial {\bf w}^{(1)}_2} = \frac{\partial f^K(f^{K-1})}{\partial f^{K-1}} \cdot  \frac{\partial f^{K-1}(f^{K-2})}{\partial f^{K-2}} \cdots \frac{\partial f^2(f^1)}{\partial f^1} \cdot \frac{\partial f^1({\bf x};{\bf w}^{(1)})}{\partial {\bf w}_2^{(1)}}.$$

### General Recursive Gradient Computation (Backpropagation)

More generally, for deep neural networks we have no hope of writing down gradient formula for all parameters. We need a recursive method.
* **backpropagation** = recursive application of the chain rule along a computational graph to compute the gradients of all inputs/parameters/intermediates 
  * Widely used implementations maintain a graph structure, where the nodes implement the forward() / backward() functions. 
  * forward pass: compute result of an operation and save any intermediates needed for gradient computation in memory 
  * backward pass: apply the chain rule to compute the gradient of the loss function with respect to the inputs. 

The recursion can be explained with a single image. Consider the following general algorithm to recursively compute the gradient:
* The activations of the hidden neurons are given by $\hat{{\bf h}}^{(k)} = (1,\sigma({\bf W}_k \hat{{\bf h}}^{(k-1)}))$, $k=1,\ldots,K$, where
  * The input is $\hat{{\bf h}}^{(0)} = ({\bf x},1)$, where ${\bf x}$ is a single training example.
  * And the operator $(1,{\bf z})$ concatenates $1$ to vector ${\bf z}$.
* $L(\hat{{\bf h}}^{(K)})$ is the log-likelihood of a single example. If we consider multiple training examples $\{{\bf x}_1,\ldots,{\bf x}_N\}$, we have the loss over $L(\{\hat{{\bf h}}^{(K)}(i)\}_{i=1}^N)$, which is the sum of the losses over each individual training example.

<img src="Backprop.png" width=1400 height=1400>

### Backpropagation: Practical Challenges with Deep Models

**Quiz 1**: Understanding backpropagation as an algorithm that is called up to $K$ times, recursively, to multiplies gradients, what can be the practical challenges of performing gradient descent of a deep model ($K \gg 1$)?

* (a) If too many of these gradients are small, their product may cause numerical underflow: final gradient will be zero.
* (b) If too many of these gradients are large, their product may cause numerical overflow: final gradient will be INF.
* (c) I see no problem.

**Hint:** What could happen with a long multiplication like this:
$$\frac{\partial f^K(f^{K-1}(\cdots f^2(f^1(x;{\bf w}^{(1)}))\cdots))}{\partial {\bf w}^{(1)}_2} = \frac{\partial f^K(f^{K-1})}{\partial f^{K-1}} \cdot  \frac{\partial f^{K-1}(f^{K-2})}{\partial f^{K-2}} \cdots \frac{\partial f^2(f^1)}{\partial f^1} \cdot \frac{\partial f^1({\bf x};{\bf w}^{(1)})}{\partial {\bf w}_2^{(1)}}.$$



#### <span style="color:blue"> The following code requires Python 3.5 or greater.</span>


##  Example: Feedforward Classification using Python + Numpy

### In this iPython noteboook we will see how to create a neural network classifier using python and numpy.

<hr>
<hr>
First, let's create a simple dataset and split into training and testing.


```python
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import pylab
import numpy as np

X, y = make_moons(n_samples=5000, random_state=42, noise=0.1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42,test_size=0.3)
```

### Ploting the data...


```python
pylab.scatter(X[:,0], X[:,1], c=y)
pylab.show()
```


    
![png](BackPropagation_files/BackPropagation_17_0.png)
    


### Create the Neural Network Weights and Initialize Them

We first define:
* the input layer (two coordinates)
* number of hidden layers (we will use one)
* the number of output neurons (number of classes, two in our case) 

#### These are all defined by defining the hidden layer matrices

<span style="color:blue">Quizz 2:We have only one hidden layer, how many matrices do we have?</span>

<span style="color:red"> A1: Two matrices, $W_1$ and $W_2$.</span><br>
<span style="color:red"> A2: One matrix, $W$.</span>

<span style="color:blue">Quiz 3: How do we initialize these matrices?</span>

<span style="color:red">A1: With zeros.</span><br>
<span style="color:red">A2: With ones.</span><br>
<span style="color:red">A3: Randomly. We can use a Standard Normal distribution, for instance.</span>


```python
# There are only two features in the data X[:,0] and X[:,1]
n_feature = 2
# There are only two classes: 0 (purple) and 1 (yellow)
n_class = 2


def init_weights(n_hidden=100):
    # Initialize weights with Standard Normal random variables
    model = dict(
        W1=np.random.randn(n_feature + 1, n_hidden),
        W2=np.random.randn(n_hidden + 1, n_class)
    )

    return model
```

### Define the nonlinear activation function (will be used in the last layer)

We will use the softmax function. 

$$
\text{softmax}(x_i) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}
$$

If there are only two classes, the softmax is equivalent to the logistic function (do the math to convince yourself).

#### Python + Numpy tricks
Numpy is *very* handy. If we give a vector $x$, np.exp($x$) returns a vector with all elements of $x$ exponentiated.

If $y$ is a vector, $y$.sum() returns the sum of the elements in $y$.


```python
# Defines the softmax function. For two classes, this is equivalent to the logistic regression
def softmax(x):
    return np.exp(x) / np.exp(x).sum()
```

## Define the forward pass

Here, we define how the neural network get an input $x$ and use the model paramters (weights) $W_1$ and $W_2$ and biases $b_1$ and $b_2$ to predict the class labels of the input

### Hidden layer activation

From the input vector $x$ to the hidden layer neurons $h$, we need to get the intermediate value
$$
z_1 = x W_1 + b_1
$$
and pass it through an activation function.

Our activation function is the ReLU:
$$
\text{ReLU}(z) = \begin{cases} z & ,\text{if }z \geq 0 \\
0 & ,\text{if }z < 0
\end{cases}
$$
Thus, $$h = \text{ReLU}(z_1).$$

Once we get the hidden layer values $h$, we do
$$
z_2 = h W_2 + b_2
$$
and pass it through the activation of the last layer
$$
\hat{y} = \text{softmax}(z_2).
$$




```python
# For a single example $x$
def forward(x, model):
    x = np.append(x, 1)
    
    # Input times first layer matrix 
    z_1 = x @ model['W1']

    # ReLU activation goes to hidden layer
    h = z_1
    h[z_1 < 0] = 0

    # Hidden layer values to output
    h = np.append(h, 1)
    hat_y = softmax(h @ model['W2'])

    return h, hat_y
```

### Define backpropagation

Now, we need to backpropagate the derivatives of each example

The backpropagation function gets:
* all input data $\{x_i\}_i$
* corresponding hidden values of *all* training examples: $\{h_i\}_i$
* errors of each output neuron for *all* training examples: $\{y_i - \hat{y}_i\}_i$ (this is a subtraction of two vectors)

Our score function of training example $i$ will be, which is the log likelihood of a one-hot enconding vector of the classes,
$$
L(i) = \sum_{j=1}^2 y_i(j) \log \hat{y}_i(j) ,
$$
where $y_i(j)$ is the element $j$ of the vector representing the one-hot enconding of the class of training example $i$ and $\hat{y}_i(j)$ is the output of the $j$-th output neuron for training example $i$,
$$
\hat{y}_i(j) = \frac{\exp(z_2(j))}{\sum_k \exp(z_2(k))}.
$$
The derivative of the loss with respect to $z_2$ will be a vector (that we will represent using the variables without the index $j$)
$$\frac{\partial L(i)}{\partial z_2} = (y_i(1) - \hat{y}_i(1),\ldots,y_i(\text{n\_class}) - \hat{y}_i(\text{n\_class})) = y_i - \hat{y}_i.$$
**Note that we can get this derivative directly from the relative error `errs`.**

#### Other derivatives

It will compute the following derivatives for each training example:
* The derivative of the last layer parameters are
$$
\frac{\partial L(i)}{\partial W_2} = \frac{\partial z_2(i)}{\partial W_2}  \frac{\partial L(i)}{\partial z_2} = h_i^T  (y_i - \hat{y}_i)
$$
and
$$
\frac{\partial L(i)}{\partial b_2} = \frac{\partial z_2(i)}{\partial b_2}  \frac{\partial L(i)}{\partial z_2} =  (y_i - \hat{y}_i),
$$
as 
$$
\frac{\partial z_2(i)}{\partial b_2} = 1.
$$

* The derivatives with respect to the hidden values of the previous layer are
$$
\frac{\partial L(i)}{\partial h} = \frac{\partial z_2(i)}{\partial h}  \frac{\partial L(i)}{\partial z_2} =  W_2 (y_i - \hat{y}_i)
$$

We then backpropagate $\partial L(i)/\partial h $ to the previous layer. This will be needed in the final derivative
the final derivatives are
$$
\frac{\partial L(i)}{\partial W_1} = \frac{\partial z_1(i)}{\partial W_1} \frac{\partial h(i)}{\partial z_1} \frac{\partial L(i)}{\partial h},
$$ 
and
$$
\frac{\partial L(i)}{\partial b_1} = \frac{\partial z_1(i)}{\partial b_1} \frac{\partial h(i)}{\partial z_1} \frac{\partial L(i)}{\partial h},
$$ 

where 
$$
\frac{\partial z_1(i)}{\partial W_1} = x_i,
$$
and
$$
\frac{\partial z_1(i)}{\partial b_1} = 1,
$$
and the derivative of the ReLU
$$
\frac{\partial h(i)}{\partial z_1} = \begin{cases} 1 &, \text{if }z_1(i) > 0\\
                                                   0 & \text{otherwise}. \end{cases}.
$$

The final output are the derivatives of the parameters.

<span style="color:blue"> In the above, we have described the backpropagation algorithm *per training example*. 
The following python code will, as described earlier, give all examples as inputs. Thus, the input is a matrix whose rows are the vectors of each training example.</span>

This function outputs 
$$
\text{d}W_1 =  \sum_{i=1}^N \frac{\partial L(i)}{\partial W_1},
$$ 
$$
\text{d}b_1 =  \sum_{i=1}^N \frac{\partial L(i)}{\partial b_1},
$$ 
$$
\text{d}W_2 =  \sum_{i=1}^N \frac{\partial L(i)}{\partial W_2},
$$
and
$$
\text{d}b_2 = \sum_{i=1}^N \frac{\partial L(i)}{\partial b_2}.
$$


```python
def backward(model, xs, hs, errs):
    """xs, hs, errs contain all information (input, hidden state, error) of all data in the minibatch"""
    # errs is the gradients of output layer for the minibatch
    dW2 = (hs.T @ errs)/xs.shape[0]

    # Get gradient of hidden layer
    dh = errs @ model['W2'].T
    dh[hs <= 0] = 0
    
    # The bias "neuron" is the constant 1, we don't need to backpropagate its gradient
    # since it has no inputs, so we just remove its column from the gradient
    dh = dh[:, :-1]

    # Add the 1 to the data, to compute the gradient of W1
    xs = np.hstack([xs, np.ones((xs.shape[0], 1))])

    dW1 = (xs.T @ dh)/xs.shape[0]

    return dict(W1=dW1, W2=dW2)
```

## Do the forward and backward procedures to get the gradient

For each input example $i$ in the training data, perform a forward pass and:
* store all the hidden units of all the hidden layers associated with example $i$ (we only have to store one vector of hidden values)
* store the gradient of the error of example $i$ with respect to the prediction

Once we have store all hidden layer values and all the derivatives of all examples, 
we will do the backard pass and return the derivatives of the error with respect to the paramters $W_1$, $b_1$, $W_2$, and $b_2$.


```python
def get_gradient(model, X_train, y_train):
    xs, hs, errs = [], [], []

    for x, cls_idx in zip(X_train, y_train):
        h, y_pred = forward(x, model)

        # Create one-hot coding of true label
        y_true = np.zeros(n_class)
        y_true[int(cls_idx)] = 1.

        # Compute the gradient of output layer
        err = y_true - y_pred

        # Accumulate the informations of the examples
        # x: input
        # h: hidden state
        # err: gradient of output layer
        xs.append(x)
        hs.append(h)
        errs.append(err)


    # Backprop using the informations we get from the current minibatch
    return backward(model, np.array(xs), np.array(hs), np.array(errs))
```

## One gradient ascent step

Perform a single gradient ascent step.

Get the gradients and perform the following updates for $N$ training examples:
$$
W_1 =W_1 + \epsilon \frac{1}{N} \sum_{i=1}^N \frac{\partial L(i)}{\partial W_1},
$$
$$
b_1 =b_1 + \epsilon \frac{1}{N} \sum_{i=1}^N \frac{\partial L(i)}{\partial b_1},
$$
$$
W_2 =W_2 + \epsilon \frac{1}{N} \sum_{i=1}^N \frac{\partial L(i)}{\partial W_2},
$$
and
$$
b_2 =b_2 + \epsilon \frac{1}{N} \sum_{i=1}^N \frac{\partial L(i)}{\partial b_2},
$$
where $\epsilon = 10^{-1}$ in our example.


```python
def gradient_step(model, X_train, y_train, learning_rate=1e-1):
    grad = get_gradient(model, X_train, y_train)
    model = model.copy()

    # Update every parameters in our networks (W1 and W2) using their gradients
    for layer in grad:
        # Learning rate: 1e-1
        model[layer] += learning_rate * grad[layer]

    return model
```

## Quiz

What information from the forward pass must be stored to compute gradients during backpropagation?

A) Only the final output

B) Only the weights

C) Intermediate neuron activations (${\bf h}$) at each layer

D) Only the gradients from the previous iteration


## Do gradient ascent some fixed number of times


```python
from tqdm import tqdm

def gradient_ascent(model, X_train, y_train, no_iter=10):
    for iter in tqdm(range(no_iter), desc="Progress"):
        model = gradient_step(model, X_train, y_train)
    
    return model

```

## Train the model and test the accuracy over the test data

We now train the model and output the prediction error over the test data.

Note that the output has two neurons for the two classes. Our prediction will chose the class corresponding to the 
largest output neuron value.


```python
no_iter = 1000

# Reset model
model = init_weights()

# Train the model
model = gradient_ascent(model, X_train, y_train, no_iter=no_iter)

y_pred = np.zeros_like(y_test)

accuracy = 0

for i, x in enumerate(X_test):
    # Predict the distribution of label
    _, prob = forward(x, model)
    # Get label by picking the most probable one
    y = np.argmax(prob)
    y_pred[i] = y

    # Accuracy of predictions with the true labels and take the percentage
    # Because our dataset is balanced, measuring just the accuracy is OK
    accuracy = (y_pred == y_test).sum() / y_test.size

print('Accuracy after {} iterations: {}'.format(no_iter,accuracy))
```

    Progress: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [00:27<00:00, 36.84it/s]

    Accuracy after 1000 iterations: 0.996


    



```python
pylab.scatter(X_test[:,0], X_test[:,1], c=y_pred)
pylab.show()
```


    
![png](BackPropagation_files/BackPropagation_39_0.png)
    



```python
no_iter = 300
no_runs = 10

accuracies = np.zeros(no_runs)


for run in range(no_runs):
    print("Run {}".format(run))
    # Reset model
    model = init_weights()

    # Train the model
    model = gradient_ascent(model, X_train, y_train, no_iter=no_iter)

    y_pred = np.zeros_like(y_test)
    
    for i, x in enumerate(X_test):
        # Predict the distribution of label
        _, prob = forward(x, model)
        # Get label by picking the most probable one
        y = np.argmax(prob)
        y_pred[i] = y

        # Accuracy of predictions with the true labels and take the percentage
        # Because our dataset is balanced, measuring just the accuracy is OK
        accuracies[run]= (y_pred == y_test).sum() / y_test.size

print('Mean accuracy over test data: {}, std: {}'.format(accuracies.mean(), accuracies.std()))
```

# Optimization Methods in Machine Learning

## Slide 1: Core Optimization Algorithms

**Goal:** Minimize loss (score) $L({\bf W}) = \frac{1}{n} \sum_{i=1}^{n} \ell(f_{{\bf W}}(x_i), y_i)$ by updating parameters ${\bf W}$, where $\ell$ is typically the negative log-likelihood.

### Stochastic Gradient Descent (SGD)
$${\bf W}_{t+1} = {\bf W}_t - \eta \frac{1}{B} \sum_{i \in \mathcal{B}_t} \nabla \ell(f_{{\bf W}_t}(x_i), y_i)$$
- Approximates gradient using mini-batches (B = 32-256)
- Fast but noisy; sensitive to learning rate $\eta$

### SGD with Momentum
$$v_{t+1} = \beta v_t + (1 - \beta) \nabla L({\bf W}_t), \quad {\bf W}_{t+1} = {\bf W}_t - \eta v_{t+1}$$
- Accumulates velocity ($\beta = 0.9$) to dampen oscillations
- Faster convergence, especially in narrow valleys

### Adam (Adaptive Moment Estimation)
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$${\bf W}_{t+1} = {\bf W}_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
- Combines momentum + adaptive learning rates per parameter
- **Most popular:** Robust defaults ($\eta=0.001, \beta_1=0.9, \beta_2=0.999$)

### AdamW
- Adam with decoupled weight decay: ${\bf W}_{t+1} = {\bf W}_t - \eta(\text{Adam update} + \lambda{\bf W}_t)$
- **Best for transformers and large models**


## Quick Reference Guide

| Optimizer | When to Use | Typical LR |
|-----------|-------------|------------|
| **Adam/AdamW** | Default choice, prototyping, transformers | 0.001 |
| **SGD + Momentum** | CNNs, best generalization (needs tuning) | 0.1 |

### Key Practical Tips
- **Learning rate is very important:** Try [0.0001, 0.001, 0.01, 0.1]
- **Batch size:** 32-256 (smaller = more noise = tends to lead to better generalization)
- **Gradient clipping** for RNNs: `clip_grad_norm_(params, 1.0)`

### PyTorch Quick Start
```python
# Adam - start here
optimizer = optim.Adam(model.parameters(), lr=0.001)

# AdamW - for transformers
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# SGD + Momentum - for best generalization
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)

# Training loop
for batch_x, batch_y in train_loader:
    loss = criterion(model(batch_x), batch_y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```


```python

```
