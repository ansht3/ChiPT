# **CS58700 - Foundations of Deep Learning**

# **Spring 2026**

# **Instructor and Copyright: Bruno Ribeiro**

# **Bayesian Deep Learning: Markov Chain Monte Carlo & Hamiltonian Monte Carlo**

# **Reading:**

The reading for this lecture:

Reading:

- (Neal, 2011) Neal, Radford M. [MCMC using Hamiltonian dynamics](https://arxiv.org/abs/1206.1901). Handbook of Markov Chain Monte Carlo 2, no. 11 (2011).
- Chib, Siddhartha, and Edward Greenberg. [Understanding the Metropolis-Hastings](https://eml.berkeley.edu/reprints/misc/understanding.pdf) [Algorithm.](https://eml.berkeley.edu/reprints/misc/understanding.pdf) The American Statistician 49, no. 4 (1995): 327-335

Suggested reading:

- Geyer, Charles J. [Markov Chain Monte Carlo Lecture Notes](https://www.stat.umn.edu/geyer/f05/8931/n1998.pdf) (1998). This is a complete graduate-level course covering Monte Carlo foundations, Metropolis-Hastings, and MCMC theory.
# **Bayesian Deep Learning**

Suppose we have a neural network classifier and a training dataset . p(y|x;W) D = {(xi , yi )}N i=1

- The likelihood of the data given the model is

$${\mathcal{L}}(\mathbf{W},{\mathcal{D}})=\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}).$$

- The maximum likelihood estimator (MLE) obtains

$$\mathbf{W}^{\star}={\underset{\mathbf{W}}{\operatorname{argmax}}}\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}).$$

- But is just one model. There may be weight matrices (models) that achieve the same or nearly the same likelihood. W⋆ W′ ≠ W⋆
- If these other alternative models give the same (different) softmax outputs, this may allow us to be more (less) confident in our predictions.
- **Bayesian models:** In Bayesian modeling, we want to be able to sample from the posterior of models given the data:

$$\mathbf{W}_{\mathrm{r.v.}}\sim p(\mathbf{W}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N}).$$

- Each sampled is a model. Then, the label prediction can be described as Wr.v.
$p_{\text{Bayesian model}}(\mathbf{y}|\mathbf{x};\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})=\int_{\mathbf{W}}p(\mathbf{y}|\mathbf{x};\mathbf{W})p(\mathbf{W}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})d\mathbf{W},$

which is clearly intractable.

- In practice, we will sample a few models i.i.d. from , . The following model output is an unbiased estimate of : W(1) r.v. ,…,W(K) r.v. W(k) r.v. ∼ p(W|{(xi, yi)} N i=1 ) k = 1,…, K pBayesian model(y|x)

$${\hat{\vec{p}}}_{\mathrm{Bayesian~model}}\bigl(\mathbf{y}|\mathbf{x};\{\bigl(\mathbf{x}_{i},\mathbf{y}_{i}\bigr)\}_{i=1}^{N}\bigr)={\frac{1}{K}}\sum_{k=1}^{K}p(\mathbf{y}|\mathbf{x};\mathbf{W}_{\mathrm{r.v.}}^{(k)})$$

## **Bayes Theorem and Model Posterior**

**Q1:** How do we obtain ? p(W|{(xi, yi)} N i=1 )

**A1:** We can apply Bayes theorem.

- Let be the prior probability of . For instance, . P(W) W W ∼ Normal(0, I)
- Bayes theorem:

$$p(\mathbf{W}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})={\frac{\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W})P(\mathbf{W})}{p(\{\mathbf{y}_{i}\}_{i=1}^{N}|\{\mathbf{x}_{i}\}_{i=1}^{N})}},$$

where

$$p(\{\mathbf{y}_{i}\}_{i=1}^{N}|\{\mathbf{x}_{i}\}_{i=1}^{N})=\int_{\mathbf{W}}\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W})P(\mathbf{W}).$$

