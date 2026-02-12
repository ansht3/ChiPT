## CS37300 - Data Mining & Machine Learning
### Fall 2025
#### Instructor & Copyright: Bruno Ribeiro


# Convolutional Neural Networks (CNNs)

### Learning objectives

1. Understand CNN fundamentals: Architecture, convolutional/pooling layers, and their advantages for spatial data.
2. Master key operations: Convolution, padding, striding, and filter functions.
3. Understand convolution Feature Maps and their properties / shortcomings.
4. Implement CNNs: Build models for image tasks using PyTorch.
5. Train & optimize: use data augmentation and tune hyperparameters.

### CNNs for Image Tasks

- **(Supervised learning)** Image classification
    - ImageNet dataset:

<img src="ImageNet.png"  width=500px height=300px>

- **(Unsupervised learning)** CNNs can also be used to generate images

# 1. Tasks  

Students will gain hands-on experience with the following CNN applications:  

**Image Classification**:  
Given a dataset of labeled images $\{({\bf X}_i, y_i)\}_{i=1}^N$, where ${\bf X} \in \mathbb{R}^{3 \times n \times m}$ represents an $n \times m$ RGB image, design and train a CNN to learn the conditional probability distribution $$P(Y = y_i \mid {\bf X_i})$$ The goal is to accurately classify images into predefined categories.  

**Image Super-Resolution**:  
Given pairs of low-resolution (LR) and high-resolution (HR) images $\{({\bf X}_i, {\bf Y}_i)\}$, where ${\bf X}_i \in \mathbb{R}^{n \times n}$ and ${\bf Y}_i \in \mathbb{R}^{2n \times 2n}$, train a CNN to map LR images to their corresponding HR versions. This involves optimizing the network to minimize the difference between the generated HR image and the ground truth, assuming a Normal distribution for the errors.  
$$P(Y = {\bf Y}_i \mid {\bf X}_i).$$

<center><img src="superres_results.png" width="80%"/></center>

**Additional Tasks**:  
- **Object Detection**: Implement a CNN to detect and localize objects within an image (e.g., bounding box prediction).  
- **Semantic Segmentation**: Train a model to assign a class label to each pixel in an image.  
- **Style Transfer**: Explore CNNs for artistic style transfer between images.  
- **Image/Video generation**: CNNs can also be used to generate images and videos.

By completing these tasks, students will develop practical skills in building, training, and evaluating CNNs for diverse computer vision challenges.

## 1.1. Image Classification with MLPs

Vector inputs are useful for a variety of tasks, but in some tasks the data structure contains information

- MLPs (Feedforward networks) can be used for image classification tasks.
- Task input: The input is a $n \times m \times C$ tensor ${\bf X}$: $C$ matrices, each $n \times m$, representing images in $C$ colors.
    - MLP input: vectorize $\text{vec}({\bf X})$
    - We will call each "color" as a "channel"
        - Sometimes a channel will encode light intensity rather than a "color"
    - MLP output: softmax output predicting $P(Y=y | {\bf X})$

<center><img src="MLPforImages.png" width=1000px height=500px></center>

## 1.2. Convolutional Neural Networks

Convolutional neural networks will take advantage of pixel locality to more easily learn local pixel structure.
- This is what we call an inductive bias (we are adding some world knowledge to our neural network)

Local pixel structural information will be extracted as a filter.
- Based on the concept of local convolutions

### CNNs: The revolution in image processing
<img src="EvolutionOfImagClass.png">

### CNNs: The revolution comes at a computational cost
<img src="EvolutionOfImagClass1.png">

