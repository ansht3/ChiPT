## CS37300 - Data Mining & Machine Learning
### Fall 2025
##### Instructor & Copyright: Bruno Ribeiro
----

### Deep Learning: Feedforward Neural Networks

# 1. Logistic Regression Review

## 1.1. Logistic Regression

- Model: $$ f({\bf x}) = \sum_{j=1}^m w_j x_j + b,$$
with
$$
P(y = 1 | {\bf x}; {\bf w}) = \sigma(f({\bf x})),
$$
where $\sigma(a) = \frac{\exp(a)}{1+\exp(a)}$

- The sum is the inner product between ${\bf w}$ and ${\bf x}$:
It gives the length of projection of ${\bf x}$ onto ${\bf w}$.

- If inner product is 0, then if ${\bf x}$ is perpendicular to ${\bf w}$
- Add b,
    - if $f({\bf x}) > 0$, then $\sigma(f({\bf x})) > 0.5$
    - if $f({\bf x}) < 0$, then $\sigma(f({\bf x})) < 0.5$

## 1.2. Logistic Activation (sigmoid)

<center><img src="Sigmoid.png" width=500px></center>

# Quiz (Logistic Regression)
<img src="output_7_0.png" width=300px>
In the above training dataset with input ${\bf x} \in \mathbb{R}^2$ with two classes $y \in \{\text{yellow, purple}\}$, the optimal <strong>logistic regression classifier</strong> will achieve:<br>

<ul>
    <li> a. About 85% training accuracy </li>
    <li> b. About 98% training accuracy </li>
</ul>

<br>

<strong>Hint 1:</strong> $P(Y=1|X=(x_1,x_2)) = \sigma(f(x_1,x_2))$, where $f(x_1,x_2) = w_1 x_1 + w_2 x_2 + b$. <br>
<strong>Hint 2:</strong> $P(Y=1|X=(x_1,x_2)) = 0.5 = \sigma(f(x_1,x_2))$, which means $f(x_1,x_2) = 0 = w_1 x_1 + w_2 x_2 + b$ which yields $x_1 =  - \frac{w_2}{w_1} x_2 - \frac{b}{w_1}$. 

## 1.3. Solution

Logistic regression training predictions:

<center><img src="LogisticSolution.png" width=400px/></center>

# 2. Deep Learning


### Quiz

Background Assessment
How familiar are you with deep learning:

(a) I have never written a program that uses a neural network

(b) Used neural networks in my code through APIs (e.g., OpenAI, Cohere, Anthropic, Google, Co-Pilot)

(c) Have implemented neural networks from scratch or trained models end-to-end

(d) Research experience in deep learning (publications/projects)

## 2.2. Language Model Demo


```python
import importlib

def install_if_missing(library):
    try:
        importlib.import_module(library)
        print(f"'{library}' is already installed.")
    except ImportError:
        print(f"Installing '{library}'...")
        !pip install {library}

install_if_missing('transformers')
install_if_missing('sentencepiece')
```

    'transformers' is already installed.
    'sentencepiece' is already installed.



```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name,legacy=True,clean_up_tokenization_spaces=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)
```


