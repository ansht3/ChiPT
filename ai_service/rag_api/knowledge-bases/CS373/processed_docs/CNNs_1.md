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