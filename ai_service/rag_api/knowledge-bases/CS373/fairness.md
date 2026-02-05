## CS37300 - Data Mining & Machine Learning

----
### Fairness

## Announcements
- Next two classes we will have an in-class review (80% in our last poll prefer in-class)
- Please come prepared with lectures we should revisit and questions you want answered.

## Fairness: A Challenge for Machine Learning

-  There is a common misconception that data science is objective
    - "The data does not lie"
    - True, but the data can be misleading
- A good reference for fairness in machine learning is [Fairness and machine learning: Limitations and Opportunities](https://fairmlbook.org/) by Solon Barocas, Moritz Hardt, Arvind Narayanan.
    - Part of the material of today's class can be found in these [online slides](https://fairmlclass.github.io/4.html#/)

### Example (Machine Learning for Bail Decisions)

- Police in the U.S. make about 12M arrests each year

<center><img src="releasedetain.png" width=300px /></center>

- Release vs. Detain is a high-stakes decision
    - Pre-trial detention can go up to 9 to 12 months
    - Consequential for jobs and families of defendants as well as crime
    
(Ack: Hima Lakkaraju)

- Bail decision is important and prone to human error:
<center><img src="baildecision.png" width=400px /></center>
- Judge is making a prediction: Will the defendant commit ‘crime’ if released on bail?

- Can *data science* help?
    - Northpointe developed COMPAS, an algorithm used to predict recidivism (commit a crime again)
    - COMPAS was found to have much higher false positive rate for african-americans than caucasians (Fig2, [Larson et al. ProPublica, 2016](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)):
<center><img src="COMPASS.jpg" width=450px /></center>

### Example (Machine Learning for Job Search)

- XING.com is a job platform similar to Linked-in
    - XING was found to rank less qualified male candidates higher than more qualified female candidates (Table I, [Lahoti et al. 2018](https://arxiv.org/pdf/1806.01059.pdf))
    
<center><img src="xing.png" width=400px /></center>


### Fairness

- The above examples point to possible unfair outcomes of classifiers and ranking algorithms
- Sometimes the unfair outcome is a due to biases within the data
- Sometimes the unfair outcome is the result of other mistakes:
    - Maybe the data cannot answer the question
    - Maybe the algorithm used cannot answer the question
    

### Typical Setup

- $X$ are features of an individual
- $X_A$ is a sensitive attribute (race, gender, ...)
- $Y$ is actual outcome (target variable)
- $C = C(X,X_A)$ classifier maps $X$ and $X_A$ to some prediction $C$

### Task Definition is Challenging

- $X$ may incorporate all sorts of measurement biases
- $X_A$ is often not even known, ill-defined, misreported, inferred
- $C$ is often not well defined, e.g., large data science production system
- $Y$ is often poor proxy of actual variable of interest

### Data Biases

([Barocas and Selbst, 2016](http://www.californialawreview.org/wp-content/uploads/2016/06/2Barocas-Selbst.pdf)) lists a few sources of data biases:

- **Skewed sampling:** If the initial data has a bias, such bias may compound over time: Future observations confirm prediction and fewer opportunity to make observations that contradict prediction. One example is police record. The record of crimes only come from those crimes observed by police. The police department tends to dispatch more officers to the place that was found to have higher crime rate initially and is thus more likely to record crimes in such regions. Even if people in other regions have higher crime rate later, it is possible that due to less police attention, the police department still record that these regions have lower crime rate. The prediction system trained using data collected in this way tends to have recommend less policing in regions with less police.

- **Tainted samples:** Any classifier will just mimic the existing bias in data. For example, in word embeddings trained on Google News articles “exhibit female/male gender stereotypes to a disturbing extent”, e.g., the relationship between “man” and “computer programmers” was found to be highly similar to that between “woman” and “homemaker” ([Bolukbasi et al. 2016](https://arxiv.org/pdf/1607.06520.pdf)).

- **Limited features:** Features may be less informative or reliably collected for minority group(s). If the reliability of the label from a minority group is much lower than the counterpart from a majority group, the system tends to have much lower accuracy for the prediction of the minority group due to noise.

- **Sample size disparity:** If the training data coming from the minority group has fewer examples than those coming from the majority group, the classifier will have an incentive to focus on the majority group and treat the minority group as "noise" that need not to be predicted accurately.

- **Sensitive attribute proxies:** Even if sensitive attribute (attributes that are considered should not be used for a task e.g. race/gender) are not used for training a classifier, there can be other features always be other features that are proxies of the sensitive attribute (e.g. neighborhood). If such features are included, the bias will still happen. Sometimes, it is hard to determine if a relevant feature is too correlated with protected features and if we should include it in training.

(Ack Ziyuan Zhong)

### Removing Data Biases is Hard

- **Skewed sampling** happens more often than one imagines. For instance:
    - The movies we watch on Netflix are skewed towards recommended movies.
        - These, in turn, are skewed towards the movies we watch on Netflix.
            - Which in turn further skews the movies we watch
                - Which further skews the recommended movies...
    - This also creates a [filter bubble](https://en.wikipedia.org/wiki/Filter_bubble), where we only watch movies that are similar to the ones we have already watched (little diversity).

- **Tainted samples:** Large text data is a significant source of bias in machine learning for natural language (used to train voice assitants such as Amazon's Alexa, Google Assistant, Apple's Siri). Which sources of text data are unbiased? Books? Wikipedia? Unclear.

- **Limited features:** Can be corrected if we have access to the original individuals and can rectify the data. Often, however, forcing answers in surveys will elicit random answers. Moreover, data collection is an industry that makes more money if more data is collected. The incentive of data collectors is not always aligned with accuracy.

- **Sample size disparity**: One group has much larger representation in the training data than the another group. There are techniques to try to correct disparities. We will see these later.

- **Sensitive attribute proxies:** Seems easy: *just ignore sensitive attributes*. It is surprisingly hard as we see next. 

### Sensitive Attribute Proxies are Hard to Eliminate

- Q: Consider three features, defined by binary features $(X_\text{gender}, X_1, X_2)$, with $X_\text{gender}, X_1, X_2 \in \{0,1\}$.
    - Assume $X_\text{gender}$ is a protected feature (should not be included for classification). 
    - Assume $X_\text{gender}$ and $X_1$ are independent in our data. 
    - Assume $X_\text{gender}$ and $X_2$ are independent in our data. 
    - Can we conclude that if we removed $X_\text{gender}$ from the data, we can safely keep $X_1$ and $X_2$?

- A: **No, the vector $X'= (X_1,X_2)$ may still be a proxy for $X_\text{gender}$**
    - If $X_\text{gender}$ and $X_1$ are independent and $X_\text{gender}$ and $X_2$ are independent, **it does not mean** $X_\text{gender}$ and $X' = (X_1,X_2)$ are independent!
    - Example: 
        - Assume $X_1$ and $X_2$ are independent and $X_\text{gender} = X_1 \text{ XOR } X_2$. 
        - Then, $X_\text{gender} =1$ if $(X_1,X_2) \in \{(0,1),(1,0)\}$ and $X_\text{gender} = 0$ if $(X_1,X_2) \in \{(1,1),(0,0)\}$. 
        - But $X_\text{gender}$ is independent of each individual variable $X_1$ and $X_2$.

-----

Lecture stopped here


### Sample Size Disparity and Fairness Challenges 
#### Demographic parity classifier 

Wanted property:

- Demographic parity
    - Classifier $C$ satisfies demographic parity if $C$ is independent of $X_A$.
    - That is, if the output of C is binary 0/1, this means $$P(C=1 | X_A=a) = P(C=1 | X_A = b)$$ for all groups $a,b$.
    - Approximate parity: $$| P(C=1 | X_A=a) - P(C=1 | X_A = b) | \leq \epsilon$$ for some small $\epsilon$.

- Issues:
    - Data collection quality (laziness)
        - Collect random people in group $a$ but only qualified people in group $b$.
        - Can happen for lack of training data (see sample size disparity earlier)
    - Not compatible with optimal classifier
        - Rules out perfect classifier $C(X,X_A)=Y$ when true base rates are different: $P(C=1 | X_A = a) \neq P(C=1|X_A = b)$.

(Partial ack. Moritz Hardt)

### Sample Size Disparity and Fairness Challenges
#### Accuracy parity classifier

- Classifier C satisfies accuracy parity if $$P(C = Y | X_A = a) = P( C=Y | X_A = b)$$ for all groups $a,b$.

- Solves:
    - Discourages data collection laziness by equalizing error rates across groups.
        - Classifier error is bounded by the data collection quality of all groups
    - Allows perfect classifier $C(X,X_A)=Y$.
- Issue:
    - The type of error matters:
        - Allows us to make up for rejecting qualified women by accepting unqualified men.
        
(Partial ack. Moritz Hardt)

### Sample Size Disparity and Fairness Challenges
#### True positive parity classifier

- Assume $C$ and $Y$ are binary 0/1-variables.
- **Definition**:
    - A classifier C satisfies true positive parity if for all groups $a,b$ $$P(C=1∣Y=1,X_A = a)=P(C=1∣Y=1,X_A = b)$$.

- This is also called *equal opportunity* ([Hardt et al. (2016)](https://arxiv.org/abs/1610.02413)).

- Solves:
    - The type of error matters. Focuses on positive outcomes
    - Suitable when positive outcome (Y = 1) is desirable

- Issue:
    - Primary harm is due to imbalance in false negatives.
    
(Partial ack. Moritz Hardt)

### Sample Size Disparity and Fairness Challenges
#### Equalized odds classifier

- Assume $C$ and $Y$ are binary 0/1-variables.
- **Definition**:
    - A classifier $C$ has *equalized odds* ([Hardt et al. (2016)](https://arxiv.org/abs/1610.02413)) if
    - Classifier $C$ satisfies true positive parity if $$P(C=1∣Y=1,X_A = a)=P(C=1∣Y=1,X_A = b)$$ for all groups $a,b$.
    - Classifier $C$ satisfies true negative parity if $$P(C=1∣Y=0,X_A = a)=P(C=1∣Y=0,X_A = b)$$ for all groups $a,b$.
- A classifier $C$ will satisfy equalized odds if $C$ is conditionally independent of $X_A$ given $Y$.

- Solves:
    - The type of error matters by balancing positive and negative outcomes

- Issue:
    - Can be too conservative
    
(Partial ack. Moritz Hardt)

### Sample Size Disparity and Fairness Challenges
#### Predictive value parity classifier

- Assume $C$ and $Y$ are binary 0/1-variables
- **Definition**: 
    - A classifier $C$ satisfies 
        - Positive predictive value parity if for all groups a,b $$P(Y=1∣C=1,X_A=a)=P(Y=1∣C=1,X_A = b).$$
        - Negative predictive value parity if for all groups a,b $$P(Y=1∣C=0,X_A=a)=P(Y=1∣C=0,X_A = b).$$

- Solves:
    - Equalizes chance of success given acceptance
    
(Partial ack. Moritz Hardt)

#### Revisiting Northpointe COMPAS vs Probublica

- Probublica's charge:
    - Black defendants experienced higher false positive rate.

- Northpointe's defense:
    - Scores satisfy accuracy parity.
    

### Individual Fairness

- The previous criteria were all group-based.
- We will now see an individual-based criteria. 
- It was first proposed by [Dwork et al., 2012](https://arxiv.org/abs/1104.3913), one of the foundational works in fairness. 

- Let $C$ be our classifier with $K$ classes.
- Let $X \in \mathbb{R}^p$ be the attributes we will use in our classifier.
- Define two distance functions $D:[0,1]^K \to \mathbb{R}$ and $d:\mathbb{R}^{2 p } \to \mathbb{R}$.
    - $D$ is a distance between two discrete $K$-class distributions.
    - $d$ is the distance between two features

- Then, individual fairness is defined as $D(P(C | X), P(C | X')) \leq d(X,X’)$.

### Fairness Trade-offs

- Assume differing base rates $P(Y=1|X_A = a) \neq P(Y=1|X_A = b)$ and an imperfect classifier $C\neq Y$. Then, either
    - Positive rate parity fails, or
    - Predictive value parity fails

- Also true for risk scores ($P(Y=C)$)
    - This trade-off also happens when predicting probabilities rather than hard values $C = \langle\text{value}\rangle$ ([Kleinberg et al. (2016)](https://arxiv.org/abs/1609.05807))

### Example: FICO credit scores

- Based on sample of 301536 TransUnion TransRisk scores from 2003 (made available by US Federal Reserve)

- $R$: Credit score ranging from 300 to 850

- $Y$: Default (failed to pay debt for at least 90 days on at least one account)

- $A$: Race (Asian, Black, Hispanic, White)

(Ack. Moritz Hardt)

#### FICO base rates

<center><img src="fico-marginals.svg" width=800px /></center>
(Ack. Moritz Hardt)

#### FICO score targets
<center><img src="fico-targets.svg" width=800px /></center>
(Ack. Moritz Hardt)

### Counterfactual Fairness

- All previous definitions of fairness are mostly meaningless in the presence of confounders
    - Example: Simpson's paradox from our lecture on causality

Counterfactual fairness considers fair predictors in the presence of confounders:
- Let $X$ be a set of attributes and $X_R$ be $X$ without the protected attribute $X_A$

- A **counterfactual fair classifier** gives the same prediction even when the individual is forced to be part of groups $a$ or $b$  [(Kusner et al., 2017)](https://proceedings.neurips.cc/paper/2017/file/a486cd07e4ac3d270571622f4f316ec5-Paper.pdf): $$P(C=y|  X_R=r, X_A=a) = P(C(X_A=b)=y | X_R = r, X_A = a)$$ 
    - **Notation:** $P(C(X_A=b))$ is the same as $P(C|\text{do}(X_A=b))$ we have seen in our causality class.
    - That is, given we have seen $X_R=r$ and $X_A = a$ in our data and our prediction is $y$ with a given probability, then the prediction $Y=y$ for forcing $X_A=b$ should also have the same probability.

- Note that this is **different** from just "changing" $X_A=a$ to $X_A=b$. 
    - For instance, in the bank loan example, just changing $X_A = \text{"White"}$ to $X_A = \text{"Black"}$ will not change their FICO score
    - While $\text{do}(X_A = \text{"Black"})$ would also have an impact on the FICO score

- Implementing counterfactual fairness in with real-world is still mostly an open problem

- **Issues:** 
    - Counterfactual fairness does not guarantee demographic parity
        - Hence, $C$ may depend on $X_A$.
    - The attributes in $X_R$ that are descendents of $X_A$ in the causal DAG are hard to use.
        - Generally, counterfactually fair classifierrs will **remove** all attributes in $X_R$ that are descendants of $X_A$.
        - In practice, it is hard to define the causal DAG.
        - Deciding which features are descendants of $X_A$ and removing them may lead to a large loss in accuracy, while most of the removed features are not strongly influenced by $X_A$.



```python

```
