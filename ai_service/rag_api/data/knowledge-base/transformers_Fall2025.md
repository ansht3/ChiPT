## CS37300 - Data Mining & Machine Learning
## Fall 2025
##### Instructor: Bruno Ribeiro
##### Slides: Bruno Ribeiro



# Transformers 
### Variable input-size Sequence Models

# 1. Variable-size Sequence Representation

**Consider a sequence of $n$ words:** $(x_1,\ldots,x_n)$, where $x_i \in \mathbb{R}^d$ is a unique vector that defines the word (e.g., a one-hot encoding of the vocabulary).

For instance, ``I don't like avocado thank you`` broken up into tokens gives the following 7 tokens ``["I", "do", "n't", "like", "avocado", "thank", "you"]``

**How should we predict the next word?**

### Written language is a sequence of words

A sentence is clearly a sequence of words

```I don't like avocado thank```

**Task:** Our task is to predict the next word

```I don't like avocado thank``` => ```you```

However, sometimes, one can undertand the meaning of a sentence from just its words without their relative ordering (bag of words):


```{avocado, like, thank, I, do, n't}```

Statistically, using just the set of words above, we can even predict the next word: "you"

Just learning a set of words rather than their relative order in the sequence is statistically easier, since the absence of order requires fewer samples. 
Consider the above example. How many more training examples are needed if we have to discern between:

```I don't like avocado thank```

```avocado I don't like thank```

```I avocado don't like thank```

- **MLPs** need fixed-size inputs
    - One potential solution for variable-size inputs is padding
    - We make the MLP take as many tokens as we can, then pad the unused tokens with zeros


- **CNNs** focus on local dependencies
    - Consider a 1D convolutional neural network
    - CNNs use (local) convolutional filters that each process a small window of nearby tokens, learning representations locally.
        - For example, a 1D CNN might use a filter of size 3, meaning each convolution operation considers three neighboring tokens at a time.
        - When inputs are distant from each other (e.g., $x_1$ and $x_n$), the interaction between these inputs is achieved through multiple layers of convolution. Each layer of convolution increases the receptive field (i.e., the portion of the input that influences the output), but the rate of growth depends on the filter size and the stride.

<center><img src="1DCNN.png" width=500px/></center>

# 2. Encoding Text


## Tokenization: Breaking Text into Meaningful Units

## What is Tokenization?

Tokenization is the process of breaking down raw text into smaller units called **tokens** that can be processed by machine learning models like transformers. While humans read text as a continuous stream of characters, computers need discrete numerical representations to work with.

### Why Tokenization Matters for Transformers

Transformers operate on sequences of tokens rather than raw text. The quality of tokenization directly impacts:
- Model performance and understanding
- Vocabulary size and computational efficiency
- Handling of rare words, morphologically complex languages, and special characters

## Common Approaches to Tokenization

### 1. Word-Based Tokenization

The simplest approach that splits text into words based on spaces.

**Example:**
```
"I don't like avocado thank you" → ["I", "don't", "like", "avocado", "thank", "you"]
```

**Pros:**
- Intuitive and easy to understand
- Preserves word-level meaning

**Cons:**
- Creates large vocabulary (thousands or tens of thousands of unique words)
- Cannot handle out-of-vocabulary (OOV) words
- Struggles with morphology (e.g., "running" vs. "run")
- Ignores subword information

### 2. Subword Tokenization

A better approach splits words into meaningful subword units.

#### Byte-Pair Encoding (BPE)
Used in models like GPT, RoBERTa:
1. Start with characters as initial tokens
2. Merge most frequent character pairs iteratively
3. Continue until reaching vocabulary size limit

**Example:**
```
"unhappiness" → ["un", "happi", "ness"]
```

#### WordPiece
Used in BERT:
- Similar to BPE but uses a likelihood-based criterion for merging

**Pros:**
- Handles OOV words by breaking them into known subwords
- Reduces vocabulary size significantly
- Preserves morphological information
- Works well across languages with different writing systems

**Cons:**
- More complex to implement
- May create less interpretable tokens

