# Data Mining & Machine Learning
## CS37300 
Instructor: Bruno Ribeiro

**Purdue University**  

August 27, 2025

---

# Probability and Statistics Basics

## Modeling Uncertainty

• Necessary component of almost all data analysis
• Approaches to modeling uncertainty:
  - Fuzzy logic
  - Possibility theory  
  - Confidence sets
  - **Probability (focus in this course)**

## Probability Basics

• **Basic element**: Random variable
  - Mapping from a property of objects to a variable that can take one of a set of possible values
  - **Notation**: $X$ refers to random variable; $x$ refers to a value of that random variable

• **Types of random variables**
  - **Discrete RV** has a finite set of possible values
  - **Continuous RV** can take any value within an interval
  - **Boolean**: e.g., Warning (is there a storm warning? = <yes, no>)
  - **Discrete**: e.g., Weather is one of <sunny,rainy,cloudy,snow>
  - **Continuous**: e.g., Temperature

• **Sample space ($\mathcal{S}$)**
  - Set of all possible outcomes of an experiment

• **Event**
  - Any subset of outcomes contained in the sample space $\mathcal{S}$
  - When events A and B have no outcomes in common they are said to be mutually exclusive

## Examples

| Random variable(s) | Sample space |
|-------------------|-------------|
| One coin toss | H, T |
| Two coin tosses | HH, HT, TH, TT |
| Select one card | 2♥, 2♦, ..., A♣ (52) |
| Play a chess game | Win, Lose, Draw |
| Inspect a part | Defective, OK |
| Cavity and toothache | TT, TF, FT, FF |

## Axioms of Probability

For a sample space $\mathcal{S}$ with possible events $A \subseteq S$, a function that associates real values with each event $A$ is called a probability function if the following properties are satisfied:

1. **$0 \leq P(A) \leq 1$** for every $A$
2. **$P(S) = 1$**
3. **$P(A_1 \cup A_2 \cup \ldots \cup A_n) = P(A_1) + P(A_2) + \ldots + P(A_n)$** if $A_1, A_2, \ldots, A_n$ are pairwise mutually exclusive events

## Implications of Axioms

For any events A, B in universe S:

* **$P(A) = 1 - P(S \setminus A)$**
* **$P(S) = 1$** and **$P(\emptyset) = 0$**
* If A and B are mutually exclusive then **$P(A \cap B) = 0$**
* **$P(A \cup B) = P(A) + P(B) - P(A \cap B)$**

<center><img src="Venn.png" width=400px/></center>

*Note: Venn diagram showing the relationship between sets A and B with their intersection is shown here*

## Quiz
Given $P(A) = 0.7$, $P(B) = 0.4$, and $P(A \cap B) = 0.2$, what is $P(A \cup B)$?

a) 1.1  
b) 0.9  
c) 0.8  
d) 0.5

## Interpreting Probabilities

• Meaning of probability is focus of debate and controversy
• Two main views: **Frequentist** and **Bayesian**

## Frequentist View

- Dominant perspective for last century
- Probability is an **objective** concept
- Defined as the frequency of an event occurring under repeated trials in "same" situation
- E.g., number of heads in repeated coin tosses
- Restricts application of probability to repeatable events

## Calculating Probabilities (Frequentist)

- **Frequentist view**
  - Let $n$ be the number of times an experiment is performed
  - Let $n(A)$ be the number of outcomes in which $A$ occurs
  - Then as $n \to \infty$, $P(A) = \frac{n(A)}{n}$

- When the various outcomes of an experiment are equally likely, the task of computing probability reduces to counting
  - Let $N$ be size of sample space (i.e., number of simple outcomes)
  - Let $N(A)$ be the number of outcomes contained in $A$
  - Then: **$P(A) = \frac{N(A)}{N}$**

## Example

**Roll two 6-sided dice. What is the probability that the result sums to 8?**

- $P = \frac{\text{num ways event can occur}}{\text{possible outcomes}}$
- What is the size of the sample space?
  - $6 \times 6 = 36$
- How many events involve the two dice summing to 8?
  - $\{(2,6), (3,5), (4,4), (5,3), (6,2)\} = 5$ ways
- Overall probability?
  - $\frac{5}{36} \approx 0.139$

## Permutations and Combinations

• An **ordered** sequence of k objects taken from a set of n distinct objects without replacement, is called a **permutation of size k**
  - The number of permutations of size k that can be constructed from the n objects is:
  
    $$P_{k,n} = n!/(n-k)!$$

