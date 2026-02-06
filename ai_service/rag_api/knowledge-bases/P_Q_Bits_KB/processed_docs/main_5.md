Now, you see, if at time $t$ we have ${P}+{A}$, then what will happen at
time $t+1$? Well, it will get multiplied by $W$, and ${W}{P}$ will give
me ${P}$, but ${W}{A}$ will give me $\lambda {A}$. Why? Because ${A}$ is
also an eigenvector of ${W}$, but with an eigenvalue $\lambda$.

And so, every time I propagate one time step the ${P}$ stays ${P}$, but
the ${A}$, that part keeps picking up a factor of $\lambda$. So after
$n$ time steps, we have ${P}+\lambda^n{A}$. And the point is, I'd
mentioned before that this eigenvalue of 1 is actually the one with the
largest magnitude. Every other one, all other $\lambda$'s, they may be
complex, but the point is their magnitude will be less than 1. That's
one of the properties of this stochastic matrix. So because it's less
than 1, when you raise it to the power $n$, it gradually disappears. If
you take 0.1 and raise the power 100, it becomes a very small number.
And so eventually only the ${P}$ remains, everything else disappears.

#### Fig. [3.7](#fig:fig3_1_10){reference-type="ref" reference="fig:fig3_1_10"} {#fig.-figfig3_1_10}

![Stationary Distribution.](./Week3_1/figure10.jpg){#fig:fig3_1_10
width="90%"}

So how many time steps does it take for these other components to
disappear? Well, you can estimate it this way, take $|\lambda|^n$, and
write it in this form $|\lambda|^n=\exp{(n\ln{|\lambda|})}$.

You can always write $\lambda$ as $\exp{(\ln{|\lambda|})}$, that's an
identity. (see Fig. [3.7](#fig:fig3_1_10){reference-type="ref"
reference="fig:fig3_1_10"}) So, you could take this quantity and write
it this way $|\lambda|^n=\exp{(n\ln{|\lambda|})}$. What that means is,
that if the number of time steps $n$ is equal to $-1/(\ln{|\lambda|})$,
then you see this $|\lambda|^n$ would be $\exp{(-1)}$, which means after
$-1/(\ln{|\lambda|})$ time steps. this component will have decayed to
$1/e$ of its original value.

So how much is that? Well, if $\lambda$ we'll say a little less than 1,
write it as $1-\varepsilon$, then you can show that this number will be
$1/\varepsilon$. This is an approximate result, but it works well if
$\varepsilon$ is small. So what that means is if say, this eigenvalue
happened to be 0.99, that means, $\varepsilon$ is 0.01. Then it would
take like hundred time steps before this component becomes $1/e$ of its
original value.

#### Fig. [3.8](#fig:fig3_1_11){reference-type="ref" reference="fig:fig3_1_11"} {#fig.-figfig3_1_11}

![Markov Chain Monte Carlo.](./Week3_1/Picture11.png){#fig:fig3_1_11
width="90%"}

So, bottom line is, we have this $[W]$ matrix, the transition matrix,
you can use it to generate a chain of time samples. And they will tend
to this distribution ${P}$, the stationary distribution ${P}$. And what
distribution is it? Well, it's given by the eigenvector of $[W]$ with
this eigenvalue 1. (see Fig. [3.8](#fig:fig3_1_11){reference-type="ref"
reference="fig:fig3_1_11"})

#### Fig. [3.9](#fig:fig3_1_12){reference-type="ref" reference="fig:fig3_1_12"} {#fig.-figfig3_1_12}

Now, what we want is a method of time sampling where the samples obey
the Boltzmann law, $p_i=(1/Z)\exp{(-\widetilde{E}_i)}$ which is our
target distribution.

