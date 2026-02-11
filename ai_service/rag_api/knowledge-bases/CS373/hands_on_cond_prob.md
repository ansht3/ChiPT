## CS37300 - Data Mining and Machine Learning
### Instructor: Bruno Ribeiro
### Notes: Bruno Ribeiro and Bonan Kou

----
# Hands-on Data Handling

## Learning Objectives
In this lecture, we will cover:
1. Working with real-world data in python.
2. Understanding ML applications of probabilities and conditional probabilities.
3. Building and analyzing models.
4. Performing conditional probability calculations.
5. Applying Laplace smoothing to handle small datasets.

## 1. Handling Data

Let's create some fake data and write it to disk.


```python
import pandas as pd
import numpy as np

data = {
    'Age': [25, 25, 22, np.nan, 35, 28, 40, 33, np.nan, 29],
    'Salary': [50000, 50000, 45000, 52000, np.nan, 48000, 70000, np.nan, 62000, 58000],
    'Department': ['HR', 'HR', 'IT', 'IT', 'HR', 'Marketing', 'Finance', 'HR', 'Marketing', 'IT']
}

df = pd.DataFrame(data)

df.to_csv("week1_handons.csv", index=False)

print(df)
```

        Age   Salary Department
    0  25.0  50000.0         HR
    1  25.0  50000.0         HR
    2  22.0  45000.0         IT
    3   NaN  52000.0         IT
    4  35.0      NaN         HR
    5  28.0  48000.0  Marketing
    6  40.0  70000.0    Finance
    7  33.0      NaN         HR
    8   NaN  62000.0  Marketing
    9  29.0  58000.0         IT


## Data sampling

Let's sample 5 rows of this data.


```python
sampled_df = df.sample(n=5, random_state=42)

print(sampled_df)
```

        Age   Salary Department
    8   NaN  62000.0  Marketing
    1  25.0  50000.0         HR
    5  28.0  48000.0  Marketing
    0  25.0  50000.0         HR
    7  33.0      NaN         HR


## Data cleaning
We want to remove the NAs from the dataframe.


```python
df_cleaned = df.dropna()
print(df_cleaned)
```

        Age   Salary Department
    0  25.0  50000.0         HR
    1  25.0  50000.0         HR
    2  22.0  45000.0         IT
    5  28.0  48000.0  Marketing
    6  40.0  70000.0    Finance
    9  29.0  58000.0         IT


## Dropping duplicates


```python
df_cleaned_nodup = df_cleaned.drop_duplicates()
print(df_cleaned_nodup)
```

        Age   Salary Department
    0  25.0  50000.0         HR
    2  22.0  45000.0         IT
    5  28.0  48000.0  Marketing
    6  40.0  70000.0    Finance
    9  29.0  58000.0         IT


## One-hot Encoding: Creating binary variables from categorical ones
**One-Hot Encoding:**

- The pd.get_dummies() function converts categorical variables into a series of binary (0 or 1) columns.
- For each unique category in the 'Department' column, a new column is created.
    - Deparment = {"HR", "Sales", "IT", and "Finance"}
    - Each row gets a 1 if it belongs to that category and a 0 otherwise.
    

*Avoiding multicollinearity in the encoding (drop_first=True)*:
- Multicollinearity can occur in statistical models when variables are correlated or dependent on each other. This may make it hard to estimate the true relationship between variables.
- By setting drop_first=True, the function drops the first category to avoid multicollinearity in methods like regression (we will revisit this later).
    - This also helps reduce redundancy since the dropped category can be inferred from the other binary columns.

- In our scenario 'Department' has values like "HR", "Sales", "IT", and "Finance".
    - The new DataFrame contains columns like Department_Sales, Department_IT, Department_HR, with Department_Finance dropped due to drop_first=True.



```python
df_cleaned_nodup_onehot = pd.get_dummies(df_cleaned_nodup, columns=['Department'], drop_first=True)
print(df_cleaned_nodup_onehot)
```

        Age   Salary  Department_HR  Department_IT  Department_Marketing
    0  25.0  50000.0              1              0                     0
    2  22.0  45000.0              0              1                     0
    5  28.0  48000.0              0              0                     1
    6  40.0  70000.0              0              0                     0
    9  29.0  58000.0              0              1                     0


# 2. How to interpret data?

In machine learning, we often treat observed data as a realization of a random variable, meaning the data is assumed to be a sample drawn from an underlying probability distribution that captures the true nature of a phenomenon. The observed data is a reflection of some underlying reality, with the randomness accounting for variability in measurements, sampling, or external factors.