• An **unordered** sequence of k objects taken from a set of n distinct objects without replacement, is called a **combination of size k**
  - The number of combinations of size k that can be constructed from the n objects is:
  
    $$C_{k,n} = P_{k,n}/k! = n!/(k!(n-k)!)$$


```python
import math

def permutation(n, k):
    """Calculate P(n,k) = n!/(n-k)!"""
    return math.factorial(n) // math.factorial(n - k)

def combination(n, k):
    """Calculate C(n,k) = n!/(k!(n-k)!)"""
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# Test the functions
print(f"P(5,3) = {permutation(5, 3)}")
print(f"C(5,3) = {combination(5, 3)}")
```

    P(5,3) = 60
    C(5,3) = 10


## Example

- An urn contains ten balls, six of which are red and four of which are white. Five balls are drawn at random. What is the probability of drawing three red and two white balls?

  $\frac{C_{3,6} \cdot C_{2,4}}{C_{5,10}} = \frac{\binom{6}{3}\binom{4}{2}}{\binom{10}{5}} = \frac{\frac{6!}{3!3!} \cdot \frac{4!}{2!2!}}{\frac{10!}{5!5!}} = \frac{5!5!}{10!}$

- An urn contains five balls, numbered from 1 to 5. Three balls are drawn at random. What is the probability that we draw the sequence 3, 4, 1?

  $\frac{1}{P_{3,5}} = \frac{(5-3)!}{5!} = \frac{2!}{5!}$


```python
# Example 1: Urn with red and white balls
red_balls = 6
white_balls = 4
total_balls = red_balls + white_balls
drawn_balls = 5
red_drawn = 3
white_drawn = 2

# Ways to choose 3 red from 6 red balls
ways_red = combination(red_balls, red_drawn)
# Ways to choose 2 white from 4 white balls
ways_white = combination(white_balls, white_drawn)
# Total ways to choose 5 from 10 balls
total_ways = combination(total_balls, drawn_balls)

probability_1 = (ways_red * ways_white) / total_ways

print("Example 1: Red and White Balls")
print(f"Ways to choose {red_drawn} red from {red_balls}: {ways_red}")
print(f"Ways to choose {white_drawn} white from {white_balls}: {ways_white}")
print(f"Total ways to choose {drawn_balls} from {total_balls}: {total_ways}")
print(f"Probability: {probability_1:.4f}")
print()

# Example 2: Numbered balls sequence
n_balls = 5
k_drawn = 3

# Total permutations of drawing 3 from 5
total_permutations = permutation(n_balls, k_drawn)
# Probability of specific sequence
probability_2 = 1 / total_permutations

print("Example 2: Numbered Balls Sequence")
print(f"Total permutations P({n_balls},{k_drawn}): {total_permutations}")
print(f"Probability of sequence 3,4,1: {probability_2:.4f}")
```

    Example 1: Red and White Balls
    Ways to choose 3 red from 6: 20
    Ways to choose 2 white from 4: 6
    Total ways to choose 5 from 10: 252
    Probability: 0.4762
    
    Example 2: Numbered Balls Sequence
    Total permutations P(5,3): 60
    Probability of sequence 3,4,1: 0.0167


# Bayesian view

- **Growing importance:** Increasing significance over last decades due to advances in computational power that facilitate previously intractable calculations

- **Subjective probability:** Probability represents an individual's degree-of-belief that an event will occur
  - E.g., belief that we will have another snow storm tomorrow

- **Bayesian approach:** Begin with prior belief estimates $P(A)$ and update those by conditioning on observed data using Bayes' rule:
  
  $P(A|\text{data}) = \frac{P(\text{data}|A) P(A)}{P(\text{data})}$

- **Key advantage:** Allows incorporation of prior knowledge and systematic updating of beliefs as new evidence becomes available

## Calculating probabilities: Bayesian

- **Begin with prior belief estimates:** $P(A)$
  - E.g., After the Seahawks won their conference, Vegas casinos believed the Seahawks were likely to win the Superbowl over the Patriots:  
    $P(S \text{ wins}) = 0.525$, $P(P \text{ wins}) = 0.475$

- **Observe data**
  - But then Vegas observed a heavy majority of the betters (80%) chose the Patriots, which is unlikely given their current belief

- **Update belief by conditioning on observed data**  
  $P(A|\text{data}) = \frac{P(\text{data}|A) P(A)}{P(\text{data})}$

- **Result:** So they updated their belief to increase the Patriots's chance of a win:  
  $P(S \text{ wins} | \text{betting}) = \frac{P(\text{betting} | S \text{ wins}) P(S \text{ wins})}{P(\text{betting})} = 0.50$