## **Rejection sampling (detour)**

- In rejection sampling, we want to sample from X p(x)
	- First we need a proposal distribution from which we will sample examples q(x)
		- Unlike , we know how to sample from . p(x) q(x)

- E.g., is a multivariate Normal distribution q(x)
- First need to know a value such that . M M ≥ supx p(x) q(x)
- We will then generate samples according to an acceptance-rejection sampling algorithm.

Acceptance-rejection sampling algorithm:

- 1. sample from the proposal distribution x ∼ q(x) q(x)
- 2. sample independently of u ∼ Uniform(0, 1) X
- 3. while , reject and GOTO 1: u > p(x) Mq(x) x
- 4. Accept (output) as a sample from . x p(x)

**Lemma:** Let be sampled using the acceptance-rejection algorithm. Then . X′ X′ ∼ p(x)

**Proof:** Let and , then X′ ∼ acc-rej algo X ∼ q(x)

$$p(X^{\prime}=x)=p(X=x|\mathrm{Accept})={\frac{p(X=x,\mathrm{Accept})}{p(\mathrm{Accept})}}=p(x)$$

because

$${\frac{P(X=x,\mathrm{Accept})}{P(\mathrm{Accept})}}={\frac{P(\mathrm{Accept}|X=x)p(X=x)}{P(\mathrm{Accept})}}={\frac{{\frac{p(x)}{M(x)}}q(x)}{P(\mathrm{Accept})}}={\frac{{\frac{p(x)}{M}}}{P(\mathrm{Accept})}}=p(x)$$

as

$$P(\text{Accept})=\int P(\text{Accept}|X=x)p(X=x)dx=\int\frac{p(x)}{Mq(x)}q(x)dx=\frac{1}{M}\int p(x)dx=\frac{1}{M}$$

## **Bayesian modeling: Posterior sampling via rejection sampling (impractical)**

Acceptance-rejection sampling algorithm for posterior sampling.

Let $M\geq\frac{p(\mathbf{W}|\{(\mathbf{x}_i\mathbf{y}_i)\}_{i=1}^N)}{P(\mathbf{W})},\forall\mathbf{W}$ be a constant.

- 1. sample from the proposal distribution , which is our prior over the neuron weights W′ ∼ q(W) = P(W) P(W)
- 2. sample independently of 3. while , reject and GOTO 1: u ∼ Uniform(0, 1) W′ u > p(W′ |{(xi,yi )}N i=1 ) MP(W′) W′

- 4. Accept (output) as a sample from . W′ p(W|{(xi, yi)} N i=1 )
- Assumption:
	- , i.e., the posterior support is contained in the support of the proposal distribution. supp(p(W|{(xi, yi)} N i=1 )) ⊆ supp(q(W))
	- This assumption will be very important when we study GANs and diffusion models

The rejection/acceptance procedure in

$$u>{\frac{p(\mathbf{W}^{\prime}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})}{M P(\mathbf{W}^{\prime})}}={\mathrm{acceptance~prob}}$$

is not a complex as it seems.

Since

$$p(\mathbf{W}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})={\frac{\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W})P(\mathbf{W})}{p(\{\mathbf{y}_{i}\}_{i=1}^{N}|\{\mathbf{x}_{i}\}_{i=1}^{N})}},$$

we can simplify

$$\mathrm{acceptance\,prob}={\frac{p(\mathbf{W}^{\prime}|\{(\mathbf{x}_{i},\mathbf{y}_{i})\}_{i=1}^{N})}{M P(\mathbf{W}^{\prime})}}$$

as

acceptance prob = $\dfrac{\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}^{\prime})P(\mathbf{W}^{\prime})}{M^{\prime}P(\mathbf{W}^{\prime})}=\dfrac{\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}^{\prime})}{M^{\prime}}=\dfrac{\mathcal{L}(\mathbf{W}^{\prime},\mathcal{D})}{M^{\prime}}$ ,

where