```python
# Example prompt
inputs = tokenizer("Translate English to Portuguese: \"What is Machine Learning?\"", return_tensors="pt")
outputs = model.generate(**inputs, max_length=30)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

    "Qué é o estudo de máquinas?"


# 3. Feedforward Neural Network Classifier

<center><h1>Input:</h1><img src="test_MLP_classification_input.png" width=300px>
    <h1>Precicted:</h1><img src="test_MLP_classification.png" width=300px></center>

## 3.1. Logistic Regression
<center><img src="LogisticStructure.png" width=500px></center>

### 3.1.1. Logistic Regression (Example 1)
Task: Predict if a person is rich.

- Training dataset $\{({\bf h}_i,y_i)\}_{i=1}^n$
    - Where $h_1, h_2 \in \{0,1\}$ are the input features
    - Target output: $y \in \{0,1\}$ if the person is rich or not
- Task: Given ${\bf h} \in \{0,1\}^2$ predict $y \in \{0,1\}$.
<center><img src="NNexample1.png" width=500px></center>

### 3.1.2. Logistic Regression Example 1 (Revisited)
<center><img src="NNexample2.png" width=500px></center>

### 3.1.3. But we can predict Yacht and Mansion ownership (Examples 2 and 3)
- Now suppose we do not have $h_1$ and $h_2$ above.
    - But we have the features ${\bf x} \in \{0,1\}^4$ and two pre-trained (existing) classifiers that can predict $h_1$ and $h_2$ from these fetures
<center><img src="YatchMansion.png" width=800px></center>

### 3.1.4. Combining Logistic Regressions (Example 4a) 
<center><img src="NNExample3.png" width=900px></center>
- Now we find the optimal logistic regression parameters ${\bf w^{(3)}}$ via gradient ascent to maximize the likelihood over the training data 

# Quiz

- We would likely get $\underline{\hspace{2cm}}$ likelihood over the training if we performed gradient ascent not only over ${\bf w^{(3)}}$ but also over parameters ${\bf w^{(1)}}$ and ${\bf w^{(2)}}$.
    - (a) Higher
    - (b) Lower

### 3.1.5. Equivalent Model (Example 4b)
<center><img src="NNExample4.png" width=900px></center>

### 3.1.6. A More Flexible Model (Example 5, a Feedforward Neural Network)
<center><img src="NNExample5.png" width=900px></center>

## 3.2. Feedforward Neural Networks

Both models in **Examples 4 and 5** are neural networks.
- Example 4 is a special case of Example 5
- Example 5 uses a fully connected neural network (**Multilayer Perceptron** or **Feedforward Network**)

### 3.2.1. Feedforward Neural Network Architecture (MLP)
<center><img src="NN1.png" width="70%"></center>

- Note that in most drawings (like the one above), the bias $b$ is not explicitly described

<center><img src="superres_mlp_viz.svg" width="120%"></center>

- Example of an MLP that could perform a SuperResolution on input images 300x225x3 and output 600x450x3 images.
    - Vectorize the input RGB image tensor (300x225x3 = 202,500-dimennsional input vector)
    - Vectorize the output RGB image tensor (600x450x3 = 810,000-dimennsional output vector)
    - This MLP has ~ 4 billion parameters!
    - If each parameter is described in BF16 it takes 2 bytes (16 bits) = 8GB to store the parameters (a.k.a. neuron weights)
    - Overhead of training: store neural network weights + computed gradient + optimizer states ~ 8GB*3 = 24GB of VRAM per training image. 
        - With batch size = 4 (training 4 images at a time), it takes ~ 96GB of VRAM
   
- In the CNN class we will see a type of neural network that is better for images.

### 3.2.2. Model search
- Training data: $\{({\bf x}_1,y_1),\ldots,({\bf x}_n,y_n)\}$
- ${\bf x} = (1,x_{i1},x_{i2},x_{i3},x_{i4})$
- ${\bf w}^{(k)} = (w^{(k)}_1,w^{(k)}_2,w^{(k)}_3,w^{(k)}_4,w^{(k)}_5)$, $k=1,2$
- ${\bf w}^{(3)} = (w^{(3)}_1,w^{(3)}_2,w^{(3)}_3)$


Optimize the log-likelihood
$$\begin{align*}
{\bf w}^{(1)\star},{\bf w}^{(2)\star},{\bf w}^{(3)\star}= &{\arg\!\max}_{{\bf w}^{(1)},{\bf w}^{(2)},{\bf w}^{(3)}} \sum_{i=1}^n \log p(y = y_i | {\bf x}_i; {\bf w}^{(1)}, {\bf w}^{(2)}, {\bf w}^{(3)} ) \\
&=  \sum_{i=1}^n y_i \log \sigma(({\bf w}^{(3)})^T {\bf h}({\bf x}_i)) + (1 - y_i) \log (1-\sigma(({\bf w}^{(3)})^T {\bf h}({\bf x}_i))) ,
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

### Questions:
- Describe the training data

- Describe the model

- What is the score function?

- What is the search procedure?

- Which model is more likely to overfit the data? Example 3, Example 4, or Example 5?

- Why are Examples 3 and 4 equivalent?

# 4. Neural Network Definitions

What were the sigmoids in the logistic regression, now are called **"activation functions"**
<center><img src="NNArch.png" width=500px></center>

# 5. Introduction to Pytorch
<img src="Pytorch_logo.png" width=300px>

In our course we will use [Pytorch](https://pytorch.org/)
- Pytorch is an open source project [Git repository](https://github.com/pytorch/pytorch) under [The Linux Foundation](https://www.linuxfoundation.org/)
- Easy to debug models
- Fast to prototype new models
- Can be used as a numpy library with GPU acceleration
- Supports dynamic backpropagation computation graphs
- Widely used by industry (e.g. Tesla, Facebook, Nvidia, etc.)
- Leading framework in academia

## 5.1. Model Search with the Pytorch Library 
### 5.1.1. Automatic Differentiation

* Understanding **Pytorch tensors**: <a href="https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#sphx-glr-beginner-blitz-tensor-tutorial-py">tutorial</a>

#### Understanding Pytorch's Automatic Differentiation

First, we will create a variable $x \in \mathbb{R}$ and assign it value $x = 3$.

- We will first make a common mistake:



```python
import torch

# Assigns a constant zero to unidimensional variable x with requires_grad=True, meaning we want to compute the gradient
x = torch.zeros(1, requires_grad=True) 

# However, this assignment overwrites the tensor 'x' with a Python float (3.0), losing its gradient tracking
x = 3.0  # x is no longer a torch tensor, but a regular float.

try:
    # Attempting to access 'x.data' will cause an error because 'x' is now a float, not a torch tensor
    print(f'Value of x = {x.data}')  # This will raise an AttributeError since floats don't have 'data'
    
except AttributeError as e:
    print(f"Error: {e}")

```

    Error: 'float' object has no attribute 'data'


- This is the correct way to attribute values to differentiable variables in pyTorch


```python
import torch

x = torch.zeros(1, requires_grad=True) # Assigns a constant zero to unidimensional variable x 
                                       # requires_grad=True tells pytorch we will compute gradients for this variable
x.data.fill_(3.)  

print(f'Value of x = {x.data}') # Will return [3] as a tersor variable
print(f'Gradient of x = {x.grad}') # Will return None because it we need to invoke .backward() first
```

    Value of x = tensor([3.])
    Gradient of x = None


Consider the following function:
$$
z(x) = 10 y(x)^2,
$$
where
$$
y(x) = 2 x + 1.
$$

Now, let's compute $$\left. \frac{\partial z(x)}{\partial x} \right|_{x = 3},$$
which is the derivative of $z$ with respect to $x$ evaluated at $x=3$.


```python
x = torch.zeros(1, requires_grad=True) # Assigns a constant zero to unidimensional variable x 
                                       # requires_grad=True tells pytorch we will compute gradients for this variable

x.data.fill_(3.) # Constant MUST be floating point (if the tensor is an Integer, it won't work)

y = 2 * x + 1
z = 10 * y * y
z.backward()     # automatically computes the gradient ∂z/∂x evaluated at x = 3 using backpropagation
print(x.grad)    # ∂z/∂x = 280
```

    tensor([280.])


## 5.2. Knowledge Representation: Create Logistic Regression Model using Pytorch Libraries


```python
# Import the necessary modules from PyTorch
import torch
import torch.nn as nn
import torch.nn.functional as F

# PyTorch is object-oriented, so we need to define our model as a class.
# We must extend nn.Module, which is the base class for all neural network modules in PyTorch.
class LogisticRegression(nn.Module):
    # Define the neural network parameters in the constructor (__init__)
    def __init__(self, input_size, output_size):
        """
        Constructor:
        - This method initializes the model with two key components:
            1. The input size: The number of features in the input data (dimensionality).
            2. The output size: The number of classes (for binary classification, this is 1).
        - We initialize weights using `nn.Linear`, which is a simple, fully-connected layer (a.k.a. a linear transformation).
        - The 'super()' call invokes the constructor of the parent class nn.Module to ensure proper initialization of the module.
        """
        super(LogisticRegression, self).__init__()  # Calls the parent class (nn.Module) constructor
                                                    # This will also initialize the model weights randomly
        
        # Create a fully connected linear layer (f_x(x) = W x + b) that will compute the transformation from input to output.
        # The layer is defined by the input size (number of input features) and the output size (number of classes).
        self.f_x = nn.Linear(input_size, output_size, bias=True)  # The 'bias' term is the intercept (optional, default=True)
        self.output_size = output_size  # Store the output size for later use in the forward pass
    
    # Define the forward pass, which is we apply the model to the input x.
    def forward(self, x):
        """
        Forward method:
        - This method takes input 'x' and applies the linear transformation defined by 'f_x'.
        - If output_size is 1 (binary classification), apply the sigmoid activation function.
        - If output_size > 1 (multi-class classification), apply the softmax function to get the class probabilities.
        - The softmax function ensures that the output values sum to 1, making them interpretable as probabilities.
        
        Input: 
        - x: Input features tensor of shape (batch_size, input_size)
        
        Output:
        - y_hat: The predicted probabilities, either as a scalar between 0 and 1 (binary classification),
                 or a vector of probabilities (multi-class classification).
        """
        
        # Binary classification: output should be one probability value between 0 and 1
        if self.output_size == 1:
            # Apply the sigmoid activation function to the linear transformation
            y_hat = torch.sigmoid(self.f_x(x))  # Sigmoid squashes output into range [0, 1]
        
        # Multi-class classification: output should be a probability distribution across multiple classes
        else:
            # Apply the softmax activation function to get probabilities for each class
            y_hat = F.softmax(self.f_x(x), dim=1)  # Softmax outputs a distribution across classes, dim=1 refers to classes
        
        return y_hat  # Return the predicted output (probabilities for each class)

