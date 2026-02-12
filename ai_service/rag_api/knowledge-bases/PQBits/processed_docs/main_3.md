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

## Fig. [1.38](#fig:fig1_6_1){reference-type="ref" reference="fig:fig1_6_1"}: 5-minute summary {#fig.-figfig1_6_1-5-minute-summary}

This is [Chapter 1 summary: Watch youtube
video](https://www.youtube.com/watch?v=4j9ligUVrmk)

Welcome to a \"five minute\" summary of the last five lectures.

![Summary of Lectures 1.1-1.5.](./Week1_6/Picture1.6.png){#fig:fig1_6_1
width="\\textwidth"}

Well, we started in Lecture 1.1 by introducing the state space. You see,
usually we always draw this one electron space, but if you have $n$
states here, in state space you have $2^n$ states, which can be labeled
with binary numbers like this $[i:{1001\cdots}]$, where each digit tells
you whether one of these is occupied or empty. It's very important to be
clear about which space we are talking about, the $n$ space or the $2^n$
space. Boltzmann law is stated in terms of the latter. It is the central
law of equilibrium statistical mechanics, not to be confused with the
Boltzmann approximation to the Fermi function that you may have seen in
semiconductor courses.

In Lecture 1.2 we try to explain why this law is so general that it
applies to any system irrespective of its details. The reason is that
the law comes from a property of the reservoir, not the system. If the
system is in a lower energy state, then the reservoir has higher energy,
and because it has higher energy, it has many more states that are
accessible to it. So the chances of finding the system in a lower energy
is high because corresponding to it there are many more states of the
reservoir. This is the aspect that is captured through this function
$W(E,N)$, which tells you how many states are accessible, and the
logarithm of that is what's called the entropy, $S(E,N)=k\ln{W(E,N)}$.

In Lecture 1.3 explicitly evaluated the entropy (S), energy (E) and the
number of particles (N) in terms of the probabilities of occupation of
its different states represented by $\widetilde{p}_{i}$, where we have
introduced the $tilde$ to distinguish from the equilibrium probabilities
$p_{i}$ given by the Boltzmann law. So the expressions we obtain are
quite general, they apply to the system whether it's close to
equilibrium, at equilibrium, or totally out of equilibrium. But at
equilibrium with $\widetilde{p}_i=p_i$ we can relate the derivatives of
the entropy to the temperature T and the electrochemical potential
$\mu$.

To show this in Lecture 1.4, we introduced the concept of free energy,
which has a $minimum$ value of $-kT\ln{Z}$ at equilibrium, when the
probabilities $\widetilde{p}_i$ are actually equal to the equilibrium
probabilities $p_i$. A system not in equilibrium has a higher free
energy which it will lower as it comes to equilibrium. This also
corresponds to an increase in the total entropy of the system plus
reservoir.

And finally in Lecture 1.5, we talked about something different, namely
this self consistent field (SCF) method, which is widely used in
condensed matter physics and device physics. Boltzmann law works in this
$2^n$ space, which gets to be huge in a hurry. So it's important in
practical problems, to have a method that can be applied in $n$ space,
like the SCF method. But the real reason I have introduced it is that an
extension of this method leads us to the concept of Gibbs sampling that
we'll see much more of in the coming lectures when we get into neural
networks.

# Boltzmann Machines

## Sampling

This is [Lecture 2.1: Watch youtube
video](https://www.youtube.com/watch?v=MY2UPRDfZS4)

### Figs. [2.1](#fig:fig2_1_1){reference-type="ref" reference="fig:fig2_1_1"}-[2.4](#fig:fig2_1_6){reference-type="ref" reference="fig:fig2_1_6"}: From $f$ to $n$ {#figs.-figfig2_1_1-figfig2_1_6-from-f-to-n}

#### Figs. [2.1](#fig:fig2_1_1){reference-type="ref" reference="fig:fig2_1_1"}: Recap {#figs.-figfig2_1_1-recap}

![Boltzmann law and the self-consistent field
method](./Week2_1/Picture1.png){#fig:fig2_1_1 width="\\textwidth"}

Now, in Chapter 1, as you may recall (see Fig.
[2.1](#fig:fig2_1_1){reference-type="ref" reference="fig:fig2_1_1"}), we
were generally talking about the basic principles of equilibrium
statistical mechanics starting from the Boltzmann law:
$p_i=(1/Z)\exp{(-(E_i-\mu N_i)/kT)}$. We noted that this law operates in
the space with $2^n$ states, which increases exponentially with $n$
often making it impractical to use.

At the end in Lecture 1.5 we introduced what's called the self
consistent field ($\bf{SCF}$)method, where you have these two equations,
$f_r=\sigma(-\widetilde{x}_r)$ and
$\widetilde{x}_r=x_r+\sum_{q}{(U_{rq}/kT)}f_q$, that you can solve self
consistently to obtain the equilibrium probabilities. This self
consistent field method operates in the $n$ space, which is a much
smaller space and hence much more practical. However, it is kind of
approximate. I gave you an example where the error was $7\%$, and it
could be less or more depending on the parameters in the problem.

#### Fig. [2.2](#fig:fig2_1_3){reference-type="ref" reference="fig:fig2_1_3"}: Replace f with n {#fig.-figfig2_1_3-replace-f-with-n}

Now what I'll be describing to you in this lecture may look like a minor
modification of the self-consistent field method, but it goes way beyond
that, the full significance of which will only be evident after we talk
about Markov chain Monte Carlo and transition matrices in Chapter 3. For
the moment let me just say that the Boltzmann result can be written as a
sum over an exponentially large number of $\textit{'Feynman paths'}$. An
exact evaluation is impractical, but depending on the problem at hand it
is often possible to obtain accurate results with far fewer paths
sampled using appropriate sampling algorithms. The basic idea is not
unlike that of predicting an election from an exit poll of only a few
voters sampled from a much larger population. But as we know, from time
to time such predictions fail badly too!

Interestingly the \"minor\" modification I am talking about leads to a
very popular sampling algorithm known as Gibbs sampling. The
modification involves replacing the Fermi function $f$ with a binary
variable $n$ (see Fig. [2.2](#fig:fig2_1_3){reference-type="ref"
reference="fig:fig2_1_3"}), which we could view as the number of
electrons, that can only be 0 or 1: you can't really have half an
electron. What the Fermi function tells us is the probability that it's
1.

To obtain $n$ we can use a random number generator to generate a random
number, $R_{0,1}$, uniformly distributed in the window between 0 and 1.
If that random number happens to be less than f, that's to the left,
then we choose $n_{r}=1$. Otherwise we choose $n=0$. That way, the
probability of $n$ being 1 is proportional to $f_r$ whereas the
probability of $n_{r}$ being 0 is proportional to $1-f_r$.

Mathematically we can write $n_r = \vartheta (f_r-R_{0,1})$. Suppose
$f_{r}$ is $0.5$, then $f_r-R_{0,1}$ will be positive $50\%$ of the
time, so that the step function $\vartheta$ gives 1 for $n_r$. The other
$50\%$ of samples will give $n_{r}=0$ since $f_r-R_{0,1}$ will be
negative. So we have a sequence of roughly equal number of 0's and 1's.
But if $f_{r} = 0.9$ then $f_r-R_{0,1}$ will be positive $90\%$ of the
time making $n_r = 1$. $n_r$ will be zero only $10\%$ of the time as
shown.

![From $f$ to $n$](./Week2_1/figure4.jpg){#fig:fig2_1_3
width="\\textwidth"}

#### Fig. [2.3](#fig:fig2_1_5){reference-type="ref" reference="fig:fig2_1_5"} {#fig.-figfig2_1_5}

![Replace $f$ with $n$](./Week2_1/Picture6.png){#fig:fig2_1_5
width="\\textwidth"}

What we are going to do then is to take the self consistent field from
Chapter 1 and replace the $f$'s with $n$'s (see Fig.
[2.3](#fig:fig2_1_5){reference-type="ref" reference="fig:fig2_1_5"}).
We'll add this equation $n_r=\vartheta\left(f_r-R_{0,1}\right)$ which
chooses the binary variable $n_{r}$ according to the Fermi function
$f_r=\sigma(-\widetilde{x}_r)$. That's what is called a $\bf{binary}$
$\bf{stochastic}$ $\bf{neuron}$ in the machine learning literature. We
will generally refer to it as a probabilistic or a $\bf{p}$-$\bf{bit}$
to contrast it with the qubits of quantum computing to be discussed in
Chapters 4 amd 5.

For the self consistent field equation,
$\widetilde{x}_r=x_r+\sum_{q}{(U_{rq}/kT)}f_q$, we replace $f_q$ with
$n_q$. We also replace $U_{rq}/kT$ with a dimensionless number $w_{rq}$
since we will not be modeling physical systems with interaction energy
and thermal energy any more. Just an abstract system with a weight logic
$w_{rq}$ that defines what is called the $synapse$
$\widetilde{x}_r=x_r+\sum_{q}{w_{rq}}n_q$ in the machine learning
literature.

#### Fig. [2.4](#fig:fig2_1_6){reference-type="ref" reference="fig:fig2_1_6"}: Generating samples {#fig.-figfig2_1_6-generating-samples}

![Generating samples](./Week2_1/Picture7.png){#fig:fig2_1_6
width="\\textwidth"}

With this replacement then our self consistent field method morphs into
a sampling method (see Fig. [2.4](#fig:fig2_1_6){reference-type="ref"
reference="fig:fig2_1_6"}). We start with a set of initial samples
$n_{r}$, representing the state of all the neurons, calculate $x$, then
use that $x$ to generate this Fermi function
$f_r=\sigma(-\widetilde{x}_r)$, which is then used to update all neurons
giving us a new set of samples. Keep doing this and thereby you'd be
generating a entire series of samples of the states of the neurons. If
you use those time samples to generate a histogram, then you get the
Boltzmann probabilities that you're looking for.

### Figs. [2.5](#fig:fig2_1_7){reference-type="ref" reference="fig:fig2_1_7"}-[2.8](#fig:fig2_1_11){reference-type="ref" reference="fig:fig2_1_11"}: Synapse from interaction energy {#figs.-figfig2_1_7-figfig2_1_11-synapse-from-interaction-energy}

#### Figs. [2.5](#fig:fig2_1_7){reference-type="ref" reference="fig:fig2_1_7"} {#figs.-figfig2_1_7}

As you may recall, the synapse function
$\widetilde{x}_r=x_r+\sum_{q}{w_{rq}}n_q$ (see Fig.
[2.5](#fig:fig2_1_7){reference-type="ref" reference="fig:fig2_1_7"})
came from the interaction energy. So the idea was that these electrons
had a pairwise interaction energy of $U_{rq}$ between the electron, $r$,
and the electron, $q$ and this $w$ is that interaction energy normalized
to $kT$. Let us try to get a deeper understanding of the synaptic
function by delving a little more into this connection with the
interaction energy.

![Synapse from Interactions](./Week2_1/Picture8.png){#fig:fig2_1_7
width="75%"}

#### Fig. [2.6](#fig:fig2_1_8){reference-type="ref" reference="fig:fig2_1_8"}: {#fig.-figfig2_1_8}

I'd mentioned earlier that one way of thinking of this self consistent
potential (see Fig. [2.6](#fig:fig2_1_8){reference-type="ref"
reference="fig:fig2_1_8"}), is to consider how much the normalized
interaction energy ($\widetilde{E} \equiv E/kT$) would change if $n_r$
were to change from 1 to 0:
$\widetilde{x}_r=\widetilde{E}(n_r=1)-\widetilde{E}(n_r=0)$, which you
could write as $\partial\widetilde{E}/\partial n_r$.

That's not generally true though, but it's true if it's a linear
function like say $\widetilde{E}=10n_r$. Now the thing is, in this
context, we'll always be dealing with linear functions. Why is that?
Well, because $n_r$ is a binary variable, it's either 0 or 1. And as
such it has the property that you can raise it to any power, and it's
basically the same variable since $0^2= 0$, $1^2=1$. So basically,
$n_r^k$ is really the same as $n_r$, k being any real number.

One other point, that in our discussions last week we had often made the
distinction between $E$ and $E- \mu N$, but going forwards, we'll just
write this normalized quantity, as $\widetilde{E}$, and we won't make
these distinctions anymore.

![Synapse from Interactions
(contd.)](./Week2_1/Picture9.png){#fig:fig2_1_8 width="\\textwidth"}

#### Fig. [2.7](#fig:fig2_1_10){reference-type="ref" reference="fig:fig2_1_10"}: {#fig.-figfig2_1_10}

Now, often the interactions are what you might call quadratic (see Fig.
[2.7](#fig:fig2_1_10){reference-type="ref" reference="fig:fig2_1_10"}),
in the sense you have pairwise interactions, that is between $n_r$ and
$n_q$. In that case, when you take the derivative, the synapse function
will be linear. On the other end in general, you could have higher order
interactions. You could have a three body interactions, involving $n_r$,
$n_q$, $n_s$. In which case the synapse function would involve quadratic
terms, but most of the time people deal with this quadratic interactions
and linear synapses. So we often write the linear version
$\widetilde{x}_r=x_r+\sum_{q}{w_{rq}}n_q$, but more generally, of
course, you could have a more higher order interactions and in that
case, you should find the synapse from the derivative.

![Synapse from Interactions
(contd.)](./Week2_1/Picture11.png){#fig:fig2_1_10 width="95%"}

#### Fig. [2.8](#fig:fig2_1_11){reference-type="ref" reference="fig:fig2_1_11"}: A simple code {#fig.-figfig2_1_11-a-simple-code}

Okay, next, if you actually want to solve a particular problem and
generate these samples (see Fig.
[2.8](#fig:fig2_1_11){reference-type="ref" reference="fig:fig2_1_11"}),
it is relatively easy to write down a code. Here's a MATLAB^®^ code that
will do exactly what is stated on the right hand side. I have also tried
to write down the Python version of the same code. If you want to try
out on your own, you could do that.

![Codes](./Week2_1/Picture12.png){#fig:fig2_1_11 width="95%"}

### Figs. [2.9](#fig:fig2_1_12){reference-type="ref" reference="fig:fig2_1_12"}-[2.15](#fig:fig2_1_18){reference-type="ref" reference="fig:fig2_1_18"}: Toy example {#figs.-figfig2_1_12-figfig2_1_18-toy-example}

#### Fig. [2.9](#fig:fig2_1_12){reference-type="ref" reference="fig:fig2_1_12"}: Solution, the Boltzmann way {#fig.-figfig2_1_12-solution-the-boltzmann-way}

![Toy Example](./Week2_1/Picture13.png){#fig:fig2_1_12 width="75%"}

Now what we'll do in the rest of this lecture is to go through what you
might call a toy example (see Fig.
[2.9](#fig:fig2_1_12){reference-type="ref" reference="fig:fig2_1_12"}).
So we don't really need a computer to do this, we could just do it on
paper, as we'll be doing in the next few slides. So consider a problem
with two neurons or two energy levels, 1 and 2, and whose energy levels
are below their chemical potentials. So, $E-\mu$ is, like $-1$ and so
our energy function is $-n_1-n_2$. So you could make up the set of
energies for all the state space levels. The state space, it could be
$\{00\}$, $\{0 1\}$, $\{1 0\}$, and $\{1 1\}$ and corresponding to that,
the energies would be $0$, $-1$, $-1$ and $-2$ and we can now use this
to find the probabilities using the general Boltzmann law. Now, if we
add interactions, so supposing there is a term that's like $2n_1n_2$,
that's an interaction term. So, how will that change this table of
energies? Well, the first three are not affected at all because $n_1n_2$
is 0. Only the last one changes, where we add a $+2$ and so these two
add to give me 0. So finally we get a table like this, where $\{0 0\}$
and $\{1 1\}$, both have an energy of 0 whereas $\{0 1\}$, and
$\{1 0\}$, have a lower energy, which is $-1$.

#### Fig. [2.10](#fig:fig2_1_13){reference-type="ref" reference="fig:fig2_1_13"}: {#fig.-figfig2_1_13}

So Boltzmann law, then tells me that the probabilities will be
proportional to $e^{0}=1$, $e^{0}=1$, and then $e^{1}=2.7$, $e^{1}=2.7$.
So the probabilities of the system being in these four states is
proportional to $[1 \ 1 \ 2.7 \ 2.7]$ respectively. The actual
probabilities are obtained by normalizing them such that they add up to
1: $[1 \ 1 \ 2.7 \ 2.7]./7.4$ (see Fig.
[2.10](#fig:fig2_1_13){reference-type="ref" reference="fig:fig2_1_13"}).

![Toy Example](./Week2_1/figure14.jpg){#fig:fig2_1_13
width="\\textwidth"}

Moving on, if let's say we multiply this energy function by a factor of
10. Well, then what happens is that the 0's still remain 0's, but the
-1's now become -10. And so now when we look at the probabilities. What
we'll find is that, $\{0 1\}$ and $\{1 0\}$ have a much bigger
probability proportional to $e^{10}$. If you now draw the histogram,
you'd see just two peaks with the other two strongly suppressed. In
physical systems the normalized energy function $\widetilde{E}=E/kT$
increases when we lower the temperature and this is just what you see:
at higher temperatures things tend to be relatively, uniformly
distributed probability wise. At lower temperatures they tend to lock
into the lowest energy states.

#### Fig. [2.11](#fig:fig2_1_14){reference-type="ref" reference="fig:fig2_1_14"}: How NOT to sample {#fig.-figfig2_1_14-how-not-to-sample}

Now in the next few slides, I just want to explain how you'd get the
same answers from the sampling method (see Fig.
[2.11](#fig:fig2_1_14){reference-type="ref" reference="fig:fig2_1_14"}).
First let us look at a sampling method that does not work.

![How NOT to sample](./Week2_1/figure15.jpg){#fig:fig2_1_14
width="\\textwidth"}

Say we start with both states empty, at $\{0 0\}$. Okay, so next we
calculate this synaptic function, and we get $-10$ for each one. Okay,
so now if it's $-10$, then when we calculate the Fermi function, it
tells us that both states must be occupied, so we fill them both up to
get $\{1 1\}$. But once both are occupied, with $n_1=1$ and $n_2=1$, the
synaptic functions are $+10$ and $+10$, which then tells you that both
states must be unoccupied, taking us back to $\{0 0\}$. Now if you try
again, you're back to the old situation, so now you again predict that
the next state should be $\{1 1\}$. So this clearly isn't working
because from Boltzmann, you expect $\{0 1\}$ and $\{1 0\}$ to be high
probability, while this seems to be just oscillating between $\{0 0\}$
and $\{1 1\}$.

#### Fig. [2.12](#fig:fig2_1_15){reference-type="ref" reference="fig:fig2_1_15"}: Solution by sampling {#fig.-figfig2_1_15-solution-by-sampling}

Where did we go wrong? We were updating both $p$-$bits$ simultaneously.
What you need to do is update them one by one (see Fig.
[2.12](#fig:fig2_1_15){reference-type="ref" reference="fig:fig2_1_15"}),
and then it will work. So the way it would work then is, start with
$\{0 0\}$ so it tells you that they should both be filled, but we don't
fill both of them, we just do one of them. update the synaptic function,
and then go to the next $p$-$bit$.

So let's say we update only the first $p$-$bit$ to get $\{1 0\}$ instead
of $\{1 1\}$. Then when we recalculate the synaptic functions,
$\widetilde{x}_2$ goes from $-10$ to $+10$, telling me to keep $p$-$bit$
2 at 0. On the other hand, $\widetilde{x}_1$ remains $-10$ because I've
only changed $n_1$, I have not changed $n_2$, telling me to keep
$p$-$bit$ 1 at 1. So the system gets stuck in $\{1 0\}$ thereafter.

If we go back to our physical picture with electrons occupying two
levels, it is as if the presence of an electron in level 1 has raised
level 2 way up making it empty. But level 1 itself hasn't changed
because the electron doesn't feel anything due to itself. And so it
stays full and $\{1 0\}$ represents a self-consistent state that the
system locks into.

![How to sample](./Week2_1/figure16.jpg){#fig:fig2_1_15
width="\\textwidth"}

#### Fig. [2.13](#fig:fig2_1_16){reference-type="ref" reference="fig:fig2_1_16"}: {#fig.-figfig2_1_16}

But wait a minute. Why did the system lock into $\{1 0\}$ and not
$\{0 1\}$. That too would be a self-consistent state with level 2 filled
($n_2=1$) and level 1 empty ($n1=0$). Well if we had updated neuron 2
first the system would indeed have locked into $\{0 1\}$ instead of
$\{1 0\}$ as shown in Fig. [2.13](#fig:fig2_1_16){reference-type="ref"
reference="fig:fig2_1_16"}.

![How to sample](./Week2_1/figure17.jpg){#fig:fig2_1_16 width="90%"}

#### Fig. [2.14](#fig:fig2_1_17){reference-type="ref" reference="fig:fig2_1_17"}: {#fig.-figfig2_1_17}

So the bottom line is that simultaneously updating two $p$-$bits$ that
are interconnected synaptically does not work. But if you update
sequentially, what you'd find is that the system locks into one of two
$self$-$replicating$ states (see Fig.
[2.14](#fig:fig2_1_17){reference-type="ref" reference="fig:fig2_1_17"}).
That is once you get into one of them, you just stay there, you don't
move and that's why when you create a histogram, you'll see large peaks
corresponding to these $\{1 0\}$ and $\{0 1\}$. Whereas if you start in
any of the other ones like $\{0 0\}$ or $\{1 1\}$, you get out of it
right away.

But why do I see two peaks? Shouldn't we see one or the other? Indeed
that is true if $E_0$ is large making the synaptic functions like
$\pm 10$ as we assumed in our discussion. In practice you don't want
this $E_0$ to be too big, you want it something intermediate, so that
the synaptic functions are smaller like say $\pm 2$. In that case
neither $\{10\}$ nor $\{01\}$ is firmly locked in, and each has a
reasonable chance to go over to one of the low probability states
$\{00\}$ or $\{11\}$ and then transition over to the other high
probability state. That way, you can pick up both peaks as you draw more
and more samples.

![Self-replicating
states](./Week2_1/Self-replicating.jpg){#fig:fig2_1_17
width="\\textwidth"}

#### Fig. [2.15](#fig:fig2_1_18){reference-type="ref" reference="fig:fig2_1_18"}: Sampling method, key points {#fig.-figfig2_1_18-sampling-method-key-points}

![Sampling method, key points](./Week2_1/Picture19.png){#fig:fig2_1_18
width="\\textwidth"}

Fig. [2.15](#fig:fig2_1_18){reference-type="ref"
reference="fig:fig2_1_18"} tries to summarize our discussion regarding
the sampling method. The key message is that this method will reproduce
the Boltzmann law (see Fig. [2.15](#fig:fig2_1_18){reference-type="ref"
reference="fig:fig2_1_18"}), as long as you update
$\textit{synaptically connected}$ $p$-$bits$ sequentially, and not
simultaneously. It is also important to avoid large values of $E_0$
which could lock the system into a subset of all the states.

### Quiz

#### Question 1

What is the relation between the Fermi function $f_r$ and the electron
number $n_r$?[^25]

#### Question 2

If the energy of a system of three levels is given by
$\widetilde{E} = x_3 n_3 + n_1 n_2 n_3$\
what is the the synaptic output driving level 3?[^26]

#### Question 3

If the energy of a system with two levels is given by
$\widetilde{E} = 2 n_1 n_2 - n_1 - n_2$\
which states have the highest probability?[^27]

## Orchestrating Interactions

This is [Lecture 2.2: Watch youtube
video](https://www.youtube.com/watch?v=SzL0vkGMJLs)

As you may recall, in the last lecture, we introduced the sampling
method which works in $n$ space, but it allows us to analyze the
response in the huge $2^n$ space. Now, just to remind you what I mean by
$n$ space and $2^n$ space: $n$ represents the number of binary
stochastic neurons or $p$-$bits$, and $2^n$ tells you, how many
configurations they represent and the Boltzmann law, gives us the
probability of each configuration in this $2^n$ space. But $2^n$, can be
a huge number and so the sampling method is really very attractive since
it allows us to work in the $n$ space and yet give accurate results for
the probability distribution, in the $2^n$ space.

As an example we had talked about a system with just two $p$-$bits$. And
that means, $n=2$, $2^n=4$ which is no big deal. This was meant to be
toy example, to just illustrate the principles. Now, what we will do
first is to generalize this a little bit. Then we will try to get a
feeling for how the interactions in $n$ space affect and control the
probability response in $2^n$ space.

### Figs. [2.16](#fig:fig2_2_3){reference-type="ref" reference="fig:fig2_2_3"}-[2.20](#fig:fig2_2_9){reference-type="ref" reference="fig:fig2_2_9"}: Generalizing the toy model {#figs.-figfig2_2_3-figfig2_2_9-generalizing-the-toy-model}

#### Figs. [2.16](#fig:fig2_2_3){reference-type="ref" reference="fig:fig2_2_3"} {#figs.-figfig2_2_3}

![Generalizing the two $p$-$bit$ energy expression to arbitrary number
of $p$-$bits$](./Week2_2/figure2.jpg){#fig:fig2_2_3 width="\\textwidth"}

Earlier we had just two $p$-$bits$, so it was easy to write out the
energy expression. There were just a few terms in there. But in general,
if we had say 10 $p$-$bits$ then we would be just writing forever. So to
write it in a compact way, what you could do is use these summations
$\widetilde{E}=\sum_{r}{n_rx_r}+\sum_{r,q}{n_rw_{rq}n_q}$. So for
example, what I've written here,
$\widetilde{E}=\sum_{r}{n_rx_r}+\sum_{r,q}{n_rw_{rq}n_q}$, is a
generalization of what was done earlier for just two $p$-$bits$. To see
this you can write out all the terms in the summation, assuming that
there are only two $p$-$bits$ so that the indices $r$ and $q$ each take
on just two values 1 and 2. You can see that we get our old expression
$\widetilde{E}=-n_1-n_2+2n_1n_2$ if we set $x_1=1$, $x_2=1$ and
$w_{11}=0$, $w_{12}=+2$, $w_{21}=+2$, $w_{22}=0$.

#### Fig. [2.17](#fig:fig2_2_4){reference-type="ref" reference="fig:fig2_2_4"}: {#fig.-figfig2_2_4}

Now, what we'll do is describe to you something that's even more compact
using matrix notation as shown in Fig.
[2.17](#fig:fig2_2_4){reference-type="ref" reference="fig:fig2_2_4"}. So
the idea is that we could write $\sum_{r}{n_rx_r}$ in the form of a row
vector $\{n_1 \ n_2 \ \cdot \cdot \}$ times a column vector
$\{x_1 \ x_2 \ \cdot \cdot \}^{T}$, which in matrix notation becomes
$n^{T}x$. Similarly the term $\sum_{r,q}{n_rw_{rq}n_q}$ in matrix
notation becomes $n^Twn$ as shown.

![Matrix Notation](./Week2_2/Picture1.jpg){#fig:fig2_2_4
width="\\textwidth"}

#### Fig. [2.18](#fig:fig2_2_6){reference-type="ref" reference="fig:fig2_2_6"}: Four level example {#fig.-figfig2_2_6-four-level-example}

In general, the energy function $\widetilde{E} = n^T x + (1/2) n^T w n$
is defined by two parameters $x$ and $w$: $x$ is a column vector,
sometimes called the bias, and $w$ is what's called the weight matrix.

So for example (see Fig. [2.18](#fig:fig2_2_6){reference-type="ref"
reference="fig:fig2_2_6"}), if you had four $p$-$bits$, then $x$ would
be a $4 \times 1$ column vector and $w$ would be a $4 \times 4$ matrix.
So what would the response look like? I have plotted it in Fig.
[2.18](#fig:fig2_2_6){reference-type="ref" reference="fig:fig2_2_6"}
with two $p$-$bits$ on one axis, and the other two on another axis. And
we plot the probability along the vertical axis, the third one. Of
course we could have just written all four neurons in one line, but then
we'd have 16 points along that line. Instead we have written it in a two
dimensional matrix, 4 of them on one side, and 4 on the other side.

![Four Levels with all-to-all
interactions](./Week2_2/Picture5a.png){#fig:fig2_2_6
width="\\textwidth"}

Now, if we actually put down those numbers and solve it, what you'd see
is four peaks, corresponding to the lowest energy states. Which ones are
they? As you can see from the plot they are $\{0010\}$, $\{0001\}$,
$\{0100\}$, and $\{1000\}$. In terms of our physical picture of energy
levels filled with electrons, these all represent states having just one
electron, so that only one of the four is 1, rest are zero. Why don't we
have states with two, three or four electrons? Because of this strong
interaction term, $w$, what happens is if you try to put more than one
electron the energy becomes too high because of the interaction. Why not
eliminate electrons altogether and go to the $\{0000\}$ state? Then you
do not take advantage of the bias $x_r=-1$. Anytime you put in an
electron, there's an energy term like an $n_1x_1$ or an $n_2x_2$, which
are negative, so they give rise to a lower energy. So finally, the
lowest energy states are those which have one electron, but that one
electron could be in any one of the levels.

#### Fig. [2.19](#fig:fig2_2_7){reference-type="ref" reference="fig:fig2_2_7"}: {#fig.-figfig2_2_7}

Now, what happens if I, let's say (see Fig.
[2.19](#fig:fig2_2_7){reference-type="ref" reference="fig:fig2_2_7"}),
only keep nearest neighbor interactions? So what I've done is taken out
the 2's from the intercation matrix $[w]$, when they're far from the
diagonal, and I'm only keeping the upper diagonal and the lower
diagonal, rest are all set to zero. And physically that would correspond
to, electrons only interacting with electrons next to them, but not if
they're far away.

Now the lowest energy states are those having two electrons but not in
contiguous levels. There are three such configurations: $\{1001\}$,
$\{0101\}$ and $\{1010\}$.

![Four Levels with nearest neighbor
interactions](./Week2_2/Picture5b.png){#fig:fig2_2_7
width="\\textwidth"}

Now, what would happen if I take off one of the bias terms, namely the
one for Level 2, so that $x=\{-1 \ 0 \ -1 \ -1\}^T$? One of the three
peaks in Fig. [2.19](#fig:fig2_2_7){reference-type="ref"
reference="fig:fig2_2_7"} would be eliminated, namely the one having an
electron in Level 2. That would leave only two peaks: $\{1001\}$ and
$\{1010\}$.

#### Fig. [2.20](#fig:fig2_2_9){reference-type="ref" reference="fig:fig2_2_9"}: {#fig.-figfig2_2_9}

Fig. [2.20](#fig:fig2_2_9){reference-type="ref"
reference="fig:fig2_2_9"}), summarizes the four combinations of
different $x$'s and $w$'s that we just discussed. My main point is that
the parameters $\{x\}$ and $[w]$ in $n$ space control the response in
the $2^n$ state space. In these simple examples you can understand the
results in terms of a physical picture that views $p$-$bits$ as energy
levels that can be full (1) or empty (0).

![Four Levels: Summary](./Week2_2/Picture2.png){#fig:fig2_2_9
width="\\textwidth"}

### Figs. [2.21](#fig:fig2_2_11){reference-type="ref" reference="fig:fig2_2_11"}-[2.23](#fig:fig2_2_14){reference-type="ref" reference="fig:fig2_2_14"}: From natural to orchestrated interactions {#figs.-figfig2_2_11-figfig2_2_14-from-natural-to-orchestrated-interactions}

#### Figs. [2.21](#fig:fig2_2_11){reference-type="ref" reference="fig:fig2_2_11"}: {#figs.-figfig2_2_11}

Next what we want to do is kind of change our approach a little bit. You
see, so far, as you know, we are coming from this Boltzmann law and
equilibrium statistical mechanics where the objective is to understand
nature, and nature gave us certain $x$'s and $w$'s with the interaction
coming from *Coulomb interaction* between electrons. So it's the natural
interaction that dictates it and the objective was, well, how do I
analyze the state space response that I get?

Going forward (see Fig. [2.21](#fig:fig2_2_11){reference-type="ref"
reference="fig:fig2_2_11"}), we will want a particular state space
response, in order to solve a certain problem. There is some application
that requires us to solve some problem, and that's what the state space
response is supposed to do for us. Now the question is what kind of $x$
and $w$ will get us there? So $x$ and $w$ are no longer things that
nature gives us. It's something that we have to figure out so that it
gives us a particular state space response. So a complete reversal of
which comes first and which comes next.

![Change in approach](./Week2_2/Picture3.png){#fig:fig2_2_11
width="\\textwidth"}

#### Fig. [2.22](#fig:fig2_2_13){reference-type="ref" reference="fig:fig2_2_13"}: Software implementation {#fig.-figfig2_2_13-software-implementation}

But then you might ask, well, supposing I figured out $x$ and $w$? How
will I implement them? The answer is straightforward if you're doing all
this in software: we can implement any $x$ and $w$. For example (see
Fig. [2.22](#fig:fig2_2_13){reference-type="ref"
reference="fig:fig2_2_13"}), as I mentioned in this method, you could
write a MATLAB^®^ code or a Python code to simulate all this. So there
will be a line which says okay, this is how you find these $x$'s. You
use the $x$ and $w$ to figure out the next state of the neurons. Then
you can put in any $x$ and any $w$ you want, we are not restricted by
the physics of anything.

![Software Implementation](./Week2_2/Picture5.png){#fig:fig2_2_13
width="90%"}

#### Fig. [2.23](#fig:fig2_2_14){reference-type="ref" reference="fig:fig2_2_14"} {#fig.-figfig2_2_14}

![Changing n to s](./Week2_2/Picture4.png){#fig:fig2_2_14 width="90%"}

So in this approach, in software, we view $n$ as just a binary variable.
And just to keep this in mind (see Fig.
[2.23](#fig:fig2_2_14){reference-type="ref" reference="fig:fig2_2_14"}),
what I'll do going forwards is instead of $n$ I'll write $s$, just a
change in symbol. I mean, $n$ had two values, 0 and 1, same is true for
$s$, it also has two values, 0 and 1. That's, it. It's just that $n$ has
this connotation of being the number of electrons in a particular level
which I'd used to motivate it when we got started, but going forwards
we'll just write as it as a binary variable it $s$. So the equations are
exactly what I had before, but now instead of $n$ I've written $s$,
that's all, $\widetilde{E}=(s^{\rm T}x+(1/2)s^{\rm T}ws)E_0$.

### Figs. [2.24](#fig:fig2_2_16){reference-type="ref" reference="fig:fig2_2_16"}-[2.25](#fig:fig2_2_17){reference-type="ref" reference="fig:fig2_2_17"}: p-bits and q-bits {#figs.-figfig2_2_16-figfig2_2_17-p-bits-and-q-bits}

#### Figs. [2.24](#fig:fig2_2_16){reference-type="ref" reference="fig:fig2_2_16"}: {#figs.-figfig2_2_16}

One more thought before we move on. We started with the electron number
$n$ to motivate the concept of a $\textit{binary stochastic neuron}$ or
a $p$-$bit$ and then replaced it with a binary variable $s$ not tied to
any specific physical representation, noting that we will be
implementing all in software anyway. The strength of a software
implementation is its generality, it can implement any $\{x\}$, $[w]$
and even more complicated energy functions that may not have simple
analytical expressions.

On the other hand there is a lot of interest in
$\textit{hardware accelerators}$ that take advantage of appropriate
hardware to implement computational steps in a fast and energy-efficient
manner. And so it is of practical interest to ask what physical hardware
could represent a $p$-$bit$. In any case physical representations can be
useful in providing intuitive physical pictures.

We have already seen one physical representation for $p$-$bits$, namely
an energy level that can be filled (1) or empty (0). Another possibility
is the basis of MRAM[^28] technology, namely nanomagnets which represent
1 or 0 depending on whether the north pole is upwards or downwards. For
memory devices stable magnets are desirable, magnets that stay 1 or 0
for a very long time. But a well-known problem with nanomagnets is that
as you make them smaller they become unstable and tend to fluctuate
between 0 and 1. This is bad for memory applications, but perfect for
implementing a $p$-$bit$.

However, in order to be useful as a hardware accelerators, the challenge
is to design a complete device that can take an analog input
$\widetilde{x}$ as input and produce a binary output which is 1 with
probability $\sigma(-\widetilde{x})$.

![Physical Representation of
$p$-$bits$](./Week2_2/Picture7.png){#fig:fig2_2_16
width=".8\\textwidth"}

![$p$-$bits$ and q-bits](./Week2_2/Picture8.png){#fig:fig2_2_17
width="85%"}

#### Fig. [2.25](#fig:fig2_2_17){reference-type="ref" reference="fig:fig2_2_17"}: {#fig.-figfig2_2_17}

Now this nanomagnet representation for a $p$-$bit$ is kind of nice
because it naturally morphs over into a $\textit{q-bits}$ which we will
talk about in the quantum part of this course (see Fig.
[2.25](#fig:fig2_2_17){reference-type="ref" reference="fig:fig2_2_17"}).
You see nanomagnets are actually composed of lots of elemental magnets
which have all lined up because of certain internal interactions. Now,
what are these elementary magnets?

The basic elemental magnet is the electron itself. We all know that an
electron carries a charge, but it also carries a magnetic moment and
often pictorially you think of it as spinning, as if you have a spinning
charge which gives rise to a circulating current that is giving you a
magnetic field. However, these electrons, this elemental magnet is
actually a quantum magnet and that requires a conceptual change from
where we are, that's what we'll try to do in the last two chapters.

But for the moment, we will stick to classical spins that you could
visualize as classical magnets and try to understand the behavior of
$p$-$bit$ networks. We believe this provides a perfect backdrop for
understanding q-bit networks. Indeed that is why we use the word
$p$-$bit$ to contrast with $q$-$bits$ that are the building blocks of
quantum hardware.

### Quiz

If the energy of a system of four levels is given by
$\widetilde{E} = \big(n^T x + 0.5 \ n^T w n \big) \times E_0$ where
$x = \left \{ \begin{array}{r}
-1 \\
-1 \\
-1 \\
-1 \ \\
\end{array} \right \}$ and $w = \left [ \begin{array}{r r r r}
0 & \ 2 & \ 0 & \ 0 \\
2 & \ 0 & \ 2 & \ 0 \\
0 & \ 2 & \ 0 & \ 2 \\
0 & \ 0 & \ 2 & \ 0 \\
\end{array} \right ]$\

#### Question 1

what is the synaptic output driving level 4?[^29]

#### Question 2

what are the states with the highest probability?[^30]

## Optimization

This is [Lecture 2.3: Watch youtube
video](https://www.youtube.com/watch?v=7TDkwrnER-o)

In the last lecture we showed that the $n \times 1$ bias vector $\{x\}$
and the $n \times n$ weight matrix $[w]$ control the response in $2^n$
state space. In this lecture we will see how we can design $\{x\}$ and
$[w]$ so that the state space response actually does something useful
for us. The problem we'll consider (see Fig.
[2.26](#fig:fig2_3_1){reference-type="ref" reference="fig:fig2_3_1"}),
graph partitioning, is an example of a very broad class of problems that
you could call constrained optimization.

### Figs. [2.26](#fig:fig2_3_1){reference-type="ref" reference="fig:fig2_3_1"}-[2.27](#fig:fig2_3_2){reference-type="ref" reference="fig:fig2_3_2"}: Graph partitioning {#figs.-figfig2_3_1-figfig2_3_2-graph-partitioning}

#### Fig. [2.26](#fig:fig2_3_1){reference-type="ref" reference="fig:fig2_3_1"}: {#fig.-figfig2_3_1}

Let's say there are six nodes, having some connections between them
described by the connection matrix $[C]$. The connections are
bi-directional in the sense that $C_{12}$ is the same as $C_{21}$.

Now the min-cut problem would be, how do I take these six nodes and
break it up into two groups so that they are as weakly connected as
possible between the two groups? So the groups may have internal
connections, but there should be very little connection between one
group and the other. The reverse problem, that's your max-cut problem,
that is how do you divide them so that the connections are as strong as
possible.

![Graph partitioning](./Week2_3/figure1.jpg){#fig:fig2_3_1
width="\\textwidth"}

#### Fig. [2.27](#fig:fig2_3_2){reference-type="ref" reference="fig:fig2_3_2"}: {#fig.-figfig2_3_2}

![Mincut problem](./Week2_3/figure2.jpg){#fig:fig2_3_2
width="\\textwidth"}

With the given connection matrix $[C]$, the answer to the mincut problem
is kind of obvious because of the way I chose the connections here is
that 1, 2, and 5 have connections and 3, 4, and 6 have connections. So
you obviously break it up as $\{1 \ 2 \ 5 \}$ and $\{3 \ 4 \ 6 \}$.

The answer to the max-cut problem, is not immediately obvious. It seems
that well, you should take 1, 2, and maybe another from the other group.
Or maybe one and two more from the other groups. So there are many
possibilities and it's not immediately obvious which one will be the
maximum. Now the method we'll describe to you kind of allows you to
solve both these problems.

### Figs. [2.28](#fig:fig2_3_4){reference-type="ref" reference="fig:fig2_3_4"}-[2.31](#fig:fig2_3_7){reference-type="ref" reference="fig:fig2_3_7"}: Defining Energy {#figs.-figfig2_3_4-figfig2_3_7-defining-energy}

#### Figs. [2.28](#fig:fig2_3_4){reference-type="ref" reference="fig:fig2_3_4"}: {#figs.-figfig2_3_4}

Now, the question is (see Fig.
[2.28](#fig:fig2_3_4){reference-type="ref" reference="fig:fig2_3_4"}),
how do I choose my energy function $\widetilde{E}$ in terms of $x$ and
$w$, so that the peaks tell me the answer. For example if the peak
occurs at $\{110010\}$ then the 1's will define one group, namely
$\{1 \ 2 \ 5 \}$ and the 0's will define the other group, namely
$\{3 \ 4 \ 6 \}$.

First we write $\widetilde{E} = \sum_{r,q} C_{rq} F_{rq}$ What is
$F_{rq}$? Well, the idea is that if $r$ and $q$ both belong to the same
group, which means if both are 0 or if both are 1, then it doesn't
contribute to the energy, that's 0. On the other hand, if one is 0 and
the other is 1, that means you're kind of cutting across from one group
to the other and in that case, the $F_{rq}$ is 1. This way, when I add
them all up, we will basically add up the value of $C$ for all those
connections between the two separate groups[^31]. So when I minimize the
energy, it will tend to minimize it such that the $C$'s are as small as
possible between the two groups.

So how do I write this ? Well, one way to write it is $(S_r- S_q)^2$,
well, why? Because while you see the two are equal, I get 0. If the two
are not equal, one is 1, and the other is 0, I get 1, that's it. So,
this is it really.

![Defining the energy function for the mincut
problem](./Week2_3/figure4.jpg){#fig:fig2_3_4 width="\\textwidth"}

#### Fig. [2.29](#fig:fig2_3_5){reference-type="ref" reference="fig:fig2_3_5"}: {#fig.-figfig2_3_5}

So once you have written this energy, the point is the energy is a
minimum when you have this min cut condition is satisfied. So whatever
I'll do for the next few slides is work on this a little bit
algebraically, so that I can come out with the $x$ and $w$ matrices,
that I need in order to do my time sampling.

So first thing is I squared this, so $(a-b)^{2}$ is, $a^2+b^2-2ab$, so
we get $s_r^2+s_q^2-2s_rs_{rq}$. I then note that you see $s$ being this
binary variable 0 or 1, $s^2$ is really equal to $s$, so I dropped the
squares. So then basically
$\widetilde{E}=\sum_{r,q}{C_{rq}(s_r+s_q-2s_rs_q)}$.

![Simplifying the energy function](./Week2_3/figure5.jpg){#fig:fig2_3_5
width="\\textwidth"}

#### Figs. [2.30](#fig:fig2_3_6){reference-type="ref" reference="fig:fig2_3_6"}-[2.31](#fig:fig2_3_7){reference-type="ref" reference="fig:fig2_3_7"}: Finding x,w {#figs.-figfig2_3_6-figfig2_3_7-finding-xw}

![Identifying $\{x\}$, $[w]$ from the energy
function](./Week2_3/figure6.jpg){#fig:fig2_3_6 width="\\textwidth"}

![Identifying $\{x\}$, $[w]$ from the energy function
(contd.)](./Week2_3/Picture1.jpg){#fig:fig2_3_7 width="\\textwidth"}

Now, what I want to do is take this
$\widetilde{E}=\sum_{r,q}{C_{rq}(s_r+s_q-2s_rs_q)}$ and put it in our
canonical form
$\widetilde{E}=\sum_{r}{s_rx_r}+(1/2)\sum_{r,q}{s_rw_{r,q}s_q}$. There
is a term that's linear, which is what you often called the bias term
and then there's a term that's quadratic, which you call the weight
term. So, what I want to do is fool around with this
$\widetilde{E}=\sum_{r,q}{C_{rq}(s_r+s_q-2s_rs_q)}$ a little bit,
manipulate it, so that I can write it in the form
$\widetilde{E}=\sum_{r}{s_rx_r}+(1/2)\sum_{r,q}{s_rw_{r,q}s_q}$. The
algebra is spelt out in Figs. [2.30](#fig:fig2_3_6){reference-type="ref"
reference="fig:fig2_3_6"} and [2.31](#fig:fig2_3_7){reference-type="ref"
reference="fig:fig2_3_7"}. The end result is
$x_r=\sum_{q}{(C_{rq}+C_{qr})}$, and $w_{rq} = -4C_{rq}$.

### Figs. [2.32](#fig:fig2_3_8){reference-type="ref" reference="fig:fig2_3_8"}-[2.38](#fig:fig2_3_14){reference-type="ref" reference="fig:fig2_3_14"}: Imposing constraints {#figs.-figfig2_3_8-figfig2_3_14-imposing-constraints}

#### Fig. [2.32](#fig:fig2_3_8){reference-type="ref" reference="fig:fig2_3_8"}: State space response {#fig.-figfig2_3_8-state-space-response}

Now that we have $x$, $w$ we can just simulate this system the system of
six $p$-$bits$ generating a sequence of samples and it will do
automatically is select out the lowest energy states, and those lowest
energy states would be the solutions to my min cut problem.

Now if we do that (see Fig. [2.32](#fig:fig2_3_8){reference-type="ref"
reference="fig:fig2_3_8"}), actually, so this is relatively
straightforward. You could do it numerically or actually if you want to
write out all the energies, you can, in this case, you see you don't
really need to do the sampling method, you could just do it the
Boltzmann way. Which means write out the energy of all the 64 states and
calculate their probabilities and see which ones are highest.

Anyways, so if you do all that, you will see that you actually get the
peaks that we talked about. These were the correct solutions, remember,
but you also get two additional solutions here. One, that's all 0 and
the other that's all 1, why? Because you see both of them satisfied the
condition we imposed. We say that, if a for any bond, any connection
that goes between a 1 and a 0 should be as small as possible, well, here
they're all 1s, so there are no bonds between 1 and 0, and the same
here. So these kind of satisfy the condition we imposed, and so it's not
surprising that these solutions also came up. But of course, it's not
the solution we want, because the original problem said, take your six
neurons, six nodes and break it up into two equal groups, put three in
one and three in the other. So here we have taken all six and put them
in one group, then the same here, so that's not what you're looking for.

![State space response](./Week2_3/figure8.jpg){#fig:fig2_3_8
width="\\textwidth"}

#### Figs. [2.33](#fig:fig2_3_9){reference-type="ref" reference="fig:fig2_3_9"}-[2.35](#fig:fig2_3_11){reference-type="ref" reference="fig:fig2_3_11"}: Constraints through energy {#figs.-figfig2_3_9-figfig2_3_11-constraints-through-energy}

![Imposing constraint through
energy](./Week2_3/figure9.jpg){#fig:fig2_3_9 width="\\textwidth"}

![Imposing constraint through
energy](./Week2_3/figure10.jpg){#fig:fig2_3_10 width="\\textwidth"}

![Imposing constraint through
energy](./Week2_3/figure11.jpg){#fig:fig2_3_11 width="\\textwidth"}