- and M′ ≥ Mp({yi} N i=1 |{xi} N i=1)
- is the likelihood of the proposed model under our training dataset . L(W, D) W′ D

### **Defining** M′

First, we can easily find since, fundamentally, is just making sure , hence M′ M′ acceptance prob ∈ (0, 1]

$$M^{\prime}=\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}^{*}),$$

where

$$\mathbf{W}^{\star}={\underset{\mathbf{W}}{\operatorname{argmax}}}\prod_{i=1}^{N}p(\mathbf{y}_{i}|\mathbf{x}_{i};\mathbf{W}).$$

# **The above rejection sampling procedure is impractical**

But if we *understand* the principles behind the above rejection sampling procedure, we will understand all current and future techniques for **Bayesian deep learning**.

As before:

- is the MLE solution W⋆
- is the prior probability P(W)

Note:

- Note that is a very good sample, since it is accepted with probability one. W⋆
	- Likely, for some small is also a model that will be accepted. (W⋆ + ϵ) ϵ
	- What if our proposal distribution knew that was a good proposal and tried to propose similar models? W⋆
		- Define the proposal now as a 1st order Markov chain: and let . q(Wt+1 |Wt) W0 = W⋆
		- Can we sample from by sampling from some well-designed Markov chain ? P(W) q(Wt+1|Wt)
			- But sampling from still causes too many rejections... can we improve it? P(W)
- **Can we think of 1st Markov chains that would give us better steady state proposals than ?** q(Wt+1|Wt) P(W)
	- This is probably a complex function that must consider the likelihood in the proposals L(W, D)

# **Markov Chain Monte Carlo**

Markov Chain Monte Carlo (**MCMC**) gives us a way to sample from a complex highdimensional distribution by sampling from intermediate, simpler (lower-dimensional) distributions, which generally gives us **dependent** samples . q(x) x1,…, xn

The idea behind MCMC is simple.

- Suppose the domain is finite, to simplify our exposition D
	- A more complex but similar proof works on continuous state spaces like . W
- Since we have a finite domain , and enumerate the elements of as . D D d1, d2,…, |D|
- We cannot sample directly from but suppose we knew how to construct a Markov Chain with transition matrix whose unique stationary distribution was . q(x) P q(x)

- That is, if we define
Pxt,xt+1 = q(xt+1 |xt)

and if

xt ∼ q(x),

then

$$x_{t+1}\sim q(\mathbf{x}|\mathbf{x}_{t})$$

is also sampled from . q(x)

- In the matrix , the -th row represents a conditional probability distribution . P i (q(dj |di)) |D| j=1
	- is denoted the stochastic matrix. P

To undestand why the above is true, let's describe the distribution as a column vector . q(x) q = (q(d1), q(d2),…)

For some arbitrary starting distribution , consider the recursion q (0)

$$\mathbf{q}^{(t+1)}=\mathbf{q}^{(t)}\mathbf{P}.$$

Note that

$$\operatorname*{lim}_{t\to\infty}\mathbf{q}^{(t)}=\mathbf{q}^{(0)}\mathbf{P}\mathbf{P}\cdots=\mathbf{q}^{(0)}\mathbf{P}^{\infty}.$$

- If there is a nonzero probability of transitioning from any state to any other state for some power : x x ′ t
	- Then the Perron-Frobenius theorem (Perron, 1907; Frobenius, 1908) guarantees that the largest eigenvalue is real and equal to 1.
		- Because the matrix is stochastic, all other eigenvalues must be in the range . (1, −1]
	- Note that the above condition is trivially guaranteed if for any . q(x ′ |x) > 0 x, x ′ ∈ D

If we add the condition that the Markov chain is aperiodic, all other eigenvalues are in . From the spectral decomposition of , where are the eigenvalues of , we see that (1, −1) P = Vdiag(λ)V −1 λ P