- **Note:** Even when the same data is observed, if people have different priors, they can end up with different posterior probability estimates $P(A|\text{data})$

# Bayesian vs. frequentist

- **Bayesian central tenet:**
  - Explicitly model all forms of uncertainty
  - E.g., Parameters, model structure, predictions
- **Frequentist** often model same uncertainty but in less-principled manner, e.g.,:  
  - Parameters set by cross-validation
  - Model structure averaged in ensembles
  - Smoothing of predicted probabilities
- Although interpretation of probability is different, underlying calculus is the same

# Probability distribution

- **Probability distribution** (i.e., probability mass function or probability density function) specifies the probability of observing every possible value of a random variable

## Discrete
- Denotes probability that $X$ will take on a particular value:
  
  $$P(X = x)$$

## Continuous
- Probability of any particular point is 0, have to consider probability within an interval:
  
  $$P(a < X < b) = \int_a^b p(x)dx$$

# Joint probability

- **Joint probability distribution** for a set of random variables gives the probability of every atomic event on those random variables

E.g., P(Warning, Weather) = a 4 × 2 matrix of values:

| | sunny | rainy | cloudy | snow |
|---|-------|-------|--------|------|
| warning = Y | 0.005 | 0.08 | 0.02 | 0.02 |
| warning = N | 0.415 | 0.12 | 0.31 | 0.03 |

- **Every question about events can be answered by the joint distribution**

- E.g.: **Marginal probability distribution** for a subset of random variables gives the probability of every atomic event on those random variables

E.g., P(Warning) = P(Warning,Weather=sunny) + P(Warning,Weather=rainy) + P(Warning,Weather=cloudy) + P(Warning,Weather=snow)

# Conditional probability

- **Conditional (or posterior) probability:**
  - e.g., P( warning=Y | snow=T ) = 0.4

- **Complete conditional distributions** specify conditional probability for all possible combinations of a set of RVs:

P( warning | snow ) =  
{P( warning = Y | snow = T ), P( warning = N | snow = T )},  
{P( warning = Y | snow = F ), P( warning = N | snow = F )}

- If we know more, then we can update the probability by conditioning on more evidence
  - e.g., if Windy is also given then P( warning | snow, windy ) = 0.5

## Mathematical Definitions

- **Definition of conditional probability:**
  
  **$P(A|B) = \frac{P(A \cap B)}{P(B)}$, if $P(B) > 0$**

- **Product rule** gives an alternative formulation:
  
  **$P(A \cap B) = P(A|B)P(B) = P(B|A)P(A)$**

- **Bayes rule** uses the product rule:
  
  **$P(A|B) = \frac{P(B|A)P(A)}{P(B)}$**

  <center><img src="Venn.png" width=400px/></center>


# Example

- **Conditional probability:**
  
  **$P(A|B) = \frac{P(A \cap B)}{P(B)}$, if $P(B) > 0$**

- Example: What is $P(\text{Weather} = \text{sunny} | \text{warning} = Y)$?

| | sunny | rainy | cloudy | snow |
|---|-------|-------|--------|------|
| warning = Y | 0.005 | 0.08 | 0.02 | 0.02 |
| warning = N | 0.415 | 0.12 | 0.31 | 0.03 |


```python
# Calculate P(Weather = sunny | warning = Y)
# P(A|B) = P(A ∩ B)/P(B)

# P(sunny ∩ warning=Y) = 0.005
# P(warning=Y) = 0.005 + 0.08 + 0.02 + 0.02 = 0.125

p_sunny_and_warning_y = 0.005
p_warning_y = 0.005 + 0.08 + 0.02 + 0.02

p_sunny_given_warning_y = p_sunny_and_warning_y / p_warning_y
print(f"P(Weather = sunny | warning = Y) = {p_sunny_given_warning_y:.3f}")
```

    P(Weather = sunny | warning = Y) = 0.040


# Conditional probability (Chain Rule)

- **Chain rule of probability** is derived by successive application of product rule:

$P(X_1,...,X_n) = P(X_n|X_1,...,X_{n-1})P(X_1,...,X_{n-1})$  
$= P(X_n|X_1,...,X_{n-1})P(X_{n-1}|X_1,...,X_{n-2})P(X_1,...,X_{n-2})$  
$= ...$  
$= \prod_{i=1}^n P(X_i|X_1,...,X_{i-1})$

**This property is very important in machine learning**

# Example: Large Language Model Training & Inference

Large language models (LLMs) are trained to predict the next word in a sequence using conditional probabilities.

## Core Concept

Given a sequence of "words" $X_1, X_2, \ldots, X_{t-1}$, an LLM estimates the probability distribution over all possible next "words":