[Image credit](https://ai.googleblog.com/2019/05/efficientnet-improving-accuracy-and.html)


## 2. Understanding 2D Convolutions

In what follows, we will learn about 2D convolutions



```python
%matplotlib inline
import matplotlib.pyplot as plt

def show(img, title=None, cmap_='Greys'):
    ## converting to a CPU memory numpy array
    npimg = img.cpu().numpy()
    if title != None:
        print(title)
    plt.imshow(npimg, cmap=cmap_, vmin=0,  interpolation='nearest')

```

### Loading the MNIST data using Pytorch

Now we will:
- Define image size
- Define batch size
- Check if CUDA GPUs are available


```python
import torch
from   torchvision import datasets, transforms
import numpy as np
#from class_cnn import *


IMAGE_SIZE = int(28*28)
IMAGE_WIDTH = IMAGE_HEIGHT = 28

batch_size = 64

# Do we have GPUs available?
use_cuda = torch.cuda.is_available()
```

Next:
- Define device we will use for matrix computations (CPU or GPU)
    - We will use the variable ```device``` to define if the matrix computations will be on CPU or GPU
- Define how many threads will be used to load data from disk into the memory
    - Multiple threads are useful if we use multiple GPUs


```python
# Handy way to use GPUs if there are any
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# Data loader parameters
kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

# Load data
train_data = datasets.MNIST('../../data/mnist/', train=True, download=True , transform=transforms.ToTensor())
test_data  = datasets.MNIST('../../data/mnist/', train=False, download=True, transform=transforms.ToTensor())
train_loader = torch.utils.data.DataLoader(train_data, shuffle=True, batch_size=batch_size, drop_last=True, **kwargs)
test_loader = torch.utils.data.DataLoader(test_data, shuffle=False, batch_size=batch_size, drop_last=True, **kwargs)
```

### Example of training image

We now show a random training image

- Since MNIST images are B/W (Black & White), the tensor ${\bf X}$ is actually just a $28\times 28$ matrix


```python
import random
# Look at random example from training data
train_image, train_label = random.choice(train_data)

# Let's see which digit we got
train_image = train_image[0].view([1, 1, IMAGE_WIDTH, IMAGE_HEIGHT])
#train_label = train_image[1]
show(train_image.data[0][0],title="Original Image")

```

    Original Image



    
![png](CNNs_files/CNNs_16_1.png)
    


## 2.1. Step 1: Apply Convolutional Filter

### Step 1.1: Break the original image into image patches

-  Divide image into overlapping image patches based on stride (pad image corners with zeros if needed)
    - Patch (filter) size $k$ = patch is of size $k\times k$, $k \geq 2$
        - The filter is applied over $k \times k$ image patches (over each channel)
    - Stride = number of pixels we will skip after making the previous patch
        - These patches overlap accodring to stride, which is by how much each block must be separated horizontally and vertically. 
    - Padding = number of extra padding "0" values we add to the corners of the image
        - If $k$ is not a multiple of the image height of width, we will need padding (increase image height (width) by adding a row (column) of zeros).
- We will **not** save the image patches

### Patch Example

- To define a patch, we first need to define $k$
    - i.e., we must define the size of the $k \times k$ filter
- ```torch.FloatTensor``` creates a tensor in Pytorch
    - The parameter ```,device=device``` indicates which memory (CPU or GPU) will hold the tensor
    - The filter is a $1 \times k \times k$ tensor (since we only have a single B/W channel)


```python
# Filter has only a single channel as our image is black and white
W1 = torch.zeros((1,3,3), device=device)

# An arbitrary initial value for our filter (this is a special toy filter)
W1[0, :, :] = torch.tensor([[[-1, 0, 1],
                             [-1, 0, 1],
                             [-1, 0, 1]]],dtype=torch.float,device=device)

```

- We now define a patch
    - Patches must have a stride parameter
    - There is no padding for now (to simplify)


```python
# Defines patches
def conv_patch(img, filter_size, stride=1, willshow=False):
    
    if willshow:
        fig=plt.figure(figsize=(8, 8))
        cnt = 0

    # Iterate to segment the image for the convolution operation.
    i_vec = np.uint32(np.arange(filter_size/2, img.shape[0]-filter_size/2+1, step=stride))
    j_vec = np.uint32(np.arange(filter_size/2, img.shape[1]-filter_size/2+1, step=stride))
    for i in i_vec:
        for j in j_vec:
            img_region = img[(i-np.uint32(np.floor(filter_size/2))):(i+np.uint32(np.ceil(filter_size/2))), 
                             (j-np.uint32(np.floor(filter_size/2))):(j+np.uint32(np.ceil(filter_size/2)))]
            if willshow:
                cnt += 1
                no_i = i_vec.shape[0]
                no_j = j_vec.shape[0]
                ax = fig.add_subplot(no_i,no_j,cnt) #img.shape[0]//stride -stride, img.shape[1]//stride + stride, cnt)
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
                show(img_region)
    if willshow:
        plt.show()

```

Showing all image patches of my_filter (1x3x3 filter)


```python
conv_patch(train_image.data[0][0], filter_size=W1.shape[1], stride=2, willshow=True)
```


    
![png](CNNs_files/CNNs_24_0.png)
    


## Step 1.2: Applying the convolution filter


#### Convolutions:
- A convolution is a mathematical operation of two functions that produces a third function expressing how the shape of one is modified by the other (Wikipedia definition)
- In discrete spaces, it is (informally) defined as
$$
 (f * g)(i) = \sum_j f(j) g(i - j)
$$

**Applying the convolution filter**:
1. For each $C \times k \times k$  image patch ${\bf M}$
2. The filter has learnable parameters ${\bf W}_1$ which is a  $C \times k \times k$ tensor and $b_1 \in \mathbb{R}$ a scalar
3. Apply the filter (our filter defined above does not have a bias):
$$
\text{out} = \sigma(\text{sum}({\bf M} \odot {\bf W}_1) + b_1)
$$
     1. The operator $\odot$ is the Hadamard product (element-wise multiplication)
     2. The filter takes two $C \times k \times k$ tensors (${\bf M}$ and ${\bf W}_1$) and a scalar $b_1$.
     3. The operator $\text{sum}(\cdot)$ sums over all the values of a $C \times k \times k$ tensor.
4. The filter is really just a single-layer MLP with a single output neuron applied over a vectorized image patch of each channel

**Visual representation** of the convolution for the $i$-th channel:

Let $\text{vec}({\bf M})$ be the patch and $\text{vec}({\bf W}_i)$ be the parameters of the $i$-th filter in vector form, respectivelly:
 
<center>
<table><tr>
    <td> <img src="BlockToFilter.png" width=500px height=500px /> </td>
    <td> <img src="LatticeNeuron.png" width=400px height=400px /> </td>
 </tr></table>
</center>

### 2.2. Step 1.2: Feature Map
Then, we apply this convolution in layers, multiple times. Note that each pixel in the previous layer has a *convolution representation* in the next layer, which we will call a **Feature Map**.
<img src="LayeredCNN.png" width=400px height=400px>

Code for the *convolution* operation


```python
# Convolution with the filter

def convolve_with_filter(img, c_filter, stride=1, device=None, willshow=False):
    
    if willshow:
        fig=plt.figure(figsize=(8, 8))
        cnt = 0

    filter_size = c_filter.shape[1]
    
    c_filter = c_filter.view((filter_size*filter_size,1))

    result = torch.zeros(img.shape,device=device)
    
    img = img.to(device)
    #Looping through the image to apply the convolution operation.

    for i in np.uint32(np.arange(filter_size/2, img.shape[0]-filter_size/2+1, step=stride)):
        for j in np.uint32(np.arange(filter_size/2, img.shape[1]-filter_size/2+1, step=stride)):
            img_region = img[(i-np.uint32(np.floor(filter_size/2))):(i+np.uint32(np.ceil(filter_size/2))), 
                             (j-np.uint32(np.floor(filter_size/2))):(j+np.uint32(np.ceil(filter_size/2)))]
            
            # Linearizes both filter and region, and perform inner product of vectors. Result is a real number.
            #   .contiguous() is need to place the segmentation of the image into a contigous region of the memory
            result[i, j] = img_region.contiguous().view((-1,filter_size*filter_size)) @ c_filter 

    # Neuron output.
    output = torch.relu(result[np.uint32(filter_size/2):result.shape[0]-np.uint32(filter_size/2), 
                          np.uint32(filter_size/2):result.shape[1]-np.uint32(filter_size/2)])

    if willshow:
        cnt += 1
        # Shows the absolute values returned by the filter
        show(output.cpu())
                
    if willshow:
        plt.show()

    return output

```

Applying the filter over the input image: 
- The result is the next layer (called **Feature Map**)
- Note that our filter example ${\bf W}_1$ is a vertical edge detector


```python
## Remember our initial toy filter (a real CNN filter matrix is a parameter of the algorithm):
# W1[0, :, :] = torch.tensor([[[-1, 0, 1],
#                              [-1, 0, 1],
#                              [-1, 0, 1]]],dtype=torch.float,device=device)


conv_img = convolve_with_filter(train_image.data[0][0], c_filter=W1[0,:,:], stride=1, device=device, willshow=True)

```


    
![png](CNNs_files/CNNs_32_0.png)
    


### 2.2.1. An important CNN property of Feature Layers (Equivariant Transformation)

A function $f$ is said to be equivariant to a transformation $T$ if $$ T(f(x)) = f(T(x)).$$

- **CNN Convolutions are approximately shift-equivariant**
    - If $T$ is a shift operation over the image, then $$T(\text{convolve\_with\_filter}(x, \text{stride}=1)) \approx \text{convolve\_with\_filter}(T(x), \text{stride}=1),$$ the difference being at the image boundaries.
    
    
# Quiz:

What happens to feature maps when a number (or object) is moved within an image processed by a CNN?

A) The feature maps shift by the same amount as the movement but generally retain their original outputs (now shifted).

B) The feature maps remain unchanged and stay in their original positions.

C) The feature maps change in response to the movement, becoming different outputs.


```python
print("Original image")
show(train_image.data[0][0])
print("Original image after applying all convolutions")
conv_img = convolve_with_filter(train_image.data[0][0], c_filter=W1[0,:,:], stride=1, device=device, willshow=True)

print("--------------------")

print("Shifted image")
translated_image = transforms.functional.affine(train_image.data[0], angle=0, translate=(5,-5), scale=1, shear=[0])[0]
show(translated_image)
print("Shifted image after applying all convolutions")
conv_img = convolve_with_filter(translated_image, c_filter=W1[0,:,:], stride=1, device=device, willshow=True)
```

    Original image
    Original image after applying all convolutions



    
![png](CNNs_files/CNNs_34_1.png)
    



    
![png](CNNs_files/CNNs_34_2.png)
    


    --------------------
    Shifted image
    Shifted image after applying all convolutions



    
![png](CNNs_files/CNNs_34_4.png)
    



    
![png](CNNs_files/CNNs_34_5.png)
    