$$\mathbf{P}^{t}=\left(\mathbf{V}\mathrm{diag}(\boldsymbol{\lambda})\mathbf{V}^{-1}\right)^{t}=\mathbf{V}\mathrm{diag}(\boldsymbol{\lambda}^{t})\mathbf{V}^{-1}.$$

Thus, the process thus converges to an unique **stationary distribution** sometimes also called the equilibrium distribution. And this unique stationary distribution , has the following property: q

q = qP.

**Algorithm 1**: The convergence property of Markov chains gives the following algorithm to sample from : q(x)

- 1. 2. sample from any initial distribution 3. sample 4. and GOTO 3: 5. output t ← 0 x0 ∼ q (0)(x) q (0) xt+1 ∼ q(x|xt) t ← t + 1 x∞
Then, . x∞ ∼ q(x)

# **Metropolis-Hastings Sampling**

Metropolis-Hastings sampling will merge rejection sampling with the Markov chain sampling of **Algorithm 1** and get rid of the problematic constant . M

Consider the Markov chain sampling **Algorithm 1** again,

## **Algorithm 1 (revisiting)**:

- 1. 2. sample from any initial distribution 3. sample 4. and GOTO 3: t ← 0 x0 ∼ q (0)(x) q (0) xt+1 ∼ q(x|xt) t ← t + 1
- 5. output x∞ ∼ q(x)

Suppose is also intractable. In Metropolis-Hastings we will use rejection sampling to sample from the 1st order Markov chain . q(x|xt) q(x|xt)

## **Rejection sampling (Refresh)**

Acceptance-rejection sampling algorithm (for ): M ≥ supx p(x) q(x)

- 1. sample from the proposal distribution x ∼ q(x) q(x)
- 2. sample independently of u ∼ Uniform(0, 1) X
- 3. while , reject and GOTO 1: u > p(x) Mq(x) x
- 4. Accept (output) as a sample from . x p(x)

Rejection sampling is very difficulty in high-dimensional domains (e.g., images) because of the large value of . M

### **Building the Markov chain also via rejection sampling** q(x|xt)

- The Metropolis Hastings algorithm starts with a target objective density

$$\mathrm{target~density}:=p(\mathbf{x}).$$

- The proposal distribution is a conditional density that has full support over (i.e., can generate all samples that can generate). xt+1 ∼ q(x|xt) p(x) p
- The general requirement for is that the ratio q

$$\frac{p(\mathbf{x}^{\prime})}{q(\mathbf{x}^{\prime}|\mathbf{x})}$$

is known for any and up to a *constant* that is *independent* of . x ′ x x

The Metropolis-Hastings algorithm is a type of acceptance-rejection sampling algorithm:

- 1. , . t ← 0 x0 ∼ q (0)
- 2. sample from the proposal distribution x ∼ q(x|xt) q(x|xt)
- 3. sample independently of u ∼ Uniform(0, 1) x
- 4. **If**

$$u>\frac{p({\bf x})q({\bf x}_{t}|{\bf x})}{p({\bf x}_{t})q({\bf x}|{\bf x}_{t})}\ ;$$

Reject and make . x xt+1 ← xt

- 5. **Otherwise:** Accept and make . x xt+1 ← x
- 6. t ← t + 1
- 7. GOTO 2:
- 8. Accept (output) as a sample from . x∞ p(x)

## **Practical Issues**

- Metropolis-Hastings is an easy way to construct a posterior sampler.
- The trick is finding a proposal Markov chain distribution that keeps the rejection probability low.
	- Note that Gibbs sampling is generally more efficient than the Metropolis-Hastings algorithm as the Gibbs sampling "proposal" is always accepted.

# **Metropolis-Hastings for Bayesian Deep Learning**

Consider a supervised learning task with data . Consider a deep neural network with paramters with likelihood function D = {(xi, yi)} N i=1 W

$$\mathrm{likelihood}=p({\mathcal{D}}|\mathbf{W}).$$

If we want a Bayesian view of deep learning, we will sample model paramters according to