$$P(X_t \mid X_1, X_2, \ldots, X_{t-1})$$

## Training Process

The model learns these conditional probabilities through a three-step process:

### 1. Context Encoding
The input sequence $X_1, X_2, \ldots, X_{t-1}$ is processed by the transformer architecture to produce a high-dimensional representation vector $h_{t-1} \in \mathbb{R}^d$, where $d$ is the model's hidden dimension.

### 2. Probability Distribution
The representation vector is transformed into a probability distribution over the vocabulary of all "words" using a softmax function:

$$P(X_t \mid X_1, X_2, \ldots, X_{t-1}) = \text{softmax}(W h_{t-1} + b) \quad \text{\#we will explain softmax and $h_{t-1}$ means throughout the course}$$

where $W \in \mathbb{R}^{|V| \times d}$ is the output projection matrix and $|V|$ is the vocabulary size.

### 3. Next "Word" Prediction
During inference, the model selects the "word" with the highest probability:

$$\hat{X}_t = \arg\max_{X \in V} P(X \mid X_1, X_2, \ldots, X_{t-1})$$

## Key Insight
This autoregressive approach allows LLMs to generate coherent text by learning statistical patterns in language during training on large text corpora.


```python
# Simple example of chain rule in language modeling
# Suppose we want to calculate P("The cat sits")
# Using chain rule: P(The, cat, sits) = P(The) * P(cat|The) * P(sits|The, cat)

# Example probabilities (hypothetical)
p_the = 0.1  # P("The")
p_cat_given_the = 0.05  # P("cat" | "The")
p_sits_given_the_cat = 0.3  # P("sits" | "The", "cat")

# Chain rule calculation
p_sentence = p_the * p_cat_given_the * p_sits_given_the_cat

print(f'P("The cat sits") = P("The") × P("cat"|"The") × P("sits"|"The", "cat")')
print(f'P("The cat sits") = {p_the} × {p_cat_given_the} × {p_sits_given_the_cat} = {p_sentence:.6f}')
```

    P("The cat sits") = P("The") × P("cat"|"The") × P("sits"|"The", "cat")
    P("The cat sits") = 0.1 × 0.05 × 0.3 = 0.001500


# Marginal probability

- **Marginal** (or unconditional) probability corresponds to belief that event will occur regardless of conditioning events

- **Marginalization:**
  
  **$P(A) = \sum_{b \in B} P(A,b)$** (sum over $b \in B$)  
  **$= \sum_{b \in B} P(A|b)P(b)$** (sum over $b \in B$)

- Example: What is $P(\text{cloudy})$?

| | sunny | rainy | cloudy | snow |
|---|-------|-------|--------|------|
| warning = Y | 0.005 | 0.08 | 0.02 | 0.02 |
| warning = N | 0.415 | 0.12 | 0.31 | 0.03 |


```python
# Calculate P(cloudy) using marginalization
# P(cloudy) = P(cloudy, warning=Y) + P(cloudy, warning=N)

p_cloudy_warning_y = 0.02
p_cloudy_warning_n = 0.31

p_cloudy = p_cloudy_warning_y + p_cloudy_warning_n

print(f"P(cloudy) = P(cloudy, warning=Y) + P(cloudy, warning=N)")
print(f"P(cloudy) = {p_cloudy_warning_y} + {p_cloudy_warning_n} = {p_cloudy}")
```

    P(cloudy) = P(cloudy, warning=Y) + P(cloudy, warning=N)
    P(cloudy) = 0.02 + 0.31 = 0.33


# Example

- A student is leading an environmental protest outside PMU today

- **What is more likely?**

  a) That the student is also an oil executive?

  b) That the student is an oil executive studying Environmental Engineering at Purdue?

**Conjunction Fallacy**:
- Option (a): P(Oil executive)
- Option (b): P(Oil executive AND Environmental Engineering major)

By probability axioms: $P(A \cap B) \leq P(A)$
- Therefore, option (a) is always either more or equally likely than option (b), but often smore likely.

This demonstrates why people often fall for the conjunction fallacy -
option (b) seems more 'representative' but is mathematically less probable.

# Independence

- $A$ and $B$ are independent iff:
  - **$P(A|B) = P(A)$** or **$P(B|A) = P(B)$** or **$P(A, B) = P(A) P(B)$**
- Knowing $B$ tells you nothing about $A$

- **Examples:**
  - Coin flip 1 and coin flip 2?
  - Weather and storm warning?
  - Weather and coin flip=$H$?
  - Weather and election?