### CNNs Convolutions do not preserve rotations

If $T$ is a rotation operation over the image, then, for arbitrary convolution weights $$T(\text{convolve\_with\_filter}(x, \text{stride}=1)) \neq \text{convolve\_with\_filter}(T(x), \text{stride}=1),\quad \forall x.$$

Let's test if our CNN convolution is rotation equivariant



```python
print("Original image")
show(train_image.data[0][0])
print("Original image after applying all convolutions")
conv_img = convolve_with_filter(train_image.data[0][0], c_filter=W1[0,:,:], stride=1, device=device, willshow=True)

print("Rotated image")
rotated_image = transforms.functional.affine(train_image.data[0], angle=-90, translate=(0,0), scale=1, shear=[0])[0]
show(rotated_image)
print("Rotated image after applying all convolutions")
conv_img_rot = convolve_with_filter(rotated_image, c_filter=W1[0,:,:], stride=1, device=device, willshow=True)
```

    Original image
    Original image after applying all convolutions



    
![png](CNNs_files/CNNs_36_1.png)
    



    
![png](CNNs_files/CNNs_36_2.png)
    


    Rotated image
    Rotated image after applying all convolutions



    
![png](CNNs_files/CNNs_36_4.png)
    



    
![png](CNNs_files/CNNs_36_5.png)
    


## 2.3. Step 1.3: Downsampling via Pooling Layer

### Pooling Layer
<img src="Downsampled.png" width=600px>
- Pooling will output either the max or the average value of a feature map patch


```python
def max_pooling(img, filter_size=3, stride=1, device=None, willshow=False):
    
    if willshow:
        fig=plt.figure(figsize=(8, 8))
        cnt = 0

    result = torch.zeros(img.shape,device=device)
    
    img = img.to(device)
    #Looping through the image to apply the convolution operation.

    for i in np.uint32(np.arange(filter_size/2, img.shape[0]-filter_size/2+1, step=stride)):
        for j in np.uint32(np.arange(filter_size/2, img.shape[1]-filter_size/2+1, step=stride)):
            img_region = img[(i-np.uint32(np.floor(filter_size/2))):(i+np.uint32(np.ceil(filter_size/2))), 
                             (j-np.uint32(np.floor(filter_size/2))):(j+np.uint32(np.ceil(filter_size/2)))]
            
            # Max over window
            result[i, j] = torch.max(img_region.contiguous().view((-1,filter_size*filter_size))) 

    if willshow:
        cnt += 1
        # Shows the absolute values returbed by the filter
        show(torch.abs(result.cpu()))
                
    if willshow:
        plt.show()
    
    return result

```

Max pooling over $3\times 3$ patches of the previous feature map (stride = 2)


```python
## Remember our initial toy filter (a real CNN filter matrix is a parameter of the algorithm):
# W1[0, :, :] = torch.tensor([[[-1, 0, 1],
#                              [-1, 0, 1],
#                              [-1, 0, 1]]],dtype=torch.float,device=device)

print("Image after CNN convolution")
conv_img = convolve_with_filter(train_image.data[0][0], c_filter=W1[0,:,:], stride=1, device=device, willshow=True)

print("Image after max pooling")
max_pooled_img = max_pooling(conv_img, filter_size = 3, stride = 2, willshow=True)

```

    Image after CNN convolution



    
![png](CNNs_files/CNNs_41_1.png)
    


    Image after max pooling



    
![png](CNNs_files/CNNs_41_3.png)
    


## End of Convolutional Filter

## 2.4 Dealing with Color Images
- There are multiple ways to deal with RGB color images
    - The simplest way is to apply 3 different filters to form a single pixel in the feature map 
<img src="RGBFilter.png" width=600px>

### Colored CNN Filter Example 
- This example show the filters, the padding and the various filters
<img src="CNNstep.png" width=600px>

# 3. A Complete CNN Architecture for Image Classification with 2 classes

### Stack Multiple Convolutional Filters

- Use multiple filters per image channel (channel = "color")
    - Filters specialize, will learn to perform functions on "ears", "fur", "feet", etc.
- Last **feature map** becomes the *image* of the next set of filters 
- We can reshape multiple feature maps to become a real image
A CNN will alternate convolution filters, pooling filters, and finally a feedforward network at the end.
<center><img src="CNN.svg" width=2000px/></center>

# 4. Data Agumentation: Making CNNs robust to image transformations?

Note that our vectorization of image patches leave the output of the filter **rotation-sensitive**. 

- That is, consider the following image of a bird and the various rotation orientations that patches of this bird can be found in images:

<img src="Bird.jpg" width=150px height=150px>

#### Ideally, we would like patches to be permutation-invariant:
<table align="center">
  <tr>
    <th>Patch Version 1</th>
    <th>Patch Version 2</th> 
    <th>Patch Version 3</th>
  </tr>
  <tr>
    <td><img src="Bird1.png" width=100px height=100px></td>
    <td><img src="Bird2.png" width=100px height=100px></td> 
    <td><img src="Bird3.png" width=100px height=100px></td>
  </tr>
</table> 


### Data Agumentation (Most Flexible & Common Solution)

- Ideally, CNNs should be trained to be translation and rotation-invariant. However, existing CNN architectures are not rotation and translation invariant.

- Cropping, Rotation, Translation, Illumination are data augmentation hacks that can help a neural network become more rotation / translation invariant

- At each gradient descent step, randomly rotate, translate, and change the illumination of the mini-batch images
    - This is equivalent to adding these random transformations to the dataset
    - But computationally cheaper, since we simply transform the original data when we load the data into the GPU rather than adding a new image to our dataset

<img src="my6.png" width=400px height=400px>

```python
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(size=(224,224), scale=(0.6, 1.0), ratio=(0.75, 1.3333333333333333), interpolation=transforms.functional.InterpolationMode.BICUBIC),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(degrees=(-30,30), resample=False, expand=False, fill=(0,0,0)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean and std of ImageNet
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean and std of ImageNet
        ]),
    }
```

## More complex data agumentation

- Transformations can also include events that do not happen in our data but we want to be able to handle
- For instance, suppose we want to develop a self-driving vision system
    - In our dataset we only have images of people and pets walking on sidewalks and crossing streets
    - In an emergency, we may see people and pets running in the middle of a highway
    - Data augmentation solution: Create a transformation of the data where we add people running on in the middle of a highway and with the label "do not run over"


```python
from IPython.display import HTML

HTML("""
<center><h2>Tesla AI Day: Aug, 2021</h2> <h3> Example of data augmentation for the Tesla CNN: People running on highway</h3></center>
    <video alt="Tesla" controls width=400px>
        <source src="Tesla.mp4" type="video/mp4">
    </video>
""")
```





<center><h2>Tesla AI Day: Aug, 2021</h2> <h3> Example of data augmentation for the Tesla CNN: People running on highway</h3></center>
    <video alt="Tesla" controls width=400px>
        <source src="Tesla.mp4" type="video/mp4">
    </video>




# 5. An Example Beyond Image Classification
# Super-Resolution Convolutional Neural Network Example

We will now explore a **super-resolution neural network** – a CNN that takes low-resolution images and generates high-resolution versions. Our specific task is to upscale images from 225×300 pixels to 450×600 pixels (a 2x increase in each dimension).