$$p(\mathbf{W}|{\mathcal{D}})={\frac{p({\mathcal{D}}|\mathbf{W})p(\mathbf{W})}{\int p({\mathcal{D}}|\mathbf{W})p(\mathbf{W})d\mathbf{W}}}={\frac{p({\mathcal{D}}|\mathbf{W})p(\mathbf{W})}{p({\mathcal{D}})}}.$$

The parameter prior is a standard Normal: . The challenge is sampling . p(W) Normal(0, I) W

Approach 1: Rejection sampling (for a constant ). M

- 1. Sample W0 ∼ p(W)
- 2. sample independently of . u ∼ Uniform(0, 1) W0
- 3. while , reject and GOTO 1: u > p(W|D) Mp(W) W0
- 4. Accept (output) as a sample from . W0 p(W|D)

Note that

$${\frac{p(\mathbf{W}|{\mathcal{D}})}{M p(\mathbf{W})}}={\frac{p({\mathcal{D}}|\mathbf{W})}{M p({\mathcal{D}})}}={\frac{p({\mathcal{D}}|\mathbf{W})}{M^{\prime}}},$$

where . Note that M′ = Mp(D)

$$M^{\prime}\geq\operatorname*{max}_{\mathbf{W}}p({\mathcal{D}}|\mathbf{W}).$$

 can be very large for large datasets , forcing us to reject most samples. This happens when the Normal prior is a poor proposal. M′ (N ≫ 1)

## **Using Metropolis-Hastings for better proposals**

The Metropolis-Hastings algorithm is a type of acceptance-rejection sampling algorithm:

1. 2. sample from the proposal distribution 3. sample independently of 4. **If** t ← 0 W′ ∼ q(W|Wt) q(W|Wt) u ∼ Uniform(0, 1) W0

$$u>\frac{p(\mathbf{W}^{\prime}|{\mathcal{D}})q(\mathbf{W}_{t}|\mathbf{W}^{\prime})}{p(\mathbf{W}_{t}|{\mathcal{D}})q(\mathbf{W}^{\prime}|\mathbf{W}_{t})}:$$

Reject and make . W′ Wt+1 ← Wt

- 5. **Otherwise:** Accept and make . W′ Wt+1 ← W′
- 6. t ← t + 1
- 7. GOTO 2:
- 8. Accept (output) as a sample from . W∞ p(W|D)

- Example of : If set is to set , where is a lowvariance zero mean Normal variable of the same dimension as . q(W|Wt) q(W|Wt) W′ = Wt + Σ Σ W
**Q1:** Given the above , , , how do we compute the ratio W′ = Wt + Σ Σ ∼ Normal(0, σI) σ > 0

$$\frac{q(\mathbf{W}_{t}|\mathbf{W}^{\prime})}{q(\mathbf{W}^{\prime}|\mathbf{W}_{t})}\,?$$

**A1:** The ratio is **one**, as is symmetric around the x-axis and and . Normal(0, σI) q(W′ |Wt) = p(Σ) q(Wt|W′ ) = p(−Σ)

- The challenge of Metropolis-Hastings is still a high rejection rate (in general better than rejection sampling, but not good enough yet).
# **Hamiltonian Monte Carlo**

There are three desirable properties we want to have:

- 1. so we don't have to compute this ratio; and q(Wt |W′ ) = q(W′ |Wt)
- 2. We should use the gradient to make better proposals. p(D|W) ∣ ∣Wt ∂ ∂W
- 3. We want to alleviate the Brownian motion-type behavior (e.g., randomly samping Normals) to reduce correlation between samples.

## **Metropolis-adjusted Langevin algorithm (MALA)**

- We will first use gradients to make a new proposal distribution:

$$\mathbf{W}^{\prime}\sim q(\mathbf{W}|\mathbf{W}_{t})=\mathrm{Normal}\!\left(\mathbf{W}_{t}-\frac{\sigma^{2}}{2}\frac{\partial}{\partial\mathbf{W}}U(\mathbf{W})\big|_{\mathbf{W}_{t}},\sigma^{2}\mathbf{I}\right)\!,$$

