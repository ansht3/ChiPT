### Quiz

#### Question 1

Why does the Boltzmann Law $p_i = (1/Z) e^{-(E_i - \mu N_i)/kT}$\
apply to all systems irrespective of its details?[^13]

#### Question 2

At equilibrium, why are states with less energy more probable?[^14]

#### Question 3

What is the Boltzmann law corresponding to systems that exchange BOTH
energy and particles with the reservoir?[^15]

## Entropy

This is [Lecture 1.3: Watch youtube
video](https://www.youtube.com/watch?v=yYvKBcVHKh4)

As you may recall, in the first lecture, we stated the Boltzmann law
$p_i=(1/Z)\exp{(-(E_i-\mu N_i)/kT)}$, which gives us the probability
that a system will be in a certain state in the state space. In the
second lecture, we went a little deeper and recognized that what makes
the law applicable to all systems is that it is a property of the
reservoir, and all normal reservoirs shared a certain non-obvious
property. In the process, we introduced the concept of entropy,
$S(E,N)=k\ln{(W(E,N))}$, whose derivatives give you the two parameters
$\mu$ and $T$ that enter the equilibrium law. Now what we'll be doing in
this lecture is to introduce a model for this reservoir and use it to
calculate quantities like $W(E,N)$ so that we get a little more insight
into how $\partial S/\partial E$ and $\partial S/\partial N$ help define
$\mu$ and $T$.

### Figs. [1.16](#fig:fig1_3_1){reference-type="ref" reference="fig:fig1_3_1"}-[1.18](#fig:fig1_3_3){reference-type="ref" reference="fig:fig1_3_3"}: Entropy from reservoir model {#figs.-figfig1_3_1-figfig1_3_3-entropy-from-reservoir-model}

#### Fig. [1.16](#fig:fig1_3_1){reference-type="ref" reference="fig:fig1_3_1"}: Model for reservoir {#fig.-figfig1_3_1-model-for-reservoir}

![Model for reservoir as a collection of identical 2-level
units.](./Week1_3/fig1_3_1.jpg){#fig:fig1_3_1 width="\\textwidth"}

Let me introduce a simple model for the $reservoir$ that's also composed
of these little two level systems, 0 and 1, and there are many of them,
that's the small $n$, and they are all non-interacting (see Fig.
[1.16](#fig:fig1_3_1){reference-type="ref" reference="fig:fig1_3_1"}).
Notice that I'm using $\widetilde{p}_i$, to distinguish it from the
equilibrium probabilities $p_i$. Of course, the reservoir could also be
in equilibrium, in which case these probabilities would be given by
$p$'s without the tilde. But just to keep it general we have the tilde.

#### Fig. [1.17](#fig:fig1_3_2){reference-type="ref" reference="fig:fig1_3_2"} {#fig.-figfig1_3_2}

![Entropy from reservoir model.](./Week1_3/fig1_3_2.jpg){#fig:fig1_3_2
width="\\textwidth"}

Now, consider $n$ units, so there will be $2^n$ states, each one could
be described by a string of 1's and 0's (see Fig.
[1.17](#fig:fig1_3_2){reference-type="ref" reference="fig:fig1_3_2"}a).
And the number of units that will be in state 1 will be
$N= n\widetilde{p}_1$, the total number times $\widetilde{p}_1$. The
energy will be $E=\varepsilon n\widetilde{p}_1$, where $\varepsilon$ is
the energy corresponding to 1, relative to the zero.

Now, we write the entropy, that's this $k \ln{W}$, $k$ being the
Boltzmann constant, and $W$ is the number of different states that
correspond to that particular, for a given $\widetilde{p}_1$, the number
of different states that correspond to it.

Now let me explain what I mean by that. Supposing $\widetilde{p}_1$ were
1 (see Fig. [1.17](#fig:fig1_3_2){reference-type="ref"
reference="fig:fig1_3_2"}b), then there's only one state that one could
write down, that's all 1s, or if the $\widetilde{p}_1$ were 0, it would
be all 0's and so $W$ would be 1, and the entropy would be 0. On the
other hand, if the probability is, say, 50%, (0.5) (see Fig.
[1.17](#fig:fig1_3_2){reference-type="ref" reference="fig:fig1_3_2"}c),
that means half are 0 and half are 1, and then you will see there are
many ways of writing that, and so there will be lots of states, $W$ will
be a big number, and the corresponding entropy would also be big.

Now, mathematically, I could write $W$ as ${}^nC_{n\widetilde{p}_1}$
(see Fig. [1.17](#fig:fig1_3_2){reference-type="ref"
reference="fig:fig1_3_2"}d): The idea is, I've got $n$ units, in how
many ways can I choose $n\widetilde{p}_1$ units that will be 1. And this
is also equal to $W={}^nC_{n\widetilde{p}_0}$: In how many ways can I
choose $n\widetilde{p}_0$ units, that will be 0. And those are
mathematically the same thing:
$W=(n!)/((n\widetilde{p}_0)!(n\widetilde{p}_1)!)$. This is the
elementary combinatorial law that you have probably seen, if not, you
could look it up easily.

#### Fig. [1.18](#fig:fig1_3_3){reference-type="ref" reference="fig:fig1_3_3"} {#fig.-figfig1_3_3}

![Plot of entropy versus $\widetilde{p}_1$ for different number of
units, $n$.](./Week1_3/fig1_3_3.jpg){#fig:fig1_3_3 width="\\textwidth"}

Now, if we take $W=(n!)/((n\widetilde{p}_0)!(n\widetilde{p}_1)!)$ and
plot it as a function of $\widetilde{p}_1$, you'll get a curve looking
like this (see Fig. [1.18](#fig:fig1_3_3){reference-type="ref"
reference="fig:fig1_3_3"}). When $\widetilde{p}_1$ is zero at that end,
as we discussed, there is only one state possible. When
$\widetilde{p}_1$ is 1, again, only one state is possible. So at either
of those ends, the entropy is 0, in the middle, when it's 0.5, that's
when the entropy is the maximum and if you plot it for different values
of $n$, $n$, meaning the total number of units. As you increase $n$ it
converges to a particular curve. So, once you get to, say, 1000, it
really doesn't matter whether $n$ is 1000 or 10,000, you get much the
same curve.

And this curve has a maximum of $\ln{(2)}$, and actually, there is a
simple expression that describes this limiting curve, the one that you
get when $n$ tends to infinity. Now, what we'll be showing is that
starting from this combinatorial expression,
$W=(n!)/((n\widetilde{p}_0)!(n\widetilde{p}_1)!)$ and
$S = k \ln{(W(\widetilde{p}_1)}$, how you get to this relatively simple
expression,
$S/n=-k(\widetilde{p}_0 \ln{\widetilde{p}_0} + \widetilde{p}_1\ln{\widetilde{p}_1})$.

### Figs. [1.19](#fig:fig1_3_4){reference-type="ref" reference="fig:fig1_3_4"}-[1.20](#fig:fig1_3_5){reference-type="ref" reference="fig:fig1_3_5"}: Thermodynamic versus information entropy {#figs.-figfig1_3_4-figfig1_3_5-thermodynamic-versus-information-entropy}

#### Fig. [1.19](#fig:fig1_3_4){reference-type="ref" reference="fig:fig1_3_4"} {#fig.-figfig1_3_4}

![Similarity in expressions between thermodynamic entropy and the
Shannon entropy used in information
theory.](./Week1_3/fig1_3_4.jpg){#fig:fig1_3_4 width="\\textwidth"}

But before we go on, let me just mention that there is a similar
expression you may have seen if you have taken a course in information
theory, because in information theory the way you think is, supposing I
send a message with $n$ bits that looks like this, 100111. What is the
information content? The argument is that if there were, let's say 100
possibilities, then when I send you one particular message, the
information content is $\ln{(100)}$. So, that is how you define the
information content and in information theory, entropy is a
$dimensionless$ number, whereas, in what we are doing, we're coming at
it from the point of view of thermodynamics, and the thermodynamic
entropy is a $dimensionful$ number. It has the same units as the
*Boltzmann constant*, $k$. And if you Google it, you'll see lots of
discussions about the relationship between the thermodynamic entropy and
the information entropy. Some believe there is a deep relation, some
don't and there's a lot of arguments about that.

#### Fig. [1.20](#fig:fig1_3_5){reference-type="ref" reference="fig:fig1_3_5"}: Expression for entropy {#fig.-figfig1_3_5-expression-for-entropy}

![Deriving the expression for
entropy.](./Week1_3/fig1_3_5.jpg){#fig:fig1_3_5 width="\\textwidth"}

Now, we'll go through a little bit of algebra to show how you get from
this combinatorial expression to a relatively simple expression (see
Fig. [1.20](#fig:fig1_3_5){reference-type="ref"
reference="fig:fig1_3_5"}). So the first step is, you take the logarithm
of both sides, because you want $\ln{W}$, and
$\ln{W}=\ln{(n!)}-\ln{(n\widetilde{p}_0)!}-\ln{(n\widetilde{p}_1)!}$.
Now, next what we use is something called the *Stirling's
Approximation*, which is that when $n$ is large, remember, this
equivalence we are trying to prove only applies for large $n$. So when
$n$ is large, you can write the $\ln{(n!)}$ as $n\ln{(n)}-n$. So instead
of $\ln{(n!)}$, we can write $n\ln{(n)}-n$. Similarly, instead of
$\ln{(n\widetilde{p}_0)!}$, we can write
$n\widetilde{p}_0\ln{(n\widetilde{p}_0)}-n\widetilde{p}_0$. Similarly,
$\ln{(n\widetilde{p}_1)!}$ becomes
$n\widetilde{p}_1\ln{(n\widetilde{p}_1)}-n\widetilde{p}_1$. So, we are
applying this *Stirling's Approximation* to each of the three things.
Now, you'll notice that, what's in here, $n$ $-n\widetilde{p}_0$
$-n\widetilde{p}_1$, that just cancels out. Why? Because, remember,
$\widetilde{p}_0$ plus $\widetilde{p}_1$ is equal to 1 and so we are
left with the top-line
$n\ln{(n)}-n\widetilde{p}_0\ln{(n\widetilde{p}_0)}-n\widetilde{p}_1\ln{(n\widetilde{p}_1)}$.

Next what we do is, we expand it a little in the sense that when you
have $\ln{(n\widetilde{p}_0)}$, that's like
$\ln{(n)}+\ln{(\widetilde{p}_0)}$. Similarly, $\ln{(n\widetilde{p}_1)}$
is $\ln{(n)}+\ln{(\widetilde{p}_1)}$. So from here, we get this
$n\ln{(n)}-n\widetilde{p}_0\ln{(n)}-n\widetilde{p}_1\ln{(n)}-n\widetilde{p}_0\ln{(\widetilde{p}_0)}-n\widetilde{p}_1\ln{(\widetilde{p}_1)}$.
We have broken up each of these two terms into these two each, so now we
have five terms there and here again, what I'd argue is that this top
line cancels out, because $n\widetilde{p}_0+n\widetilde{p}_1=n$. So
everything in that top line cancels out and so we are now left with just
this,
$-n\widetilde{p}_0\ln{(\widetilde{p}_0)}-n\widetilde{p}_1\ln{(\widetilde{p}_1)}$,
which is what I've written here,
$S/k=-n(\widetilde{p}_0\ln{(\widetilde{p}_0)}+\widetilde{p}_1\ln{(\widetilde{p}_1)})$.
And that's basically what we set out to prove,
$S/n=-k(\widetilde{p}_0\ln{(\widetilde{p}_0)}+\widetilde{p}_1\ln{(\widetilde{p}_1)})$.
So that's all the algebraic steps, getting from the original
combinatorial expression to the relatively simpler expression at the
end.

### Figs. [1.21](#fig:fig1_3_6){reference-type="ref" reference="fig:fig1_3_6"}-[1.22](#fig:fig1_3_7){reference-type="ref" reference="fig:fig1_3_7"}: Reservoir model with d-level units {#figs.-figfig1_3_6-figfig1_3_7-reservoir-model-with-d-level-units}

#### Figs. [1.21](#fig:fig1_3_6){reference-type="ref" reference="fig:fig1_3_6"} {#figs.-figfig1_3_6}

![Generalization from $2$-level to $d$-level
units.](./Week1_3/fig1_3_6.jpg){#fig:fig1_3_6 width="\\textwidth"}

So this is the result when the reservoir is composed of little two-level
systems, 0 and 1. Now, if the reservoir is composed of, say $d$ level
systems, you have lots of levels from 0 to $d$, $d$ could be 10, could
be 4, whatever it is. Once again, we have $n$ number of units but if you
have multi levels like this, then the generalization is, instead of
$\widetilde{p}_0\ln{(\widetilde{p}_0)}+\widetilde{p}_1\ln{(\widetilde{p}_1)}$,
you get a sum over all of these. So, we'll have
$\widetilde{p}_0\ln{(\widetilde{p}_0)}+\widetilde{p}_1\ln{(\widetilde{p}_1)}+\widetilde{p}_2\ln{(\widetilde{p}_2)}+\widetilde{p}_3\ln{(\widetilde{p}_3)}$,
and so on. So, that's what this summation is
$S/n=-k\sum_{i=0}^{d-1}{\widetilde{p}_i\ln{(\widetilde{p}_i)}}$. It says
go and sum them all up. So that's the general expression for the
entropy. Finally to complete the story, we can also generalize
expressions for the energy and the number of particles:
$E/n=\sum_{i=0}^{d-1}{\widetilde{p}_iE_i}$ and
$N/n=\sum_{i=0}^{d-1}{\widetilde{p}_iN_i}$.

#### Fig. [1.22](#fig:fig1_3_7){reference-type="ref" reference="fig:fig1_3_7"} {#fig.-figfig1_3_7}

![Expressions for S,E,N per unit.](./Week1_3/Picture2.png){#fig:fig1_3_7
width="90%"}

In deriving expressions for S,E,N we started from a model with $n$
$identical$ units, $n$ being a large number, 1000 of them, for example.
But another way to think about it is that we have only one unit which is
continually jumping around and you can average over time. So, instead of
writing the total entropy of $n$ units, you could take the entropy per
unit and think of it as the entropy of one unit, but when averaged over
time. Alternatively you could interpret it as an ensemble average,
averaged over an ensemble of $n$, identical units (Fig.
[1.22](#fig:fig1_3_7){reference-type="ref" reference="fig:fig1_3_7"}).

### Fig. [1.23](#fig:fig1_3_8){reference-type="ref" reference="fig:fig1_3_8"}: $\mu$, T from entropy $S$ {#fig.-figfig1_3_8-mu-t-from-entropy-s}

![Connecting entropy, $S$ back to the concepts of electrochemical
potential, $\mu$ and temperature,
$T$.](./Week1_3/fig1_3_8.jpg){#fig:fig1_3_8 width="90%"}

In the last lecture we said that $T$ is related to the derivative of
entropy with respect to energy, whereas the $\mu /T$ is related to the
derivative of $S$ with respect to $N$ (see Fig.
[1.23](#fig:fig1_3_8){reference-type="ref" reference="fig:fig1_3_8"}b).
We could combine the two expressions and write it this way,
$\mathrm{d}S= (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$ (see Fig.
[1.23](#fig:fig1_3_8){reference-type="ref" reference="fig:fig1_3_8"}c).
Is this relation satisfied by the explicit expressions for $S$, $E$ and
$N$ that we have obtained from an explicit model?

The answer is $not$ always, but only if $\widetilde{p}_i = p_i$.
Meaning, if we assume that this reservoir that we are talking about is
actually in equilibrium, which is often the case for reservoirs. But we
may want to apply these expressions to other things which are out of
equilibrium and we could still use these expressions. That is why I went
to the trouble of putting a tilde on top of $p$, ($\widetilde{p}_i$), to
make it clear that the expressions we're obtaining are valid in general.
But if the entity is in equilibrium, so that the $\widetilde{p}$'s
happen to equal the $p's$ then you'd have this interesting relation
$\mathrm{d}S= (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$. We will pick this up
in the next lecture.

### Quiz

#### Question 1

What is the entropy of a collection of $8$ one-electron levels that are
all full?[^16]

#### Question 2

What is the entropy of a collection of $n$ identical units, EACH having
$3$ levels that are all equally probable.[^17]

#### Question 3

What is the entropy of a collection of 8 one-electron levels each have a
probability of $0.5$ of being full?[^18]

## Free Energy

This is [Lecture 1.4: Watch youtube
video](https://www.youtube.com/watch?v=OPomTKE9eEg)

As you may recall we started by introducing the Boltzmann law for the
equilibrium probabilities $p_{i}$. In general of course a system need
not be in equilibrium and the probabilities could be something very
different, $\widetilde{p}_{i}$. In this lecture we will introduce the
concept of free energy $F = E- \mu N - TS$ and show that it has a
$minimum$ value at $equilibrium$ when all the $\widetilde{p}_{i}=p_{i}$.
This property of F leads to the $equilibrium$ relation
$\mathrm{d}S= (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$ that I stated at the
end of the last lecture.

### Fig. [1.24](#fig:fig1_4_1){reference-type="ref" reference="fig:fig1_4_1"}: Free energy, F {#fig.-figfig1_4_1-free-energy-f}

Now, to start with we'll be doing a bit of algebra, starting from the
expression for the free energy $F = E-\mu N-TS$ (Fig.
[1.24](#fig:fig1_4_1){reference-type="ref" reference="fig:fig1_4_1"}).\
$\textbf{Step 1:}$ Substitute for E,N and S from the expressions that we
obtained in the last lecture (see Fig.
[1.24](#fig:fig1_4_1){reference-type="ref" reference="fig:fig1_4_1"},
lower right):
$S = -k\sum_{i=0}^{d-1}{\widetilde{p}_i\ln{\widetilde{p}_i}}$,
$E = \sum_{i=0}^{d-1}{\widetilde{p}_i E_i}$ and
$N = \sum_{i=0}^{d-1}{\widetilde{p}_i N_i}$. This takes us to
$\ \ F = kT\sum_{i}{\widetilde{p}_{i}((E_i-\mu N_i)/kT)+\ell n{\widetilde{p}_i}}$).\

![Deriving an expression for free
energy.](./Week1_4/fig1_4_1.jpg){#fig:fig1_4_1 width="90%"}

$\textbf{Step 2:}$ Use equilibrium probabilities
$\ \ p_i = (1/Z)\exp{(-(E_i-\mu N_i)/kT)}$, to replace the term
$(E_i-\mu N_i)/kT$ with $-\ell n Z - \ell n p_{i}$ to obtain
$F=-kT\ell n{Z}+kT\sum_{i}{\widetilde{p}_i\ell n{(\widetilde{p}_i/p_i)}}$.\
Now, you'll notice that if the probabilities of your system, are
actually equal to the equilibrium probabilities, then you see,
$\ell n{(\widetilde{p}_i/p_i)}= \ell n{(1)} = 0$, and so the term
$kT\sum_{i}{\widetilde{p}_i\ell n{(\widetilde{p}_i/p_i)}}$ drops out
giving us just $F = -kT\ell n{Z}$.

### Fig. [1.25](#fig:fig1_4_2){reference-type="ref" reference="fig:fig1_4_2"}: Gibbs' inequality {#fig.-figfig1_4_2-gibbs-inequality}

Now, what's not so clear is that when you're off equilibrium, so that
these $\widetilde{p}_i$, are a little different from the equilibrium
ones, $p_{i}$, the term
$kT\sum_{i}{\widetilde{p}_i\ell n{(\widetilde{p}_i/p_i)}}$
$\textit{will always be positive}$, it will never be negative (see Fig.
[1.25](#fig:fig1_4_2){reference-type="ref" reference="fig:fig1_4_2"}).
This means that the free energy is equal to $-kT\ell n{Z}$, plus a
quantity that's always positive. So, at equilibrium, when the
$\widetilde{p}_i$ is equal to the equilibrium $p_i$, you get a minimum
value for the free energy. Any other distribution will give you
something bigger.

![Illustrating Gibbs' inequality from the expression for free
energy.](./Week1_4/fig1_4_2.jpg){#fig:fig1_4_2 width="\\textwidth"}

Let me give you an example, to show how this works. I ran on MATLAB^®^
you could do it also, and check it out (see Fig.
[1.25](#fig:fig1_4_2){reference-type="ref" reference="fig:fig1_4_2"}a).
With 10 states, I have chosen two probability distributions,
$\widetilde{p}_{i}$ and $p_{i}$. They're both just selected at random,
so if you look at the difference (see Fig.
[1.25](#fig:fig1_4_2){reference-type="ref" reference="fig:fig1_4_2"}b),
some will be positive, some will be negative, but if you add them all
up, it will be 0. Why? Because the sum of all the $\widetilde{p}_i$ is
equal to 1, and sum of all the $p_i$ is also equal to 1, both being
probability distributions. So if we look at the difference and sum it,
that must be 0, since the sum of each one is 1. That's exactly what
you'll find.\
But if you plot this quantity,
$\widetilde{p}_i\ell n{(\widetilde{p}_i/p_i)}$ (see Fig.
[1.25](#fig:fig1_4_2){reference-type="ref" reference="fig:fig1_4_2"}c),
then you will find that the positives are a little bigger than the
negatives and overall it always comes out positive. This is the *Gibbs'
inequality*, something you can prove mathematically. In statistics,
people often compare two distributions: one is a reference distribution,
the $p_i$, just like our equilibrium distribution and the other is some
other distribution like our non-equilibrium one. To quantify how far one
is from the other, one measure people use is the *Kullback-Leibler
divergence* (see Fig. [1.25](#fig:fig1_4_2){reference-type="ref"
reference="fig:fig1_4_2"}d) and that's exactly the expression that came
up from our free energy expression. When the distributions
$\widetilde{p}_{i}$ and $p_{i}$ match, you get zero. When the
distributions don't match, we get some positive number.

### Fig. [1.26](#fig:fig1_4_3){reference-type="ref" reference="fig:fig1_4_3"}: Equilibrium free energy {#fig.-figfig1_4_3-equilibrium-free-energy}

![Properties of free energy at
equilibrium.](./Week1_4/fig1_4_3.jpg){#fig:fig1_4_3 width="\\textwidth"}

So when you're at equilibrium, we have $F=-kT\ln{Z}$ (see Fig.
[1.26](#fig:fig1_4_3){reference-type="ref" reference="fig:fig1_4_3"})
and this represents a $minimum$ value. If you change the probabilities a
little bit, the energy E or the number of particles N or the entropy S
might all change, but $F = E - \mu N - TS$ won't change because it's a
minimum where the derivative is zero.

The result is that $\mathrm{d}F = 0$ when you make small changes in your
probabilities. Since
$\mathrm{d}F= \mathrm{d}E-\mu \mathrm{d}N- T\mathrm{d}S$, with a little
algebra, you can write
$\mathrm{d}S= (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$. And this is the
expression that I had stated before: remember that $1/T$ was defined as
the derivative of $S$ with respect to $E$ and $-\mu/T$ was the
derivative of $S$ with respect to $N$. But these relations all hold ONLY
when you're really close to equilibrium. Away from equilibrium the free
energy is something bigger given by
$F=-kT\ln{Z}+kT\sum_{i}{\widetilde{p}_i\ln{(\widetilde{p}_i/p_i)}}$ and
$\mathrm{d}F \neq 0$ so that
$\mathrm{d}S \neq (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$.

### Figs. [1.27](#fig:fig1_4_4){reference-type="ref" reference="fig:fig1_4_4"}-[1.28](#fig:fig1_4_6){reference-type="ref" reference="fig:fig1_4_6"}: Entropy drives flow {#figs.-figfig1_4_4-figfig1_4_6-entropy-drives-flow}

#### Figs. [1.27](#fig:fig1_4_4){reference-type="ref" reference="fig:fig1_4_4"} {#figs.-figfig1_4_4}

:

Now, in the next few slides I'd like to explain how a lot of flow that
we see in the real world is driven by $entropy$. This is kind of
important because we often tend to ascribe all flow to mechanical or
electrical forces.

You see in physics there are two big branches, one is mechanics and the
other is thermodynamics: Mechanics started with Newton's laws that
explained planetary motion for example. A few hundred years later came
heat engines and that's when the science of thermodynamics started.
People recognized that heat was a form of energy, but it was very
different from mechanical or electrical energy. Mechanics is usually
driven by force but heat is driven by entropy and what I'd like to give
you is a few examples of entropy driven processes.

![Total entropy increases when an out-of-equilibrium system interacts
with a reservoir.](./Week1_4/fig1_4_4.jpg){#fig:fig1_4_4
width="\\textwidth"}

Suppose I have a system (see Fig.
[1.27](#fig:fig1_4_4){reference-type="ref" reference="fig:fig1_4_4"}),
which is away from equilibrium and is exchanging energy and particles
with some reservoir, which is close to equilibrium. Now, when this
energy and particles are exchanged, the free energy change of the
reservoir will be zero because it's close to equilibrium, but for the
system, what will happen is, the free energy will always go down because
to start with you're not at equilibrium so $F$ is $-kT \ell n{Z}$
$\textit{plus}$ some positive quantity and then as you get to
equilibrium, this second term goes away and you get $-kT \ell n{Z}$.

So, what that means is,
$\mathrm{d}F= \mathrm{d}E-\mu \mathrm{d}N- T\mathrm{d}S \geq 0$ but
$\mathrm{d}F_R= \mathrm{d}E_R-\mu \mathrm{d}N_R- T\mathrm{d}S_R = 0$.
With a little algebra, if you turn it around, you'd see that the entropy
change of the reservoir,
$\mathrm{d}S_R = (\mathrm{d}E_R/T)-(\mu \mathrm{d}N_R/T)$ while the
entropy change of the system,
$\mathrm{d}S > (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$ and this difference
is because the reservoir is close to equilibrium, while the system is
$not.$

Next we note that because the overall energy stays the same, we must
have $\mathrm{d}E+\mathrm{d}E_R=0$. If $\mathrm{d}E$ is positive, then
$\mathrm{d}E_R$ must be negative so that they add up to zero. Similarly
the overall number of particles stays the same, we must have
$\mathrm{d}N+\mathrm{d}N_{R}=0$. This means that
$\mathrm{d}S+\mathrm{d}S_R \geq 0$. In words, this means that the flow
will occur in such a way that the
$\textit{overall entropy of the system plus the entropy of the reservoir will go up}$.

This can be understood by noting that entropy is a measure of the number
of states that are available and generally speaking, all flow occurs in
such a way that things spread out in terms of available states. If only
certain states are filled to start with, then as you let it evolve, it
will tend to fill all accessible states, and so the entropy will
increase.

Note that if both sides are at equilibrium to start with, then energy
and/or particle exchange does not result in change of entropy, since we
have an equality for both system and reservoir:
$\mathrm{d}S_R = (\mathrm{d}E_R/T)-(\mu \mathrm{d}N_R/T)$,
$\mathrm{d}S = (\mathrm{d}E/T)-(\mu \mathrm{d}N/T)$. Adding the two we
get $\mathrm{d}S_R+\mathrm{d}S = 0$, noting the conservation of the
total energy and particle number: $\mathrm{d}E+\mathrm{d}E_R=0$,
$\mathrm{d}N+\mathrm{d}N_R=0$.

#### Fig. [1.28](#fig:fig1_4_6){reference-type="ref" reference="fig:fig1_4_6"}: Flow driven by temperature {#fig.-figfig1_4_6-flow-driven-by-temperature}

![Heat flow between two systems at different
temperatures.](./Week1_4/fig1_4_6.jpg){#fig:fig1_4_6
width="\\textwidth"}

Now one interesting condition is when both are in equilibrium but with
different temperatures (see Fig.
[1.28](#fig:fig1_4_6){reference-type="ref" reference="fig:fig1_4_6"}a),
like one of them is hot and the other is cold and we bring them
together. The question is, which way will the energy flow and which way
will the particles flow?

Okay, this time we can write the changes in the entropy for system and
reservoir as $\mathrm{d}S= (\mathrm{d}E/T_1)-(\mu \mathrm{d}N/T_1)$ and
$\mathrm{d}S_R= (\mathrm{d}E_R/T)-(\mu \mathrm{d}N_R/T)$. Both are
locally in equilibrium, so we have an equality for both. But the
temperatures are different, so they don't cancel when we add them, even
though E,N are still conserved: $\mathrm{d}E+\mathrm{d}E_R=0$,
$\mathrm{d}N+\mathrm{d}N_R=0$. Instead we get
$\mathrm{d}S+\mathrm{d}S_R=d(E-\mu N) \times (1/T_1 - 1/T)$.

Now the question is, which way will energy/particles flow? Answer: In
such a way as to make the total change in entropy,
$\mathrm{d}S+\mathrm{d}S_R \geq 0$.

Say the system is hot and the reservoir is cold, meaning $T_1 > T$. That
means this $1/T_1 < 1/T$ making this ($1/T_1-1/T$) quantity negative.
Hence to make the overall entropy change positive, the flow will occur
in a way so as to make the quantity $\mathrm{d}(E- \mu N)$ negative. Let
us now look separately at dE and dN, the energy flow and the particle
flow.\
$\textbf{Exchange of energy only, no particles:}$ Since $dN = 0$, the
flow will be such as to make $dE < 0$, meaning that the system will
$lose$ energy. Total energy is conserved, so this means $dE_{R} > 0$
indicating that the reservoir $gains$ energy. This should come as no
surprise, since we all know that heat flows from $\textit{hot to cold}$,
which in this case means $\textit{system to reservoir}$. But it provides
us with a nice $\textit{reality check}$.\
$\textbf{Exchange of particles:}$ Now let us look at something for which
the answer is a little less well-known. Suppose electrons are exchanged
(see Fig. [1.28](#fig:fig1_4_6){reference-type="ref"
reference="fig:fig1_4_6"}c) so that $\mathrm{d}N \neq 0$. There is also
an associated change in energy which is $\varepsilon  \mathrm{d}N$ if
each electron or particle carries an energy $\varepsilon$. So
$\mathrm{d}(E- \mu N)$ now looks like $(\varepsilon- \mu)\mathrm{d}N$
and this quantity must be less than 0.

So which way will the particles flow? Well, it depends on whether you're
talking of energy levels above $\mu$ or below $\mu$ (see Fig.
[1.28](#fig:fig1_4_6){reference-type="ref" reference="fig:fig1_4_6"}d),
because if you are above $\mu$, then you see ($\varepsilon- \mu$) is a
positive quantity and then $\mathrm{d}N$ must be negative. What that
means is that the flow must be from system to reservoir, from hot to
cold. On the other hand, if you look below $\mu$, then
($\varepsilon- \mu$) is negative, and so $\mathrm{d}N$ must be positive.
And that means they'll flow from cold to hot.

So in other words, for energy levels above $\mu$, electrons will flow
from hot to cold, below $\mu$, they'll flow from cold to hot and this is
actually a very well known phenomenon in the field of
*thermoelectricity*. There are two types of solids: (a) n-type where
there are more states above $\mu$ than below, and so when you put a hot
probe and a cold probe, the net electron flow is from
$\textit{hot to cold}$, (b) p-type where there are more states below
$\mu$ than above, and in that case electrons flow from
$\textit{cold to hot}$. Once again, a well known phenomena, but what
we're trying to show here is that everything follows from this principle
of increasing entropy which is what is known as the second law of
thermodynamics (see Fig. [1.28](#fig:fig1_4_6){reference-type="ref"
reference="fig:fig1_4_6"}e).

You see, everybody has heard of the first law of thermodynamics which
says that energy is conserved. But the $\textit{second law}$ is
relatively less appreciated. It says that, yes, energy is conserved but
it continually spreads out over the available states. So if it is
originally in one particular state, it will want to spread out over
everything that is available to it, making the overall entropy increase
continually.

### Quiz

#### Question 1

Consider an out-of-equilibrium system that exchanges energy and
particles with a reservoir as it comes to equilibrium. In this process
what happens to the (a) free energy of the system, (b) overall entropy
of the system + reservoir [^19]

#### Question 2

Consider contacts 1 and 2 held at the same temperature T, but at two
different electrochemical potentials $\mu_1 > \mu_2$. If a number of
electrons $\Delta N$ is transferred from 1 to 2, what is the overall
increase in entropy in terms of $\mu_1, \mu_2, \Delta N$.[^20]

#### Question 3

Consider contacts 1 and 2 held at two different temperatures
$T_1 > T_2$. If an energy $\Delta E$ is transferred from 1 to 2, what is
the overall increase in entropy in terms of $T_1, T_2, \Delta E$.[^21]

## Self-Consistent Field

This is [Lecture 1.5: Watch youtube
video](https://www.youtube.com/watch?v=CRXsu_7NcYo)

### Figs. [1.29](#fig:fig1_5_1){reference-type="ref" reference="fig:fig1_5_1"}-[1.32](#fig:fig1_5_4){reference-type="ref" reference="fig:fig1_5_4"}: The exponential problem {#figs.-figfig1_5_1-figfig1_5_4-the-exponential-problem}

#### Figs. [1.29](#fig:fig1_5_1){reference-type="ref" reference="fig:fig1_5_1"} {#figs.-figfig1_5_1}

![Need for the self-consistent field method to handle large
systems.](./Week1_5/fig1_5_1.jpg){#fig:fig1_5_1 width="\\textwidth"}

In the last four lectures we have tried to summarize some of the seminal
concepts of statistical mechanics like the Boltzmann law, entropy and
free energy. Now this Boltzmann law is very general, it applies to any
system but one thing about it is that it operates in a space with $2^n$
states which is so large that it is often impractical to use. As $n$
increases, this $2^n$ actually increases very rapidly, that is
exponentially. Just to appreciate this point, I've put together a little
table here, when $n$ is 1 well $2^n$ is 2, if $n$ is 10, $2^n$ is about
1000. Now, from 10 to 20 point is 1000 becomes a million, because it
gets squared, it being in the exponent. Going from 20 to 40, that gets
squared and so it becomes enormous like in a hurry. And so once you have
a reasonable number of states, working in state space, although
conceptually very sound, is often not practical.

What I'll be describing to you is a method that is widely used
everywhere, in condensed matter physics, semiconductor devices,
everywhere we are always using this method to describe electron electron
interactions. It allows you to do your calculations in this other space,
the space of $n$ states, which is much more manageable. This will also
lead us into the rest of the course where we'll be talking about neural
networks and quantum computing.

#### Fig. [1.30](#fig:fig1_5_2){reference-type="ref" reference="fig:fig1_5_2"}: Toy example {#fig.-figfig1_5_2-toy-example}

![Toy example to illustrate the direct Boltzmann law
approach](./Week1_5/fig1_5_2.jpg){#fig:fig1_5_2 width="\\textwidth"}

To understand this practical approach then, let's start with a toy
example and first see how we would apply the Boltzmann law to it. If
you've got a bunch of one electron levels (see Fig.
[1.30](#fig:fig1_5_2){reference-type="ref" reference="fig:fig1_5_2"}a),
each level can be occupied or unoccupied. And so in the state space, you
have states that are described by these binary numbers, like
$1001\cdots$. Now, if you have say 10 states (see Fig.
[1.30](#fig:fig1_5_2){reference-type="ref" reference="fig:fig1_5_2"}b),
then there will be 1,024 states in state space. So these 10 states have
different energies, which I've shown here (see Fig.
[1.30](#fig:fig1_5_2){reference-type="ref" reference="fig:fig1_5_2"}c).

So what is the occupation of these states? Now, Boltzmann law tells us
how they're occupied at equilibrium but the Boltzmann law applies to the
state space, which is not the $n=10$ space but rather the $2^{10}$
space. The way you would apply the Boltzmann law is to say that, okay,
let's consider a particular state, say 1001000110, and we want to know
its probability. So to apply the Boltzmann law, I first need to know the
energy and the number of electrons involved in that state. Now, the
number of electrons is the number of ones, which is four. What is the
energy? Well, all of these are empty except for those four, so the total
energy is $E_i=\varepsilon_1+\varepsilon_4+\varepsilon_8+\varepsilon_9$.

#### Fig. [1.31](#fig:fig1_5_3){reference-type="ref" reference="fig:fig1_5_3"} {#fig.-figfig1_5_3}

![Occupation factors of different energy levels for the example
considered of Fig. [1.30](#fig:fig1_5_2){reference-type="ref"
reference="fig:fig1_5_2"}.](./Week1_5/fig1_5_3.jpg){#fig:fig1_5_3
width="\\textwidth"}

Now, what you could do then is write down the probabilities of all these
types (see Fig. [1.31](#fig:fig1_5_3){reference-type="ref"
reference="fig:fig1_5_3"}), so this one has a certain probability from
Boltzmann law, next one has a certain probability and then you add up
the probabilities of all the 512 states that have $r=1$. So supposing I
want to know, well what is the occupation of the fourth state? Well when
I write down all of these 1024 states, half of them will have 1 in the
fourth state and half of them will have 0. So, what you do is that,
consider the half that have one, add up their probabilities, and that
will then tell you how many electrons are there in the fourth state. So
that's how you could do this if you are starting from the Boltzmann law.
Of course, it forces you to work in the $2^{10}$ space.

But in this case though, if you just applied the *Fermi function* to
each of these ten levels, you would have come up with exactly the same
answer that you get from this much more elaborate procedure using
Boltzmann law. You can see I've compared the Boltzmann law to the *Fermi
function*, they match each other perfectly. The Fermi function of course
you can understand easily. You see, those levels that are above the
equilibrium chemical potential, like this one, they are weakly occupied,
that's why the *Fermi function* is relatively low. Whereas the ones that
are way below the equilibrium chemical potential, that's where the Fermi
function is higher, it is more occupied. So in this case you could do it
either way and you'll get the same answer. Then you would say, well why
am I even wasting my time with this $2^{10}$ thing? Let's just work with
the $n=10$ space.

#### Fig. [1.32](#fig:fig1_5_4){reference-type="ref" reference="fig:fig1_5_4"} {#fig.-figfig1_5_4}

![Boltzmann law and Fermi function produce different results when
interactions are included.](./Week1_5/fig1_5_4.jpg){#fig:fig1_5_4
width="\\textwidth"}

But the problem is that as soon as you include interactions (see Fig.
[1.32](#fig:fig1_5_4){reference-type="ref" reference="fig:fig1_5_4"}),
the answers you will actually get from Boltzmann law, that's these blue
ones, are very different from the answer that you'd get if we just
applied the *Fermi function*, and see, they don't match at all in this
case. We have assumed that there is some interaction energy in this
case, and that's why they don't match. If it was completely
non-interacting, then it would have matched.

Now how do you include the interactions? Well in terms of Boltzmann law,
the point is that when you evaluate the energies you not only add up the
energies of all these levels, like I had done, but you also add the
interaction energy. Let's say $U$ is the interaction energy per pair of
electrons, so the overall interaction energy will be $U$ times the
number of pairs, which is what I've written here mathematically:
$U \times \sum_{r<q}{\sum_{q=1}^{10}{[n_rn_q]_i}}$.

Consider for example the state $\{1001000110\}$ having four electrons.
What is the interaction energy? Answer: U times the number of pairs. How
many pairs? How many ways can you choose 2 electrons out of 4? Answer:
${}^4C_{2} = 6$. You could write them out explicitly if you like. Levels
1, 4, 8, and 9 are occupied by electrons and the six possible pairs are
(1-4), (1-8), (1-9), (4-8), (4-9), and (8-9). Those are the pairs, and
there's 6 of them, so the energy is $6U$. So this way you have to take
into account the energies of all the $2^{10}$ states and then use the
Boltzmann law the same way we did the non-interacting problem. That's
how you get this blue curve and the point is it wouldn't match the
*Fermi function* at all.

### Figs. [1.33](#fig:fig1_5_5){reference-type="ref" reference="fig:fig1_5_5"}-[1.36](#fig:fig1_5_8){reference-type="ref" reference="fig:fig1_5_8"}: SCF method {#figs.-figfig1_5_5-figfig1_5_8-scf-method}

So when I have an interacting system, how would we actually get the
correct answers? You might say well apply Boltzmann law. Yes, but then
that requires us to work in this $2^{10}$ space and as I mentioned at
the outset, that's a problem. Okay, thousand is not too big, but if
instead of $2^{10}$, we had $2^{20}$, that would be a million and if it
is, like $2^{40}$, it would be like a trillion. So this is the number
that goes up in a hurry. So we need a method for dealing with
interacting systems, a practical method, and that's what we'll be
describing now, what's called the self consistent field method. It works
reasonably well for weakly interacting systems and is widely used.

![Outline of the self-consistent field
method.](./Week1_5/fig1_5_5.jpg){#fig:fig1_5_5 width="\\textwidth"}

So how does this work? Well, if there were no interactions, then we
would look at these energy levels $\varepsilon_{r}$ (see Fig.
[1.33](#fig:fig1_5_5){reference-type="ref" reference="fig:fig1_5_5"},
right hand side), calculate this dimensionless quantity, $x_r$ and then
find the *Fermi function*, which is the mirror image of the sigmoid
function, $f_r=\sigma(-x_r)\equiv 1/(1+e^{x_r})$. The self consistent
field method defines an $\textit{interacting energy level}$
$\widetilde{\varepsilon}_r$, as if each of the bare energy levels
$\varepsilon_{r}$ gets raised by an amount that depends on how many
levels are filled and then proceeds as before applying the *Fermi
function* to the interacting levels $\widetilde{\varepsilon}_r$.

How do we calculate the $\widetilde{\varepsilon}_r$? The idea is that
every time there is an electron in some level $q$, it gives rise to an
interaction energy $U$ with the $r$th level. So what you have to do is
to add up these effects of all the occupied levels, except for itself
because no electron affects itself, only the others. So,the new levels
are given by
$[\widetilde{\varepsilon}_r=\varepsilon_r+\sum_{q\neq r}{Uf_q}]$.

So that's the idea. It sounds almost as simple as doing the
non-interacting case, but not quite, it's actually a little more
complicated and the reason is this. You see, when we didn't have this
interaction term, $[\widetilde{x}_r=x_r+\sum_{q\neq r}{(U/kT)f_q}]$, it
was straightforward. You calculate $x_r$, find the
$f_r=\sigma(-\widetilde{x}_r)$ and you have your answer. Now you see I
can't calculate $\widetilde{x}_r$ till I know $f_r$. So what I have to
do is I assume some $x_r$ and use it to calculate the $f_r$, but then I
use that $f_r$ to recalculate the $x_r$ and of course, it won't match
what I had started with, so what I do is, I take it, feed it back again,
again calculate $f_r$ and keep iterating till the result converges to a
self-consistent answer. So that's what is called the Self Consistent
Field Method which is widely used everywhere in condensed matter physics
and in device physics.

#### Fig. [1.34](#fig:fig1_5_6){reference-type="ref" reference="fig:fig1_5_6"} {#fig.-figfig1_5_6}

Now, this actually works quite well if the interaction isn't too large
(Fig. [1.34](#fig:fig1_5_6){reference-type="ref"
reference="fig:fig1_5_6"}). So for example, I mentioned earlier that
when $U/(kT) = 1$ I showed you results that the Boltzmann and the *Fermi
function* were not matching at all, but once you do the self consistent
method, they match reasonably well.

![Occupation factors and energy levels obtained from SCF method for the
problem considered in Fig. [1.30](#fig:fig1_5_2){reference-type="ref"
reference="fig:fig1_5_2"}.](./Week1_5/fig1_5_6.jpg){#fig:fig1_5_6
width="\\textwidth"}

You'll notice it's not exact and actually numerically if you check the
difference between these two distributions (see Fig.
[1.34](#fig:fig1_5_6){reference-type="ref" reference="fig:fig1_5_6"}),
there's about a $7\%$ difference, so it hasn't matched very well and if
$U$ were bigger, actually the discrepancy would also get bigger. But for
relatively small $U$ it works quite well and is, as I said, widely used
in this field.

#### Fig. [1.35](#fig:fig1_5_7){reference-type="ref" reference="fig:fig1_5_7"} {#fig.-figfig1_5_7}

Now, if you plot these $\widetilde{x}_rs$ then you'll get these red
levels the ones have shown here. So you might ask then well, in practice
when people draw energy levels, which ones do they really mean? Do they
mean the red ones or the black ones? The answer is that it's really the
red ones that you are drawing as if the interactions have already been
considered.

![Illustration of photo-emission method to determine energy
levels.](./Week1_5/fig1_5_7.jpg){#fig:fig1_5_7 width="\\textwidth"}

Now, how do we know that? Well consider how you actually measure the one
electron energy levels that we commonly use? You do what's called a
photo emission experiment (see Fig.
[1.35](#fig:fig1_5_7){reference-type="ref" reference="fig:fig1_5_7"}).
You hit it with light and see what photon energy is needed to knock the
electron out. The photon energy we need is the difference in the energy
between two configurations that are basically identical, except that in
one case the $r$-th level is filled and in the other case the $r$-th
level is empty.

What is the difference? It is equal not to the bare $\varepsilon_r$, but
to the interacting $\widetilde{\varepsilon}_r$. When I take out an
electron, I've also removed its interaction with all the other
electrons. So the difference bewteen the final and the initial energy
which the photon has to supply, is not just the bare level, but also
includes the interaction term,
$\widetilde{\varepsilon}_r=\varepsilon_r+\sum_{q\neq r}{Uf_q}$.

#### Fig. [1.36](#fig:fig1_5_8){reference-type="ref" reference="fig:fig1_5_8"} {#fig.-figfig1_5_8}

Now another way to think about it is well, what would you have expected
from Boltzmann Law? Consider the same two configurations which are
identical except that in one case one $r$ is not occupied , which we
call state 0, and in the other case $r$ is occupied, which we call
state 1. The ratio of their probabilities should equal
$(1-f_{r})/f_{r}$.

Boltzmann law gives the ratio of their probabilities as
$exp(-(E_0-\mu N_0)/kT)$ divided by $exp(-(E_1-\mu N_1)/kT)$ which we
have inverted and switched the minus to a plus to write as
$exp(+(E_1-\mu N_1)/kT)$ divided by $exp((E_0-\mu N_0)/kT)$. Now
$N_1 - N_0 = 1$, and we saw earlier that
$E_1 - E_0 = \widetilde{\varepsilon}_r$. Hence the probability ratio
from Boltzmann ratio is $exp((\widetilde{\varepsilon}_r-\mu)/kT)$ =
$exp(\widetilde{x}_r)$.

Equating the Boltzmann ratio $exp(\widetilde{x}_r)$ to
$(1-f_{r})/f_{r}$, a little algebra tells us that
$f_r = 1/(1+exp(\widetilde{x}_r))$, which is also the sigmoid function
of the negative, okay. So, Boltzmann law also kind of leads you to the
same idea that basically what you have are these interacting energy
levels and then you have to apply the Fermi function to the interacting
levels.

![Interacting energy levels from Boltzmann
law.](./Week1_5/fig1_5_8.jpg){#fig:fig1_5_8 width="\\textwidth"}

Finally one little thing: I assumed that the interaction between the
$q$-th electron and the $r$-th electron is aconstant $U$. In general,
what could happen is you could have different interactions between them
because levels $r$ and $q$ may be right next to each other, in which
case the interaction will be large, or they could be far away in which
case it would be small. So you can generalize it to put $U_{rq}$ instead
of just constant $U$ as shown on the lower right in Fig.
[1.36](#fig:fig1_5_8){reference-type="ref" reference="fig:fig1_5_8"}.

### Fig. [1.37](#fig:fig1_5_9){reference-type="ref" reference="fig:fig1_5_9"}: SCF and neural networks {#fig.-figfig1_5_9-scf-and-neural-networks}

![Similarity in expressions between SCF method and
neural-networks.](./Week1_5/fig1_5_9.jpg){#fig:fig1_5_9
width="\\textwidth"}

$Fig. \ref{fig:fig1_5_9}$ shows our SCF equations in pictorial form: Top
one is the sigmoid function and the bottom one is the summation. The
reason I'm drawing it this way is that we'll next be talking about
Boltzmann machines which are one kind of stochastic neural networks. In
the context of neural networks, you often see pictures just like this.
The sigmoid function is called the $neuron$ while the summation is
called the $synapse$.

But there is a $\bf{subtle}$ $\bf{difference}$. Remember that the Fermi
function $f_{r}$ is a number between 0 and 1 which gives us the average
occupation of a level, not the actual occupation which can only be
either 0 or 1. The SCF method treats $f_{r}$ as the actual occupation
and does not do justice to this point.

By contrast, in Boltzmann machines, the output of the neuron is not
$f_{r}$, but a binary number which is 0 with probability $1-f_{r}$ and
is 1 with probability $f_{r}$, just like the number of electrons in an
energy level. This extension of the SCF method leads us to the concept
of Gibbs sampling which we will see a lot of in the coming lectures. But
I am getting ahead of myself. Let us pick this up in Lecture 2.1.

### Quiz

#### Question 1

Consider a collection of 10 one-electron energy levels whose occupation
we can calculate in two ways: (1) using the general Boltzmann Law and
(2) using the self-consistent field method. How many probabilities do we
have to evealuate in each case?[^22]

#### Question 2

Consider four one-electron energy levels each of energy $\varepsilon$
having an interaction U for every pair of electrons. What is the total
energy of the state $\{0110 \}$?[^23]

#### Question 3

Consider four one-electron energy levels each of energy $\varepsilon$
having an interaction U for every pair of electrons. What is the total
energy of the state $\{0111 \}$?[^24]