```python
# Example: Testing independence
import numpy as np

# Simulate two coin flips
np.random.seed(42)
n_trials = 10000

# Independent coin flips
coin1 = np.random.choice([0, 1], n_trials)  # 0=Tails, 1=Heads
coin2 = np.random.choice([0, 1], n_trials)

# Calculate probabilities
p_coin1_heads = np.mean(coin1)
p_coin2_heads = np.mean(coin2)
p_both_heads = np.mean((coin1 == 1) & (coin2 == 1))

print(f"P(Coin1 = Heads) = {p_coin1_heads:.2f}")
print(f"P(Coin2 = Heads) = {p_coin2_heads:.2f}")
print(f"P(Both Heads) = {p_both_heads:.2f}")
print(f"P(Coin1) × P(Coin2) = {p_coin1_heads * p_coin2_heads:.2f}")
print(f"")
print(f"Independence check: P(A,B) ≈ P(A)×P(B)? {abs(p_both_heads - p_coin1_heads * p_coin2_heads) < 0.05}")
```

    P(Coin1 = Heads) = 0.50
    P(Coin2 = Heads) = 0.50
    P(Both Heads) = 0.25
    P(Coin1) × P(Coin2) = 0.25
    
    Independence check: P(A,B) ≈ P(A)×P(B)? True


# Conditional independence

- Two variables $A$ and $B$ are **conditionally independent** given $Z$ iff for all values of $A$, $B$, $Z$:
$$P(A, B | Z) = P(A | Z) P(B | Z)$$

- **Note:** independence does not imply conditional independence or vice versa


```python
# Causal Graph for Fire-Smoke-Alarm Example
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Create directed graph
G = nx.DiGraph()

# Add nodes
nodes = ['Fire', 'Smoke', 'Alarm']
G.add_nodes_from(nodes)

# Add edges (causal relationships)
edges = [('Fire', 'Smoke'), ('Fire', 'Alarm')]
G.add_edges_from(edges)

# Set up the plot
plt.figure(figsize=(10, 6))

# Define positions for nodes
pos = {
    'Fire': (0, 1),      # Top center
    'Smoke': (-1, 0),    # Bottom left
    'Alarm': (1, 0)      # Bottom right
}

# Draw the graph
plt.subplot(1, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=2000, font_size=12, font_weight='bold',
        arrows=True, arrowsize=20, edge_color='black', width=2)
plt.title('Causal Graph', fontsize=14, fontweight='bold')

# Add explanation
plt.subplot(1, 2, 2)
plt.text(0.1, 0.8, 'Causal Structure:', fontsize=14, fontweight='bold')
plt.text(0.1, 0.7, '• Fire causes Smoke', fontsize=12)
plt.text(0.1, 0.6, '• Fire causes Alarm', fontsize=12)
plt.text(0.1, 0.5, '• No direct edge Smoke ↔ Alarm', fontsize=12)

plt.text(0.1, 0.35, 'Conditional Independence:', fontsize=14, fontweight='bold')
plt.text(0.1, 0.25, '• Smoke ⊥ Alarm | Fire (Smoke independent of Alarm given Fire', fontsize=12)
plt.text(0.1, 0.15, '• Given Fire status, knowing Smoke', fontsize=12)
plt.text(0.1, 0.05, '  tells us nothing about Alarm', fontsize=12)

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.axis('off')

plt.tight_layout()
plt.show()

# Print the conditional independence statement
print("\n" + "="*50)
print("CONDITIONAL INDEPENDENCE")
print("="*50)
print("Smoke ⊥ Alarm | Fire")
print("\nInterpretation:")
print("Given knowledge of Fire, Smoke and Alarm are independent")
print("The common cause (Fire) explains their correlation")
```


    
![png](stats-basics_files/stats-basics_34_0.png)
    


    
    ==================================================
    CONDITIONAL INDEPENDENCE
    ==================================================
    Smoke ⊥ Alarm | Fire
    
    Interpretation:
    Given knowledge of Fire, Smoke and Alarm are independent
    The common cause (Fire) explains their correlation



```python
# Example of conditional independence
# Consider: Fire (F), Smoke (S), and Alarm (A)
# S and A might be dependent (both caused by fire)
# But S and A might be conditionally independent given F

# Conditional Independence Example
# Fire (F), Smoke (S), and Alarm (A)

import numpy as np

# Define probabilities
P_F = 0.1           # Prior probability of fire
P_S_given_F = 0.9   # P(Smoke | Fire)
P_S_given_no_F = 0.05  # P(Smoke | No Fire)
P_A_given_F = 0.8   # P(Alarm | Fire)
P_A_given_no_F = 0.02  # P(Alarm | No Fire)

print("=== CONDITIONAL INDEPENDENCE EXAMPLE ===")
print("Variables: Fire (F), Smoke (S), Alarm (A)")
print()

# Calculate marginal probabilities
P_S = P_S_given_F * P_F + P_S_given_no_F * (1 - P_F)
P_A = P_A_given_F * P_F + P_A_given_no_F * (1 - P_F)

print("WITHOUT CONDITIONING:")
print(f"P(Smoke) = {P_S:.3f}")
print(f"P(Alarm) = {P_A:.3f}")

# Joint probability without conditioning (dependent)
P_SA = (P_S_given_F * P_A_given_F * P_F + 
        P_S_given_no_F * P_A_given_no_F * (1.0 - P_F))
print(f"P(Smoke, Alarm) = {P_SA:.3f}")
print(f"P(Smoke) × P(Alarm) = {P_S * P_A:.3f}")
print(f"Dependent? {abs(P_SA - P_S * P_A) > 0.001}")
print()

print("WITH CONDITIONING ON FIRE:")
print("Given Fire = True:")
print(f"  P(Smoke, Alarm | Fire) = P(Smoke | Fire) × P(Alarm | Fire) = {P_S_given_F * P_A_given_F:.3f}")
print("Given Fire = False:")  
print(f"  P(Smoke, Alarm | No Fire) = P(Smoke | No Fire) × P(Alarm | No Fire) = {P_S_given_no_F * P_A_given_no_F:.3f}")
print()
print("[IMPORTANT] Smoke and Alarm are CONDITIONALLY INDEPENDENT given Fire!")
print("[IMPORTANT] P(S, A | F) = P(S | F) × P(A | F)")
```

    === CONDITIONAL INDEPENDENCE EXAMPLE ===
    Variables: Fire (F), Smoke (S), Alarm (A)
    
    WITHOUT CONDITIONING:
    P(Smoke) = 0.135
    P(Alarm) = 0.098
    P(Smoke, Alarm) = 0.073
    P(Smoke) × P(Alarm) = 0.013
    Dependent? True
    
    WITH CONDITIONING ON FIRE:
    Given Fire = True:
      P(Smoke, Alarm | Fire) = P(Smoke | Fire) × P(Alarm | Fire) = 0.720
    Given Fire = False:
      P(Smoke, Alarm | No Fire) = P(Smoke | No Fire) × P(Alarm | No Fire) = 0.001
    
    [IMPORTANT] Smoke and Alarm are CONDITIONALLY INDEPENDENT given Fire!
    [IMPORTANT] P(S, A | F) = P(S | F) × P(A | F)


# Probability and Linear Algebra Fundamentals

This notebook covers key concepts in probability theory and linear algebra, essential for understanding machine learning and data science.

## Independence vs Conditional Independence

Understanding the difference between independence and conditional independence is crucial in probability theory.

### Example: Sprinkler and Rain

**Independence:**
- Sprinkler-on and raining are independent events
- Mathematically: $P(S | R) = P(S)$
- The probability of the sprinkler being on doesn't change whether it's raining or not

**Conditional Independence:**
- Sprinkler-on and raining are NOT conditionally independent given grass is wet
- Mathematically: $P(S | R, W) \neq P(S | R)$
- Key insight: Once we know the grass is wet, if it's not raining, then the explanation for the grass being wet has to be the sprinkler

This demonstrates how conditioning on additional information can change the independence relationship between variables.

## Expectation (Expected Value)

The expectation denotes the expected value or mean value of a random variable $X$.

### Definitions:

**For Discrete Random Variables:**
$$E[X] = \sum_x x \cdot p(x)$$

**For Continuous Random Variables:**
$$E[X] = \int x \cdot p(x) dx$$

### Properties:

- **Expectation of a function:** $E[h(X)] = \sum_x h(x) \cdot p(x)$
- **Linearity:** $E[aX + b] = a \cdot E[X] + b$
  - Where $a$ and $b$ are constants
  - This property makes expectation a linear operator

### Example: Fair Coin Tosses

Let $X$ be a random variable representing the number of heads when a fair coin is tossed three times.

**Sample Space and Probabilities:**
- $X \in \{0, 1, 2, 3\}$
- $P(X=0) = \frac{1}{8}$ (TTT)
- $P(X=1) = \frac{3}{8}$ (HTT, THT, TTH)
- $P(X=2) = \frac{3}{8}$ (HHT, HTH, THH)
- $P(X=3) = \frac{1}{8}$ (HHH)

**Calculation:**
$$E[X] = 0 \cdot \frac{1}{8} + 1 \cdot \frac{3}{8} + 2 \cdot \frac{3}{8} + 3 \cdot \frac{1}{8} = \frac{3}{2} = 1.5$$

This result makes intuitive sense: on average, we expect 1.5 heads when tossing a fair coin three times.

## Variance

Variance measures the squared deviation of $X$ from its mean, indicating how spread out the distribution is.

### Definitions:

**Variance:**
- $\text{Var}(X) = E[(X - E[X])^2]$
- Alternative formula: $\text{Var}(X) = E[X^2] - (E[X])^2$

**Standard Deviation:**
- $\sigma = \sqrt{\text{Var}(X)}$
- Provides a measure of spread in the same units as the original variable

### Properties:

- **Linear transformation:** $\text{Var}(aX + b) = a^2 \cdot \text{Var}(X)$
  - Adding a constant doesn't change variance
  - Scaling by $a$ scales variance by $a^2$
- **General function:** $\text{Var}(h(X)) = \sum_x (h(x) - E[h(X)])^2 \cdot p(x)$

### Example: Variance of Coin Tosses

Using the same coin toss example where $E[X] = \frac{3}{2}$:

**Calculation using the definition:**
$$\text{Var}(X) = \sum_x (x - E[X])^2 \cdot p(x)$$

$$\text{Var}(X) = \left(0 - \frac{3}{2}\right)^2 \cdot \frac{1}{8} + \left(1 - \frac{3}{2}\right)^2 \cdot \frac{3}{8} + \left(2 - \frac{3}{2}\right)^2 \cdot \frac{3}{8} + \left(3 - \frac{3}{2}\right)^2 \cdot \frac{1}{8}$$

$$= \frac{9}{4} \cdot \frac{1}{8} + \frac{1}{4} \cdot \frac{3}{8} + \frac{1}{4} \cdot \frac{3}{8} + \frac{9}{4} \cdot \frac{1}{8} = \frac{3}{4} = 0.75$$

The standard deviation is $\sigma = \sqrt{0.75} \approx 0.866$.

# Linear Algebra Introduction

Linear algebra provides the mathematical foundation for many computational methods in data science and machine learning.

## Why Linear Algebra?

Understanding the motivation behind linear algebra helps appreciate its importance in computational applications.

### Why Algebra?
- **Mathematical description:** Provides a way to mathematically describe and manipulate data
- **Computational foundation:** Computing is fundamentally about algebraic operations
- **Abstraction:** Allows us to work with complex relationships in a systematic way

### Why Linear?
- **Computational efficiency:** Fast algorithms and tools are available for linear operations
- **Simplicity:** Linear systems are easier to understand and analyze
- **Approximation power:** Many non-linear problems can be:
  - Transformed into linear systems
  - Approximated using linear methods
  - Solved using linear techniques as building blocks

### Practical Benefits:
- The combination of algebraic structure and linearity works exceptionally well in practice
- Forms the backbone of machine learning algorithms
- Enables efficient computation on large datasets

## Vector Properties

For a set $V$ to be considered a vector space, it must satisfy several fundamental properties.

### Fundamental Vector Space Axioms:

If $V$ is a vector space, then for all vectors $u, v, w \in V$ and scalars $a, b, c$:

**Addition Properties:**
1. **Commutative law:** $u + v = v + u$
2. **Associative law:** $(u + v) + w = u + (v + w)$
3. **Zero element:** There exists $\mathbf{0}$ such that $v + \mathbf{0} = v$
4. **Inverse element:** For any $v$, there exists $-v$ such that $v + (-v) = \mathbf{0}$

**Scalar Multiplication Properties:**
1. **Distributive law I:** $c(u + v) = cu + cv$
2. **Distributive law II:** $(a + b)v = av + bv$
3. **Associative law:** $a(bv) = (ab)v$
4. **Identity:** $1 \cdot v = v$

These properties ensure that vector operations behave in predictable and useful ways.

## Vector Basis

A basis provides a way to represent any vector in a space using a minimal set of building blocks.

### Definition:
The vectors $v_1, v_2, \ldots, v_n$ form a **basis** for vector space $V$ if and only if:
1. **Linear Independence:** No vector can be written as a linear combination of the others
2. **Spanning Property:** Any vector $u \in V$ can be expressed as:
   $$u = c_1v_1 + c_2v_2 + \cdots + c_nv_n$$
   for some scalars $c_1, c_2, \ldots, c_n$

### Dimension:
- If vector space $V$ has a basis of $n$ vectors, then $V$ has **dimension** $n$
- All bases of the same vector space have the same number of vectors

### Important Theorems:
For a vector space $V$ of dimension $n$:
- **Sufficiency:** Any set of $n$ linearly independent vectors spans $V$
- **Necessity:** Any $n$ vectors that span $V$ are linearly independent
- **Minimality:** No set of fewer than $n$ vectors can span $V$

## Vector Products

Vector products provide ways to combine vectors and extract geometric and algebraic information.

### Inner Product (Dot Product)

For column vectors $u, v \in \mathbb{R}^{n \times 1}$:

**Definition:**
$$\langle u, v \rangle = u^T v = \sum_{i=1}^n u_i v_i$$

**Key Properties:**
- **Positive definite:** $\langle v, v \rangle \geq 0$, with equality only when $v = \mathbf{0}$
- **Euclidean norm:** $\|v\|_2^2 = \langle v, v \rangle$
- **Orthogonality:** $\langle u, v \rangle = 0$ means $u \perp v$ (vectors are orthogonal)
- **Geometric interpretation:** $\langle u, v \rangle = \|u\| \|v\| \cos \theta$
  - Where $\theta$ is the angle between vectors $u$ and $v$

### Outer Product

For column vectors $u \in \mathbb{R}^{m \times 1}$ and $v \in \mathbb{R}^{n \times 1}$:

**Definition:**
$$u \otimes v = uv^T$$

This produces an $m \times n$ matrix where each element $(i,j)$ equals $u_i v_j$.

## Matrix Properties

Matrices provide a compact way to represent linear transformations and systems of equations.

## Orthogonal Vectors

Orthogonal vectors form the foundation for many important linear algebra concepts and algorithms.

### Definitions:

Consider row vectors $u_1, \ldots, u_k \in \mathbb{R}^{1 \times n}$:

**Orthogonal Vectors:**
- Vectors are orthogonal if $\langle u_i, u_j \rangle = 0$ for $i \neq j$
- Orthogonal vectors are automatically linearly independent

**Orthonormal Vectors:**
- Vectors are orthonormal if they are both:
  - **Orthogonal:** $\langle u_i, u_j \rangle = 0$ for $i \neq j$
  - **Normalized:** $\|u_i\| = 1$ for all $i$

### Benefits:
- Orthonormal bases simplify many calculations
- Provide numerical stability in computations
- Enable efficient algorithms for projection and decomposition

## Orthogonal Projections
Orthogonal projections allow us to decompose vectors into components along orthogonal directions.

### Mathematical Framework:
Let $U \in \mathbb{R}^{n \times k}$ be a matrix whose columns are orthonormal vectors $u_1, \ldots, u_k$ where $k \leq n$.

**Key Properties:**
- $U^T U = I_k$ (the $k \times k$ identity matrix)
- $UU^T = P$ is the projection matrix onto $\text{span}(U)$

**Projection Formula:**
For any vector $a \in \mathbb{R}^n$:
$$P a = UU^T a = \sum_{i=1}^k u_i u_i^T a$$

**Component Decomposition:**
The projection of $a$ onto $\text{span}(U)$ is:
$$\text{proj}_U(a) = \sum_{i=1}^k u_i(u_i^T a)$$

### Interpretation:
- $U^T a \in \mathbb{R}^k$ gives the **coordinates** of the projection in the orthonormal basis
- Each scalar $(u_i^T a)$ is the **component** of $a$ along direction $u_i$
- Each term $(u_i^T a) u_i$ represents the **projection** of $a$ onto the line spanned by $u_i$
- The sum reconstructs the projection of $a$ onto the subspace spanned by $U$

### Geometric Visualization:
![image.png](stats-basics_files/image.png)

Where $a_1$ and $a_2$ are the projections onto orthogonal basis vectors $u_1$ and $u_2$.

## Non-Orthogonal Basis

While orthogonal bases have many computational advantages, it's important to understand that bases don't need to be orthogonal.

### Key Points:
- **Flexibility:** We can have non-orthogonal basis vectors
- **Trade-offs:** Non-orthogonal bases may complicate some calculations
- **Applications:** Sometimes natural or problem-specific bases are not orthogonal
- **Transformation:** Non-orthogonal bases can often be transformed to orthogonal ones using techniques like Gram-Schmidt orthogonalization

### When Non-Orthogonal Bases Are Used:
- **Natural coordinates:** When the problem naturally suggests non-orthogonal directions
- **Computational efficiency:** Sometimes working in the original basis is more efficient
- **Physical systems:** Some coordinate systems in physics are non-orthogonal