for , where σ > 0

$$U(\mathbf{W})=-\log\left(p({\mathcal{D}}|\mathbf{W})p(\mathbf{W})\right),$$

with where is the number parameters in (i.e., is the dimension of . p(W) = exp(− ∥W∥ 2 2 )/(2π) d/2 , 1 2 d W d vec(W)

The above proposal is equivalent to

$${\bf W}^{\prime}={\bf W}_{t}-\left.\frac{\sigma^{2}}{2}\,\frac{\partial}{\partial{\bf W}}U({\bf W})\right|_{{\bf W}_{t}}+\left.\sigma\Sigma,$$

where . Σ ∼ Normal(0, I)

- We then accept the proposal with the usual Metropolis-Hastings acceptance procedure.
- Note that as , the proposals become symmetric: σ → 0

$$\frac{q(\mathbf{W}_{t}|\mathbf{W}^{\prime})}{q(\mathbf{W}^{\prime}|\mathbf{W}_{t})}=1$$

and we will accept all proposals since . W′ ≈ Wt

- This procedure is equivalent to a Lavengin diffusion, a set of stochastic differential equations with as solution p(W|D)
## **Hamiltonian Monte Carlo (HMC)**

- Hamiltonian Monte Carlo extends MALA to allow multiple steps in the proposal.
- Our goal is to make proposals that will **always** be accepted. Wt+1 ∼ q(W|Wt+1)
- Let's call the *potential* energy of position . U(W) W
- Let's introduce an auxiliary variable of the same dimentionality of where ϕ W

$$\phi\sim\mathrm{Normal}({\bf0},R),$$

where is a covariance matrix and a hyperparameter of the algorithm. R

- Then, define

$$K(\phi)=-\log(p(\phi))=\frac{1}{2}\phi^{T}R^{-1}\phi+\frac{1}{2}\log(2\pi^{d}|R|),$$

where is the dimension of . d vec(W)

Call the momentum and the kinetic energy. where ϕ K(ϕ)

- The total **energy** of the system (Hamiltonian)

$$H(\mathbf{W},\phi)=U(\mathbf{W})+K(\phi).$$

- This implies the following statistical symmetry (invariance):

$$p(\mathbf{W},\phi|{\mathcal{D}})=p(\mathbf{W}|{\mathcal{D}})p(\phi|{\mathcal{D}})=p(\mathbf{W}|{\mathcal{D}})p(\phi)={\frac{1}{C}}\exp(-U(\mathbf{W}))\exp(-K(\phi))={\frac{1}{C}}\phi^{\prime},$$

where is a normalizing constant. C = P(D)

- Consider the following:
	- Marginally sample

$$\phi_{t}\sim\mathrm{Normal}({\bf0},R).$$

- Marginally sample

$$\mathbf{W}_{t}\sim p(\mathbf{W}|{\mathcal{D}}).$$

- The is the joint of some Hamiltonian p(Wt , ϕt |D)

$$H(\mathbf{W}_{t},\phi_{t})=U(\mathbf{W}_{t})+K(\phi_{t}).$$

- Any other values of and with the same Hamiltonian will have the same joint probability W′ ϕ ′ H(Wt , ϕt) = H(W′ , ϕ ′) p(Wt, ϕt|D) = p(W′ , ϕ ′ |D)
- Hence, if we treat and as proposals for a "rejection sampling" algorithm: But since that there is **nothing to reject in our joint proposal** and since W′ ϕ ′ p(W′ , ϕ ′ |D) = p(Wt , ϕt |D) W′ ϕ ′ = 1. p(W′ ,ϕ ′ |D) p(Wt,ϕt|D)
- Note that has as its marginal. p(W′ , ϕ ′ |D) p(W′ |D)
	- Hence, by sampling from and throwing away , we are sampling from the posterior . p(W′ , ϕ ′ |D) ϕ ′ p(W|D)
- Here, we will use the deterministic Hamiltonian dynamics above to make a deterministic update to both and . ϕ W

Noether's theorem states that for any physical law with a conserved quantity (e.g., energy conservation), there must be symmetry, in this case the proposals

$$\frac{q(\mathbf{W}_{t},\phi_{t}|\mathbf{W}^{\prime},\phi^{\prime})}{q(\mathbf{W}^{\prime},\phi^{\prime}|\mathbf{W}_{t},\phi_{t})}=1$$

are symmetic. And this observation is at the heart of Radford Neil's ingenuous Hamiltonian Monte Carlo method.

**Hamiltonian Monte Carlo (HMC)** Algorithm:

- 1. t ← 0
- 2. Sample . ϕt ∼ Normal(0, R)
- 3. Simulate Hamiltonian dynamics to get proposal from . (W′ , ϕ ′) (Wt, ϕt)
- 4. . (assumes acceptance probability is one) Wt+1 ← W′
- 5. . t ← t + 1
- 6. GOTO 2:

### **Simulating the Hamiltonian Dynamics:**

Dicretization of Hamiltonian dynamics into discrete steps introduces errors. The resulting Markov chain is not longer symmetric (reversible) if simulated naively.

**Solution:** Leapfrog dynamics. Repeat steps, where is a discretization of the dynamics and is an abitrary constant. T/ϵ ϵ > 0 T > 0

For in increments: τ = 0 to T ϵ

$${\bf W}_{t+\tau/T+\epsilon/2}={\bf W}_{t+\tau/T}+(R^{-1}\phi_{t+\tau/T})\frac{\epsilon}{2}\tag{1}$$

$$\phi_{\tau+\epsilon}=\phi_{t+\tau/T}+\left(\frac{\partial}{\partial W}U({\bf W})\Big|_{{\bf W}_{t+\tau/T+\epsilon/2}}\right)\epsilon\tag{2}$$

$${\bf W}_{t+\tau/T+\epsilon}={\bf W}_{t+\tau/T+\epsilon/2}+(R^{-1}\phi_{t+\tau/T+\epsilon})\frac{\epsilon}{2}\tag{3}$$

You can verify that the above Markov chain is reversible, that is,

$p(\mathbf{W}_{t+1},\phi_{t+1}|\mathcal{D})p(\mathbf{W}_{t},\phi_{t}|\mathbf{W}_{t+1},\phi_{t+1},\mathcal{D})=p(\mathbf{W}_{t},\phi_{t}|\mathcal{D})p(\mathbf{W}_{t+1},\phi_{t+1}|\mathbf{W}_{t},\phi_{t},\mathcal{D})$ .  
  

However, the acceptance probability is no longer one, and we need to perform a true Metropolis-Hastings acceptance step.

**Final HMC Algorithm**. HMC Algorithm with imperfect Hamiltonian Simulation:

- 1. 2. Sample . 3. Simulate Hamiltonian dynamics to get proposal . 4. sample independently of 5. **if** Reject and make . 6. **else:** accept and let . 7. 8. GOTO 2: t ← 0 ϕt ∼ Normal(0, R) (W′ , ϕ ′) u ∼ Uniform(0, 1) X u > exp(H(W′ , ϕ ′) − H(Wt, ϕt)) : (W′ , ϕ ′) Wt+1 ← Wt Wt+1 ← W′ t ← t + 1
# **Stochastic Gradient MCMC (Welling & Teh, 2011)**

Recall the negative log-likelihood for parameters with a prior , , is: p(W) W ∈ R d

$$\frac{\partial}{\partial W}{\mathcal{L}}({\mathcal{D}}^{\mathrm{train}};W)=-\frac{1}{N}\sum_{i=1}^{N}\frac{\partial}{\partial W}\mathrm{log}\,p(y_{i}|x_{i};W)-\frac{1}{N}\frac{\partial}{\partial W}\mathrm{log}\,p(W),$$

where if is a multivariate standard normal, then . W log p(W) ∝ ∥W∥ 2 2 ∂ ∂W

For a learning rate , the update equations are: η

$$m^{(t)}=(1-\eta\gamma)m^{(t-1)}-\eta n\frac{\partial}{\partial W}{\mathcal{L}}({\mathcal{D}}^{\mathrm{train}};W)+\sqrt{2\gamma\eta}T M^{1/2}R^{(t)},$$

where

$$W^{(t)}=W^{(t-1)}+\eta M^{-1}m^{(t)},$$

where

- is the learning rate η
- is a sample from a standard normal vector. R(t) ∼ Nd(0, Id)
- is a friction parameter γ
- is a temperature parameter T
	- scales the effect of the noise. T
	- turns SG-MCMC into SGD T → 0
	- makes SG-MCMC ignore the likelihood T → ∞
- The mass matrix is a preconditioner, and if we use no preconditioner then M = I, such that all M-related terms vanish from the equations. M
- There should be an accept/reject Metropolis-Hastings corrections in SG-MCMC.
	- However, if , one can show that the acceptance probability tends to one. η → 0

### **SG-MCMC in Literature**

Best results achieved with cold posteriors : T < 1

- (Li et al., 2016) . T = 1/√N
- (Leimkuhler et al., 2019) . T < 10 −3
- (Heek & Kalchbrenner, 2020) . T = 1/5
- (Zhang et al., 2020) . T = 1/√50000
- Zhang et al. (2020) proposes to use to perform cycles of iterations with a high-to-low step size schedule. t = 1, 2,…
	- Another way to understand the idea is to consider the start of the cycle as having high temperatures ( large) and end the cycle having low temperatures ( small). T T
	- Still, sampling largely uses cold posteriors . T < 1
- (Wenzel et al., 2020) does a deep-drive into the necessity of cold posteriors for Bayesian deep learning.

# **References**

- (Neal, 2011) Neal, Radford M. "MCMC using Hamiltonian dynamics." Handbook of Markov Chain Monte Carlo 2, no. 11 (2011): 2.
- (Hinton, 2006) G. Hinton, To Recognize Shapes, First Learn to Generate Images, Tech Report 2006<http://www.cs.toronto.edu/~fritz/absps/montrealTR.pdf>
- Wenzel, Florian, Kevin Roth, Bastiaan S. Veeling, Jakub Świątkowski, Linh Tran, Stephan Mandt, Jasper Snoek, Tim Salimans, Rodolphe Jenatton, and Sebastian Nowozin. "How good is the bayes posterior in deep neural networks really?." ICML 2020.
- Li, C., Chen, C., Carlson, D., and Carin, L. Preconditioned stochastic gradient Langevin dynamics for deep neural networks. In Thirtieth AAAI Conference on Artificial Intelligence, 2016.
- Heek, J. and Kalchbrenner, N. Bayesian inference for large scale image classification. In International Conference on Learning Representations (ICLR 2020), 2020
- Zhang, R., Li, C., Zhang, J., Chen, C., and Wilson, A. G. Cyclical stochastic gradient MCMC for Bayesian deep learning. In International Conference on Learning Representations (ICLR 2020), 2020
- Leimkuhler, B., Matthews, C., and Vlaar, T. Partitioned integrators for thermodynamic parameterization of neural networks. arXiv preprint arXiv:1908.11843, 2019.
- Florian Wenzel, Kevin Roth, Bastiaan S. Veeling, Jakub Świątkowski, Linh Tran, Stephan Mandt, Jasper Snoek, Tim Salimans, Rodolphe Jenatton, Sebastian Nowozin, How Good is the Bayes Posterior in Deep Neural Networks Really?, ICML 2020, <https://arxiv.org/abs/2002.02405>

In [ ]: