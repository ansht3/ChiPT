# Data Mining & Machine Learning
## CS37300
### Purdue University
**Instructor: Bruno Ribeiro**  


## Learning Outcomes

• We will learn about the different types of hypotheses  
• We will see an example of data bias and how to correct it

## Primer on hypotheses

## The Scientific Method

The scientific method follows these steps:
![image.png](lecture-stathyp_files/image.png)

## What is a hypothesis?

- Hypotheses are tentative statements of the expected relationships between two or more variables

- **Inductive hypotheses** are formed through inductively reasoning from many specific observations to tentative explanations (bottom-up)

- **Deductive hypotheses** are formed through deductively reasoning implications of theory (top-down)

- **Reasons for using hypotheses**
  - Provides focus and directs research investigation
  - Allows the investigator to confirm or refute relationships
  - Provides a useful framework for organizing and summarizing results and conclusions

## Types of hypotheses

### Broad categories
- **Descriptive**: propositions that describe a characteristic of an object
- **Relational**: propositions that describe the relationship between 2+ variables  
- **Causal**: propositions that describe the effect of one variable on another

### Specific characteristics
- **Non-directional**: a differential outcome is anticipated but the specific nature of it is not known (e.g., yelling at your boss will change your salary)
- **Directional**: a specific outcome is anticipated (e.g., CS graduates have the highest average starting salary of all Purdue graduates)

**Hierarchy (Stronger →):**
1. Descriptive Hypothesis
2. Non-Directional Relational Hypothesis
3. Directional Relational Hypothesis
4. Directional Causal Hypothesis

![image.png](lecture-stathyp_files/image.png)

## From claims to testable hypotheses

• Israel COVID cases breakdown Aug 17, 2021

| Age | Total Conditional Individuals (approx.) | Not Vax % | Fully Vax % | Severe Cases Not Vax per 100k | Severe Cases Fully Vax per 100k | Score function Conditional Efficacy |
|-----|------------------------------------------|-----------|-------------|-------------------------------|----------------------------------|-------------------------------------|
| [12,15] | 650,000 | 62.1% | 29.9% | 0.3 | 0.0 | 100.0% |
| [16,19] | 600,000 | 21.9% | 73.5% | 1.6 | 0.0 | 100.0% |
| [20,29] | 1,200,000 | 20.5% | 76.2% | 1.5 | 0.0 | 100.0% |
| [30,39] | 1,050,000 | 16.2% | 80.9% | 6.2 | 0.2 | 96.8% |
| [40,49] | 900,000 | 13.2% | 84.4% | 16.5 | 1.0 | 94.2% |
| [50,59] | 750,000 | 10.0% | 88.0% | 40.2 | 2.9 | 93.2% |
| [60,69] | 550,000 | 8.8% | 89.8% | 76.6 | 8.7 | 89.8% |
| [70,79] | 350,000 | 4.2% | 94.6% | 190.1 | 19.8 | 90.6% |
| **[80,89]** | **120,000** | **5.6%** | **92.6%** | **252.3** | **47.9** | **84.0%** |
| **90+** | **50,000** | **6.1%** | **90.5%** | **510.9** | **38.6** | **93.0%** |

## From claims to testable hypotheses

**Claim**: Vaccine efficacy is higher for 90+ y/o individuals than for [80,89] y/o individuals

**Building the hypothesis:**

- **Step 1**: Express data as random variables (jointly). E.g.:
  - $A$ = age
  - $S_V$ = severe case vax per 100k
  - $S_U$ = severe case unvax per 100k
  - $Y$ = observed vaccine efficacy = $S_U/(S_U + S_V)$

## From claims to testable hypotheses

**Claim**: Vaccine efficacy is higher for 90+ y/o individuals than for [80,89] y/o individuals

**Building the hypothesis:**

- **Step 2**: Restate claim as a hypothesis about the relationship between the random variables, e.g.,
  - Recall: $A$ = Age; $Y$ = observed vaccine efficacy
  - Hypothesis: $E[Y|A \geq 90] > E[Y|80 \leq A \leq 89]$

- **Step 3**: Determine type of hypothesis (and consider whether you can make it stronger), e.g.,
  - Directional-relational: $A \geq 90$ is associated with larger $Y$ than $80 \leq A \leq 89$

## From claims to testable hypotheses

