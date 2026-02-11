::: center
**p-Bits & q-Bits:** \
*for Probabilistic and Quantum Computing*\

Lecture Notes\
from the online course \
*Boltzmann Law: Physics to Computing*\
offered since Fall 2020 on\
[nanoHUB](https://nanohub.org/courses/BPC)     &
[edX](https://www.edx.org/course/boltzmann-law-physics-to-computing)

**Supriyo Datta**\
:::

::: dedication
*To Anuradha*
:::

# Acknowledgements {#acknowledgements .unnumbered}

# A note to readers {#a-note-to-readers .unnumbered}

# Prologue {#prologue .unnumbered}

Welcome to our course Boltzmann Law: Physics to Computing. We normally
cover this course in 5 weeks: Week 1 on statistical mechanics, Weeks 2-3
on topics that you might see in a course on machine learning and finally
weeks 4-5 on topics that you might see in a course on quantum computing.
That is quite a spectrum of topics each of which is usually taught over
multiple semesters in distinct academic communities. What could they
have in common to merit a course like this, one that cannot possibly do
justice to any of the topics individually?

## Fig. [0.1](#fig0_1){reference-type="ref" reference="fig0_1"}: n versus $2^n$ {#fig.-fig0_1-n-versus-2n}

![$n$ versus $2^n$](./Prologue/Fig1.png){#fig0_1 width="40%"}

The short answer is that if we are talking about a system with $n$ bits,
then all these topics require us to visualize and work in a space with
$2^n$ components as opposed to our familiar space with $n$ components.
Those two numbers are vastly different as you can see. An $n$ of just
$40$ leads to $2^n \sim 10^{12}$ ! The computing paradigms we will talk
about derive their power from being able to manipulate a system of $n$
bits to control a response in a space with $2^n$ components.[^1]

Now for a long answer, hope you don't find it too long :-)

## Figs. [0.2](#fig0_3){reference-type="ref" reference="fig0_3"}-[0.3](#fig0_5){reference-type="ref" reference="fig0_5"}: Spintronics {#figs.-fig0_3-fig0_5-spintronics}

We are all familiar with the wonders of modern electronics made possible
by the high-speed operation of billions of transistors all integrated
into a single chip. Information is stored and manipulated using bits or
binary units each of which has two states that can be used to represent
a $0$ or a $1$. This has proved to be a powerful paradigm which has
continued the triumphant march of Moore's law decade after decade with
no end in sight, though there is talk of slowing down. There is,
however, extensive interest in an alternative paradigm generally
referred to as quantum computing based on the use of $q$-$bits$. How are
$q$-$bits$ different from $bits$?

#### Fig. [0.2](#fig0_3){reference-type="ref" reference="fig0_3"} {#fig.-fig0_3}

![One of the many possible physical representations of a $bit$ and a
$q$-$bit$.](./Prologue/Fig3.png){#fig0_3 width="80%"}

One way to understand the difference between $q$-$bits$ and $bits$ is to
consider a specific physical representation. A $bit$ could be
represented using small magnets or $\textit{nanomagnets}$ whose
magnetization can be reversed as in MRAM[^2] technology. The nice thing
about this representation is that it connects smoothly with a
representation for q-bits based on elemental $\textit{quantum magnets}$.

Everyone knows that an electron carries an elemental charge, $q$. What
is less-well known is that an electron is also an elemental magnet
carrying a magnetic moment of $q \hbar/2m \sim 10^{-23} A$-$m^2$. It is
as if the electronic charge is $spin$ning to give rise to a current,
generating a magnetic moment whose magnitude is roughly what would be
created by a loop of area $1 \ nm^2$ carrying a current of
$10 \  \mu A$. This elemental magnet or $spin$ is the prototypical
$q$-$bit$. How is it different from a classical magnet which is a
prototypical $bit$?

#### Fig. [0.3](#fig0_5){reference-type="ref" reference="fig0_5"} {#fig.-fig0_5}

The difference can be understood by considering an experiment that took
the scientific world by storm when first performed a hundred years ago.
Suppose we come in with a beam of magnets that have been passed through
a strong magnetic field $B$ along $\hat{z}$, such that their magnetic
moments are all aligned in that direction. They are passed through a
detector that separates magnetic particles based on their magnetic
moment along a specific direction $\hat{n}$ that makes an angle $\theta$
with $\hat{z}$. The classical magnets all bend by the same amount
determined by $cos \ \theta$ producing a $\textit{single spot}$ on the
screen.

![Classical magnet versus quantum magnet, polarized
collection](./Prologue/Fig5.png){#fig0_5 width="80%"}

Experimentally it is found that the quantum magnets produce
$\textit{two spots}$, but not equally strong. A fraction
$cos^2 (\theta/2)$ produce the spot corresponding to $+ \mu_{B} \hat{z}$
while a fraction $sin^2  (\theta/2)$ produce the spot corresponding to
$- \mu_{B} \hat{z}$, giving an $average$ magnetic moment of
$cos^2 (\theta/2)$ - $sin^2 (\theta/2)$ = $cos \ \theta$.[^3] The two
spots suggest that each quantum magnet has a magnetic moment
$\sim + \hat{n}$ or $\sim - \hat{n}$, with the degree of bending
indicating a magnitude of $\mu_{B}=q \hbar/2m \sim 10^{-23} A$-$m^2$ for
the associated magnetic moment.[^4]

These observations may defy \"common sense\", but those are the facts
and a straightforward mathematical framework has been developed to
describe them. We say that quantum magnets do not have a magnetic moment
$\vec{m}$, only a 2-component probability amplitude
$\psi(\vec{m}) = \{u \ \ v\}^T$. Any property $S$, like the
$x$-$component$ of spin, has an associated $2 \times 2$ matrix $S_{op}$:
the average value of repeated measurements will be given by
$\psi^T S_{op} \psi$. There is thus a major conceptual jump from a
classical magnet to a quantum magnet, replacing a moment $\hat{m}$ with
a complex probability amplitude $\psi(\vec{m})$, which can be used to
tell the probability of measuring one of the two possible outcomes for
any measurement.

These results were originally discovered through experiments conducted
in vacuum with atoms, but have subsequently been exploited in devices as
well leading to the term $spintronics$. Such spin-related effects are
routinely included in the description of electronic devices, as some of
you may remember from our course on quantum transport.[^5] In short
quantum effects $\textit{per se}$ are not new to device physicists. But
then, what distinguishes $q$-$bits$ and quantum computing from these
\"everyday\" quantum effects?

## Fig. [0.4](#fig0_6){reference-type="ref" reference="fig0_6"}: It's the Correlations! {#fig.-fig0_6-its-the-correlations}

The key distinction is that $q$-$bits$ and quantum computing require
$strong$ $correlations$ among the quantum magnets, while the usual
design of everyday devices rely on the correlations being weak. To
understand this we can consider a toy device with just two $q$-$bits$,
one of which shows has a $70$-$30$ probability of being $0$ or $1$,
while the other has a $30$-$70$ probability. What is the composite
probability of the collection being $00$,$01$,$10$,$11$?

The answer may seem simple: Probability of $\{00\}$ equals
$70\% \times 30\% = 21 \%$, that of $\{01\}$ equals
$70\% \times 70\% = 49 \%$, and so on. This should be accurate if the
two are uncorrelated or only weakly correlated as we assume in our usual
devices. But if they are $\textit{strongly correlated}$ then the
composite probability is not the product of the components. For example
if the two are perfectly anti-correlated then we may not have any $00$
or $11$, only $01$ and $10$ with probabilities $70$-$30$ as shown. This
is consistent with the individual $p_1$, $p_2$ shown, but it is not
unique. We could come up with other composite probabilities that are
intermediate between the fully correlated and un-correlated limits
shown.

![Composite probability distribution cannot be obtained from the product
of individual distributions
$\textit{if they are strongly correlated}$.](./Prologue/Fig6.png){#fig0_6
width="90%"}

In more general terms, we can say that in the uncorrelated case the
composite $p$ with $2^n$ components can be written as the Kronecker
product of the $n$ individual $p_i$'s each having $2$ components. This
means we can specify a distribution with $\sim n$ parameters. By
contrast, to specify a distribution with strong correlations, we need
$\sim 2^n$ parameters, making it much richer in the amount of embedded
information. And as we noted at the outset
(Fig.[0.1](#fig0_1){reference-type="ref" reference="fig0_1"}) there is
an enormous difference between the two: An $n$ of $40$ corresponds to a
$2^n$ of $\sim 10^{12}$ ! And this exponential advantage is what quantum
computing seeks to harness.

## Figs. [0.5](#fig0_7){reference-type="ref" reference="fig0_7"}-[0.6](#fig0_8){reference-type="ref" reference="fig0_8"}: q-bits versus p-bits {#figs.-fig0_7-fig0_8-q-bits-versus-p-bits}

#### Fig. [0.5](#fig0_7){reference-type="ref" reference="fig0_7"}: q-bits {#fig.-fig0_7-q-bits}

A gated quantum computer (GQC) consists of a system of $n$ $q$-$bits$
that are operated on sequentially by a set of quantum gates to put them
into a strongly correlated state such that if we measure the output
repeatedly we will get a specific probability distribution whose peaks
will solve some practical problem for us. The challenge of course is to
construct gates operating in $n$-$space$ for times of order $n$, that
will give us a desired response in $2^n$-space. Grover search and Shor's
algorithm[^6] are two celebrated algorithms that you may have heard of
in this context.

![A system of $n$ $q$-$bits$ can be correlated through a sequence of
quantum gates to generate samples according to a desired distribution
with $2^n$ components.](./Prologue/Fig7b.png){#fig0_7 width="90%"}

![A system of $n$ $p$-$bits$ can also be correlated through a sequence
of classical gates to generate samples according to a desired
distribution with $2^n$ components.](./Prologue/Fig8b.png){#fig0_8
width="90%"}

#### Fig. [0.6](#fig0_8){reference-type="ref" reference="fig0_8"}: p-bits {#fig.-fig0_8-p-bits}

If the $2^n$ advantage we are talking about comes from
$\textit{strong correlations}$ then perhaps a classical probabilistic
system could also do something similar, namely prepare a strongly
correlated classical state with $2^n$ components? The answer is kind of,
but not exactly.

How could we construct the probabilistic version of the GQC sketched in
Fig.[0.5](#fig0_7){reference-type="ref" reference="fig0_7"} which
operates on a set of 'n' $q$-$bits$ with coherent quantum gates to
transform its $2^n$ component complex wavefunction from $\psi(t)$ into
$\psi(t+1)$? Answer: By replacing the quantum magnets in
Fig.[0.5](#fig0_7){reference-type="ref" reference="fig0_7"} with
classical magnets as in Fig.[0.6](#fig0_8){reference-type="ref"
reference="fig0_8"}, and using classical gates to transform its $2^n$
component real non-negative probability distribution function $p(t)$
into $p(t+1)$.

Could such a $p$-$computer$ be useful? The reader may have heard of deep
belief networks (DBN) used in the field of machine learning (ML) which
are essentially the $p$-$computer$ sketched in
Fig.[0.6](#fig0_8){reference-type="ref" reference="fig0_8"}. Each
$p$-$bit$ takes on one of two values $0$ and $1$ with probabilities
determined by the weighted sum of the current values of all $p$-$bits$.
In the ML literature these elements are known as binary stochastic
neurons (BSN). The weights used in this summation can be
$\textit{trained}$ to provide a desired response in $2^n$-space. We
could view the DBN sketched in Fig.[0.6](#fig0_8){reference-type="ref"
reference="fig0_8"} as the classical analog of the GQC sketched in
Fig.[0.5](#fig0_7){reference-type="ref" reference="fig0_7"}.

I should note that in this course we will focus on the use of binary
units or $p$-$bits$ to correspond to standard $q$-$bits$. More generally
we could think of $d$-valued units[^7] or even continuous valued units.
The latter are used in deep neural networks (DNN) based on $neurons$
whose output takes on continuous analog values determined by applying a
non-linear activation function to the weighted sum. The basic principle
is that of interconnecting 'n' units to obtain a desired response in an
exponentially larger space, in a manner that some readers may find
reminiscent of Koopman operators.

## Figs. [0.7](#fig0_9){reference-type="ref" reference="fig0_9"}-[0.8](#fig0_11){reference-type="ref" reference="fig0_11"}: The key difference {#sec:Magic}

#### Fig. [0.7](#fig0_9){reference-type="ref" reference="fig0_9"} {#fig.-fig0_9}

So what distinguishes the $q$-$circuit$ from the $p$-$circuit$?

As we will see, their mathematics look similar\
$q$-$bits$ : $\psi(t+1) = \textbf{U} \times \psi(t)$   **U**: Unitary
matrix    (Chapter [5](#Sec:Quantum Transition){reference-type="ref"
reference="Sec:Quantum Transition"})\
$p$-$bits$: $p(t+1) = \textbf{W} \times p(t)$   **W**: Stochastic matrix
   (Chapter [3](#Sec:Transition){reference-type="ref"
reference="Sec:Transition"})\
But there is at least one $\textit{fundamental}$ difference:
$\textbf{U}$ is a unitary matrix with complex components while
$\textbf{W}$ is a stochastic matrix with real non-negative real
components. In his seminal 1982 paper that inspired much of quantum
computing, Feynman referred to this as the $\textit{only difference}$.

![The key distinction between quantum hardware and classical
probabilistic hardware arises from the complex elements of the
$\textbf{U}$ matrix in place of the non-negative real components of
$\textbf{W}$. ](./Prologue/Fig9.png){#fig0_9 width="80%"}

#### Fig. [0.8](#fig0_11){reference-type="ref" reference="fig0_11"} {#fig.-fig0_11}

To understand this key difference, it may be helpful to compare two toy
examples one representing a 2 $p$-$bit$ $circuit$ and the other a 2
$q$-$bit$ $circuit$. Each one has four states labeled
$\{00 \ 01 \ 10 \ 11\}$ and each circuit converts an evenly distributed
probability into one that is peaked at $\{00\}$.

![A $p$-$circuit$ and a $q$-$circuit$ each of which converts a
probability evenly spread among four states $\{00 \ 01 \ 10 \ 11\}$ into
one peaked at $\{00\}$.](./Prologue/Fig11b.png){#fig0_11 width="95%"}

The $p$-$circuit$ achieves this conversion with classical gates that
effectively multiply the initial distribution with a stochastic matrix
$\textbf{W}$ having real non-negative components, while the
$q$-$circuit$ achieves this conversion with quantum gates that
effectively multiply the initial distribution with a unitary matrix
$\textbf{U}$ having complex components,

In the first case, the only way to get $0$ at the output is by making
the entire row zero, since all elements are positive. But in the second
case there are positive and negative elements[^8] which can cancel each
other out to produce a net zero output. But this added flexibility comes
with the need to control each of the elements accurately so that the
positives and negatives indeed cancel out to produce zero.

Note that with $q$-$circuits$ the $\psi$ represents a complex
probability amplitude whose squared magnitude is a non-negative number
that gives us the actual probability of a particular observation. All
components of the probability function $p(t)$ add up to one, while it is
the the squared magnitudes of the components of the wavefunction
$\psi(t)$ that add up to one.

In the classical case when the probability distribution $p(t)$ is not
factorizable, the system is said to be $\textbf{correlated}$. In the
quantum case when the complex wavefunction $\psi(t)$ is not
factorizable, the system is said to be $\textbf{entangled}$.

## Fig. [0.9](#fig0_12){reference-type="ref" reference="fig0_12"}: Hardware acceleration {#fig.-fig0_12-hardware-acceleration}

Both probabilistic circuits (Chapters 2,3) and quantum circuits
(Chapters 4,5) have to be designed to control the interactions among $n$
elements to control the response in $2^n$-space. Their key difference is
the nature of the $2^n \times 2^n$ matrices, $\textbf{W}$ and
$\textbf{U}$ operating on the probability distribution $p(t)$ and the
wavefunction $\psi(t)$ respectively. One has real non-negative elements
describing classically understood behavior, while the other has complex
elements that can enable non-classical behavior, some of which can be
very intriguing like the EPR experiment discussed in Section
[4.6](#Sec:EPR){reference-type="ref" reference="Sec:EPR"}.

![Both $p$- and $q$-$circuits$ are designed in $n$-space to control the
response in $2^n$-space. But their key difference is the nature of the
matrices $\textbf{W}$ and $\textbf{U}$. One has real non-negative
elements, the other has complex elements that can enable non-intuitive
behavior like the EPR experiment discussed in Section
[4.6](#Sec:EPR){reference-type="ref"
reference="Sec:EPR"}.](./Prologue/Figure12.png){#fig0_12 width="90%"}

Note that if we are actually multiplying matrices then it is not too
much more difficult to handle complex matrices relative to real
matrices. But these matrices are $2^n \times 2^n$ which can be enormous
even for modest values of $n$. And so in practice, one uses powerful
Monte Carlo sampling techniques which can often provide sufficiently
accurate approximate results, not unlike the way a well-designed
$\textit{exit poll}$ of a few thousand people can predict the results of
a full election with millions of voters.

The sampling technique often works well for $p$-$circuits$ with
non-negative probabilities, but are less effective for $q$-$circuits$
with complex probabilities that show large degrees of cancellation.[^9]
Indeed this is the chief rationale behind building $q$-$circuits$ that
can sum up the complex probabilities through its
$\textit{intrinsic quantum physics}$.

For problems that only involve non-negative probabilities,
$p$-$circuits$ can be just as effective as the corresponding
$q$-$circuits$, provided the $p$-$circuit$ is implemented using the
natural physics of $p$-$bits$ and classical circuits. Usually the
sampling algorithms are implemented by writing a code in a high level
language, making it versatile but inefficient. Much can be gained simply
by replacing software with specialized hardware, and such improvements
should be distinguished from those that come from exploiting the magic
of quantum physics through the cancellation properties of the complex
wavefunction $\psi$.

This is why we find it instructive to use $p$-$circuits$ as a
counterpoint to clarify what is unique about a specific $q$-$circuit$.
Both have to design the interactions among $n$ bits and implement them
in hardware, so as to generate desired samples form a vast repertoire
with $2^n$ possibilities. One has the added power that comes from the
use of complex probability amplitudes, but which also comes with
stringent demands on the phase.

## Statistical mechanics

Hope you see my rationale for looking at both probabilistic (Chapters 2
and 3) and quantum (Chapters 4 and 5) generative models in the same
course. But why Chapter 1 on statistical mechanics?

It reviews seminal concepts like the Boltzmann law, entropy and free
energy that were developed in the $19^{th}$ century to understand
macroscopic properties in terms of the atoms at the microscopic level.
This may sound very different, but this too is about relating
interactions in $n$-space with response in $2^n$-space. Their
motivation, however, is reversed from ours. We want a response in
$2^n$-space and train our gates in $n$-space to provide the necessary
interactions. By contrast, they took the \"gates\" provided by Nature in
$n$-space and wanted to calculate the resulting properties in
$2^n$-space. But their insights can be useful to us, an example of which
is the $\textit{diffusion model}$ in machine learning.

It is time to get started :-)

# Statistical mechanics

## State space

Welcome to our course, $\textit{Boltzmann Law: Physics to Computing.}$
This is [Lecture 1.1: Watch youtube
video](https://www.youtube.com/watch?v=tDFyxWiF8xo)

### Fig. [1.1](#fig:fig1_1){reference-type="ref" reference="fig:fig1_1"}: Fermi Function {#fig.-figfig1_1-fermi-function}

Let me start with something that probably most of you have seen before.
Whenever we talk about any material like an atom or a molecule or a
solid, we draw a set of energy levels which the electrons in that
material can occupy (Fig. [1.1](#fig:fig1_1){reference-type="ref"
reference="fig:fig1_1"}a). And usually left to itself at equilibrium,
the electrons all want to go to the lowest energy levels.

Now, why don't they all crowd into the same level? Well, that's where we
invoke the exclusion principle and say that each level can at most
accommodate one electron. And so the lowest levels are usually filled
and the high upper levels are empty. At low temperatures, there's a nice
clean dividing line between them, which we call the electrochemical
potential or $\mu$.

But as you raise the temperature, that dividing line becomes more
diffuse, and we have something called the *Fermi function* (see Fig.
[1.1](#fig:fig1_1){reference-type="ref" reference="fig:fig1_1"}(b)).
This Fermi function is plotted here on the horizontal axis, whereas on
the vertical axis, I have this dimensionless quantity which tells you
how far the level is from the electrochemical potential, normalized to
the thermal energy, $kT$. $k$ is Boltzmann's constant and $T$ is the
absolute temperature.

![**Fermi Function**](./Week1/fig1_1.jpg){#fig:fig1_1 width="90%"}

When you consider levels that are way above the electrochemical
potential, the Fermi function is 0, indicating that the level is surely
empty. When you're down way below the electrochemical potential, that's
when the Fermi function is 1 indicating that the level is surely full.
And in between, it changes from 0 to 1. Right at $\varepsilon = \mu$
it's 0.5. What does that mean? Well, not that there's half an electron
there. What it means is that levels there are sometimes full and
sometimes empty, and the average occupation is 0.5. Anyway, this is the
Fermi function that you have probably seen before.

But what I really want to talk about is a much more general law,
*Boltzmann law*. The Fermi function can be obtained from it. You may
have heard of the *Bose-Einstein distribution* that's obeyed by photons.
Well, that too can be obtained from the Boltzmann law, although we won't
be talking about it. The *Boltzmann law* applies to all systems in
equilibrium. It doesn't matter how complicated or simple it is.

### Fig. [1.2](#fig:fig1_2){reference-type="ref" reference="fig:fig1_2"}: Boltzmann Law {#fig.-figfig1_2-boltzmann-law}

![**State space and Boltzmann law:**](./Week1/fig1_2.jpg){#fig:fig1_2
width="\\textwidth"}

Now, in order to explain the Boltzmann law, I need to introduce the
concept of *state space* which is a very important concept in this
entire course. The idea is that each of our one electron levels (see
Fig. [1.2](#fig:fig1_2){reference-type="ref" reference="fig:fig1_2"}(a))
can be in one of two possible states. It can be either full or empty,
that's a 0 state or a 1 state. So when you want to describe the states
of the entire system, then you have to write a binary number, something
like this (see Fig. [1.2](#fig:fig1_2){reference-type="ref"
reference="fig:fig1_2"}(b)): $\{10011\}$, meaning the first state is
full. The second state is empty. The third state is empty. Fourth state
is full. Fifth state is full, and so on.

So how many such states are possible in state space? The answer is
$2^n$, because you see, there are $n$ of these digits and each one can
be 0 or 1: Overall you can think of $2^n$ combinations. And that's the
state space as opposed to the one electron space, which has only $n$
levels.

Now, the $\textit{Boltzmann law}$ is stated in this state space (see
Fig. [1.2](#fig:fig1_2){reference-type="ref" reference="fig:fig1_2"}(c))
and what it says is that the probability for the system to be in the
$i$-th state, depends on the exponential of the negative of this
quantity ($(E_i-\mu N_i)/kT$). What is this quantity? It involves the
energy $E_{i}$ of the $i^{th}$ state and the number $N_{i}$ of electrons
in the $i^{th}$ state, and the thermal energy, as in the Fermi function,
the same $kT$.

And what's this constant ($1/Z$) in front? Well, that constant should be
chosen so that all the probabilities add up to 1, because the system
must be in one state or another. What I'll show you next is how from
this general law you can obtain the Fermi function. Because as I said,
this is the most general law that applies to anything. Doesn't matter
how complicated or simple, okay?

### Figs. [1.3](#fig:fig1_3){reference-type="ref" reference="fig:fig1_3"}-[1.4](#fig:fig1_4){reference-type="ref" reference="fig:fig1_4"}: Fermi function from Boltzmann Law {#figs.-figfig1_3-figfig1_4-fermi-function-from-boltzmann-law}

#### Fig. [1.3](#fig:fig1_3){reference-type="ref" reference="fig:fig1_3"} {#fig.-figfig1_3}

Let's take the simplest thing, a system with just one level (see Fig.
[1.3](#fig:fig1_3){reference-type="ref" reference="fig:fig1_3"}(a)). So
in the one electron space, there's just one state. Now, how many states
are there in state space? Well, $2^1$, which is to say that you have a
zero state and a one state. And to write down the Boltzmann law, I need
the energy and the number of electrons for each one of those.

![**System with one energy level**](./Week1/fig1_3.jpg){#fig:fig1_3
width="\\textwidth"}

The number of electrons is (a) 0 for the zero state and (b) 1 for the
one state. The energy is (a) 0 for the zero state and (b) equal to
whatever the energy level is $\epsilon_1$ for the one state. So we can
now write down the $(E - \mu N)/kT$ as (a) 0 for the zero state and
$(\epsilon_1 - \mu )/kT$ for the one state.

Now we are ready to write down the probabilities (see Fig.
[1.3](#fig:fig1_3){reference-type="ref" reference="fig:fig1_3"}(b)). The
probability of the zero state is $1/Z$, because $e^0$ is 1. The
probability of the one state, well that's $e^{-x_1}/Z$, where we define
this dimensionless quantity $x_1$, as $(\epsilon_1- \mu)/kT$.

Well, then how do I find $Z$? The idea is that the two probabilities
must add up to one because this system has only two possibilities (see
Fig. [1.3](#fig:fig1_3){reference-type="ref"
reference="fig:fig1_3"}(c)). And so $p_0 + p_1 = 1+\exp{(-x_1)}$ divided
by $Z$ must equal one, which tells me that $Z$ must be $1+\exp{(-x_1)}$.

#### Fig. [1.4](#fig:fig1_4){reference-type="ref" reference="fig:fig1_4"}: Boltzmann Law is NOT the Boltzmann approximation {#fig.-figfig1_4-boltzmann-law-is-not-the-boltzmann-approximation}

So now we can take this Z and substitute it back to write $p_1$ as
$\exp{(-x_1)}$ divided by $1+\exp{(-x_1)}$ (see Fig.
[1.4](#fig:fig1_4){reference-type="ref" reference="fig:fig1_4"}(a)). And
with a little bit of algebra, you can write it in a form, that you will
recognize as the Fermi function that I've stated before. So what I've
shown you then is that starting from Boltzmann law when I apply to a
simple system, I get the Fermi function.

![**Fermi function from Boltzmann law**](./Week1/fig1_4.jpg){#fig:fig1_4
width="90%"}

Sometimes people approximate the Fermi function with $\exp{(-x_1)}$.
They say, well if $x\gg 1$, then I can drop the one and then this will
become $\exp{(-x_1)}$. And that's often referred to as the Boltzmann
approximation (see Fig. [1.4](#fig:fig1_4){reference-type="ref"
reference="fig:fig1_4"}(b)). And if you have taken courses in
semiconductor devices, you've probably seen it and used it extensively.

But I want to stress again, that the Boltzmann law we are going to talk
about in this course, is not this Boltzmann approximation. What we are
talking about is the Boltzmann Law which is far more general than the
Fermi function, and certainly not an approximation to it.

Finally, just as we wrote down the Fermi function $f_1$ describing the
probability for the system to be in state 1, we could also write down
the probability for the system to be in state 0 (see Fig.
[1.4](#fig:fig1_4){reference-type="ref" reference="fig:fig1_4"}(c)). And
that, as you might expect will be $1- f_1$ so that the two probabilities
add up to one. All this follows straight from the Boltzmann law applied
to a one level system.

### Figs. [1.5](#fig:fig1_5){reference-type="ref" reference="fig:fig1_5"}-[1.7](#fig:fig1_7){reference-type="ref" reference="fig:fig1_7"}: Two non-interacting energy levels {#figs.-figfig1_5-figfig1_7-two-non-interacting-energy-levels}

#### Fig. [1.5](#fig:fig1_5){reference-type="ref" reference="fig:fig1_5"} {#fig.-figfig1_5}

Let me now go through a little more complicated example involving two
energy levels in the one-electron space, each of which can be 0 or 1.

![**System with two energy levels**](./Week1/fig1_5.jpg){#fig:fig1_5
width="\\textwidth"}

In this system then, I could label all the different states as $\{00\}$,
$\{01\}$, $\{10\}$, and $\{11\}$. $\{00\}$, means both are empty.
$\{01\}$ means first one's empty. second one's full. $\{10\}$ is first
one's full. second one's empty. $\{11\}$ is where both are full.

Now, to apply the Boltzmann law, I need to write down $(E- \mu N) /kT$
for each one of these possibilities. So let's first write down the
number of electrons. For $\{00\}$ there are no electrons, so $N_i = 0$.
For $\{01\}$ or $\{10\}$, there's one electron, so $N_i = 1$. For
$\{11\}$, then there are two electrons because both are full and
$N_i = 2$.

What about the energy? $\{00\}$ has no electrons and the energy
$E_i =0$. For $\{01\}$, then then energy $E_i = \epsilon_1$. For
$\{10\}$ energy is $E_i = \epsilon_2$. And for $\{11\}$, then
$E_i = \epsilon_1 + \epsilon_2$.

So now you can fill out $(E_i- \mu N_i)/kT$ for each of the four
possibilities as shown. For $\{00\}$, $(E_i- \mu N_i)/kT$ is just 0. For
$\{01\}$ it is $(\epsilon_1- \mu)/kT$. For $\{10\}$ it is
$(\epsilon_2- \mu)/kT)$. And finally for $\{11\}$, it is
$(\epsilon_1 + \epsilon_2- 2\mu)/ kT$.

#### Fig. [1.6](#fig:fig1_6){reference-type="ref" reference="fig:fig1_6"}: $E - \mu N$ {#fig.-figfig1_6-e---mu-n}

Now I can fill out the probabilities as shown in Fig.
[1.6](#fig:fig1_6){reference-type="ref" reference="fig:fig1_6"}(a)).

![**State Space probabilities of a system with two
levels**](./Week1/fig1_6.jpg){#fig:fig1_6 width="\\textwidth"}

What's the next step? Well, now I have to find $Z$. For this I require
all probabilities to add up to 1 (see Fig.
[1.6](#fig:fig1_6){reference-type="ref" reference="fig:fig1_6"}(a)). So,
I have to add all four probabilities, and the answer should be 1. Which
means just like before, $Z$ should be equal to the sum of the
numerators, which is
$1+\exp{(-x_1)}+\exp{(-x_2)}+\exp{(-x_2)}\exp{(-x_1)}$.

Just to simplify the algebra a little, I've given names to two of these
terms. This exponential of $-x_1$, I call it $y_1$, and $\exp{(-x_2)}$,
well that's $y_2$. And $\exp{(-x_2)}\exp{(-x_1)}$? Well, that's $y_2$
times $y_1$. Now, I can easily factorize this and I can write it as
$(1 + y_2) (1 + y_1)$. You can see that when you multiply that out,
you'll get $1 + y_2 + y_1 + y_2y_1$.

#### Fig. [1.7](#fig:fig1_7){reference-type="ref" reference="fig:fig1_7"}: Probabilities {#fig.-figfig1_7-probabilities}

So now I put Z back into the probability expressions (see Fig.
[1.7](#fig:fig1_7){reference-type="ref" reference="fig:fig1_7"}), and
with a little algebra I find that $p_{11}$ is basically just $f_1$ times
$f_2$, which is what you might have guessed if you note that $f_1$ is
the probability one level is full and $f_2$ is the probability the other
one is full. So the probability that both are full is $f_1f_2$. But it
comes straight out of the Boltzmann law.

![**State Space probabilities of a system with two levels
(contd.)**](./Week1/fig1_7.jpg){#fig:fig1_7 width="\\textwidth"}

Now, if we want to write say $p_{01}$, it'll be similar, look much the
same, except that now the numerator only has $\exp{(-x_1)}$. So I don't
have the $\exp{(-x_2)}$ anymore. And so I have two factors where the
first one $f_1$, is the same Fermi function. But the other factor
instead of being $f_2$, what I really got now is $1- f_2$. It's a little
algebra, you can check that this is indeed 1 minus that quantity. And
again, the result makes good sense if you consider what's $p_{01}$?

You're asking what is the probability that one level is full and the
other one is empty? Well, the chance that the first level is full,
that's $f_1$. The chance that the second level is empty, well, that's
$1- f_2$. So the probability of finding the system in state $\{01\}$ is
$(1- f_2)f_1$. And you could go ahead and look at $p_{10}$ and $p_{00}$
as well and you'd get the answers you expected.

### Fig. [1.8](#fig:fig1_8){reference-type="ref" reference="fig:fig1_8"}: Two levels with interaction {#fig.-figfig1_8-two-levels-with-interaction}

Now what you might say is okay, but then why am I bothering with the
Boltzmann law? Because all the information is there in the Fermi
functions, and I could have written these down anyway without using the
general law.

![**State Space probabilities of a system with two levels
(contd.)**](./Week1/Fig2.8.jpg){#fig:fig1_8 width="\\textwidth"}

Well, the answer is that that's only true because we have assumed that
the electrons are not interacting. And so when you have two electrons,
the energy is really just the sum of what you get for one electron. And
that is what allows you to nicely factorize all the probabilities into
separate Fermi functions.

But if they were interacting, then you'd have an extra term here (see
Fig. [1.8](#fig:fig1_8){reference-type="ref" reference="fig:fig1_8"}),
something that would denote the interaction energy between a pair of
electrons. That's this $U_0$. And then you wouldn't be able to factorize
it so nicely. So you wouldn't be able to write your answers in terms of
Fermi functions, but you'd still be able to use the Boltzmann law.

This general law which applies to, as I said, all systems, whether
they're interacting or not interacting, whether they're simple or
complicated. But it's only for the special case of non-interacting
electrons that you can factorize it nicely into Fermi functions.

But you might say, when I took my courses on solid state devices or
solid state physics we always used the Fermi functions but electrons are
interactive. So how did we get away with it? Well, the answer is that
the way people use the Fermi functions in this one electron space is
using something called the *mean field theory*. And this is something
we'll come back to in the last lecture of this week. We'll come back and
connect up to this and explain how that mean field theory works.

But right now the main point I wanted to make is that the Boltzmann law
is the general law that applies to any system. And everything else kind
of follows from it. This is really the central principle of equilibrium
statistical mechanics. And that's this Boltzmann law, which we just
introduced. In the next lecture I'll try to explain where it comes from.

### Quiz

#### Question 1

With 8 one-electron energy levels, what is the number of levels in state
space?[^10]\

#### Question 2

If we have two one-electron energy levels with NO interactions, what is
the probability that they will both be empty? The answer should be in
terms of the Fermi functions, $f_1$ and $f_2$ corresponding to each of
the two levels.[^11]

#### Question 3

At what value of the energy $\varepsilon$ is the Fermi function equal to
$0.5$? The answer should be in terms of the electrochemical potential
$\mu$?[^12]

## Boltzmann Law

This is [Lecture 1.2: Watch youtube
video](https://www.youtube.com/watch?v=w7qB5uJ4xU0)

In Lecture 1.1, we introduced the Boltzmann law. This is the central
principle of equilibrium statistical mechanics which says that in
equilibrium, the probabilities of the different states are given by the
$p_{i}$ shown in Fig. [1.9](#fig:fig1_2_1){reference-type="ref"
reference="fig:fig1_2_1"}d. In this lecture, I'll try to justify it.

In the last lecture, I introduced the notion of state space, which is
kind of fundamental to much of what we'll be discussing in this course.
The Boltzmann law applies to the state space. I took an example of a
problem where you had two one electron levels, and which gave rise to
$2^2$ or $4$ states in state space.

Now more generally, you could of course have an arbitrary number of
states in state space and for this discussion now, we'll just say they
are labeled as 1, 2, 3, 4, etc. and each state is characterized by a
certain number of electrons and a certain total energy. What we want to
show is why the probability that the system is in one of these states
should be given by the Boltzmann law.

### Fig. [1.9](#fig:fig1_2_1){reference-type="ref" reference="fig:fig1_2_1"}: System and reservoir {#fig.-figfig1_2_1-system-and-reservoir}

![System exchanging energy and particle with
\"Reservoir\"](./Week1_2/Picture.png){#fig:fig1_2_1 width="90%"}

Now, in order to discuss this point, the first thing to note is that our
system is continually exchanging energy as well as particles, meaning
electrons in this case, with the surroundings, which we call the
reservoir (see Fig. [1.9](#fig:fig1_2_1){reference-type="ref"
reference="fig:fig1_2_1"}), something big, with lots of energy and
particles available. You see if our system were isolated then $E$ and
$N$ couldn't change and if you started off with some $E,N$ it would kind
of stay that way. In in order to be able to change states within the
system, you need to be able to exchange E and/or N with some reservoir
which is characterized by an electrochemical potential $\mu$ and a
temperature $T$. What these words actually mean will hopefully get a
little clearer as we go further in this lecture.

In some cases you might have a system that can only exchange energy but
cannot exchange particles, as shown in Fig.
[1.9](#fig:fig1_2_1){reference-type="ref" reference="fig:fig1_2_1"}b.
Because you cannot exchange particles, the $N_i$ would be fixed, in
other words, the system would always be in states which have all the
same $N_i$, because after all, the particles have nowhere to go. So if
you're in a two electron state you stay in a two electron state.

Now in that case, you see this Boltzmann law, we have these two terms in
the exponent, you can separate them out and write it as shown at the
bottom in Fig. [1.9](#fig:fig1_2_1){reference-type="ref"
reference="fig:fig1_2_1"}). And you see if the $N_i$ is fixed, then
$exp(\mu N_i/kT)$ is also kind of part of the constant. Remember we have
this constant in front, to make sure all probabilities add up to one.So
we could take $exp(\mu N_i/kT)$ as part of that constant and then you'd
have a probability that could be written like Fig.
[1.9](#fig:fig1_2_1){reference-type="ref" reference="fig:fig1_2_1"}b,
that does not mention the $N_i$ explicitly.

So sometimes depending on the problem at hand, one might be using this
expression (see Fig. [1.9](#fig:fig1_2_1){reference-type="ref"
reference="fig:fig1_2_1"}b) rather than the other one. This is the case
that is generally referred to as a *canonical ensemble*, which means
that you have an ensemble of systems, that exchange only energy with the
reservoir. If it is exchanging both energy and particles then you call
it a *grand canonical ensemble* and use the expression in Fig.
[1.9](#fig:fig1_2_1){reference-type="ref" reference="fig:fig1_2_1"}a. So
those are the technical names that you'd see if you'd look at a book in
statistical physics.

### Figs. [1.10](#fig:fig1_2_3){reference-type="ref" reference="fig:fig1_2_3"}-[1.13](#fig:fig1_2_6){reference-type="ref" reference="fig:fig1_2_6"}: Justifying the law {#figs.-figfig1_2_3-figfig1_2_6-justifying-the-law}

Now for this discussion, let us first focus on the canonical ensemble,
where it's only exchanging energy. So the expression we're trying to
understand or justify is the one shown in Fig.
[1.9](#fig:fig1_2_1){reference-type="ref" reference="fig:fig1_2_1"}b
without the $\mu$ and the $N$ appearing explicitly. Now, as I mentioned
before, it is connected to this reservoir with which it is exchanging
energy, okay.

![Justifying Boltzmann law in canonical
ensemble.](./Week1_2/fig1_2_3.jpg){#fig:fig1_2_3 width="\\textwidth"}

#### Fig. [1.11](#fig:fig1_2_4){reference-type="ref" reference="fig:fig1_2_4"} {#fig.-figfig1_2_4}

The Boltzmann law says, that the more the energy, lower the probability.
Why is that you might ask (see Fig.
[1.10](#fig:fig1_2_3){reference-type="ref" reference="fig:fig1_2_3"}a)?
If I have a thing sitting by itself, one might have expected all states
to be equally probable. Why is it that lower energy has higher
probability?

The answer is that you see, you have to consider the states of the
entire system, meaning, system plus reservoir (see Fig.
[1.10](#fig:fig1_2_3){reference-type="ref" reference="fig:fig1_2_3"}b)
and the whole thing does fluctuate around all the different available
states with equal probability for each $composite$ state. But that does
not correspond to equal probability for all the $system$ states. If the
system is say in state, $1$, then corresponding to that the reservoir
has let's say, a certain number of states, $W_1$ (see Fig.
[1.11](#fig:fig1_2_4){reference-type="ref" reference="fig:fig1_2_4"}a).
Similarly, if the system is in state $2$, the reservoir has $W_2$ number
of states, and the point is that $W_1$ is larger than $W_2$.

![Introducing entropy, S](./Week1_2/fig1_2_4.jpg){#fig:fig1_2_4
width="\\textwidth"}

Why is that? Well, because you see, when the system has a lower energy,
the reservoir has a higher energy (see Fig.
[1.11](#fig:fig1_2_4){reference-type="ref" reference="fig:fig1_2_4"}b)
since together, they have a $fixed$ energy $E_0 + \varepsilon$. So when
the system gets a little more energy, it means that the reservoir has a
little less energy. That is the first point: lower system energy means
higher reservoir energy.

The second point is that if the reservoir has more energy then it will
also have more states that it can access (see Fig.
[1.11](#fig:fig1_2_4){reference-type="ref" reference="fig:fig1_2_4"}c).
Those are the two key points. Remember what we are trying to understand
is, why the system has a higher probability for being in a lower energy
state. The answer is, if the system has lower energy then the reservoir
has higher energy, and if it has higher energy, it can access a lot more
states.

Now, if I want to know the probability that the system will be in state
1, as opposed to in state 2, that ratio will be proportional to the
number of states of the reservoir that correspond to it (see Fig.
[1.12](#fig:fig1_2_5){reference-type="ref" reference="fig:fig1_2_5"}a) .
So $p_1/p_2 = W_1/W_2$. Let's say there are 100 states of the reservoir
for $W_1$ and only 10 for $W_2$. Then $p_1/p_2 = 100/10$, because state
$1$ of the system looks like $100$ states for the composite thing, while
state $2$ looks like $10$ states for the composite thing. Naturally the
composite thing is more likely to be in the 100 states than in the 10
states. That's the essential point.

This leads us to define something called entropy $S$ (see Fig.
[1.11](#fig:fig1_2_4){reference-type="ref" reference="fig:fig1_2_4"}d)
which is one of the very deep seminal concepts in statistical mechanics.
This $S$ is proportional to the logarithm of the number of states
available to the reservoir $S(E) = k\ln W(E)$). More the energy $E$, the
more the number of states available, so bigger the $W$ and bigger the
entropy. We can start from $S = k \ln{W}$ and turn it around to write
$W = \exp{(S / k)}$.

#### Fig. [1.12](#fig:fig1_2_5){reference-type="ref" reference="fig:fig1_2_5"} {#fig.-figfig1_2_5}

![Defining temperature T from entropy
S](./Week1_2/fig1_2_5.jpg){#fig:fig1_2_5 width="\\textwidth"}

So now we'll do a little algebra and go on from here and obtain the
Boltzmann law. We start from $p_1/p_2 = W_1/W_2$, where $W_1$ is the
value of this function W, for $E = E_0 + \varepsilon$
($W_1 = W(E_0+\varepsilon)$), while $W_2$ corresponds to the energy
$E_0$ ($W_2 = W(E_0)$). Now we replace $W$ in terms of entropy. This
gives us a ratio of exponentials like this
($\exp{(S(E_0+\varepsilon)/k)}/\exp{(S(E_0)/k)}$) which we can write it
as the difference between the two
($\exp{(S(E_0+\varepsilon)-S(E_0))}/k$).

Now this difference is something I will now approximate, using the fact
that the reservoir is a huge thing with a lot of energy and this
$\varepsilon$ is a small change in its energy. And so, we can write the
derivative of the entropy of the reservoir with respect to energy, in
this form, ($S(E_0+\varepsilon)-S(E_0)/\varepsilon$).

As you know when you first learn about derivatives in college, they
define it this way, in the limit as $\varepsilon$ tends to 0. And in
this case, we would argue that $\varepsilon$ being the energy of this
little system, it is kind of 0 in the context of the huge reservoir
energy. So you could write the derivative in this form (see Fig.
[1.12](#fig:fig1_2_5){reference-type="ref" reference="fig:fig1_2_5"}b).
What that means is, I could write this difference as $\varepsilon$ times
the derivative. So that's what I've done here. And then the key point is
that this derivative is what is defined as the inverse temperature of
the reservoir, that's what is called 1/$T$ (see Fig.
[1.12](#fig:fig1_2_5){reference-type="ref" reference="fig:fig1_2_5"}c).
And so now you can put it all together, we have this epsilon over $T$,
and then there's the $k$ here, which brings us to $\varepsilon/kT$.

#### Fig. [1.13](#fig:fig1_2_6){reference-type="ref" reference="fig:fig1_2_6"} {#fig.-figfig1_2_6}

![Obtaining Boltzmann law for canonical ensemble.
](./Week1_2/fig1_2_6.jpg){#fig:fig1_2_6 width="\\textwidth"}

So basically it says that the ratio of
$p_1/p_2 = \exp{(\varepsilon/kT)}$. And since $\varepsilon = E_2- E_1$
(see Fig. [1.13](#fig:fig1_2_6){reference-type="ref"
reference="fig:fig1_2_6"}), what we are saying is that $p_1/p_2$ =
($\exp{(-E_1/kT)} / \exp{(-E_2/kT)}$), which you can see is consistent
with the Boltzmann law. Boltzmann law says that the probability of any
state $i$, is proportional to $\exp{(-E_i/kT)}$. And what we showed in
the last few slides is that if I consider any 2 states of our system, 1
and 2, the ratio of their probabilities will be the ratio of these
exponentials. Which is consistent with exactly what the Boltzmann law
states.

### Fig. [1.14](#fig:fig1_2_7){reference-type="ref" reference="fig:fig1_2_7"}: Canonical ensemble {#fig.-figfig1_2_7-canonical-ensemble}

Recapping what we did, we're trying to figure out the probabilities for
the system. So we say that consider the entire system plus reservoir and
together the composite system will spend equal time in all possible
states. And so, the ratio of $p_1/p_2$, is proportional to the ratio of
the corresponding states of the reservoir. Which then can be written as
$\exp{(\varepsilon/kT)}$, where this inverse temperature is defined in
terms of the energy derivative of the entropy function,
$1/T=\mathrm{d}S/\mathrm{d}E$.

![Summary: Only energy exchange is involved (canonical
ensemble).](./Week1_2/fig1_2_7.jpg){#fig:fig1_2_7 width="\\textwidth"}

So that's what we have done. And the next few slides, let me just show
how this is derivation is extended to the grand canonical ensemble,
namely the case where you are also exchanging particles because
remember, I kind of simplified things a little by saying let's assume
particles are not exchanged only energy is. So when you exchange
particles as I mentioned before, the more general Boltzmann law would
not have just $E_i$ but would have $E_i-\mu N_i$. And what I had argued
before was that if $N_i$ were fixed, then you could essentially write it
this way $p_i=(1/Z)\exp{(-E_i/kT)}$, and that's the canonical ensemble.
Well, if you want to include the variations and particles, then what
would happen is $p_1/p_2$ would still be equal to this $W_1/W_2$, but
now, $W$ would be a function of both $E$ and $N$.

### Fig. [1.15](#fig:fig1_2_8){reference-type="ref" reference="fig:fig1_2_8"}: Grand canonical ensemble {#fig.-figfig1_2_8-grand-canonical-ensemble}

When they exchange particles, the total number of particles stays
constant. So the one that has a lower number of particles, would
correspond to a higher number for the reservoir. So just as we had
argued, if the reservoir had energy $E_0$ corresponding to $p_2$, then
it would have energy $E_0+\varepsilon$ corresponding to $p_1$, where
$\varepsilon$ is the energy difference.

![Summary: Both energy and particle exchanges are involved (grand
canonical ensemble).](./Week1_2/fig1_2_8.jpg){#fig:fig1_2_8
width="\\textwidth"}

Similarly, if the reservoir has $N_0$ particles corresponding to $p_2$,
then it would have $N_0 + n$ particles corresponding to $p_1$, where
this small $n$ represents the difference in the number of particles. And
what you can show is that this too can be written as
$\exp{((\varepsilon-\mu n)/kT)}$, where this extra factor this $-\mu/T$
now, is defined in terms of the derivative of the entropy function with
respect to $N$, $-\mu/T=\partial S/\partial N$. You see, previously we
wrote derivative of the entropy function with respect to energy as
$1/T$. Now we are writing derivative of the entropy function with
respect to the number of particles as $-\mu/T$. And when you put that in
there, you will get this relation $\exp{((\varepsilon-\mu n)/kT)}$,
which is consistent with the Boltzmann law as stated for the Grand
canonical ensemble. So, that kind of completes the overall derivation
here.

What needs more discussion is why we can define the temperature in terms
of $\partial S/\partial E$,
$\textit{irrespective of the details of the reservoir.}$ You see what I
said earlier is that Boltzmann Law applies to everything. It doesn't
matter how complicated your system is, it could be something complicated
like including superconducting elements for example. It could be a
strongly interacting system, or it could be something really simple,
like just a single level. It doesn't matter how complicated or simple it
is, the law is the same.

Now why is the law the same for all systems, irrespective of its
details? The answer is, well, it's because this is a property not of the
system but of the reservoir. And what it really reflects is the
non-obvious fact, that all normal reservoirs irrespective of details
kind of have this property. That if you look at the number of states
available the $W$ and define the entropy function in this way,
$S(E,N)=k\ln{W(E,N)}$ then, this $\partial S/\partial E$ would be $1/T$,
while $\partial S/\partial N$ would be $-\mu/T$ and this is irrespective
of exactly what the reservoir is comprised of. And that is not really
obvious, but in the next lecture, we'll try to clarify this point a
little when we talk more about this concept of entropy.

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