This implementation is based on the concepts introduced in [Shi et al., 2016](https://arxiv.org/abs/1609.05158)
<center><img src="PixelShuffle.png" width-"60%"></center>

## What is Super-Resolution?

Super-resolution is the process of enhancing image resolution beyond what's captured by the sensor. Unlike simple interpolation (like "zooming in" on an image in Photoshop), neural networks can learn to intelligently fill in missing details based on patterns they've seen in training data.

**Applications:**
- Enhancing old photos or videos
- Medical imaging (MRI, CT scans)
- Satellite imagery
- Forensics
- Improving low-quality surveillance footage

## The Challenge

When we upscale an image, we need to create 4× as many pixels (2× width × 2× height). The challenge is: **where does this new information come from?**

Traditional methods (bilinear interpolation, bicubic interpolation) simply smooth between existing pixels, resulting in blurry images. Our CNN learns to predict what the high-resolution details should look like based on the low-resolution input.

## Network Architecture

Our `SuperResCNN` consists of three main components:

### 1. Feature Extraction (Learning What Matters)
```python
        # Feature extraction layers - learn to recognize patterns like edges and textures
        self.conv1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)   # First conv layer
        self.conv2 = nn.Conv2d(64, 64, kernel_size=5, padding=2)   # Second conv layer
        self.conv3 = nn.Conv2d(64, 32, kernel_size=5, padding=2)   # Third conv layer
```

**Description of feature extraction layers:**
- **First Conv Layer**: Takes 3-channel RGB input and produces 64 feature maps
  - Kernel size 9×9 is relatively large, allowing the network to see broader context
  - These filters learn to detect edges, textures, and basic patterns
  
- **Second Conv Layer**: Refines the 64 feature maps into another 64 feature maps
  - Smaller 5×5 kernel focuses on local refinements
  - Learns more complex patterns built from the first layer's features

- **Third Conv Layer**: Compresses to 32 feature maps
  - Reduces dimensionality before upsampling
  - Creates a compact representation of the important features

**Why multiple layers?**
Each layer builds on the previous one:
- Layer 1 might detect edges
- Layer 2 might detect corners and simple shapes
- Layer 3 might detect textures like fabric, wood grain, or facial features

### 2. Upsampling (The Key Idea: Sub-Pixel Convolution)
```python
self.upsample_conv = nn.Conv2d(32, 3 * 4, kernel_size=3, padding=1)
self.pixel_shuffle = CustomPixelShuffle(upscale_factor=2)
```

This is where we actually increase the spatial resolution. But how?

#### The Sub-Pixel Convolution Trick

Instead of upscaling the image first (which would require interpolation), we use a clever rearrangement:

1. **Generate extra channels**: The convolution produces 12 channels ($3 \times 2^2$)
   - Why 12? Because we want 3 RGB channels at 2× resolution
   - 3 channels × (2 × 2 grid) = 12 channels

2. **Rearrange channels into space**: The `CustomPixelShuffle` operation transforms:
   - Input: (Batch, 12, Height, Width)
   - Output: (Batch, 3, Height×2, Width×2)

**How PixelShuffle Works:**

Let's visualize with a simple example. Suppose we have 4 channels at 2×2 resolution:
```
Channel 0:  [A B]    Channel 1:  [E F]
            [C D]                [G H]

Channel 2:  [I J]    Channel 3:  [M N]
            [K L]                [O P]
```

PixelShuffle rearranges these into 1 channel at 4×4 resolution:
```
Output: [A E I M]
        [B F J N]
        [C G K O]
        [D H L P]
```

Each 2×2 block in the channels becomes a single pixel's neighborhood!
<center><img src="PixelShuffle.png" width-"60%"></center>

#### Custom PixelShuffle Implementation

Here's our hand-made version that shows exactly what's happening:
```python
class CustomPixelShuffle(nn.Module):
    def forward(self, x):
        r = self.upscale_factor  # r = 2
        b, c, h, w = x.shape     # e.g., (4, 12, 225, 300)
        
        # Step 1: Reshape to separate upscale groups
        # (4, 12, 225, 300) → (4, 3, 2, 2, 225, 300)
        x = x.reshape(b, c // (r**2), r, r, h, w)
        
        # Step 2: Permute to interleave spatial information
        # (4, 3, 2, 2, 225, 300) → (4, 3, 225, 2, 300, 2)
        x = x.permute(0, 1, 4, 2, 5, 3)
        
        # Step 3: Collapse into spatial dimensions
        # (4, 3, 225, 2, 300, 2) → (4, 3, 450, 600)
        x = x.reshape(b, c // (r**2), h * r, w * r)
        
        return x
```

**Why is this better than interpolation?**
- The convolution learns how to generate these extra channels
- The network decides what information goes into each spatial position
- This is learned from data, not just mathematical smoothing


### 3. Refinement (Polishing the Output)
```python
self.refine = nn.Conv2d(3, 3, kernel_size=3, padding=1)
```

After upsampling, there might be small artifacts or inconsistencies. This final 3×3 convolution:
- Smooths out any blocky artifacts from the pixel shuffle
- Ensures color consistency across the image
- Fine-tunes the final output

Please download [myutilities.py](myutilities.py) and run in the same folder of your notebook.

## Forward Pass: Putting It All Together
```python
def forward(self, x):
    # Input: (B, 3, 225, 300), where B is the batch size (how many images we will computer in one forward pass)
    
    # Feature extraction with non-linearity
    x = torch.relu(self.conv1(x))  # (B, 64, 225, 300)
    x = torch.relu(self.conv2(x))  # (B, 64, 225, 300)
    x = torch.relu(self.conv3(x))  # (B, 32, 225, 300)
    
    # Upsampling
    x = self.upsample_conv(x)      # (B, 12, 225, 300)
    x = self.pixel_shuffle(x)      # (B, 3, 450, 600)
    
    # Refinement
    x = self.refine(x)             # (B, 3, 450, 600)
    
    return x
```
<center><img src="SuperResolutionSchema.svg" width="100%"/></center>


```python
"""
=============================================================================
SUPER-RESOLUTION MODEL EVALUATION
=============================================================================
This notebook demonstrates how to:
1. Load a trained super-resolution neural network
2. Test it on unseen data
3. Visualize the results with before/after comparisons
4. Calculate quantitative metrics (MSE and PSNR)

Super-resolution is the task of taking a low-resolution image and generating
a high-resolution version. Our model takes 225x300 images and outputs 450x600
images (2x upscaling).

A 2GB VRAM GPU is enough for the neural network
=============================================================================
"""


# Import necessary libraries for deep learning, image processing, and visualization
import torch  # Core PyTorch library for tensor operations and neural networks
import torch.nn as nn  # Neural network module from PyTorch
import torch.optim as optim  # Optimization algorithms (like Adam, SGD)
from torch.utils.data import Dataset, DataLoader, random_split  # Data utilities
from torchvision import transforms  # Image transformations
from PIL import Image  # Python Imaging Library for image handling
import os  # Operating system interface for file operations
import myutilities


# Set device and enable BF16 if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Use GPU if available, otherwise CPU
use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()  # Check if BF16 (bfloat16) is supported on the GPU
print(f"Using device: {device}")  # Print which device is being used
print(f"BF16 enabled: {use_bf16}")  # Print whether BF16 is enabled
```

    Using device: cpu
    BF16 enabled: False



```python
# Load and prepare the dataset
print("Loading dataset...")
dataset = myutilities.ImageSuperResDataset('./data/kaggle/train_x', './data/kaggle/train_y')

# Split dataset into training, validation, and test sets (70%/15%/15%)
total_size = len(dataset)
train_size = int(0.70 * total_size)  # 70% for training
val_size = int(0.15 * total_size)    # 15% for validation
test_size = total_size - train_size - val_size  # Remaining 15% for testing

# Use random_split to create subsets and set a seed for reproducibility
# We do not need the train and validation data now
_, _, test_dataset = random_split(
    dataset, [train_size, val_size, test_size],
    generator=torch.Generator().manual_seed(42)  # Fixed seed for consistent splits
)
print(f"Test samples: {len(test_dataset)}")

# Create data loaders for efficient batch processing
batch_size = 10  # Number of images to process in each batch (adjust based on GPU memory)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
```

    Loading dataset...
    Test samples: 383



```python
# =============================================================================
# SETUP: Device Configuration
# =============================================================================
# Check if GPU is available - neural networks run much faster on GPUs
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# =============================================================================
# MODEL ARCHITECTURE DEFINITIONS
# =============================================================================

# =============================================================================
# CUSTOM PIXEL SHUFFLE IMPLEMENTATION
# =============================================================================
class CustomPixelShuffle(nn.Module):
    """
    Hand-made implementation of PixelShuffle (also known as sub-pixel convolution).
    PyTorch has an implementation of it called nn.PixelShuffle
    
    This operation rearranges elements in a tensor from depth to spatial dimensions.
    It's a clever way to upscale images using learned convolutions instead of 
    simple interpolation.
    
    How it works:
    - Input:  (batch, channels * r^2, height, width)
    - Output: (batch, channels, height * r, width * r)
    
    where r is the upscale factor.
    
    Example with r=2:
    - Input:  (B, 12, 100, 100) where 12 = 3 * 2^2
    - Output: (B, 3, 200, 200)
    
    The magic is in the reshaping and permutation that rearranges the channel
    data into spatial locations.
    """
    def __init__(self, upscale_factor):
        super(CustomPixelShuffle, self).__init__()
        self.upscale_factor = upscale_factor
        
    def forward(self, x):
        """
        Rearrange tensor to increase spatial resolution.
        
        Args:
            x: Input tensor of shape (batch, channels * r², height, width)
            
        Returns:
            Output tensor of shape (batch, channels, height * r, width * r)
        """
        r = self.upscale_factor
        
        # Get input dimensions
        b, c, h, w = x.shape
        
        # Step 1: Reshape to separate the upscale factor from channels
        # (b, c, h, w) -> (b, c/r², r, r, h, w)
        # This groups the channels that will become spatial pixels
        x = x.reshape(b, c // (r**2), r, r, h, w)
        
        # Step 2: Permute dimensions to interleave spatial information
        # (b, c/r², r, r, h, w) -> (b, c/r², h, r, w, r)
        # This moves the r×r blocks next to their spatial positions
        x = x.permute(0, 1, 4, 2, 5, 3)
        
        # Step 3: Collapse the r dimensions into spatial dimensions
        # (b, c/r², h, r, w, r) -> (b, c/r², h*r, w*r)
        # Now we have increased spatial resolution!
        x = x.reshape(b, c // (r**2), h * r, w * r)
        
        return x

    
```

    Using device: cpu



```python
# =============================================================================
# SUPER RESOLUTION CNN
# =============================================================================
   
class SuperResCNN(nn.Module):
    """
    A Convolutional Neural Network for 2x image super-resolution.
    
    Architecture:
    - Feature extraction: 3 convolutional layers to learn image patterns
    - Upsampling: Sub-pixel convolution (PixelShuffle) to increase resolution
    - Refinement: Final conv layer to polish the output
    
    Input:  3-channel RGB image of size 225x300
    Output: 3-channel RGB image of size 450x600 (2x larger)
    """
    def __init__(self):
        super(SuperResCNN, self).__init__()
        # Feature extraction layers - learn to recognize patterns like edges and textures
        self.conv1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)   # First conv layer
        self.conv2 = nn.Conv2d(64, 64, kernel_size=5, padding=2)   # Second conv layer
        self.conv3 = nn.Conv2d(64, 32, kernel_size=5, padding=2)   # Third conv layer
        
        # Upsampling branch - increases image resolution by 2x
        self.upsample_conv = nn.Conv2d(32, 12, kernel_size=3, padding=1)
        # We could use PyTorch's implementation of PixelShuffle
        # self.pixel_shuffle = nn.PixelShuffle(upscale_factor=2)      # Rearranges channels to spatial dimensions
        # But we will be using our own implementation of PixelShuffle
        self.pixel_shuffle = CustomPixelShuffle(upscale_factor=2)
        
        # Final refinement layer - smooths out artifacts
        self.refine = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        """
        Forward pass through the network
        Args:
            x: Input tensor of shape (batch_size, 3, 225, 300)
        Returns:
            Output tensor of shape (batch_size, 3, 450, 600)
        """
        # Feature extraction with ReLU activation
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        
        # Upsampling to increase resolution
        x = self.upsample_conv(x)
        x = self.pixel_shuffle(x)
        
        # Final refinement
        x = self.refine(x)
        return x
```


```python
# =============================================================================
# LOAD THE TRAINED MODEL
# =============================================================================
print("\n" + "="*70)
print("LOADING TRAINED MODEL")
print("="*70)

# Create model instance and load saved weights
model = SuperResCNN().to(device)

try:
    # Attempt to load the best saved model weights in training onto the appropriate device (GPU or CPU)
    model.load_state_dict(torch.load('best_superres_model.pth', map_location=device))
    
    # Set the model to evaluation mode (disables dropout/batchnorm training behavior)
    model.eval()
    
    # Print confirmation message with parameter count
    print(f"Model loaded successfully with {sum(p.numel() for p in model.parameters()):,} parameters")
    
except FileNotFoundError:
    print("Warning: 'best_superres_model.pth' not found. Using the current model state.")
except Exception as e:
    print(f"Error loading model: {e}. Using the current model state.")
```

    
    ======================================================================
    LOADING TRAINED MODEL
    ======================================================================
    Model loaded successfully with 172,864 parameters



```python
# =============================================================================
# MAIN EVALUATION
# =============================================================================
print("\n" + "="*70)
print("TESTING SUPER-RESOLUTION MODEL")
print("="*70)

# Part 1: Visualize examples from the test set
print("\n1/2: Generating visualizations from test set...")
myutilities.visualize_super_resolution(model, test_loader, device, num_examples=5)

# Part 2: Calculate metrics on the full test set
#print("\n2/2: Calculating metrics on full test set...")
#avg_mse, avg_psnr = myutilities.evaluate_metrics(model, test_loader, device)

print("\n" + "="*70)
print("Done.")
print("="*70)
```

    
    ======================================================================
    TESTING SUPER-RESOLUTION MODEL
    ======================================================================
    
    1/2: Generating visualizations from test set...
    
    Generating super-resolution for 5 test images...
      Example 1 - MSE: 0.002435, PSNR: 26.14 dB
      Example 2 - MSE: 0.004247, PSNR: 23.72 dB
      Example 3 - MSE: 0.000933, PSNR: 30.30 dB
      Example 4 - MSE: 0.000173, PSNR: 37.62 dB
      Example 5 - MSE: 0.000318, PSNR: 34.98 dB



    
![png](CNNs_files/CNNs_67_1.png)
    


    
    ======================================================================
    Done.
    ======================================================================


# 6. A Complete Example of Image Classification

- In what follows we will present a CNN with 2 convolutional layers followed by a 2-hidden layer MLP.
    - Convolution kernels take 8x8 patches and have stride = 2
    - ReLU activations (except for last softmax output)
- The task: Classify animals in images as *ants* or *bees*
    - Input images have different sizes, must be cropped by torchvision's transforms.Compose() transforms.RandomResizedCrop
    - It is always a good idea to normalize the images, in order to make the input less sensitive to different exposures
    - Data folder must be organized as (data link: [here](data.zip)) 
    ```
        data  --+
                |-train
                |---ants
                |---bees
                |-val
                |---ants
                |---bees
```

<center><img src="CNN.svg" width=2000px/></center>


```python
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import os
import numpy as np
import copy
import time


# Show images
def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406]) # mean of ImageNet
    std = np.array([0.229, 0.224, 0.225]) # std of ImageNet
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


plt.ion()   # interactive mode
```




    <contextlib.ExitStack at 0x137bf4950>




```python
# Load data with data augmentation transformations

def load_data(data_dir, batch_size = 32):
    global b_size

    b_size = batch_size

    # Data augmentation and normalization for training
    # Just normalization for validation

    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(size=(224,224), scale=(0.6, 1.0), ratio=(0.75, 1.3333333333333333), interpolation=transforms.functional.InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean and std of ImageNet
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean and std of ImageNet
        ]),
    }

    # Read dataset from real jpeg images inside folder data_dir
    # Folder must be organized as 
    #     data_dir --+
    #                |-train
    #                |---ants
    #                |---bees
    #                |-val
    #                |---ants
    #                |---bees
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    data_loaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size,shuffle=True, pin_memory=True, drop_last=True, num_workers=4) for x in ['train', 'val']}
    
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    
    class_names = image_datasets['train'].classes
    
    return data_loaders, dataset_sizes, class_names


```


```python
data_loaders, dataset_sizes, class_names = load_data(data_dir='./data/antsbees', batch_size=32)

# Get a batch of training data
inputs, classes = next(iter(data_loaders['train']))
# Make a grid from batch
out = torchvision.utils.make_grid(inputs)
,
imshow(out, title="Mini-batch")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```


    
![png](CNNs_files/CNNs_71_0.png)
    



```python
# CNN takes 3-channel images as input
# 
class CNNNet(nn.Module):
    def __init__(self):
        super(CNNNet, self).__init__()
        #  out_channels defines how many filters we will have
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=100, kernel_size=8, stride=2)
        self.pool = nn.MaxPool2d(kernel_size=5, stride=2)
        self.conv2 = nn.Conv2d(in_channels=100, out_channels=32, kernel_size=8, stride=2)
        # Next is the feedforward neural network part
        self.fc1 = nn.Linear(32 * 10 * 10, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        # First CNN convolution + activation + pooling
        x = torch.relu(self.conv1(x))
#        print(f'conv1 {x.shape}')
        x = self.pool(x)
#        print(f'pool1 {x.shape}')
        # Second CNN convolution + activation + pooling
        x = torch.relu(self.conv2(x))
#        print(f'conv2 {x.shape}')
        x = self.pool(x)
#        print(f'pool2 {x.shape}')
        # Make the feature maps into vectors
        x = x.view(-1, 32 * 10 * 10)
        # Feed vectors to feedforward networks
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        # Model does not need to output the softmax because the CrossEntropyLoss already computes the softmax for us
        return x

model = CNNNet().to(device)
```


```python
print(model)
```

    CNNNet(
      (conv1): Conv2d(3, 100, kernel_size=(8, 8), stride=(2, 2))
      (pool): MaxPool2d(kernel_size=5, stride=2, padding=0, dilation=1, ceil_mode=False)
      (conv2): Conv2d(100, 32, kernel_size=(8, 8), stride=(2, 2))
      (fc1): Linear(in_features=3200, out_features=120, bias=True)
      (fc2): Linear(in_features=120, out_features=84, bias=True)
      (fc3): Linear(in_features=84, out_features=2, bias=True)
    )



```python
module = model.conv1
print(f'Number of weight parameters in first conv layer: {len(list(module.weight))}')
print(list(module.named_parameters()))

```

    Number of weight parameters in first conv layer: 100
    [('weight', Parameter containing:
    tensor([[[[-0.0366, -0.0613,  0.0399,  ..., -0.0335,  0.0707,  0.0340],
              [-0.0224, -0.0522,  0.0135,  ..., -0.0521,  0.0245, -0.0554],
              [ 0.0038,  0.0360,  0.0175,  ...,  0.0192, -0.0245, -0.0583],
              ...,
              [ 0.0183,  0.0321, -0.0450,  ...,  0.0281,  0.0074,  0.0578],
              [-0.0267,  0.0545, -0.0169,  ..., -0.0282, -0.0108, -0.0268],
              [ 0.0196, -0.0246,  0.0244,  ...,  0.0449, -0.0652, -0.0645]],
    
             [[-0.0699, -0.0377,  0.0249,  ...,  0.0276,  0.0266,  0.0124],
              [ 0.0068,  0.0422,  0.0197,  ..., -0.0684,  0.0423,  0.0365],
              [ 0.0538, -0.0556,  0.0467,  ..., -0.0657, -0.0243,  0.0481],
              ...,
              [ 0.0082,  0.0188, -0.0031,  ...,  0.0025, -0.0303,  0.0418],
              [ 0.0338,  0.0327,  0.0200,  ...,  0.0605, -0.0265, -0.0720],
              [-0.0102, -0.0162,  0.0296,  ...,  0.0385, -0.0223, -0.0273]],
    
             [[ 0.0487, -0.0628,  0.0038,  ..., -0.0035, -0.0657,  0.0702],
              [ 0.0649,  0.0484, -0.0117,  ...,  0.0040,  0.0556,  0.0002],
              [ 0.0044, -0.0160,  0.0442,  ...,  0.0663, -0.0317,  0.0091],
              ...,
              [ 0.0106,  0.0691,  0.0071,  ..., -0.0208, -0.0082,  0.0681],
              [ 0.0175,  0.0427, -0.0425,  ..., -0.0027, -0.0450,  0.0221],
              [ 0.0639, -0.0164, -0.0219,  ..., -0.0461,  0.0026,  0.0597]]],
    
    
            [[[ 0.0511, -0.0447, -0.0316,  ..., -0.0317,  0.0461,  0.0467],
              [-0.0271, -0.0691,  0.0001,  ..., -0.0308, -0.0078,  0.0637],
              [-0.0485,  0.0077,  0.0438,  ..., -0.0516,  0.0235,  0.0332],
              ...,
              [ 0.0509,  0.0642, -0.0463,  ...,  0.0293, -0.0180, -0.0080],
              [-0.0442, -0.0545,  0.0283,  ..., -0.0485, -0.0448,  0.0401],
              [ 0.0648, -0.0575, -0.0266,  ...,  0.0474, -0.0151,  0.0198]],
    
             [[ 0.0257,  0.0624, -0.0416,  ...,  0.0315,  0.0505,  0.0685],
              [-0.0015, -0.0337,  0.0685,  ...,  0.0678,  0.0702, -0.0190],
              [ 0.0617, -0.0594, -0.0033,  ..., -0.0092, -0.0237,  0.0606],
              ...,
              [-0.0125, -0.0436,  0.0473,  ...,  0.0282,  0.0717,  0.0147],
              [-0.0651,  0.0116,  0.0650,  ...,  0.0337,  0.0476, -0.0458],
              [ 0.0659,  0.0610, -0.0694,  ..., -0.0017,  0.0312, -0.0289]],
    
             [[ 0.0509, -0.0348, -0.0466,  ...,  0.0273,  0.0621,  0.0055],
              [ 0.0582,  0.0035, -0.0381,  ..., -0.0671,  0.0191, -0.0001],
              [-0.0013, -0.0582,  0.0262,  ..., -0.0422, -0.0540, -0.0648],
              ...,
              [-0.0112,  0.0388,  0.0507,  ..., -0.0239,  0.0342, -0.0678],
              [ 0.0274,  0.0480,  0.0082,  ..., -0.0434,  0.0157, -0.0626],
              [-0.0506,  0.0475, -0.0089,  ...,  0.0545,  0.0228, -0.0452]]],
    
    
            [[[-0.0241,  0.0395, -0.0115,  ...,  0.0492,  0.0682,  0.0716],
              [ 0.0474,  0.0685,  0.0238,  ...,  0.0366, -0.0581,  0.0137],
              [-0.0467,  0.0674,  0.0628,  ..., -0.0320, -0.0097, -0.0006],
              ...,
              [ 0.0281, -0.0184,  0.0296,  ..., -0.0332,  0.0378,  0.0470],
              [ 0.0131,  0.0594, -0.0496,  ..., -0.0657,  0.0662,  0.0489],
              [ 0.0577,  0.0042, -0.0006,  ...,  0.0622, -0.0709, -0.0015]],
    
             [[ 0.0222, -0.0089, -0.0576,  ...,  0.0400,  0.0304,  0.0482],
              [ 0.0596,  0.0062, -0.0697,  ...,  0.0305,  0.0074, -0.0072],
              [-0.0316,  0.0194, -0.0234,  ...,  0.0341, -0.0620, -0.0190],
              ...,
              [-0.0633, -0.0124, -0.0048,  ..., -0.0503,  0.0564, -0.0459],
              [ 0.0138, -0.0067, -0.0451,  ..., -0.0682, -0.0151,  0.0459],
              [ 0.0065,  0.0211, -0.0036,  ...,  0.0486, -0.0568,  0.0160]],
    
             [[ 0.0082,  0.0305,  0.0527,  ...,  0.0138,  0.0486,  0.0633],
              [ 0.0179,  0.0147,  0.0098,  ..., -0.0535, -0.0141, -0.0677],
              [ 0.0200, -0.0674, -0.0181,  ...,  0.0219,  0.0641, -0.0008],
              ...,
              [-0.0012,  0.0274,  0.0437,  ...,  0.0663,  0.0428, -0.0615],
              [ 0.0096,  0.0145, -0.0699,  ..., -0.0286, -0.0042,  0.0027],
              [-0.0104,  0.0565,  0.0312,  ..., -0.0553,  0.0551,  0.0152]]],
    
    
            ...,
    
    
            [[[ 0.0657, -0.0326,  0.0080,  ...,  0.0046, -0.0041,  0.0091],
              [ 0.0698, -0.0084,  0.0060,  ..., -0.0561,  0.0495, -0.0699],
              [ 0.0516, -0.0187, -0.0122,  ...,  0.0523, -0.0575, -0.0315],
              ...,
              [ 0.0433,  0.0182,  0.0388,  ..., -0.0281,  0.0670,  0.0336],
              [ 0.0015, -0.0009, -0.0006,  ..., -0.0382,  0.0469, -0.0720],
              [-0.0254, -0.0618,  0.0460,  ...,  0.0230, -0.0499, -0.0600]],
    
             [[ 0.0271,  0.0479, -0.0617,  ..., -0.0400, -0.0284, -0.0497],
              [-0.0486,  0.0624, -0.0223,  ..., -0.0077, -0.0431,  0.0337],
              [ 0.0682,  0.0242, -0.0187,  ..., -0.0079,  0.0684,  0.0480],
              ...,
              [ 0.0642, -0.0190,  0.0643,  ...,  0.0661,  0.0338,  0.0080],
              [-0.0685,  0.0240, -0.0485,  ...,  0.0366, -0.0496, -0.0078],
              [ 0.0295,  0.0014,  0.0603,  ...,  0.0357,  0.0143,  0.0713]],
    
             [[ 0.0254,  0.0575, -0.0192,  ..., -0.0197, -0.0579,  0.0272],
              [ 0.0340, -0.0133, -0.0189,  ...,  0.0299,  0.0325,  0.0680],
              [-0.0266, -0.0534, -0.0204,  ..., -0.0213,  0.0539,  0.0388],
              ...,
              [ 0.0169, -0.0598,  0.0405,  ..., -0.0053,  0.0639,  0.0515],
              [ 0.0611, -0.0408, -0.0626,  ..., -0.0182, -0.0211, -0.0045],
              [-0.0496, -0.0080, -0.0716,  ..., -0.0245,  0.0086,  0.0160]]],
    
    
            [[[ 0.0301,  0.0460,  0.0507,  ...,  0.0305, -0.0363,  0.0504],
              [-0.0078,  0.0367,  0.0323,  ...,  0.0720, -0.0404, -0.0003],
              [ 0.0569,  0.0166, -0.0399,  ...,  0.0116, -0.0474, -0.0403],
              ...,
              [ 0.0348,  0.0631, -0.0521,  ...,  0.0450, -0.0011,  0.0399],
              [ 0.0028, -0.0474, -0.0196,  ..., -0.0264, -0.0208, -0.0057],
              [-0.0143, -0.0628, -0.0387,  ..., -0.0411,  0.0019,  0.0635]],
    
             [[-0.0084, -0.0580,  0.0651,  ..., -0.0144, -0.0296, -0.0109],
              [ 0.0390, -0.0271,  0.0475,  ...,  0.0265,  0.0185,  0.0705],
              [-0.0107, -0.0407,  0.0714,  ..., -0.0536, -0.0415,  0.0521],
              ...,
              [ 0.0176,  0.0509, -0.0721,  ...,  0.0109,  0.0253,  0.0533],
              [ 0.0408, -0.0050,  0.0601,  ...,  0.0164,  0.0492,  0.0426],
              [ 0.0547,  0.0186,  0.0507,  ..., -0.0109, -0.0548,  0.0659]],
    
             [[ 0.0657, -0.0043, -0.0288,  ...,  0.0204, -0.0494, -0.0355],
              [-0.0053, -0.0343,  0.0252,  ..., -0.0236, -0.0425, -0.0104],
              [ 0.0636, -0.0620, -0.0336,  ...,  0.0409,  0.0692, -0.0660],
              ...,
              [ 0.0312,  0.0228,  0.0720,  ..., -0.0080, -0.0288,  0.0401],
              [ 0.0587,  0.0685, -0.0131,  ...,  0.0422,  0.0435, -0.0395],
              [-0.0516,  0.0197, -0.0293,  ...,  0.0390,  0.0056,  0.0202]]],
    
    
            [[[-0.0230,  0.0511,  0.0119,  ...,  0.0710, -0.0034,  0.0082],
              [ 0.0594, -0.0382,  0.0395,  ..., -0.0084, -0.0155, -0.0323],
              [-0.0054,  0.0684, -0.0275,  ...,  0.0050, -0.0089,  0.0282],
              ...,
              [ 0.0436,  0.0008,  0.0326,  ...,  0.0642, -0.0279,  0.0342],
              [ 0.0249,  0.0318, -0.0461,  ..., -0.0270, -0.0014,  0.0051],
              [-0.0371,  0.0591,  0.0457,  ...,  0.0541,  0.0208, -0.0542]],
    
             [[ 0.0466,  0.0072, -0.0189,  ...,  0.0366, -0.0543,  0.0011],
              [-0.0018, -0.0273,  0.0185,  ...,  0.0235, -0.0517, -0.0235],
              [ 0.0155, -0.0717,  0.0200,  ...,  0.0295,  0.0037, -0.0087],
              ...,
              [ 0.0411, -0.0260, -0.0394,  ..., -0.0151,  0.0140,  0.0620],
              [ 0.0704, -0.0056,  0.0626,  ...,  0.0131, -0.0305, -0.0510],
              [-0.0389, -0.0222,  0.0424,  ..., -0.0108, -0.0538, -0.0198]],
    
             [[ 0.0362, -0.0582,  0.0698,  ...,  0.0650,  0.0686, -0.0397],
              [ 0.0462, -0.0443, -0.0361,  ...,  0.0292, -0.0678,  0.0410],
              [-0.0317, -0.0202, -0.0607,  ..., -0.0180, -0.0143, -0.0126],
              ...,
              [-0.0289,  0.0707, -0.0202,  ..., -0.0442,  0.0160, -0.0268],
              [ 0.0410,  0.0620, -0.0223,  ...,  0.0298, -0.0445, -0.0226],
              [-0.0295,  0.0573,  0.0616,  ..., -0.0268,  0.0589,  0.0215]]]],
           requires_grad=True)), ('bias', Parameter containing:
    tensor([-0.0375,  0.0194, -0.0133,  0.0407,  0.0441, -0.0407, -0.0034, -0.0079,
            -0.0071, -0.0169,  0.0410, -0.0447, -0.0119,  0.0715,  0.0515,  0.0387,
             0.0546, -0.0050, -0.0565, -0.0038, -0.0078,  0.0275,  0.0346,  0.0413,
             0.0274, -0.0052,  0.0114, -0.0092, -0.0473,  0.0113,  0.0463,  0.0222,
             0.0172, -0.0606,  0.0449, -0.0360, -0.0498,  0.0609,  0.0334, -0.0268,
            -0.0151,  0.0147, -0.0152, -0.0346, -0.0647,  0.0708,  0.0380, -0.0196,
            -0.0155, -0.0637,  0.0188,  0.0361, -0.0180,  0.0689, -0.0345, -0.0636,
            -0.0114,  0.0245,  0.0005,  0.0451, -0.0412, -0.0709, -0.0571,  0.0176,
            -0.0375, -0.0424, -0.0456,  0.0442,  0.0429, -0.0451, -0.0497, -0.0670,
            -0.0156, -0.0070, -0.0123, -0.0051, -0.0604,  0.0488, -0.0127, -0.0367,
            -0.0088, -0.0131, -0.0712, -0.0074, -0.0627, -0.0577, -0.0625,  0.0034,
             0.0125, -0.0437, -0.0719,  0.0137, -0.0585, -0.0690,  0.0448,  0.0456,
             0.0489, -0.0499,  0.0496, -0.0716], requires_grad=True))]



```python
import torch.optim as optim

## Negative log-likelihood loss
## This is a binary classification problem
criterion = nn.CrossEntropyLoss()
## Stochastic Gradient Descent
#### Just like gradient descent, but uses just part of the data not the entire dataset
optimizer = optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-4)
```


```python
from tqdm import tqdm

def train_model(model, criterion, optimizer, num_epochs=25):
    since = time.time()

    # Will save the best model of "model" in validation data
    #   Since "model" is small, this step is fast
    best_model = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f'Epoch {epoch + 1}/{num_epochs}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train() # Set model to evaluation mode
            else:
                model.eval()   # Set model to evaluation mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in tqdm(data_loaders[phase], desc=f'{phase} phase', leave=False):
                # This is a synchronous way to transfer data to the GPU
                #   It is inneficient. We will see more efficient ways later
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the gradients of model
                optimizer.zero_grad()

                # Only compute gradients in "train" phase
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs) ## Perform forward pass
                    
                    loss = criterion(outputs, labels) # loss negative log-likelihood loss using the output "probabilities" 
                                                        # actually, the CrossEntropyLoss() does
                                                        # the softmax for us

                    _, preds = torch.max(outputs, 1) # predicted label (we will use later)
                    
                    # compute gradients & optimize only if in training phase
                    if phase == 'train':
                        loss.backward() # Compute gradient
                        optimizer.step() # One optimization step

                # compute statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # Early "stopping"
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model = copy.deepcopy(model.state_dict())

    time_elapsed = time.time() - since
    print(f'\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    # load best model weights of g obtained from early stopping
    model.load_state_dict(best_model)
    # returns  g
    return model
```


```python
trained_model = train_model(model=model, criterion=criterion, optimizer=optimizer, num_epochs=10)
```

    Epoch 1/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.6504 Acc: 0.4508


                                                                                                                                                                                                                                           

    val Loss: 0.5756 Acc: 0.4314
    Epoch 2/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.6281 Acc: 0.5369


                                                                                                                                                                                                                                           

    val Loss: 0.5845 Acc: 0.4379
    Epoch 3/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.6087 Acc: 0.5697


                                                                                                                                                                                                                                           

    val Loss: 0.5531 Acc: 0.4771
    Epoch 4/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5856 Acc: 0.5574


                                                                                                                                                                                                                                           

    val Loss: 0.6050 Acc: 0.4575
    Epoch 5/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5605 Acc: 0.5943


                                                                                                                                                                                                                                           

    val Loss: 0.5735 Acc: 0.4902
    Epoch 6/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5376 Acc: 0.6557


                                                                                                                                                                                                                                           

    val Loss: 0.6902 Acc: 0.4902
    Epoch 7/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5207 Acc: 0.6557


                                                                                                                                                                                                                                           

    val Loss: 0.5692 Acc: 0.5098
    Epoch 8/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5032 Acc: 0.6393


                                                                                                                                                                                                                                           

    val Loss: 0.6590 Acc: 0.5163
    Epoch 9/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5197 Acc: 0.5861


                                                                                                                                                                                                                                           

    val Loss: 0.6623 Acc: 0.4771
    Epoch 10/10
    ----------


                                                                                                                                                                                                                                           

    train Loss: 0.5041 Acc: 0.6557


                                                                                                                                                                                                                                           

    val Loss: 0.5659 Acc: 0.4641
    
    Training complete in 8m 39s
    Best val Acc: 0.516340


    


```python

```