### 3. Character-Based Tokenization

Splits text into individual characters.

**Example:**
```text
<arg_value>"I don't like avocado" → ["I", " ", "d", "o", "n", "'", "t", " ", "l", "i", "k", "e", " ", "a", "v", "o", "c", "a", "d", "o"]
```

**Pros:**
- Extremely small vocabulary (size ~70 for English)
- Guarantees no OOV words
- Handles any text regardless of language

**Cons:**
- Very long sequences (many tokens per word)
- Loses semantic information at the word level
- Requires more computation to learn meaningful representations

## Practical Considerations in Tokenization

### Vocabulary Size vs. Sequence Length Trade-off

| Approach | Vocabulary Size | Avg. Tokens/Word |
|----------|-----------------|------------------|
| Word-based | 30,000-50,000 | ~1.0 |
| Subword (BPE) | 10,000-40,000 | 1.2-3.0 |
| Character-based | 70-200 | 5-15 |

### Special Tokens

Transformers often include special tokens with specific meanings:

- `[CLS]` or `<s>`: Start of sequence.
- `[EOS]` or `</s>`: End of sequence.
- `[SEP]` or `</s>`: Separator between segments (e.g., question and answer). May also serve as EOS.
- `[PAD]` or `<pad>`: Padding to equalize sequence lengths.
- `[UNK]` or `<unk>`: Unknown/out-of-vocabulary tokens.
- `[MASK]`: Used in masked language modeling.

### Handling Our Example

Let's see how different tokenizers might process our example sentence:

**Original:** "I don't like avocado thank you"

| Tokenizer Type | Output Tokens |
|----------------|---------------|
| Word-based | ["I", "don't", "like", "avocado", "thank", "you"] |
| Subword (BPE) | ["I", "don", "'", "t", "like", "avo", "cado", "thank", "you"] |
| Character-based | ["I", " ", "d", "o", "n", "'", "t", " ", "l", "i", "k", "e", " ", "a", "v", "o", "c", "a", "d", "o", " ", "t", "h", "a", "n", "k", " ", "y", "o", "u"] |

## Real-World Tokenization Example

Here's how we might implement tokenization in PyTorch using Hugging Face's tokenizer library:


```python
from transformers import AutoTokenizer

# Load a pre-trained tokenizer (e.g., BERT)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Our example sentence
sentence = "I don't like avocado thank you"

# Tokenize the text
tokens = tokenizer.tokenize(sentence)
print(f"Tokens: {tokens}")

# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print(f"Token IDs: {token_ids}")

# Decode back to text (with special handling for subwords)
decoded_text = tokenizer.decode(token_ids)
print(f"Decoded: '{decoded_text}'")

# Add special tokens and padding
encoded_input = tokenizer(
    sentence,
    truncation=True,
    max_length=10,
    padding="max_length",
    return_tensors="pt"
)

print("\nWith special tokens and padding:")
print(encoded_input)
```

    Tokens: ['i', 'don', "'", 't', 'like', 'av', '##oca', '##do', 'thank', 'you']
    Token IDs: [1045, 2123, 1005, 1056, 2066, 20704, 24755, 3527, 4067, 2017]
    Decoded: 'i don ' t like avocado thank you'
    
    With special tokens and padding:
    {'input_ids': tensor([[  101,  1045,  2123,  1005,  1056,  2066, 20704, 24755,  3527,   102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}


## Why Subword Tokenization Dominates Modern NLP

Subword tokenization has become the standard for transformer models because it:

1. **Balances efficiency and coverage**: Small enough vocabulary to be manageable but large enough to capture most words
2. **Handles morphology naturally**: Can process related forms of a word (e.g., "run", "running", "ran")
3. **Transfers across languages**: Many multilingual models use the same tokenization for different languages
4. **Reduces sparsity**: More frequent tokens lead to better statistical modeling

**Key Takeaways:**
- Tokenization converts text into discrete units for processing
- Subword tokenization (BPE, WordPiece) offers the best balance for most transformer applications
- Vocabulary size and sequence length are key trade-offs in tokenization design
- Special tokens provide important structural information to transformers

# 3. The Transformer neural network
Today, we will cover the transformer network.
- A transformer is essentially a graph neural network (GNN) with 
    - a specially constructed graph (fully connected with relevance weights on the edges)
    - a few tricks that allow it to also learn how the words (tokens) are ordered in the sequence.

## 2.1. A GNN for a sequence of $n$ tokens

Consider the following **self-attention graph** $G = (V,E,X)$, with 
- Vertex set $V=\{1,\ldots,n\}$
- Vertex attributes $X= \{x_i\}_{i \in V}$.

- And edges $E$ as a function of the vertex attributes $X$:
    - The adjacency matrix (edge weights) of $G$ is ${\bf A}$, such that element ${\bf A}_{ij}$ is a function of the vertex attributes of $i,j \in V$: $${\bf A}_{ij} = \alpha(x_i,x_j; {\bf W}_\alpha),$$ where $\alpha(\cdot, \cdot; {\bf W}_\alpha)$ is a neural network parameterized by ${\bf W}_\alpha$.
    - We will call $\alpha$ the **self-attention mechanism**, a value between (0,1). 
        - It is called self-attention because it maps elements of $x_1,\ldots,x_n$ on themselves.

Consider the sentence 

```I don't like avocado, thank```

The feature set of the vertices is a vector that describe the word
$$X=\{(x_\text{avocado}), (x_\text{like}), (x_\text{thank}), (x_\text{I}), (x_\text{don't})\}$$

And recall that 

$${\bf A}_{ij} = \alpha(x_i,x_j; {\bf W}_\alpha),$$

<center><img src="AttentionGraph.png" width=500px/></center>

## 2.2. The need for positional encodings

- Running a GNN on the fully connected graph above will give a representation output that does not respect the order of the words in the sentence
    - I.e., the tokens get the same representation no matter their order in the sentence.
        - ```I don't like avocado thank```
        - ```avocado I don't like thank```
        - ```I avocado don't like thank```

- Hence, the GNN will need to add a positional encoding vector to the vector describing the tokens:
$$X'=\{(x_\text{avocado} + pos(4)), (x_\text{like} + pos(3)), (x_\text{thank} + pos(5)), (x_\text{I} + pos(1)), (x_\text{don't} + pos(2))\}$$

Let's illustrate edges of the self-attention graph $G$ with adjacency matrix ${\bf A}$:
<center><img src="Am.png" width=350px> </center>

## 2.3. Transformer = Graph-type Representations + Positional Encodings

The transformer architecture was first introduced by [(Vaswani et al., 2017)](https://arxiv.org/pdf/1706.03762.pdf)

The key idea behind the Transformer model is **self-attention with positional encoding**:

- The words in a sentence are represented by the sequence $x_1,\ldots,x_n$.
    - The words will be represented as word vector rather than 1-hot encodings (which we will cover later in the course)

- The $m$-th self-attention is a function $\alpha^{(m)}(\cdot,\cdot;\cdot) \in (0,1)$. 

- A Transformer creates multiple self-attention graphs $G_1,\ldots,G_M$. Each graph is called a **head**.

The transformer model handles variable-sized inputs through these graphs $G_1,\ldots,G_M$.

The following illustrates the operations:
<img src="QKVmultipleheads.svg" width=1200px>

What the attention neighborhood of the i-th word looks like

<img src="Attention.png" width=1000px>
(image from DeepMind tutorial)



### 2.3.1. New representation of the $i$-th token through multiple self-attention graphs (heads)

Using the sequence of $(z_i^{(1)},\ldots,z_i^{(M)})$ representations of the $i$-th token (obtained from the $G_1,\ldots,G_M$ self-attention graphs) we will construct a new token representation via the linear function $$z_i = [z_i^{(1)},\ldots,z_i^{(M)}] {\bf W}_z,$$
where ${\bf W}_z$ is a matrix of learnable parameters.

### 2.4. Types of Positional Encoding

The positional encoding:

- We will inject information (features) about the relative or absolute position of the words in the sequence.

- The positional encodings have the same dimension $d_x$ as $x_i$, $i=1,\ldots,n$, the word vectors, so that the two can be summed. There are many choices of positional encodings.

#### 2.4.1. Pos-Encoding Choice 1: Learnable positional embeddings
Define $\text{pos}(i)$ as the positional encoding of the $i$-th element of the sequence, $i=1,\dots,n$, is a $d_x$-dimensional vector parameter that is also optimized in the model.
    - Learnable positional vectors forces the transformer to have a maximum-size input.
    - The positional embedding **parameter** is added to the input sequence
        - That is, the new input is $x_i + \text{pos}(i)$
        - For reasons we don't yet fully understand, adding works better than multiplying $x_i \odot \text{pos}(i)$

#### 2.4.2. Pos-Encoding Choice 2: Periodic functions

- We can also use periodic functions such as sine and cosine functions with different frequencies (all with the same phases). 
    - The periods are chosen as a geometric progression from $2\pi$ to $L \cdot 2\pi$, where $L$ is a large constant (e.g., $L=10,\!000$). 
    - The hypothesis is that the choice of different periods allows the model to easily learn to attend to relative positions.
    - $j$-th and $j\!+\!1$-st positional features of the $i$-th word: $$\text{pos}(i,2j) = \sin(i/L^{2 j/d})$$ $$\text{pos}(i,2j+1) = \cos(i/L^{2 j/d}) $$

    - Each periodic feature is added to the word embedding, creating a new feature
        - Example in the following code


```python
#code from https://nlp.seas.harvard.edu/2018/04/03/attention.html
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import math, copy, time
from torch.autograd import Variable
import matplotlib.pyplot as plt
import seaborn
seaborn.set_context(context="talk")
%matplotlib inline
```


```python
class PositionalEncoding(nn.Module):
    "Implement the PE function."
    def __init__(self, n, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, n)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, n, 2) *
                             -(math.log(10000.0) / n))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        x = x + Variable(self.pe[:, :x.size(1)], 
                         requires_grad=False)
        return self.dropout(x)
    
```


```python
plt.figure(figsize=(10, 3))
pe = PositionalEncoding(20, 0) # 20-th dimensional positional encoding
x = Variable(torch.zeros(1, 100, 20)) # sequence of n = 100 word embedding d=20 (simply zeros)
x_prime = pe.forward(x) # x' adding positional encodings
plt.xlabel("Position i in the sequence"); plt.ylabel("x'[i] value")
plt.plot(np.arange(100), x_prime[0, :, 4:9].data.numpy())
plt.legend(["dim %d"%p for p in [4,5,6,7,8]])
plt.show()
```


    
![png](transformers_Fall2025_files/transformers_Fall2025_36_0.png)
    


#### 2.4.3.Pos-Encoding Choice 3: Rotationary Embeddings

Rotationary embeddings are created by applying learned rotation matrices to word representations, effectively encoding the position information into the transformed space. The goal is to shift each word representation vector in a way that captures its relative position to other words.

**Mathematical Formulation of Learned Rotations**:

The key idea is to represent each position as a transformation in the representation space. Specifically, each position $i$ is associated with a learned rotation matrix $R_i \in \mathbb{R}^{d \times d}$. For a given word representation vector $\text{word\_embedding}(i) \in \mathbb{R}^{d}$, the positionally-encoded representation of the $i$-th token is given by:
$$
\text{pos}(i) = R_i \cdot \text{word_representation}(i)
$$

where:
- $ R_i $ is a learned orthogonal matrix parameterizing a rotation in the $d$-dimensional space.


**Example in a Neural Network**:
If implemented within a Transformer layer, the rotationary embedding layer would multiply each word representation by the corresponding rotation matrix $R_i$. This could look like:
$$
\mathbf{H} = [R_1 \cdot \mathbf{E}_1, R_2 \cdot \mathbf{E}_2, \ldots, R_n \cdot \mathbf{E}_n]
$$

where:
- $\mathbf{E}_i$ is the representation (neuron vector) of the $i$-th token.
- $R_i$ is the learned rotation matrix corresponding to position $i$.


# 3. Complete Transformer Architecture: Encoding Steps (Sequence Representation) 

## 3.1. Transformer layer
1. Build the transformer layer for the sequence $x'_1,\ldots,x'_n$ using $M$ self-attention graphs.
2. Let $\hat{z}^{(k-1)}_i$ be the output of the $i$-th token from the $k-1$-st Transfromer layer (see figure below)
3. Add residual connections: For the $k$-th transformer layer, $z^{(k)}_i \leftarrow z^{(k)}_i + \hat{z}^{(k-1)}_i$, for all tokens $i=1,\ldots,n$.
4. Applies layer normalization (see description later), i.e., $\tilde{z}^{(k)}_i = \text{LayerNorm}(z^{(k)}_i)$
5. Pass through each $\tilde{z}^{(k)}_i$ through the same MLP $\text{MLP}$: $\hat{z}^{(k)}_i = \text{MLP}(\tilde{z}^{(k)}_i)$
6. Apply Add (residual connection) and Layer norm again
    - Residual connection $\hat{z}^{(k)}_i \leftarrow \hat{z}^{(k)}_i + \hat{z}^{(k-1)}_i$
    - Apply Layer norm: $z_i^\text{out} = \text{LayerNorm}(\text{Add}(\tilde{z}'_i))$
    - Output $z_i^\text{out}$ for this transformer layer

## 3.2. Transformer encoder architecture

- The final sentence representation (a.k.a. **encoder**) is a stack of $N$ such layers in series

<center><img src="Encoding.png" width=300px></center>

### 3.1.1. Layer Normalization
- **Layer normalization** computes the mean and variance used for normalization from all of the summed inputs to the neurons in **a layer on a single training example** [(Ba et al., 2016)](https://arxiv.org/abs/1607.06450)


```python
class LayerNorm(nn.Module):
    "Construct a layernorm module."
    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2
```

## 3.3. AutoRegressive Task: 
### Score Function: Predictions using Causal Mask

When working with sequential data like language, we often want to generate sequences one element at a time. For example:
- Predicting the next word in a sentence
- Generating text character by character
- Creating music or code sequences

This creates a challenge: how can a model predict the next token when it shouldn't "see" future tokens during training?

### The Problem with Standard Self-Attention

In standard self-attention, each token can attend to all other tokens in the sequence. For our example:
```
"I don't like avocado thank you"
```

The word "thank" would be able to see and attend to "you", which violates the principle of text generation (autoregressively predicting one token at a time).


### 3.3.1 Causal Attention (Masked Self-Attention)

To solve this, we introduce **causal masking** - a modification that prevents tokens from attending to future positions:

1. Compute attention scores as usual
2. Apply mask before softmax:
   - Set attention scores for future positions to $-\infty$
   - This makes their softmax probabilities effectively zero

Mathematically:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$$

Where $M$ is the mask matrix with zeros for allowed positions and $-\infty$ for forbidden ones.

- **Causal Mask:** Causal mask is used to learn how to predict the next token
    - The multi-headed attention layer operates slightly differently from the encoder with causal masks. 
        - The decoder must generate the sequence word by word.
            - It begins with a start token, and it takes in a list of previous outputs as inputs, as well as the encoder outputs that contain the attention information from the input. 
            - We need to prevent the decoder from conditioning a given word on future words (**decoder mask**). 
            - Hence, the self-attention $\alpha^{(m)}(\cdot,\cdot;\cdot) \in (0,1)$ of the $m$-th head from a word $x_t$ to a future word $x_{t+j}$, $j > 0$, must be zero
            - The above is done by masking future positions (e.g., setting them to -inf) before the softmax step in the self-attention calculation.
        - The decoder stops decoding when it generates an \<end of sentence\> token as an output.

<center><img src="mask.png" width="80%"/></center>

- **Score function:**
    - The score function is usually uses the probability of next token.
    - The output is a probability vector over the entire vocabulary
        

- **Padding:** Because all elements in the sequence must have a positional encoding, the transformer model **must have a maximum sequence length**.
    - Hence, a `max_length` parameter $n$ defines the maximum length of a sequence that the transformer can accept. 
    - All the sequences that are greater in length than $n$ are truncated
    - For coding reasons, it is easier to treat all sentences as having the same length
        - Shorter sequences will be padded with zeros. The zero-paddings, however, are not supposed to contribute to the attention calculation nor in the target sequence generation. This is an optional operation in the Transformer.


## 3.4. Autoregressive Training (Self-Supervised Learning)

### The Concept

Autoregressive training is a self-supervised learning approach where we train models to predict the next element in a sequence given all previous elements.

For our example:
- Input: "I don't like avocado thank"
- Target: " you" (note the leading space)
- Model learns to predict each token based on all preceding tokens

### Training Process

1. **Teacher Forcing**: During training, we feed the ground truth sequence as input and shift it by one position as target
   ```
   Input:  [SOS] I don't like avocado thank
   Target: you
   ```

2. **Score Calculation**: We compute score (typically cross-entropy) between predicted tokens and actual next tokens

3. **Optimization**: Update model parameters to minimize prediction error

### Why It is Called "Self-Supervised"

We create targets (supervision signals) automatically from the data itself:
- No human labels required
- Each token in the sequence serves as a label for predicting the next token
- The entire sequence provides multiple training examples

## 3.5. From Training to Generation

### During Inference (Generation)

Once trained, we use the model autoregressively:

1. Start with a special "start-of-sequence" token
2. Generate one token at a time:
   - Feed current sequence into model
   - Sample/predict next token
   - Append to sequence
3. Stop when generating "end-of-sequence" token or reaching max length

### Generation Strategies

1. **Greedy Search**: Always pick the most likely token
   ```
   P("you" | "I", "do","##n't", "like", "avocado", "thank"]) = 0.8 → choose "you"
   ```

2. **Top-k Sampling**: Randomly from top k tokens
   ```
   Top-3: ["you", "her", "me"] with probs [0.7, 0.2, 0.1]
   Sample from these three
   ```

3. **Temperature Scaling**: Adjust randomness by dividing logits before softmax
   - Temperature < 1 → more conservative sampling
   - Temperature > 1 → more diverse sampling
   - Temperature parameter divides the **pre-softmax values**

## 3.6. Practical Considerations

### Computational Complexity

- Standard self-attention: $O(n^2)$ complexity for sequence length $n$
- Causal attention has same complexity but with restricted connectivity
- For very long sequences, consider:
  - Sparse attention patterns. Rather than computing full $n \times n$ attention matrices, sparse patterns attend to only a subset of positions. Examples include local windowed attention (attending to nearby tokens) and strided patterns (attending at fixed intervals).
  - Linearized approximations (e.g., Linformer)
  - Recurrence mechanisms (Transformer-XL)

### Handling Variable-Length Sequences

During inference, we typically:
1. Set a maximum generation length based on the maximum lengths used in training
2. Use end-of-sequence tokens to terminate early [EOS]
3. Handle sequences of different lengths through padding during training but variable-length generation

## 4. Advantages and Disadvantages of Transformer Architecture

### 4.1. Advantages of Transformer Architecture

- Each representation (sefl-attention head) can be calculated in parallel
- Like GNNs, they work on variable-size inputs

- Far-away sequence inputs, say $x_1$ and $x_n$, can more easily affect each other's outputs
    - In an 1D CNN, $x_1$ and $x_n$ need to pass through many neural network layers to affect each other.
    - It can more easily learn long-range dependencies in the sequence.
    - Less problems with vanishing or exploding gradients
    

- Requires a lot more data in order to correctly model sequences
    - Because positional encodings must undo the Graph-like representation if the word order is important

### 3.4.2. Disadvantages of Transformer Architecture

- For a time series, where the output depends really on the last few observations, the transformer architecture may be less effective.
    - One solution would be to bias the attention to more recent items.

#### Transformer Implementations

Pytorch 2.0 has new (faster) transformer architectures

https://pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html


```python

```