```

### We we need GPUs?

* GPUs massively accelerate **linear algebra operations**, especially matrix multiplies (GEMMs).
* GPUs are **indispensable** for training and serving large deep neural networks.

Compared to CPU/GPU compute throughput, and compared to their local memory bandwidth, **I/O to storage and network remains the main bottleneck**.

* **GB/s** = Gigabytes / second
* **TFLOPS** = Floating Point operations $\times 10^{12}$ / second

### Typical modern high-end server speeds (PCIe 5.0 era, ~2025)

* **CPU**: ~2–5 TFLOPS FP32, with DDR5 bandwidth ≈ 200–400 GB/s (per socket, 8–12 channels).
* **GPU (e.g., NVIDIA H100/B100, AMD MI300)**:
    * **FP32 (single precision)**: ~60–120 TFLOPS on modern GPUs (e.g., NVIDIA H100, B100, AMD MI300).
    * **FP16/BF16 (half precision, brain float)**: ~1–2 PFLOPS (sustained) with tensor cores.
    * **FP8 (8-bit floating point)**: 4–8 PFLOPS per GPU.
* **CPU–GPU interconnect**:

  * PCIe 4.0 x16 ≈ 32 GB/s
  * PCIe 5.0 x16 ≈ 64 GB/s
  * NVLink 4/5 (H100, Blackwell) ≈ 900 GB/s (aggregate, bidirectional).
* **NVMe SSDs**: 4–7 GB/s per device.
* **Network**:

  * 100 Gbps Ethernet / InfiniBand ≈ 12.5 GB/s
  * 400 Gbps ≈ 50 GB/s (becoming common in HPC/AI clusters).

### Bottlenecks

```text
 CPU (3 TFLOPS) ── DDR5: 400 GB/s
    │
    │ PCIe 5.0 x16: 64 GB/s
    ▼
 GPU (100 TFLOPS FP32, 2 PFLOPS FP8) ── HBM3e: 4 TB/s
    │
    │ NVLink 5: 900 GB/s (GPU↔GPU, multi-GPU scaling)
    ▼
 Storage/Network (NVMe: 7 GB/s, Net: 50 GB/s per 400G link)
```
There is an **enormous imbalance** between how fast GPUs can process data at petaflop scale with multi-terabyte/s memory bandwidth, but I/O through CPU and PCIe remains orders of magnitude slower, making **data locality and pipeline design critical** for performance.

# Quiz

Tell us about your personal computing power (we will use the Scholar GPUs for this course)

(a) I own only a laptop (no GPU)

(b) I own only a laptop with a decent GPU (8GB+)

(c) I own a Mac desktop with a decent GPU (16GB+ unified RAM)

(d) I own a PC with a decent Nvidia GPU or AMD GPU that I can do AI (8GB+ VRAM, Nvidia Pascal, 6000 or greater)

(e) Other


```python
use_cuda = torch.cuda.is_available()  # Our flag to check if Nvidia GPU is available

device = torch.device("cuda" if use_cuda else "cpu") # Decide device between CUDA (GPU) and CPU compute

print(f'Is CUDA available? {use_cuda}')
```

    Is CUDA available? False


### 5.2.1. Move training data into Torch tensors

- Training data becomes a tensor
    - One of the tensor dimensions is the number of training examples
- The data moves to the GPU if device = torch.device("cuda")


```python
### Define training data
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import pylab
import numpy as np

X, y = make_moons(n_samples=5000, random_state=42, noise=0.1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42,test_size=0.3)

pylab.scatter(X[:,0], X[:,1], c=y)
pylab.xlabel("$x_1$",size=22)
pylab.ylabel("$x_2$",size=22)
pylab.show()
```


    
![png](neuralNetworks_files/neuralNetworks_44_0.png)
    



```python
# Transform original data into pytorch tensors and send to device (send data to GPU if available)
torch_X_train = torch.FloatTensor(X_train).to(device)
torch_X_test = torch.FloatTensor(X_test).to(device)
torch_y_train = torch.FloatTensor(y_train).to(device)
torch_y_test = torch.FloatTensor(y_test).to(device)

print(f'Now data is in Pytorch tensor form: {torch_y_train}')
```

    Now data is in Pytorch tensor form: tensor([1., 0., 0.,  ..., 1., 0., 1.])


### 5.2.2. Instantiate logistic regression

Creates a Logistic Regression model with
- 2-dimensional input 
- 1-dimensional ``sigmoid`` output
- Default weight initialization
    - Linear layer weight and bias values are initialized by sampling $\text{Uniform}(-\sqrt{k}, \sqrt{k})$, where $k = \frac{1}{\text{in_dimension}}$
    


```python
##    Send model parameters to "device" (GPU if the device is on the GPU)
LR = LogisticRegression(input_size = 2, output_size = 1).to(device)

print(f'Logistic regression model created: {LR}')
```

    Logistic regression model created: LogisticRegression(
      (f_x): Linear(in_features=2, out_features=1, bias=True)
    )


### 5.2.3. Initial Logistic Regression prediction

- Get current predicted training label probabilities from the MLP
- Note that these predictions are from randomly initialized parameters


```python

y_pred = LR(torch_X_train) ### Get output of feedfoward function over the training data

print(f'Predicted values of X: {y_pred}')
```

    Predicted values of X: tensor([[0.5132],
            [0.5165],
            [0.4499],
            ...,
            [0.5010],
            [0.4249],
            [0.4465]], grad_fn=<SigmoidBackward0>)


## 5.3. Score function: Compute the Negative log-likelihood score

- Define the loss function (negative log-likelihood score)
- Compute the loss


```python
# Define the loss function
# Negative log-likelihood loss for binary classes
if LR.output_size == 1:
    score = nn.BCELoss() 
else: # Negative log-likelihood loss for C > 2 classes
    score = nn.NLLLoss()

## Compute the loss of the predicted values
error = score(y_pred, torch_y_train.view(-1,1)) ## .view(-1,1) avoids a warning about the tensor dimension
```

## 5.4. Model search: Use the score to compute gradients

- Computes gradients from the score via backpropagation
    - Never forget to zero the gradient vectors first (Pytorch accumulates gradients by default)


```python
# Compute the gradients of the linear layers of MLP with respect to the error
##  Gradient computation performed via backpropagation

LR.zero_grad() ## Zero current gradients (pytorch accumulates gradients by default)

error.backward() ## Compute gradients via backpropagation
```

#### Define the learning rate

- We will revisit the effect of learning rates later
    - Very small learning rates can result in poor generalization error
    - Commonly a number between 1 and 1e-05


```python
## Define learning rate
learning_rate = 1e-2
```

### 5.4.1. Perform one gradient step

- Will subtract the (gradient * learning_rate) from all parameters


```python
print(f"Before gradient step: logistic regression bias {LR.f_x.bias}")

## Go over all parameters and subtract their gradient
##   Subtract (not sum) the gradient since we want to minimize the loss
for w in LR.parameters():
    w.data.sub_(w.grad.data * learning_rate)

print(f"After gradient step: logistic regression bias {LR.f_x.bias}")
```

    Before gradient step: logistic regression bias Parameter containing:
    tensor([-0.0422], requires_grad=True)
    After gradient step: logistic regression bias Parameter containing:
    tensor([-0.0420], requires_grad=True)


### 5.4.2. Model search: Optimize the model

- We will now perform 1000 optimization steps using the entire dataset
    - **Epoch**: Each time the entire dataset is used in the optimization
- It is useful to plot the training accuracy


```python
## Loop through multiple gradient steps

for epoch in range(3000):
    ## Predict values using updated model
    y_pred = LR(torch_X_train)
    
    ## Find predicted class (as a number {1,0})
    pred = y_pred.gt(0.5) + 0.0
    
    # Compute accuracy
    if epoch % 100 == 9:
        correct = pred.eq(torch_y_train.view_as(pred)).sum().item()
        print(f'Epoch {epoch} training accuracy: {int(correct/torch_y_train.shape[0] * 100)}%')

    ## Compute the new error
    error = score(y_pred, torch_y_train.view(-1,1)) ## .view(-1,1) avoids a warning about the tensor dimension
    
    LR.zero_grad() ## Zero current gradients (Pytorch accumulate gradients by default)

    error.backward() ## Compute gradients in Pytorch via backpropagation
    
    ## Go over all parameters and subtract their gradient
    for w in LR.parameters():
        w.data.sub_(w.grad.data * learning_rate)

## Final train accuracy
if epoch % 100 == 9:
    correct = pred.eq(torch_y_train.view_as(pred)).sum().item()
    print(f'Correct {int(correct/torch_y_train.shape[0] * 100)}%')

```

    Epoch 9 training accuracy: 21%
    Epoch 109 training accuracy: 50%
    Epoch 209 training accuracy: 79%
    Epoch 309 training accuracy: 79%
    Epoch 409 training accuracy: 80%
    Epoch 509 training accuracy: 80%
    Epoch 609 training accuracy: 80%
    Epoch 709 training accuracy: 81%
    Epoch 809 training accuracy: 81%
    Epoch 909 training accuracy: 81%
    Epoch 1009 training accuracy: 82%
    Epoch 1109 training accuracy: 82%
    Epoch 1209 training accuracy: 82%
    Epoch 1309 training accuracy: 82%
    Epoch 1409 training accuracy: 82%
    Epoch 1509 training accuracy: 82%
    Epoch 1609 training accuracy: 83%
    Epoch 1709 training accuracy: 83%
    Epoch 1809 training accuracy: 83%
    Epoch 1909 training accuracy: 83%
    Epoch 2009 training accuracy: 83%
    Epoch 2109 training accuracy: 83%
    Epoch 2209 training accuracy: 83%
    Epoch 2309 training accuracy: 84%
    Epoch 2409 training accuracy: 84%
    Epoch 2509 training accuracy: 84%
    Epoch 2609 training accuracy: 84%
    Epoch 2709 training accuracy: 84%
    Epoch 2809 training accuracy: 84%
    Epoch 2909 training accuracy: 84%


## 5.5. Model Evaluation


```python
# Prepare model for evaluation (needed to avoid computing gradient)
with torch.no_grad():
    # Prepare model for evaluation (needed to avoid computing gradient)
    LR.eval()
    # Predict the distribution of label
    y_hat = LR(torch_X_test)
    # Get label by picking the most probable one
    y_pred = y_hat.gt(0.5) + 0.0

    # Accuracy of predictions with the true labels and take the percentage
    # Because our dataset is balanced, me,,asuring just the accuracy is OK
    correct = y_pred.eq(torch_y_test.view_as(y_pred)).sum().item()
    print(f'Correctly classified test examples {int(correct/torch_y_test.shape[0] * 100)}%')

    pylab.scatter(X_test[:,0], X_test[:,1], c=y_pred)
    pylab.show()
```

    Correctly classified test examples 85%



    
![png](neuralNetworks_files/neuralNetworks_61_1.png)
    


### (Extra) Weight initialization


```python
## Try different weight initializations of the linear layers
## Not needed, but you can apply a different initialization of the weights before optimizing

def init_weights(layer):
    if type(layer) == nn.Linear:
        torch.nn.init.normal_(layer.weight)
        layer.bias.data.fill_(0.01)

LR.apply(init_weights) ## Function apply will go over all layers
```




    LogisticRegression(
      (f_x): Linear(in_features=2, out_features=1, bias=True)
    )



# 6. Feedforward Neural Network

We are going to create the following neural network for our input data (which has 2 features and one output).
- Each edge represents one weight in the neural network
<center><img src="nn.svg" height=1800px></center>

## 6.1. Common Activation Functions
In feedforward neural networks we can add other types of *non-linear activation* functions after the inner product layers. Here are some of the popular choices for non-linear activations:
* **Sigmoid**: $\sigma(z) = \frac{1}{(1+e^{-z})}$ (same as logistic regression)
* **tanh**: $\text{tanh}(z) = \frac{(e^{2z} - 1)}{(e^{2z} + 1)}$
* **ReLU**: $\text{relu}(z) = \max(0, z)$
* **ELU**: $\text{elu}(z) = \begin{cases} z & \text{if }z \geq 0,\\ \alpha (\exp(z) - 1) &\text{if } z < 0, \end{cases}$ where $\alpha$ is a small constant.
* **LeakyReLU**: $\text{LeakyRelu}(z) = \begin{cases} z & \text{if }z \geq 0,\\ \alpha z &\text{if } z < 0, \end{cases}$ where $\alpha$ is a small constant.

<center><img src="activations.png" width=600px></center>



*If the input is a vector ${\bf z}$, then each function is applied to each element of the vector.*

- Rectified Linear Units (ReLU) and Exponential Linear Units (ELUs) have been found to work well in vision-related problems.

## 6.2. Knowledge Representation: Defining Feedforward Neural Network Object

The following code defines a simple **Multi-Layer Perceptron (MLP)** or **Feedforward Neural Network (FF)** using PyTorch. 
- We will import the necessary libraries
- Define the neural network class
    - Specify its structure (how the function works)
    - Specify its forward pass.

#### 1. **Imports**:
- `torch`: The core library of PyTorch used for creating tensors and performing operations on them.
- `torch.nn`: Contains modules and layers, such as `nn.Linear`, used to define the structure of the neural network.
- `torch.nn.functional`: Provides various functions like activation functions (`relu`, `sigmoid`, etc.).
- `torch.utils.data`: Utilities for loading and managing data, although not directly used in this snippet, it's useful for handling datasets.

#### 2. **MLPNetwork Class**:
- Our **MLPNetwork** class is a subclass of `nn.Module`, which is the base class for all neural networks in PyTorch.
- This network consists of three fully connected layers (`nn.Linear`), each responsible for transforming input data through learned weight matrices and biases.

#### 3. **Constructor (`__init__` method)**:
- The constructor (`__init__`) defines the structure of the MLP network:
  - `self.fc1`: First fully connected layer that transforms input of size `input_size` to the hidden layer of size `hidden_size`.
  - `self.fc2`: Second fully connected layer, which maps the hidden layer back into a hidden space.
  - `self.fc3`: Third fully connected layer, which maps the hidden space to the final output of size `output_size`.
  - The network can handle both binary classification (`output_size=1`) or multi-class classification (`output_size > 1`).

#### 4. **Forward Pass**:
- The `forward` method defines the computation that happens when data is passed through the network:
  1. **Layer 1**: Input `x` is passed through the first fully connected layer (`self.fc1`), followed by the `ReLU` activation function.
  2. **Layer 2**: The output from the first layer is passed through the second fully connected layer (`self.fc2`), again followed by `ReLU`.
  3. **Layer 3**: The output from the second layer is passed through the third fully connected layer (`self.fc3`).
  4. **Activation Function**: 
     - If the output size is 1 (for binary classification), a **sigmoid** activation function is applied to get a probability value between 0 and 1.
     - If the output size is greater than 1 (for multi-class classification), a **softmax** function is used to produce a probability distribution over the classes.

#### 5. **Output**:
- The final output (`y_hat`) of the network is either a single probability (binary classification) or a probability distribution (multi-class classification), depending on the `output_size`.


```python
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data as data_utils

class MLPNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLPNetwork, self).__init__()
        """
        In the constructor we instantiate three nn.Linear modules and assign them to the three layers.
        The parameters of this constructor are:
            first parameter: input dimension
            second parameter: dimension of the hidden layers
            third parameter: output dimension
        """
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.fc2 = nn.Linear(hidden_size, hidden_size) 
        self.fc3 = nn.Linear(hidden_size, output_size)  
        self.output_size = output_size
    
    def forward(self, x):
        # First fully connected layer,  out = out^T W_1 + b_1
        out = self.fc1(x)
        # Activation function (sigmoid, relu, tanh, ...)
        out = torch.relu(out)
        # Second fully connected layer out = out^T W_2 + b_2
        out = self.fc2(out)
        # Activation function (sigmoid, relu, tanh, ...)
        out = torch.relu(out)
        # Third fully connected layer out = out^T W_3 + b_3
        out = self.fc3(out)
        # Final activation function (log of the sigmoid)
        if self.output_size == 1:
            y_hat = torch.sigmoid(out)
        else:
            y_hat = F.softmax(out,dim=0)  # dim is the dimension along the softmax will be computed
        return y_hat
    
```

## 6.2.1. Instantiate Feedforward Neural Network Object

This part of the code initializes the neural network classifier and sets it up for training, ensuring the model is deployed on the appropriate device (GPU or CPU).

#### 1. **Create the Neural Network Classifier**:
```python
MLP = MLPNetwork(input_size = 2, hidden_size=20, output_size = 1).to(device=device)
```
- **MLPNetwork**: This is our FF (MLP) neural network class.
- **input_size**: The number of input features for the network, set to 2 for our `two moons` training data.
- **hidden_size**: The size of the hidden layers in the network, set to 20, meaning each hidden layer has 20 neurons.
- **output_size**: The number of output neurons, set to 1 since `two moons` is a binary classification task.
- **.to(device=device)**: Moves the model to either the **GPU** or **CPU**, depending on the `device` variable. This ensures that the computations are performed on the right hardware for faster execution if GPU is available.



```python
    
    # Create the neural network classifier object in GPU or CPU memory (depending on device)
MLP = MLPNetwork(input_size = 2, hidden_size=20, output_size = 1).to(device=device)
```

## 6.3. Model Search: Optimizing model via gradient descent

We now implement a basic training loop for the **MLPNetwork** model, performing **gradient descent** to improve our `score` for 10,000 epochs, with periodic accuracy checks.

1. **Training Loop** (`for epoch in range(10000):`):
   - Iterates for 10,000 epochs (10,000 passes over the entire training data), updating the model's weights in each iteration.

2. **Model Prediction**:
   ```python
   y_pred = MLP(torch_X_train)
   ```
   - The input training data (`torch_X_train`) is passed through the model (`MLP`) to predict outputs (`y_pred`).

3. **Class Prediction**:
   ```python
   pred = y_pred.gt(0.5) + 0.0
   ```
   - Converts the predicted probabilities (`y_pred`) into binary class predictions (`1` or `0`) based on a threshold of `0.5`.
   - `.gt()` implements "greater than".

4. **Accuracy Calculation**:
   - Every 1000 epochs, the model's training accuracy is computed and printed:
   ```python
   correct = pred.eq(torch_y_train.view_as(pred)).sum().item()
   print(f'Epoch {epoch} training accuracy: {int(correct/torch_y_train.shape[0] * 100)}%')
   ```

5. **Error Computation**:
   ```python
   NLLscore = score(y_pred, torch_y_train.view(-1, 1))
   ```
   - The error (loss) between the predicted values and actual labels is computed using the `score` function
   - `.view(-1,1)` adjusts the tensor dimensions of the `y` input to avoid warnings.

6. **Gradient Zeroing**:
   ```python
   MLP.zero_grad()
   ```
   - Clears existing gradients from previous steps, as PyTorch accumulates gradients by default.

7. **Backpropagation**:
   ```python
   NLLscore.backward()
   ```
   - Computes gradients through backpropagation based on the negative log-likelihood score `NLLscore`.

8. **Gradient Descent**:
   ```python
   for f in MLP.parameters():
       f.data.sub_(f.grad.data * learning_rate)
   ```
   - Updates each parameter of the model using gradient descent, subtracting the product of the gradient and the learning rate.


```python
for epoch in range(10000):
    ## Predict values using updated model
    y_pred = MLP(torch_X_train)
    
    ## Find predicted class (as a number {1,0})
    pred = y_pred.gt(0.5) + 0.0
    
    # Compute accuracy
    if epoch % 1000 == 9:
        correct = pred.eq(torch_y_train.view_as(pred)).sum().item()
        print(f'Epoch {epoch} training accuracy: {int(correct/torch_y_train.shape[0] * 100)}%')

    ## Compute the new score
    NLLscore = score(y_pred, torch_y_train.view(-1,1)) ## .view(-1,1) avoids a warning about the tensor dimension
    
    MLP.zero_grad() ## Zero current gradients (Pytorch accumulate gradients by default)

    NLLscore.backward() ## Compute gradients in Pytorch via backpropagation
    
    ## Gradient descent:
    #     Go over all parameters and subtract their gradient * learning_rate
    for f in MLP.parameters():
        f.data.sub_(f.grad.data * learning_rate)

## Final train accuracy
if epoch % 100 == 9:
    correct = pred.eq(torch_y_train.view_as(pred)).sum().item()
    print(f'Correct {int(correct/torch_y_train.shape[0] * 100)}%')
```

    Epoch 9 training accuracy: 49%
    Epoch 1009 training accuracy: 86%
    Epoch 2009 training accuracy: 88%
    Epoch 3009 training accuracy: 89%
    Epoch 4009 training accuracy: 89%
    Epoch 5009 training accuracy: 91%
    Epoch 6009 training accuracy: 93%
    Epoch 7009 training accuracy: 96%
    Epoch 8009 training accuracy: 98%
    Epoch 9009 training accuracy: 99%


## 6.4. Model Evaluation

- We now prepare the model for evaluation by disabling gradient computation using `torch.no_grad()` and set the model to evaluation mode (`MLP.eval()`). 
- We will then predict the labels for the test set (`torch_X_test`), compute the accuracy by comparing predictions (`y_pred`) with true labels (`torch_y_test`), and visualize the predictions with a scatter plot.


```python
# Prepare model for evaluation (needed to avoid computing gradient)
with torch.no_grad():
    # Prepares model for evaluation (needed to avoid computing gradient)
    #  hence, the torch.no_grad() directive
    MLP.eval()
    # Predict the distribution of label
    y_hat = MLP(torch_X_test)
    # Get label by picking the most probable one
    y_pred = y_hat.gt(0.5) + 0.0

    # Accuracy of predictions with the true labels and take the percentage
    # Because our dataset is balanced, measuring just the accuracy is OK
    correct = y_pred.eq(torch_y_test.view_as(y_pred)).sum().item()
    print(f'Correctly classified test examples {int(correct/torch_y_test.shape[0] * 100)}%')

    pylab.scatter(X_test[:,0], X_test[:,1], c=y_pred)
    pylab.show()
```

    Correctly classified test examples 99%



    
![png](neuralNetworks_files/neuralNetworks_73_1.png)
    



```python

```