### County obesity rates in the United States
Consider, for instance, the **obesity rate** per county in the United States.
- The recorded obesity rate for a given county represents a sample (**observation**) drawn from a population distribution. Variations in obesity rates could arise due to several factors—demographics, economic conditions, access to healthcare, and more.
- That is, we assume the **observed obesity rates** are not deterministic but rather reflect the influence of multiple factors.
- This assumption allows us to model the obesity rates using **machine learning methods**, which can infer patterns, make predictions, or evaluate the effects of interventions while accounting for the randomness inherent in the data.

- In the following scenario, treating the **obesity rate** as a **random variable** helps in constructing models that generalize well beyond just the observed data.
    - For example, understanding the distribution allows us to estimate obesity rates for counties where data is missing, predict future rates, or evaluate how changes in socio-economic conditions might influence obesity trends.
    - By assuming that the data is a reflection of an underlying probabilistic process, we can apply techniques like regression, clustering, or causal inference to gain deeper insights into the factors contributing to obesity rates.


```python
import numpy as np
import pandas as pd

# Read data from census file
#  WARNING: need to replace "No Value" by "NA" in the original file
#  The library pandas is not quite scalable... do not use for very large dataset
df = pd.read_csv("2013_ObesityCensus.csv",skiprows=[0,1],names=['State','ID','County','T2013','P2013','T2012','P2012','T2004','P2004'],
        dtype={'State':str,'ID':int,'County':str,'T2013':float,'P2013':float,'T2012':float,'P2012':float,'T2004':float,'P2004':float},encoding = "ISO-8859-1")

# Create a dataframe with the variables of interest without the invalid rows (need to replace "No Value" by "NA" in the original file)
wdf = df[['State','County','T2013','P2013']].copy().dropna(axis=0)

# Number of people in county
wdf['N2013'] =  list(map(int,100*np.array(wdf['T2013'])/np.array(wdf['P2013'])))

print(wdf)
```

               State              County      T2013  P2013    N2013
    4     California  Los Angeles County  1592424.0   21.4  7441233
    5       Illinois         Cook County   989186.0   25.3  3909826
    6          Texas       Harris County   828815.0   27.2  3047113
    7        Arizona     Maricopa County   735213.0   25.4  2894539
    8          Texas       Dallas County   482453.0   27.6  1748018
    ...          ...                 ...        ...    ...      ...
    3141     Montana    Petroleum County       93.0   24.6      378
    3142       Texas       Kenedy County       83.0   26.4      314
    3143       Texas         King County       57.0   27.5      207
    3144       Texas       Loving County       21.0   29.0       72
    3145      Hawaii      Kalawao County       19.0   21.5       88
    
    [3142 rows x 5 columns]



```python
# Find the smallest county.
#     Note using the pandas library is not scalable. We are only using it to keep the code compact
smallest_county = wdf.loc[wdf['N2013'].idxmin()]

print(smallest_county)
```

    State             Texas
    County    Loving County
    T2013              21.0
    P2013              29.0
    N2013                72
    Name: 3144, dtype: object



```python
Purdues_county_idx = wdf.index[wdf['County'] == "Tippecanoe County"].tolist()[0]

Purdues_county = wdf.loc[Purdues_county_idx]

print(Purdues_county)
```

    State               Indiana
    County    Tippecanoe County
    T2013               35027.0
    P2013                  26.4
    N2013                132678
    Name: 398, dtype: object


The value of P2013 is the percentage (%) of people considered obese.
- This value is the **observed obesity rate**
- In general, we are interested in what we call the **true underlying obesity rate** $\neq$ **observed obesity rate**.
    - A high **true underlying** obesity rate may indicate a systemic problem in the county (say, [a food desert](https://en.wikipedia.org/wiki/Food_desert))

Let's understand why *Loving County* may **not** actually have a 29% "underlying obesity rate".

### Understanding the difference between observed and true obesity rates
Assume 29% is the **observed obesity rate** in *Loving County*
- If 29% were also the **underlying obesity rate** (the rate related to health factors), how would the **observed obesity rate** fluctuate in *Loving County*?

Let's understand the difference between **observed** and **underlying** quantities.
- Assume the underlying obesity rate is $p=0.35$.
- There are $N=72$ people in *Loving County*.
- Hence, the probability $k$ of them are obese with a underlying obesity rate of $p$ is

a binomial distribution
$$
P(K=k|N=n) = {n \choose k} k^p (n-k)^{1-p}
$$

For *Loving County*:
$$
P(K=k|N=72) = {72 \choose k} k^p (72-k)^{1-p}
$$
Observed obesity rate of 29% means $k=21$.
The probability of this event is


```python
from scipy.stats import binom

# Given values
N = 72  # Total population (sample size)
k = 21  # Observed obesity cases
p = 0.35  # Underlying obesity rate (35%)

likelihood = binom.pmf(k, N, p)

print(f'The likelihood the underlying obesity rate is {int(p*100)}% and we observe it to be 29% is {int(likelihood*100)}%')

k = round(0.3*N)
cdf = binom.cdf(k, N, p)
print(f'The probability the underlying obesity rate is {int(p*100)}% and we observe it to be less than 30% is {int(cdf*100)}%')

```

    The likelihood the underlying obesity rate is 35% and we observe it to be 29% is 5%
    The probability the underlying obesity rate is 35% and we observe it to be less than 30% is 25%


## How to interpret data: Recap

- In machine learning, we often treat observed data as a realization of a random variable, meaning the data is assumed to be a sample drawn from an underlying probability distribution that captures the true nature of a phenomenon.
- The observed data is a reflection of some underlying reality, with the randomness accounting for variability in measurements, sampling, or external factors.

# 3. Conditional Probabilities (of Language Models)


## Introduction to Bigrams and Conditional Probability

In language modeling, a bigram is a pair of consecutive words in a text corpus. We use bigram models to estimate the probability of a word given its preceding word.

For example, in the sentence: "The boy who lived," the bigrams are:
- ("The", "boy")
- ("boy", "who")
- ("who", "lived")

The probability of predicting a word can be expressed as:
$$P(X_2 | X_1) = \frac{P(X_1, X_2)}{P(X_1)}$$

In this lecture, we will build a bigram model from text data and demonstrate how these conditional probabilities work.

We want to build a bigram model based on "Harry Potter-Sorcerer's Stone" and use that model to demonstrate conditional probability.

First, we need to install nltk package for building the bigram model and download the required dependency ('punkt') for using `work_tokenize()` function.


```python

import os

# Prompting the user to upload text data if not available.
if not os.path.exists('harry_potter.txt'):
    print("Please place the file 'harry_potter.txt' on the same folder as this notebook.")

!pip install nltk

import nltk
nltk.download('punkt')
```

    Requirement already satisfied: nltk in /Users/ribeirob/anaconda3/lib/python3.10/site-packages (3.7)
    Requirement already satisfied: click in /Users/ribeirob/anaconda3/lib/python3.10/site-packages (from nltk) (8.0.4)
    Requirement already satisfied: joblib in /Users/ribeirob/anaconda3/lib/python3.10/site-packages (from nltk) (1.1.1)
    Requirement already satisfied: regex>=2021.8.3 in /Users/ribeirob/anaconda3/lib/python3.10/site-packages (from nltk) (2022.7.9)
    Requirement already satisfied: tqdm in /Users/ribeirob/anaconda3/lib/python3.10/site-packages (from nltk) (4.64.1)


    [nltk_data] Downloading package punkt to /Users/ribeirob/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!





    True




```python
from nltk.data import find
from nltk import word_tokenize
from nltk import ngrams, FreqDist
from collections import defaultdict, Counter
import re

def build_bigram_model(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Generate bigrams
    bigrams = list(ngrams(tokens, 2))
    # Create frequency tables
    bigram_freqs = FreqDist(bigrams)
    unigram_freqs = FreqDist(tokens)
    return bigram_freqs, unigram_freqs

# Load your text data from a file
with open('harry_potter.txt', 'r') as file:
    text = file.read()

# We get the frequency table here.
bigram_freqs, unigram_freqs = build_bigram_model(text)
```

## Quiz!

Consider the following generation:
"The boy who lived"

Suppose we want to suggest another more likely word for "boy" that would appear often in the book.

#### We want to predict the probability of saying "boy" in the sentence "The ___  who lived"?

If we denote $X_1=\text{"The"}$, $X_2=\text{"boy"}$, $X_3 = \text{"who"}$, $X_4=\text{"lived"}$, which of the options predicts the probability of saying "boy" in the sentence "The ___  who lived":

A. $P(X_4, X_3, X_2, X_1)$

B. $P(X_2|X_4, X_3, X_1)$

C. $P(X_2|X_1)$

The correct answer is **B**.

Let's calculate each of the items using our bigram probabilities. First, we have:

$$P(X_1=\text{"The"}, X_2=\text{"boy"}, X_3 = \text{"who"}, X_4=\text{"lived"}) =$$ $$=P(X_1=\text{"The"}) \cdot P(X_2=\text{"boy"}|X_1=\text{"The"}) \cdot P(X_3 = \text{"who"}|X_2=\text{"boy"}, X_1=\text{"The"}) \cdot P(X_4=\text{"lived"}|X_3 = \text{"who"}, X_2=\text{"boy"}, X_1=\text{"The"})$$

Since we are using a bigram model (**the next word only depends on previous word**), the above can be simplified:

$$P(X_1=\text{"The"}, X_2=\text{"boy"}, X_3 = \text{"who"}, X_4=\text{"lived"}) =$$
$$=P(X_1=\text{"The"}) \cdot P(X_2=\text{"boy"}|X_1=\text{"The"}) \cdot P(X_3 = \text{"who"}|X_2=\text{"boy"}) \cdot P(X_4=\text{"lived"}|X_3 = \text{"who"})$$


```python
# We start by defining two functions.
# One for getting the unigram probability (for sentence start).
def get_unigram_prob(word, unigram_freqs):
    return unigram_freqs[word.lower()] / sum(unigram_freqs.values())

# The other for getting the bigram probability.
def get_bigram_cond_prob(word1, word2, bigram_freqs, unigram_freqs):
    return (bigram_freqs[(word1.lower(), word2.lower())]/sum(bigram_freqs.values()))/get_unigram_prob(word1.lower(),unigram_freqs)

# P(x_1) * P(x_2|x_1) * P(x_3|x_2) * P(x_4|x_3)
joint_prob = get_unigram_prob('The', unigram_freqs) * get_bigram_cond_prob('The', 'boy', bigram_freqs,unigram_freqs) * get_bigram_cond_prob('boy', 'who', bigram_freqs,unigram_freqs) * get_bigram_cond_prob('who', 'lived', bigram_freqs,unigram_freqs)

print(f"P(X_1 = \"The\") * P(X_2 = \"boy\"|X_1=\"The\") * P(X_3=\"who\"|X_2=\"boy\") * P(X_4=\"lived\"|X_3=\"who\")={joint_prob}")
```

    P(X_1 = "The") * P(X_2 = "boy"|X_1="The") * P(X_3="who"|X_2="boy") * P(X_4="lived"|X_3="who")=3.8440778030569724e-07


Then,

$P(X_2 = \text{"boy"} \mid X_4 = \text{"lived"}, X_3 = \text{"who"}, X_1 = \text{"The"}) = \dfrac{P(X_4 = \text{"lived"}, X_3 = \text{"who"}, X_2 = \text{"boy"}, X_1 = \text{"The"})}{P(X_4 = \text{"lived"}, X_3 = \text{"who"}, X_1 = \text{"The"})}$

- We have calculated the numerator in the previous part.
- The denominator requires us to sum the joint distribution over all possible values of $X_2$ in the frequency table of our bigram model.


```python
from tqdm import tqdm
# We know that P(x_4, x_3, x_1)=P(x_1) * P(x_3|x_1) * P(x_4|x_3)
# Let's calculate one term at a time

# P(x_1)
prob_x1 = get_unigram_prob('The', unigram_freqs)

# P(x_3|x_1) = \sum_{\forall x_2} p(x_3,x_2|x_1) =\sum_{\forall x_2} p(x_3|x_2)p(x_2|x_1)
prob_x3_given_x1 = 0
for i in tqdm(unigram_freqs):
    prob_x3_given_x1 += get_bigram_cond_prob('The', i, bigram_freqs, unigram_freqs) * get_bigram_cond_prob(i, 'who', bigram_freqs, unigram_freqs)

# P(x_4|x_3)
prob_x4_given_x3 = get_bigram_cond_prob('who', 'lived', bigram_freqs, unigram_freqs)

conditional_prob = joint_prob / (prob_x1 * prob_x3_given_x1 * prob_x4_given_x3)

print(f"P(X_2=\"boy\"|X_1 = \"The\", X_3=\"who\", X_4=\"lived\")={conditional_prob}")

```

    100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 6071/6071 [00:03<00:00, 1981.30it/s]

    P(X_2="boy"|X_1 = "The", X_3="who", X_4="lived")=0.4331270535611973


    


Finally,

Let's compare with the probability $P(X_2=\text{"boy"}|X_1=\text{"The"})$.
This can be found by calling the get_bigram_prob() function.



```python
bigram_cprob = get_bigram_cond_prob("The", "boy", bigram_freqs, unigram_freqs)
print(f"P(X_2 = \"boy\"|X_1 = \"The\") is {bigram_cprob}")
```

    P(X_2 = "boy"|X_1 = "The") is 0.007446297252958067


Revisiting the Quiz options with the calculated probabilities, we can see that the author really prefers "boy" to fill in "The ___ who lived", and that the other options are way off.


A. $P(X_4, X_3, X_2=\text{"boy"}, X_1) =$ 3.8440778030569724e-07

B. $P(X_2=\text{"boy"}|X_4, X_3, X_1) =$ 0.4331270535611973

C. $P(X_2=\text{"boy"}|X_1) =$ 0.007446297252958067

### Computing joint probabilities of a sentence


```python

import ipywidgets as widgets
from IPython.display import display

def generate_bigrams(input_text):
    tokens = nltk.word_tokenize(input_text.lower())
    bigrams = list(ngrams(tokens, 2))
    return bigrams

def display_bigrams(input_text):
    bigrams = generate_bigrams(input_text)
    display(bigrams)
    joint_prob = 1
    start = True
    count = 0
    for (a,b) in bigrams:
        count += 1
        if start:
            joint_prob = get_unigram_prob(a, unigram_freqs)
            print(f'P(X_{count})', end='')
            start = False
        joint_prob *= get_bigram_cond_prob(a, b, bigram_freqs, unigram_freqs)
        print(f'*P(X_{count+1}|X_{count})', end='')

    print(f"={joint_prob}\n")

input_box = widgets.Text(
    value='The boy who live',
    description='Input Text:',
    disabled=False
)

box = widgets.interact(display_bigrams, input_text=input_box)

```

## Conditional Probability: Recap

- In machine learning, predictions are performed given prior data.
- The prediction is stated as a conditional probability estimate:
    - Predict the missing data (e.g., future, missing word) given the observed data (e.g., past, observed words).

## 4. Laplace Smoothing (predicting under zero frequencies)

In real-world applications, not all combinations will appear in the training data. For example, you might encounter a pair like ("I", "hate") that doesn't exist in the text corpus.
- Laplace smoothing helps us address this issue by ensuring that every possible bigram has a positive probability.

The formula for Laplace smoothing in the conditional probability of two events $A$ and $B$:
$$P(A | B) = \frac{\text{count}(A,B) + C}{\text{count}(B) + C \times \langle\text{sample space size}\rangle}$$

#### Laplace Smoothing Example

When the sample size is not big enough, we will encounter division by 0 problems when calculating conditional probabilities. In that case, we want to use Laplace smoothing.

For example, suppose we have a text corpus like this:

corpus = [

    "I like to eat apples",
    
    "I like to eat oranges",
    
    "I like to play soccer"

]

When calculating the conditional probability of:

P("eat"|"I hate to")

We will encounter a division by 0 problem if we try to do it the normal way because "hate" is not in the data:

P("eat"|"I hate to") = P("I hate to eat")/P("I hate to")


```python
from collections import defaultdict
from nltk import ngrams, word_tokenize

corpus = [
    "I like to eat apples",
    "I like to eat oranges",
    "I like to play soccer"
]

vocabulary = ["I", "like", "to", "eat", "apples", "oranges", "play", "soccer"]
```

Laplace smoothing is a way to deal with the situations of conditioning on an event that does not appear in the data.
- In Laplace smoothing, when computing frequencies of occurence, we add a constant $C$ (normally $C=1$) to the numerator and $C~\times$`<number of elements>` to the demoninator.

By adding 1, you ensure that every possible bigram has a positive probability.

In our case, `<number of elements>` is the vocabulary size (V).


```python
V = len(vocabulary)

# Initialize count dictionaries
trigram_counts = defaultdict(int)
fourgram_counts = defaultdict(int)

# Populate the counts
for sentence in corpus:
    tokens = word_tokenize(sentence.lower())
    for trigram in ngrams(tokens, 3):
        trigram_counts[trigram] += 1
    for fourgram in ngrams(tokens, 4):
        fourgram_counts[fourgram] += 1

trigram_context = ("i", "hate", "to")
word_x4 = "eat"

# Laplace smoothing for the conditional probability
numerator = fourgram_counts[trigram_context + (word_x4,)] + 1
denominator = trigram_counts[trigram_context] + V

# Calculate probability
conditional_prob = numerator / denominator

print(f"P({word_x4} | {' '.join(trigram_context)}) = {conditional_prob}")
```

    P(eat | i hate to) = 0.125