How can you make the Boltzmann distribution $p$ the stationary
distribution for $W$. By making $[W]\{p\}=\{p\}$. One way to do this is
to impose detailed balance.Which means that we require $W_{ji}p_i$ to be
equal to $W_{ij}p_j$. If this is true then I can show that
$[W]\{p\}=\{p\}$. The algebra is shown in Fig.
[3.9](#fig:fig3_1_12){reference-type="ref" reference="fig:fig3_1_12"}.

![How to make the Boltzmann distribution $p$ the stationary distribution
for W?](./Week3_1/figure12.jpg){#fig:fig3_1_12 width="90%"}

### Fig. [3.10](#fig:fig3_1_14){reference-type="ref" reference="fig:fig3_1_14"}: Metropolis algorithm {#fig.-figfig3_1_14-metropolis-algorithm}

There's a very well known algorithm that is widely used in statistical
physics. It's called the Metropolis algorithm. Consider any two states,
$i$ and $j$ and let's say $i$ has a bigger energy than $j$.

Say I am currently sitting at $i$ and I am trying to figure out the
probability of going to $j$. I choose the probability as 1 for going
down in energy, which means for $i$ to $j$, $W_{j\leftarrow i}$. If $j$
has a lower energy than $i$ take it for sure. But for the reverse
process, $W_{i\leftarrow j}$, I choose the probability as proportional
to $p_j/p_i = \exp{(-(\widetilde{E}_i-\widetilde{E}_j))}$.

This will ensure that I meet the condition of detailed balance. It
should lead us to a stationary distribution that follows Boltzmann law,
but it is not the only way. Any other choice that satisfies detailed
balance should work too, though one choice might reach the stationary
distribution faster than another. In the next lecture we will look at
another popular choice, one that we have been using, often referred to
as Gibbs sampling.

![Metropolis algorithm](./Week3_1/figure14.jpg){#fig:fig3_1_14
width="95%"}

### Quiz

#### Question 1

For any transition matrix $[W]$, what is (a) the sum of each column, (b)
the largest eigenvalue?[^40]

#### Question 2

A single spin has a transition matrix given by
$W = \left [ \begin{array}{r r}
0.2 & \ 0.4  \\
0.8 & \ 0.6  \\
\end{array} \right ]$

What is the stationary probability distribution?[^41]

## Gibbs' Sampling

This is [Lecture 3.2: Watch youtube
video](https://www.youtube.com/watch?v=VAuRc5hkYlo)

In the last lecture, we introduced the concept of a transition matrix
whose eigenvector with eigenvalue 1 gives us the stationary probability
distribution. We then showed that a transition matrix that obeys
detailed balance $W_{i\leftarrow j}/W_{j\leftarrow i}$ =
$\exp{(-(\widetilde{E}_i-\widetilde{E}_j))}$, will lead to a stationary
distribution that follows the Boltzmann law:
$p_i=(1/Z)\exp{(-\widetilde{E}_i)}$.

Now, what we'll be talking about in this lecture is what's called Gibbs'
sampling. Basically it is the sampling algorithm that we have been using
the one that I introduced in the very first lecture of in chapter 2. In
this lecture and the next, we'll see how to write down the transition
matrix for this kind of sampling, and why some approaches work and some
don't work.

### Figs. [3.11](#fig:fig3_2_4){reference-type="ref" reference="fig:fig3_2_4"}-[3.12](#fig:fig3_2_5){reference-type="ref" reference="fig:fig3_2_5"}: How it works {#figs.-figfig3_2_4-figfig3_2_5-how-it-works}

#### Fig. [3.11](#fig:fig3_2_4){reference-type="ref" reference="fig:fig3_2_4"}: {#fig.-figfig3_2_4}

Now, so how does this Gibbs sampling work? Well, the idea is that you go
to one of your $p$-$bits$, say the $r$-th, and either set it equal to
$0$ or equal to $1$, according to a certain algorithm. When you are
updating the $r$-th $p$-$bit$ you don't mess with any other $p$-$bit$
say the $q$-th if there are terms in the energy function $\widetilde{E}$
that involve both $s_r$ and $s_q$. So when you're working on the $r$-th
$p$-$bit$, you just have two choices, you can either set it to 0 or to 1
but you're not supposed to mess with the other ones. The other
$p$-$bits$ remain wherever they are, whatever configuration $\alpha$
they may be in.

So our choice is between $\alpha0$, meaning, rest of the $p$-$bits$ in
$\alpha$ and the $r$-th one in 0, or rest in $\alpha$ and the $r$-th one
in 1. And when we try to write down the $[W]$ matrix, that's the
transition matrix, we are basically trying to write down this 2 by 2
section.

![Gibbs Sampling.](./Week3_2/figure4.jpg){#fig:fig3_2_4
width="\\textwidth"}

Note of course, that the matrix itself is much bigger. You see, even
with 6 $p$-$bits$, the matrix would be $2^6$ by $2^6$, which would be
$64\times64$ and in general could be even bigger, depending on the
number of $p$-$bits$, it grows exponentially. But for this method of
sampling, when you're dealing with the $r$-th neuron, the only nonzero
elements are in this 2 by 2 block, labeled with $\alpha0$ and $\alpha1$.

And what are the elements of this block? Well, the procedure is you
first find this quantity that we call $\widetilde{x}_r$, which you
obtain from the difference in the energies between the two
possibilities, 1 and 0,
$\widetilde{x}_r=\widetilde{E}_{\alpha1}-\widetilde{E}_{\alpha0}$, and
that is what, as we discussed, you could write also as the derivative of
the energy function, $\partial\widetilde{E}/\partial s_r$, and that's
because $s$ is a binary variable.

I should also mention that in general, you often calculate this
$\widetilde{x}_r$ using the synapse equation,
${\widetilde{x}}={x}+[w]{s}$ and what we are doing here is kind of
equivalent. In fact, this is more general, because it would work, even
if energy functions had higher order terms beyond quadratic, as we have
discussed earlier.

Now, what do you do once you have the $\widetilde{x}_r$? Well, you find
the Fermi function of $\widetilde{x}_r$, which is the mirror image of
the sigmoidal function,
$f_r=1/(1+\exp{\widetilde{x}_r})=\sigma(-\widetilde{x}_r)$. The sigmoid
function is something you see a lot in the neural network literature and
the Fermi function is what you'd normally see in, I guess, solid state
devices and solid state physics courses.

Okay, now once you have this Fermi function, the rule is that
probability that this $p$-$bit$ will be set to 1 is equal to the Fermi
function. Note that this probability is independent of what the
$p$-$bit$ currently is, that doesn't matter. You just calculate
$\widetilde{x}_r$ or find $f_r$, and then depending on $f_r$, you set it
to 1 or 0.

So remember when we write the $[W]$ matrix, the columns correspond to
the current state, the state at time $t$, whereas the rows tell you the
state at time $t + 1$. And so since the state at time $t + 1$ really
doesn't depend on the state at time $t$, we put $f_r$ on both columns
here. Similarly, if you want to write the probability of putting a 0 on
that neuron, well that's $1- f_r$, and again, it's the same for both
columns.

Finally, one property of transition matrices I'd mentioned is that every
column must add up to 1, and it does (see Fig.
[3.11](#fig:fig3_2_4){reference-type="ref" reference="fig:fig3_2_4"}).
That's trivially clear, but you might wonder that well, you told me
$[W]$ was a huge matrix, and you're just writing this little $2\times2$
block, but it's that huge matrix where the columns should add up to 1.
That's true, but the way we're doing it here, all other elements of that
matrix are actually 0, because in a particular step, the only element
that can change is the $r$-th $p$-$bit$. Okay, and so if these add up to
1, it means the columns of the entire big matrix also would add up to 1.

#### Fig. [3.12](#fig:fig3_2_5){reference-type="ref" reference="fig:fig3_2_5"} {#fig.-figfig3_2_5}

![Gibbs Sampling.](./Week3_2/figure5.jpg){#fig:fig3_2_5
width="\\textwidth"}

Another question you could ask is about detailed balance,
$W_{i\leftarrow j}/W_{j\leftarrow i}=p_i/p_j=\exp{-(\widetilde{E}_i-\widetilde{E}_j)}$,
because if you remember, in the last lecture, we said that one way to
ensure that the $[W]$ matrix will give a stationary distribution that
matches the Boltzmann distribution is to ensure this detailed balance.

The question is what we wrote down here, does that satisfy this
condition? Well, we can check. With a little algebra you can show that
$(1-f_r)/f_r = e^{\widetilde{x}_r}$ and use it to show that we are
satisfying detailed balance.

### Figs. [3.13](#fig:fig3_2_6){reference-type="ref" reference="fig:fig3_2_6"}-[3.20](#fig:fig3_2_14){reference-type="ref" reference="fig:fig3_2_14"}: Toy example with n=2 {#figs.-figfig3_2_6-figfig3_2_14-toy-example-with-n2}

#### Fig. [3.13](#fig:fig3_2_6){reference-type="ref" reference="fig:fig3_2_6"}: {#fig.-figfig3_2_6}

Now let's look at a toy example with just two $p$-$bits$. How do we
write down the $[W]$ matrices?.We start, of course, with the energy
expression, which in matrix form would be written like this,
$\widetilde{E}=s^{\rm T}x+(1/2)s^{\rm T}ws$, but with just two
$p$-$bits$, you could actually spell it out, and it wouldn't be too
inconvenient. The matrix version is particularly useful when you have
lots of $p$-$bits$, because it's hard to write out all the terms. But
here you could easily write this out, the first term will give you
$s_1x_1+s_2x_2$ and the interaction term will give you this
$w_{12}s_1s_2$. Note, of course, these are Boltzmann networks for which
the $w$ matrix is symmetric, that is, $w_{12}$ is equal to $w_{21}$.

By the way, I should mention that the small $w$, which is the weight
matrix, is very different from this big $[W]$, which is the transition
matrix. The small $w$ is $n$ by $n$, the big $[W]$ is $2^n$ by $2^n$, a
different matrix. Even when $w$ is symmetric $W$ need not be.

![\[$W$\] with $n=2$.](./Week3_2/figure6.jpg){#fig:fig3_2_6
width="\\textwidth"}

Anyway, from the expression $\widetilde{E}=s_1x_1+s_2x_2+w_{12}s_1s_2$,
we can write out the energies of all the configurations. How many
configurations? Well 2 $p$-$bits$, so there are $2^2=4$configurations:
$\{00\}$, $\{01\}$, $\{10\}$ and $\{11\}$ where $\{00\}$ means
$s_1 = 0$, $s_2 = 0$ etc.

#### Fig. [3.14](#fig:fig3_2_7){reference-type="ref" reference="fig:fig3_2_7"}: Transition matrix for updating $p$-$bit$ 1 {#fig.-figfig3_2_7-transition-matrix-for-updating-p-bit-1}

![Non-zero elements in
\[$W^{(1)}$\].](./Week3_2/Picture7.png){#fig:fig3_2_7
width="\\textwidth"}

Let us write down the $[W]$ matrix for updating $p$-$bit$ 1, and I've
put a superscript, $W^{(1)}$ to indicate that. The point to note is that
the second $p$-$bit$ is fixed. So from $\{00\}$, you can go to $\{10\}$,
but you cannot go to $\{01\}$ or to $\{11\}$, because you are not
allowed to change the second one. So when you write this $W^{(1)}$
matrix, you have these red question marks and these blue question marks,
those would be the nonzero elements, rest will be zeros. Because the
rest will require changing both $p$-$bits$ and that's not allowed. In
this sampling scheme, you update one $p$-$bit$ at a time.

#### Figs. [3.15](#fig:fig3_2_8){reference-type="ref" reference="fig:fig3_2_8"}-[3.16](#fig:fig3_2_10){reference-type="ref" reference="fig:fig3_2_10"} {#figs.-figfig3_2_8-figfig3_2_10}

![\[$W^{(1)}$\].](./Week3_2/figure8.jpg){#fig:fig3_2_8 width="90%"}

![\[$W^{(1)}$\].](./Week3_2/figure10.jpg){#fig:fig3_2_10 width="90%"}

Okay, so let's just focus on the red ones, involving a transition
between $\{00\}$ and $\{10\}$. So the corresponding $\widetilde{x_1}$,
is $\widetilde{E}_{10}- \widetilde{E}_{00}$, and that's really $x_1$, as
you can see.

Incidentally, you could have got the same answer starting from the
synapse equation as well, ${\widetilde{x}}={x}+[w]{s}$ setting
$s_2 = 0$. Remember that this synapse equation is equivalent if the
energy expression has only a linear and a quadratic term as in this
case.

Now the probability of updating $p$-$bit$ 1 to one is given by the Fermi
function $f_1(\widetilde{x_1})$, and the probability of updating it to
zero is given by $1-f_1(\widetilde{x_1})$. And so we can fill up the red
question marks in Fig. [3.14](#fig:fig3_2_7){reference-type="ref"
reference="fig:fig3_2_7"} as shown in Fig.
[3.15](#fig:fig3_2_8){reference-type="ref" reference="fig:fig3_2_8"}.

Next you can go onto the blue question marks which involve a transition
between 01 and 11 and the difference is that now we have to look at the
energy difference between 11 and 01, so this
$\widetilde{x_1}=\widetilde{E}_{01}-\widetilde{E}_{11}$ which is
$x_1 + w_{12}$. The last time the energy difference was just $x_1$. So
we'll define a new Fermi function with a tilde,
$\widetilde{f}_1=1/(1+\exp{(x_1+w_{12})})$, and fill up the blue
question marks accordingly.

#### Figs. [3.17](#fig:fig3_2_11){reference-type="ref" reference="fig:fig3_2_11"}-[3.18](#fig:fig3_2_12){reference-type="ref" reference="fig:fig3_2_12"} {#figs.-figfig3_2_11-figfig3_2_12}

Is detailed balance satisfied? You can easily check it is, the way we
did it earlier (see Fig. [3.12](#fig:fig3_2_5){reference-type="ref"
reference="fig:fig3_2_5"}).

![Checking for detailed balance](./Week3_2/figure11.jpg){#fig:fig3_2_11
width="90%"}

![Checking for detailed balance](./Week3_2/figure12.jpg){#fig:fig3_2_12
width="90%"}

#### Fig. [3.19](#fig:fig3_2_13){reference-type="ref" reference="fig:fig3_2_13"}: Transition matrix for updating $p$-$bit$ 2 {#fig.-figfig3_2_13-transition-matrix-for-updating-p-bit-2}

Next we have to write down $W^{(2)}$, that is the W matrix for updating
$p$-$bit$ 2 keeping $p$-$bit$ 1 fixed. Remember that previously we
updated $p$-$bit$ 1 keeping $p$-$bit$ 2 fixed. Now you can see that we
have a different set of elements that are non-zero. These are the blocks
where the first $p$-$bit$ does not change, it's either 0 or 1 and stays
fixed.

And so you can go ahead and fill them up, again much the same
principles, but now the energy differences involved would be between
$\{01\}$ and $\{00\}$, and between $\{10\}$ and $\{11\}$. But it's the
same pattern with $f_2$ and $\widetilde{f}_2$ defined as shown.

![\[$W^{(2)}$\].](./Week3_2/figure13.jpg){#fig:fig3_2_13
width="\\textwidth"}

#### Fig. [3.20](#fig:fig3_2_14){reference-type="ref" reference="fig:fig3_2_14"} {#fig.-figfig3_2_14}

So collecting all the results, We have these two $[W]$ matrices, one for
updating 1, one for updating 2, and they depend on these various Fermi
functions that appear, each one corresponding to a different energy
difference.

Now, I'll stop here for this lecture. What we'll do is continue with
this in the next lecture with a specific numeral example and see what we
get for sequential updating the way we discussed. And then compare it
with what you get when you try to update 1 and 2 simultaneously.

![Collecting all results for \[$W^{(1)}$\] and
\[$W^{(2)}$\].](./Week3_2/figure14.jpg){#fig:fig3_2_14
width="\\textwidth"}

### Quiz

The transition matrix for updating one spin in a network of 2 spins is
$W = \left [ \begin{array}{r r r r}
1-f_1 & \ 0 & \ 1-f_1 & \ 0  \\
0 & \ 1-\widetilde{f_1} & \ 0 & \ 1-\widetilde{f_1}  \\
f_1 & \ 0 & \ f_1 & \ 0  \\
0 & \ \widetilde{f_1} & \ 0 & \ \widetilde{f_1} \\
\end{array} \right ]$

#### Question 1

What is $(1-f_1)/f_1$ in terms of the energy function $\widetilde{E}$?
[^42]

#### Question 2

What is $(1-\widetilde{f_1})/\widetilde{f_1}$ in terms of the energy
function $\widetilde{E}$? [^43]

## Sequential Versus Simultaneous updates

This is [Lecture 3.3: Watch youtube
video](https://www.youtube.com/watch?v=AwcOQJBTU-U)

### Figs. [3.21](#fig:fig3_3_2){reference-type="ref" reference="fig:fig3_3_2"}-[3.23](#fig:fig3_3_4){reference-type="ref" reference="fig:fig3_3_4"}: Sequential update {#figs.-figfig3_3_2-figfig3_3_4-sequential-update}

#### Figs. [3.21](#fig:fig3_3_2){reference-type="ref" reference="fig:fig3_3_2"}: Toy example {#figs.-figfig3_3_2-toy-example}

This lecture is kind of a continuation of the last one and what we'll
try to do is define a specific two $p$-$bit$ problem and compare what
you get when you update $p$-$bits$ sequentially and what happens when
you update them simultaneously, and show that the $W$ matrix gives you a
nice analytical way of seeing those results.

Now, recall the toy example that we used in the last lecture, two
$p$-$bits$ with energy given by
$\widetilde{E}=s^{\rm T}x+(1/2)s^{\rm T}ws$. The Figure shows the
probabilities of the four different configurations, $\{00\}$, $\{01\}$,
$\{10\}$, $\{11\}$, assuming the weight $w$ shown along with two choices
of the bias $x$.

![Numerical example](./Week3_3/figure2.jpg){#fig:fig3_3_2
width="\\textwidth"}

Now how can you understand the probabilities. Well, the easiest is by in
terms of the Boltzmann distribution because as you know, the probability
is exponential of $-E$. So what you need to find out is the energies of
these different configurations. With a bias $x= \{-1 \ -1\}^T$, if you
put in the numbers you will see that $11$ has the same energy, equal to
zero, as $00$ and so they have exactly the same probability. The ratio
of the probabilities of the first and second groups is $e^0/e^{-1}$
which is what the plot shows. All probabilities add up to one.

Now, if you change the bias on $p$-$bit \# 2$ to say $-0.5$, then the
energies come out a little different: $11$ now has a slightly higher
energy than $00$ and so it's probability goes down. $01$ and $10$ are
also not equal anymore, $01$ has a lower energy and hence a higher
probability. So that's the toy example we will use to compare the
Boltzmann result to what we get directly from two different sampling
approaches along with what we get from the eigenvectors of the
corresponding $W$ matrices that have an eigenvalue of 1.[^44]

#### Figs. [3.22](#fig:fig3_3_3){reference-type="ref" reference="fig:fig3_3_3"}: Transition matrix {#figs.-figfig3_3_3-transition-matrix}

![Recalling $W^{(1)}$ and $W^{(2)}$ from last
lecture](./Week3_3/figure3.jpg){#fig:fig3_3_3 width="\\textwidth"}

In the last lecture we spent some time writing the $W$ matrices,
$W^{(1)}$ and $W^{(2)}$, for updating $p$-$bit$ 1 with $p$-$bit$ 2 fixed
and for updating $p$-$bit$ 2 with $p$-$bit$ 2 fixed. As you can see, the
elements of these $W$ matrices involve different Fermi functions
corresponding to different energy differences.

#### Fig. [3.23](#fig:fig3_3_4){reference-type="ref" reference="fig:fig3_3_4"}: {#fig.-figfig3_3_4}

![$[W]=[W^{(1)}][W^{(2)}]$.](./Week3_3/figure4.jpg){#fig:fig3_3_4
width="90%"}

Now, how do you apply it to the problem to calculate the stationary
distribution? Well first you have to write the composite $W$ matrix,
which depends on whether you first update 1 and then 2, or the other
way. If you update $p$-$bit$ 1 first then you put the $W^{(1)}$ first.
First meaning to the right because that's the one that operates on your
distribution first, and then $W^{(2)}$. But if you update 2 first, then
$W^{(2)}$ is the one on the right and then $W^{(1)}$. The product
$W=W^{(2)}W^{(1)}$ or $W=W^{(1)}W^{(2)}$, then is the composite $W$
matrix,

You can then find the eigenvector of $W$ with eigenvalue equal to 1. And
if you do that, you will get results that will match the Boltzmann
result very nicely, along with the sampling results. So, I have now
added this third method, the $W$ matrix method. You see the first two
methods, Boltzmann and sampling, we had in Chapters 1 and 2. This $W$
matrix method is what we are adding now.

All three methods agree nicely for the two numerical examples we are
discussing.

### Fig. [3.24](#fig:fig3_3_5){reference-type="ref" reference="fig:fig3_3_5"}: Simultaneous update {#fig.-figfig3_3_5-simultaneous-update}

![simultaneous update](./Week3_3/figure5.jpg){#fig:fig3_3_5
width="\\textwidth"}

Now what I want to talk about is, what it would look like if instead of
updating them one by one, I am a little impatient and I say no, let's do
it quickly, update them both, why not? With a little thought, we can
write down the elements of the corresponding transition matrix $W^{(s)}$
as shown. Now, let us again compare the three methods, the Boltzmann
method, the sampling method and the $W$ matrix method. The sampling now
is not Gibbs sampling, but it's this simultaneous update method.

You'll notice the sampling and the $W$ matrix they match exactly. So the
yellow and the green, they are matched very nicely. So that tells you
that this $W$ matrix method actually describes this sampling procedure
very well. But you'll notice they don't match the Boltzmann answer which
is this blue peak. So when you do simultaneous update, whatever
stationary distribution you get by sampling will not look like the
Boltzmann distribution, which is generally what you want. That's why the
simultaneous updating is not used at all.

### Figs. [3.25](#fig:fig3_3_6){reference-type="ref" reference="fig:fig3_3_6"}-[3.26](#fig:fig3_3_7){reference-type="ref" reference="fig:fig3_3_7"}: Sequential versus simultaneous {#figs.-figfig3_3_6-figfig3_3_7-sequential-versus-simultaneous}

#### Fig. [3.25](#fig:fig3_3_6){reference-type="ref" reference="fig:fig3_3_6"}: {#fig.-figfig3_3_6}

![Sequential Update.](./Week3_3/figure6.jpg){#fig:fig3_3_6
width="\\textwidth"}

We saw earlier that sequential updating works very well irrespective of
the order, you could do $W^{(1)}$, $W^{(2)}$ or $W^{(2)}W^{(1)}$, in
either case it matches Boltzmann very nicely. But simultaneous updating
does not. So you might wonder, well, how do the $W$ matrices compare for
these two updating schemes? Why is it that one's working beautifully and
the other is not working? And you'll notice the differences are pretty
subtle.

You see if you actually took our $W^{(1)}$ and $W^{(2)}$ and multiplied
them out you'd get something looking a little different from $W^{(s)}$.
The basic structure is very similar, but it is just that the tildes are
in different places. These are subtle differences and yet they lead to a
major difference in the stationary distributions.

#### Fig. [3.26](#fig:fig3_3_7){reference-type="ref" reference="fig:fig3_3_7"} {#fig.-figfig3_3_7}

Now you might have noticed that the difference between the sequential
$W^{(1)}W^{(2)}$ and the simultaneous $W^{(s)}$ comes from the
difference between $f_1$ and $\widetilde{f}_1$ which comes from the
interaction term $w_{12}$. What would happen if the interaction was 0?

The answer is, if we set $w$, this interaction matrix, to 0, sure
enough, even the simultaneous update will match the Boltzmann nicely
because then you see this is kind of the trivial situation, where you
have a whole bunch of $p$-$bits$ that don't know about each other. In
that case, it really doesn't matter whether you updated them
sequentially or all simultaneously, they're all independent anyway.

![Simultaneous Update works for unconnected
$p$-$bits$](./Week3_3/figure7.jpg){#fig:fig3_3_7 width="\\textwidth"}

### Fig. [3.27](#fig:fig3_3_10){reference-type="ref" reference="fig:fig3_3_10"}: Restricted Boltzmann machine {#fig.-figfig3_3_10-restricted-boltzmann-machine}

Now, one can make use of this fact that unconnected $p$-$bits$ can be
updated simultaneously, to architect Boltzmann networks in a way that
allows updates to be performed much faster than one could otherwise. The
idea is to bunch all the $p$-$bits$ in two groups, the $A$ group and the
$B$ group. And there is no connection internally among the $A$ group and
no connection internally among the $B$ group, but there's lots of
connection between the two groups. So when I look at the weight matrix,
it has zero connections between $A$ and $A$ or $B$ and $B$. But, it has
all the connections going $B$ to $A$ and $A$ to $B$.

![Restricted Boltzmann machine
(RBM)](./Week3_3/Picture10.png){#fig:fig3_3_10 width="\\textwidth"}

What's the advantage? Well what this means is now I can update all
$p$-$bits$ in Group $A$ simultaneously because they have no connections
amongst them and so whether it's simultaneous or sequential doesn't
really matter. Similarly I can update all of Group $B$ simultaneously.

This is a big advantage because if you had 1 million $p$-$bits$ half in
Group $A$, half in Group $B$ it means you could update half a million at
a time. And then go on to the other half a million and back and forth.
This can speed up the update process enormously and so practical
Boltzmann machines often use this restricted architecture.

### Quiz

The transition matrix for updating one spin in a network of 2 spins is
$W = \left [ \begin{array}{r r r r}
1-f_1 & \ 0 & \ 1-f_1 & \ 0  \\
0 & \ 1-\widetilde{f_1} & \ 0 & \ 1-\widetilde{f_1}  \\
f_1 & \ 0 & \ f_1 & \ 0  \\
0 & \ \widetilde{f_1} & \ 0 & \ \widetilde{f_1} \\
\end{array} \right ]$

#### Question 1

How should we time sample a system of spins all connected to each other
(all $w_{ij} = w_{ji} \neq 0$), such that the samples follow the
Boltzmann distribution? [^45]

#### Question 2

For simultaneous updating of a system of 2 spins, the transition matrix
is given by W =\
$\left [ \begin{array}{r r r r}
(1-f_1)(1-f_2) & \ (1-\widetilde{f_1})(1-f_2) & \ (1-f_1)(1-\widetilde{f_2}) & \ (1-\widetilde{f_1})(1-\widetilde{f_2})  \\
(1-f_1)f_2 & \ (1-\widetilde{f_1})f_2 & \ (1-f_1)\widetilde{f_2} & \ (1-\widetilde{f_1})\widetilde{f_2}  \\
    f_1(1-f_2) & \ \widetilde{f_1}(1-f_2) & \ f_1(1-\widetilde{f_2}) & \ \widetilde{f_1}(1-\widetilde{f_2})  \\
f_1f_2 & \ \widetilde{f_1} f_2 & \ f_1 \widetilde{f_2} & \ \widetilde{f_1} \widetilde{f_2} \\
\end{array} \right ]$\
Suppose the energies of the 00, 01, 10 and 11 states are such that
$f_1 = f_2 \approx 1$ and $\widetilde{f_1} \widetilde{f_2} \approx 0$.
If the system starts out in the 00 state, how will it behave thereafter?
[^46]

## Bayesian Networks

This is [Lecture 3.4: Watch youtube
video](https://www.youtube.com/watch?v=20Ecd2Aqn40)

In this Chapter we started by defining this transition matrix
$[W]{p}={p}$ and showing how you could get the stationary probability
distribution from that matrix. Then we spend the next two lectures
talking about this sampling technique and writing down the transition
matrix and discussing why certain updating sequences work whereas the
simultaneous updating doesn't work, if the nodes are connected.

### Figs. [3.28](#fig:fig3_4_1){reference-type="ref" reference="fig:fig3_4_1"}-[3.35](#fig:fig3_4_8){reference-type="ref" reference="fig:fig3_4_8"}: Bayesian versus reciprocal networks {#figs.-figfig3_4_1-figfig3_4_8-bayesian-versus-reciprocal-networks}

![Boltzmann Network.](./Week3_4/figure1.jpg){#fig:fig3_4_1
width="\\textwidth"}

What we'll do in this lecture is we'll talk about a different kind of
network, see, which is different from the Boltzmann networks that we
have been talking about. In this network, the connections are one way.
By contrast, Boltzmann networks are always reciprocal, if there's a
$w_{12}$, there's a $w_{21}$ and they are equal.

#### Figs. [3.29](#fig:fig3_4_2){reference-type="ref" reference="fig:fig3_4_2"}-[3.30](#fig:fig3_4_3){reference-type="ref" reference="fig:fig3_4_3"}: Bayesian networks {#figs.-figfig3_4_2-figfig3_4_3-bayesian-networks}

![Bayesian Network.](./Week3_4/figure2.jpg){#fig:fig3_4_2
width="\\textwidth"}

Bayesian networks are directed. So, $w_{12}$ is 0, but $w_{21}$ is
nonzero (see Fig. [3.29](#fig:fig3_4_2){reference-type="ref"
reference="fig:fig3_4_2"}) and such networks are quite widely used
particularly because they are much easier to train than the Boltzmann
networks we have focused on. In this lecture I'd like to say a few words
about this type of network.

![Bayesian Network.](./Week3_4/figure3.jpg){#fig:fig3_4_3
width="\\textwidth"}

So first point about these networks is that there is no obvious
Boltzmann formula. You see this whole Boltzmann approach, is based on
the concept of an energy function. If the connection is not reciprocal,
then there is no simple way to write an energy function.

We have talked about three methods the Boltzmann method, the sampling
method, and the transition matrix method. As we'll see, the sampling
method and the $W$ matrix method they still agree very well. That is,
the transition matrix method does give a very good description of how
the sampling method works, that's fine, although there is no Boltzmann
to compare to.

#### Fig. [3.31](#fig:fig3_4_4){reference-type="ref" reference="fig:fig3_4_4"} {#fig.-figfig3_4_4}

So if you use the sampling method or the transition matrix method they
both give the same answer. But the answer is different depending on the
sequence of updating. You see with Boltzmann networks it doesn't matter
which way you update. It could be 1 and then 2 or it could be 2 and
then 1. But now the answers will be different.

![Bayesian Network.](./Week3_4/figure4.jpg){#fig:fig3_4_4
width="\\textwidth"}

What do we compare these answers to? We don't have Boltzmann but there
is a Bayes' theorem that allows you to predict the probabilities for
directed networks and the answer that you get will match Bayes' theorem
if you update it in the order of parent to child. You see in Bayesian
networks, you can identify parent nodes and child nodes who are
influenced by their parents. The correct way of sampling is one that
gives results that agree with Bayes' theorem, which generally describes
phenomena in the real world very well. And to agree with Bayes' theorem,
the updating order should be first parent, then child.

Let's talk about these points one by one.

#### Fig. [3.32](#fig:fig3_4_5){reference-type="ref" reference="fig:fig3_4_5"}: Why no energy function {#fig.-figfig3_4_5-why-no-energy-function}

So first point is, why is there no energy function for non reciprocal
networks? Well, if you write down the energy function like let's say
with two $p$-$bits$, you'll get a set of terms looking like this,
$\widetilde{E}=s_1x_1+s_2x_2+(1/2)w_{12}s_1s_2+(1/2)w_{21}s_1s_2$, and
we'll notice how $w_{12}$ and $w_{21}$ are kind of part of the same
term.

Now let's calculate this synaptic functions you know the
$\widetilde{x}_1$ that determines the updating of $p$-$bit$ 1, or
$\widetilde{x}_2$ which determines the updating of $p$-$bit$ 2. The way
you're supposed to do it is by taking the derivative of the energy
function with respect to $s_1$ or $s_2$:
$\partial\widetilde{E}/\partial s_1$ or
$\partial\widetilde{E}/\partial s_2$. And if you just go from an energy
function, you get the same factor in both places,
$\widetilde{x}_1=x_1+((w_{12}+w_{21})/2)s_2$ and
$\widetilde{x}_2=x_2+((w_{12}+w_{21})/2)s_1$.

This is not really an accident. It's kind of inevitable if you're
starting from an energy function. because
$\partial\widetilde{x}_1/\partial s_2 = \partial\widetilde{x}_2/\partial s_2 = \partial^2\widetilde{E}/\partial s_1 \partial s_2$.
So usually, you cannot start from an energy function and get a directed
network out of it, and if you don't have an energy function, you don't
have a Boltzmann formula either.

![Why no energy function](./Week3_4/figure5.jpg){#fig:fig3_4_5
width="\\textwidth"}

#### Fig. [3.33](#fig:fig3_4_6){reference-type="ref" reference="fig:fig3_4_6"} {#fig.-figfig3_4_6}

One thing we could do is forget about energy, and just start from the
synaptic equations getting rid of the term $w_{12}s_2$ while keeping
$w_{21}s_1$ since the weight term acts only one way.

![Synaptic functions without an energy
function](./Week3_4/figure6.jpg){#fig:fig3_4_6 width="\\textwidth"}

#### Fig. [3.34](#fig:fig3_4_7){reference-type="ref" reference="fig:fig3_4_7"} {#fig.-figfig3_4_7}

You could use the $[W]$ matrix method, to emulate both update orders for
the sampling process. It could be 1 and then 2 or 2 and then 1, and in
either case we can write down a composite $W$ matrix just as we did in
the last lecture (Fig. [3.22](#fig:fig3_3_3){reference-type="ref"
reference="fig:fig3_3_3"}). It's just that we drop the $w_{12}$ but keep
the $w_{21}$ as shown.

![$[W]$ Matrix.](./Week3_4/figure7.jpg){#fig:fig3_4_7
width="\\textwidth"}

#### Fig. [3.35](#fig:fig3_4_8){reference-type="ref" reference="fig:fig3_4_8"}: {#fig.-figfig3_4_8}

Here we show two problems, one reciprocal with $w_{12}= 2, w_{21} = 2$,
and one non-reciprocal $w_{12}= 0, w_{21} = 2$ and compare the results
from direct sampling and from the eigenvectors of the $W$ matrix. In
either case, the sampling method and the $[W]$ matrix method they agree,
showing that the $[W]$ matrix method describes the sampling process for
different networks quite well.

But the point to note is that the update order makes no difference to
the reciprocal network, but does make a difference to the Bayesian one.
But which one is more correct? With Boltzmann networks, we could have
compared to the Boltzmann result, but for Bayesian networks, what do we
compare to? Answer: Bayes' theorem which we will talk about next.

![Bayesian versus reciprocal
networks](./Week3_4/Picture8.png){#fig:fig3_4_8 width="\\textwidth"}

### Figs. [3.36](#fig:fig3_4_10){reference-type="ref" reference="fig:fig3_4_10"}-[3.37](#fig:fig3_4_11){reference-type="ref" reference="fig:fig3_4_11"}: Bayes theorem {#figs.-figfig3_4_10-figfig3_4_11-bayes-theorem}

In a Bayesian network you have a parent node that influences the child
node and the way you should do it is, you should first write down the
parent distribution because that doesn't depend on anybody else and then
use Bayes' theorem to write the overall probabilities. This should get
clearer once we look at our simple example.

In our problem, we first note that the state of the parent ($p$-$bit$ 1)
is determined solely by its bias $x_1$ irrespective of the state of the
child. So $P(s_1=0) = 1-f_1$ and $P(s_1=f_1)$, where
$f_1 = 1/(1+exp(x_1))$.

Next, suppose I want to know probability of 00. We first take the
probability that the parent is 0 and then multiply it by the probability
that the $\textit{child is 0 given that the parent is 0}$:
$P(00)=P(s_2=0)|_{s_1=0}P(s_1=0)$. This is basically the Bayes' theorem
that we are talking about.

![Bayes Theorem.](./Week3_4/figure10.jpg){#fig:fig3_4_10 width="95%"}

![Bayes Theorem.](./Week3_4/figure11.jpg){#fig:fig3_4_11 width="95%"}

So what is the probability that this child is 0 given that the parent is
0? Given that the parent is 0 means $s_1$ equal to 0. So then the
$\widetilde{x}_2$ is just $x_2$ and so the state of the child is
determined by $f_2=1/(1+\exp{x_2})$. The probability the child is 0 is
$1-f_2$. And so overall $P(00)$ is $P(00)=(1-f_2)(1-f_1)$.

Similary you can fill up P(01), P(10) and P(11) as shown. So the basic
procedure, remember, parent you can write right away, and then you have
to find the child using these conditional probabilities. Okay, so that's
the Bayes theorem.

Now if you compare what you get from sampling and from $[W]$ matrix
method with Bayes theorem, we see in this problem very clearly that when
you update from parent to child, they match beautifully. When you update
from child to parent, the sampling and the $[W]$ matrix agree as we had
discussed, but not with Bayes' theorem (see Fig.
[3.37](#fig:fig3_4_11){reference-type="ref" reference="fig:fig3_4_11"})

So, this is the basic point we want to get across here that when it
comes to directed networks, the order of update indeed matters and when
you do things parent to child, they work very well. When you do child to
parent, it doesn't agree with Bayes' theorem.

### Quiz

#### Question 1

How should we time sample a system of spins all with directed
connections (all $w_{ij} \neq 0, w_{ji} = 0$), such that the samples
follow the Bayes rule? [^47]

#### Question 2

Suppose we have a network of 2 spins labeled 00,01,10,11 in the order
$\{Parent \ \  Child\}$. The Parent node is equally likely to be 0 or 1,
while the child node is exactly the opposite of the parent node.
According to Bayes theorem, what are the probabilities of
$\{00 \ 01 \ 10 \ 11\}$?[^48]

## Feynman Paths {#sec:sec3_5}

This is [Lecture 3.5: Watch youtube
video](https://www.youtube.com/watch?v=20Ecd2Aqn40)

### Figs. [3.38](#fig:fig3_5_2){reference-type="ref" reference="fig:fig3_5_2"}-[3.42](#fig:fig3_5_7){reference-type="ref" reference="fig:fig3_5_7"}: Multiplying W-matrices {#figs.-figfig3_5_2-figfig3_5_7-multiplying-w-matrices}

#### Fig. [3.38](#fig:fig3_5_2){reference-type="ref" reference="fig:fig3_5_2"}: Why W-matrix? {#fig.-figfig3_5_2-why-w-matrix}

One of the reasons I'm spending so much time on this $[W]$ matrix method
is because it gives you a deeper understanding of how this whole
sampling technique works. But from a practical sense though, you could
say that, well, the Boltzmann law needed a $2^n$ space to work on, which
was unwieldy. But the $[W]$ matrix, it is a $2^n$ by $2^n$ matrix. Now,
such a huge unwieldy matrix, is it really useful? Well, one use is just
understanding how sampling works, but the other use is, it gives you a
nice physical picture, which also provides this conceptual bridge to
quantum computing and that's what this lecture is about. It's based on
this concept of Feynman paths.

![Why \[W\] Matrix?](./Week3_5/Picture2.png){#fig:fig3_5_2
width="\\textwidth"}

#### Figs. [3.39](#fig:fig3_5_4){reference-type="ref" reference="fig:fig3_5_4"}: {#figs.-figfig3_5_4}

![\[W\] Matrix.](./Week3_5/figure4.jpg){#fig:fig3_5_4
width="\\textwidth"}

![\[W\] Matrix.](./Week3_5/figure5.jpg){#fig:fig3_5_5
width="\\textwidth"}

Now, as you remember, the way I introduced this $[W]$ matrix, is that it
is the matrix which propagates a probability distribution function, from
one time point to the next. Now, for this lecture I'd like to generalize
this a little bit. And that is to note that firstly, you see the
components of $[W]$ as we have seen depends on this bias matrix and the
weight matrix, ${x}$ and ${w}$, and these could in principle be changing
with time.

So all these capital $[W]$'s don't have to be the same, they could be
different, it could be evolving with a different bias, or a different
weight matrix. So going forward, what I'll do is I'll put a superscript
on top, 1, 2, up to T. Where this $[W^{(1)}]$ is the transition matrix
for step one, this $[W^{(2)}]$ is the transition matrix for step two,
and so on until step $T$, $[W^{(\rm T)}]$.

#### Fig. [3.40](#fig:fig3_5_5){reference-type="ref" reference="fig:fig3_5_5"} {#fig.-figfig3_5_5}

Now, If I start with some initial state, what happens is the probability
distribution function at time 1 is equal to this $[W^{(1)}]$, times the
initial distribution ${i}$. Again, you go on to time 2, and you will
have a product of $[W^{(1)}]$ and $[W^{(2)}]$. And then in the end,
after a long time $T$, you'd have multiplied it out by all these
matrices one by one, $[W^{(1)}]$, $[W^{(2)}]$, all the way up to
$[W^{(\rm T)}]$, and so this ${i}$ is the initial distribution. Then you
have multiplied it out, and that's how you get final probability
distribution function.

#### Figs. [3.41](#fig:fig3_5_6){reference-type="ref" reference="fig:fig3_5_6"}-[3.42](#fig:fig3_5_7){reference-type="ref" reference="fig:fig3_5_7"} {#figs.-figfig3_5_6-figfig3_5_7}

Now, just look at a numerical example, a two $p$-$bit$ system which has
four configurations, 00, 01, 10, and 11. Suppose you're starting it out
in the 00 state, which means the initial distribution looks like
$\{1 0 0 0\}$.

Now, after we apply the $[W]$, and here I just took some numerical
values corresponding to certain parameters that I used. It's from one of
the examples we had discussed earlier, and you see that the distribution
which was originally $100\%$ (00) has now spread out, it is now $7\%$
(00), $20\%$ (01), $53\%$ (10), and $20\%$ (11).

You apply again, the distribution has again changed, $12\%$, $33\%$,
$40\%$, $15\%$, and of course when you add them up, it's $100\%$, since
it's a probability distribution.

![\[W\] Matrix.](./Week3_5/figure6.jpg){#fig:fig3_5_6 width="105%"}

#### Fig. [3.42](#fig:fig3_5_7){reference-type="ref" reference="fig:fig3_5_7"} {#fig.-figfig3_5_7}

![\[W\] Matrix.](./Week3_5/figure7.jpg){#fig:fig3_5_7 width="105%"}

Now, after some time, after you've applied the same $[W]$ a few times,
it gets to a stationary state, which is actually the Boltzmann
distribution, $13\%$ for (00) and (11), and a higher percentage like
$37\%$ for (01) and (10) each. So that's how you would gradually evolve
to this final state.

So if you wanted to now know that well, I started in (00), but what is
the probability that I'll end up in (01)? The answer is $37\%$. What is
the probability I'll end up in (11)? Well, it's $13\%$,. So basically
then if you want to know the probability that you'll be in state $f$, if
you have started from $i$, then what you should do is look at the $f$
component in the final distribution:
$P_{f\leftarrow i}=\left[\left[W^{(\rm T)}\right]\cdots[W^{(2)}][W^{(1)}]\{i\}\right]_f$.

### Fig. [3.43](#fig:fig3_5_8){reference-type="ref" reference="fig:fig3_5_8"}-[3.45](#fig:fig3_5_10){reference-type="ref" reference="fig:fig3_5_10"}: Matrix multiplication as sum over paths {#fig.-figfig3_5_8-figfig3_5_10-matrix-multiplication-as-sum-over-paths}

Now, we are going to make use of the
$\textit{rule of matrix multiplication}$. So what we have here is a
string of matrices that are getting multiplied. The rule for matrix
multiplication says that when you say take $[AB]$, and you want to know
the $ij$ element of the product, it is like $A_{ia}B_{aj}$, and you have
to sum over all $a$: $[AB]_{ij}=\sum_{a}{A_{ia}B_{aj}}$. This is the
basic rule of matrix multiplication. So every time you multiply two
matrices, you pick up a summation.

In our problem you see I want the final probability of $i$ to $f$. And
what I would have done is, a string of these summations, one for each
multiplication essentially. So you'd have $a_1$, and then $a_2$, and
then $a_3$, one after the other, up to $a_{T- 1}$, and all these
multiplied, and the first index here will be $i$, that's the state you
start it from, initial state, and the last index will be $f$, that's the
state you end up in. So this is a purely mathematical expansion of this
matrix multiplication, but the reason I'm doing it is, it gives you a
very interesting way of viewing this whole sampling procedure, and how
we think about these things.

![\[W\] Matrix multiplication involves summing over intermediate
states.](./Week3_5/figure8.jpg){#fig:fig3_5_8 width="\\textwidth"}

#### Fig. [3.44](#fig:fig3_5_9){reference-type="ref" reference="fig:fig3_5_9"} {#fig.-figfig3_5_9}

![\[W\] Matrix.](./Week3_5/figure9.jpg){#fig:fig3_5_9
width="\\textwidth"}

So this is what you could call a relatively simple special case of the
Feynman path integral. We can write the overall probability, as a sum
over paths, that is, this summation
$P_{f\leftarrow i}=\sum_{a_1,a_2,\ldots,a_{T-1}}{[W^{(T)}]_{f\leftarrow a_{T-1}}\cdots[W^{(2)}]_{a_2\leftarrow a_1}[W^{(1)}]_{a_1\leftarrow i}\{i\}}$.

Why sum over paths?