**Claim**: Vaccine efficacy is higher for 90+ y/o individuals than for [80,89] y/o individuals

- **Some hypotheses:**
  - **Descriptive**: Efficacy values vary (i.e., $Y$ varies).
  - **Non-directional relational**: $Y$ varies based on age (i.e., Age and $Y$ are associated)
  - **Directional-relational**: Age $\geq$ 90 individuals have higher efficacy (i.e., Age $\geq$ 90 is associated with smaller $Y$)
  - **Causal-relational**: Age > 90 folks have higher vaccine efficacy because these are monitored more closely in nursing homes and get medical interventions earlier before they get too sick

## Using Data to Test Hypotheses

## Example:

• **CLAIM 1**: The temperature of the planet is rising and the increase is due to human activities such as fossil fuel use and deforestation.

• Which kind of data could support such claim?

**Emissions correlate with temperature**

![image.png](lecture-stathyp_files/image.png)

**Not enough**
**Why?**

Global Average Temperature vs. Number of Pirates shows spurious correlation between declining pirate numbers and rising temperatures from 1820-2000

## Directional Relational Hypothesis

• **CLAIM 2**: The temperature of the planet is rising with increased human activity

**Quiz 1!**
- (A) Non-directional Relational Hypothesis  
- (B) Directional Causal Hypothesis  
- (C) Directional Relational Hypothesis

**Answer**
- **(C) Directional Relational Hypothesis**

![image.png](lecture-stathyp_files/image.png)

## Causal Claims without Experiments are Possible

**CLAIM 3**: The temperature of the planet is rising and the increase is **DUE** to human activities such as fossil fuel use.

- How would you test it?

**How it is tested:**
- Climate models (we know how climate works)
  - We know how much energy the sun outputs
  - We know how much energy the planet radiates back into space
  - We know where the energy goes inside the planet
  - We know how much CO2 is produced by different sources and how it absorbs heat
  - https://earthobservatory.nasa.gov/features/EnergyBalance

- Historic natural experiment events:

  ```"Coal-burning in Siberia after volcanic eruption led to climate change predicted by our models 250 million years ago"```

**Quiz 2!**
- (A) Non-directional Relational Hypothesis  
- (B) Directional Causal Hypothesis
- (C) Directional Relational Hypothesis


**Answer:**
- **(B) Directional Causal Hypothesis**

## Is Aspirin effective in reducing cancer risk?

Here, we are looking at causal effects...

- **Data**
  - A person represented by random variable $X \in \{\{Age\}, \{Sick, Not Sick\}, ...\}$
  - Recruit people: $x_{john}$, $x_{mary}$, $x_{eve}$, $x_{adam}$, ...
  - Medicine to take: $T \in \{aspirin, placebo\}$
  - Cancer observation: $Y \in \{1 - \text{Cancer in 1yr}, 0 - \text{No Cancer in 1yr}\}$

- **Hypothesis**
  - Force ½ (randomly chosen) of the people to take aspirin: $Y|X, do(T = aspirin)$
    - Here, the **do()** notation means forcing T to be something (intervention)
  - Force remaining ½ to NOT take Aspirin: $Y|X, do(T=placebo)$
  - **Hypothesis**: $E[Y|X, do(T=aspirin)] < E[Y|X, do(T=placebo)]$

**Quiz 3!**
- (A) Non-directional Relational Hypothesis  
- (B) Directional Causal Hypothesis
- (C) Directional Relational Hypothesis

**Answer**
- **(B) Directional Causal Hypothesis**


```python
# Aspirin RCT (toy simulation) — minimal, vectorized

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

np.random.seed(42)
n = 10_000

# Simulate participants
df = pd.DataFrame({
    "age": np.random.normal(55, 12, n),
    "risk_factor": np.random.uniform(0, 1, n),
    "treatment": np.random.choice(["aspirin", "placebo"], size=n)
})

# Baseline risk and treatment effect (aspirin RR = 0.8)
base = 0.02 + 0.03 * (df["age"] - 40) / 40 + 0.05 * df["risk_factor"]
rr   = np.where(df["treatment"].eq("aspirin"), 0.8, 1.0)
p    = np.clip(base * rr, 0, 1)

# Cancer outcome
df["cancer"] = (np.random.rand(n) < p).astype(int)

# Summary by arm
summary = df.groupby("treatment")["cancer"].agg(cases="sum", total="count", rate="mean")
print("\n=== RCT RESULTS ===")
print(summary)

# Effect size (relative risk)
asp, plc = summary.loc["aspirin","rate"], summary.loc["placebo","rate"]
RR  = asp / plc
RRR = 1 - RR
print(f"\nRelative Risk (RR): {RR:.3f}")
print(f"Risk Reduction (1−RR): {RRR*100:.1f}%")

# Minimal visualization
plt.figure(figsize=(5,4))
plt.bar(["Aspirin","Placebo"], [asp, plc], alpha=0.8)
plt.ylabel("Cancer rate")
plt.title("Cancer rate by treatment")
for i, v in enumerate([asp, plc]):
    plt.text(i, v + 0.001, f"{v:.3f}", ha="center")
plt.ylim(0, max(asp, plc)*1.2)
plt.tight_layout()
plt.show()

```

    
    === RCT RESULTS ===
               cases  total      rate
    treatment                        
    aspirin      243   5087  0.047769
    placebo      257   4913  0.052310
    
    Relative Risk (RR): 0.913
    Risk Reduction (1−RR): 8.7%



    
![png](lecture-stathyp_files/lecture-stathyp_19_1.png)
    


## Q3: Traditional Gender Roles

**Fathers who perform an equal share of household chores are more likely to have *daughters* who aspire to less "traditionally feminine occupations"**

- There is a question of **interpretation**.
  - Writing a hypothesis formally avoids miscommunication.
  - Since the author singled out **daughters** rather than **children**, the author probably wants to constrast girls to boys under the same scenarios
    - But if not, the formalization is different and the outcome may be different.

- **Simplest Data:**
  - A random child represented by three random variables (X,F)
  - $X \in \{Boy, Girl\}$, $F \in \{Father Helps, Does not Help\}$
  - Recruit young children (1/2 boys, 1/2 girls): $X_{john}$, $X_{mary}$,...
  - Observe father household chores: $F_{john}$, $F_{mary}$, ...

- **Hypothesis**
  - Check the aspiration of the child $Y_F \in \{0 = \text{Traditional Fem. job}, 1 = \text{Untraditional}\}$
  - **Hypothesis (in 2 parts):**
    - $E[Y|F = \text{Helps}, X = \text{Girl}] > E[Y|F = \text{NoHelp}, X = \text{Girl}]$  
      **and** (since author singled out daughters rather than children)
    - $E[Y|F = \text{Helps}, X = \text{Boy}] \leq E[Y|F = \text{NoHelp}, X = \text{Boy}]$

**Quiz 4!**
- (A) Non-directional Relational Hypothesis  
- (B) Non-directional Causal Hypothesis  
- (C) Directional Relational Hypothesis


**Answer**
- **(C) Directional Relational Hypothesis**

## The Strong Effect of Data Biases

### Observational Data Biases

![image.png](lecture-stathyp_files/image.png)

- Your experience with buses at peak hours:
  - Bus at 99% capacity at peak hours
  - Students wait on average 17 minutes and 9 seconds for bus to arrive

- Purdue's transportation admin:
  - buses at peak hour are at 60% capacity
  - average bus inter-arrival time is 10 minutes

**?**

## Example of data bias: Inspection Paradox

### Data bias explanation

- 40 minutes / 4 buses = 10 min inter-arrival time

- How long do you wait?
  - Assume you arrive uniformly during these 40 minutes

- What is the probability you will arrive within the 37 minute interval?

- What is the average waiting time if you arrive at the 37 min interval?

```
Bus 1 ----[37 minutes]---- Bus 2 -[1 min]- Bus 3 -[1 min]- Bus 4 -[1 min]-
```


```python
fig, ax = plt.subplots(figsize=(8, 1.2))
left = 0.0
for wi in w:
    ax.barh(0, wi, left=left, height=1, alpha=0.3)
    ax.text(left + wi/2, 0, f"{int(wi)}", ha='center', va='center')
    left += wi
ax.set_xlim(0, T); ax.set_yticks([]); ax.set_xlabel("minutes (total 40)")
ax.set_title("One long gap (37) + three short gaps (1,1,1)")
plt.tight_layout(); plt.show()
```


    
![png](lecture-stathyp_files/lecture-stathyp_24_0.png)
    


## Fixing data biases: Inverse weighted estimator

• Suppose we see observations from discrete random variable $X$ with distribution $p_x(.)$

• We want to compute $E[Y]$ the average of $Y$ with distribution $p_y(.)$

Note that (if $X$ is discrete):

$$E[Y] = \sum_{w=-\infty}^{\infty} w p_y(w) = E\left[X \frac{p_y(X)}{p_x(X)}\right] = \sum_{w=-\infty}^{\infty} w p_x(w)\frac{p_y(w)}{p_x(w)}$$

- **Our bus example**
  - $Y$ is the student's wait time with probability $p_y(w)$
  - $X$ is the bus interval according to Purdue with probability $p_x(w)$
  - We know $p_y(w) \propto p_x(w) \times \frac{w}{2}$ 
      - The half is due to the average wait being only half of the length of the interval
      - $\propto$ means "proportional to".
          - Need to divide by average $E_x[X]$ to renormalize probabilities

$$E[Y] = \sum_{w \in \{37,1\}} w p_y(w) = \sum_{w \in \{37,1\}} w \frac{p_x(w)\frac{w}{2}}{E_x[X]} = 37 \times \frac{1}{4} \times \frac{37}{20} + 3 \times \frac{1}{4} \times \frac{1}{20} = 17.15$$


```python
# Inspection paradox in a 40-min window with 4 buses: [37, 1, 1, 1]
import numpy as np
import matplotlib.pyplot as plt

w = np.array([37, 1, 1, 1], dtype=float)
T = w.sum()

# --- Naive unweighted observed samples (equal-probability buses) ---
naive_wait = (w.mean()) / 2

# --- Student's biased observation (length-biased arrivals) ---
p_len = w / T                          # P(arrive in interval i)
student_wait = (w/2 @ p_len)           # E[wait] under length bias

# ---Importance / "inverse-weighted" check ---
# p_x: equal-probability buses; p_y: length-biased over intervals
p_x = np.full(len(w), 1/len(w))
p_y = (p_x * w) / (p_x @ w)            # ∝ w; normalizes to length-bias

print("Purdue's collected expected wait (mean-interval/2):        {:.2f} min".format(naive_wait))
print("Students' observed expected wait (length-biased):          {:.2f} min".format(student_wait))

# --- Monte Carlo (simulated) sanity check (uniform arrival in [0, T]) ---
rng = np.random.default_rng(0)
N = 100_000
arrivals = rng.uniform(0, T, size=N)
edges = np.concatenate([[0], np.cumsum(w)])
idx = np.searchsorted(edges, arrivals, side='right') - 1
mc_wait = edges[idx+1] - arrivals
print("Simulated (Monte Carlo) E[wait] (uniform in [0,T]):        {:.2f} min".format(mc_wait.mean()))
```

    Purdue's collected expected wait (mean-interval/2):        5.00 min
    Students' observed expected wait (length-biased):          17.15 min
    Simulated (Monte Carlo) E[wait] (uniform in [0,T]):        17.17 min



```python
# --- Importance weighting to recover the unweighted (equal-bus) average from MC samples ---
# We sampled arrivals ~ uniform on [0,T] ⇒ interval index 'idx' is drawn from p_y(i) ∝ w_i
# Weight each sample by p_x(i)/p_y(i) ∝ 1/w_i to estimate the equal-bus expectation.
imp_raw = 1.0 / w[idx]                     # ∝ p_x(idx)/p_y(idx)
imp_w   = imp_raw / imp_raw.sum()          # self-normalized weights
naive_from_MC = np.sum(imp_w * mc_wait)    # ≈ naive_wait

print("Unweighted bus-average via Simulation + Inverse weighted estimation:          {:.2f} min".format(naive_from_MC))
```

    Unweighted bus-average via Simulation + Inverse weighted estimation:          5.04 min


## Summary

- Types of hypotheses:
   - **Descriptive**
   - **Relational**
     - **Non-directional**
     - **Directional**, and
   - **Causal (directional)**
- Translating claims to testable hypotheses requires declaring random variables and stating associations or interventions.  
- Data biases (inspection paradox) can drastically skew naive estimates; inverse probability weighting recovers correct expectations.

## References
- NASA Earth Observatory: *Earth’s Energy Budget*.  
- NOAA Global Monitoring Laboratory: Atmospheric CO$_2$ records.
