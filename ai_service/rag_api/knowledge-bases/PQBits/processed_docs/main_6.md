![\[W\] Matrix.](./Week3_5/figure9.jpg){#fig:fig3_5_9
width="\\textwidth"}

So this is what you could call a relatively simple special case of the
Feynman path integral. We can write the overall probability, as a sum
over paths, that is, this summation
$P_{f\leftarrow i}=\sum_{a_1,a_2,\ldots,a_{T-1}}{[W^{(T)}]_{f\leftarrow a_{T-1}}\cdots[W^{(2)}]_{a_2\leftarrow a_1}[W^{(1)}]_{a_1\leftarrow i}\{i\}}$.

Why sum over paths?

Well, you see, you could view this $a_1$, $a_2$, etc, as intermediate
states. In the sense you could think of it this way, that I started from
$\{i\}$, and I have a probability of going to different states in the
middle, $a_1$ is one such state, this could be 00, 01, 10, and 11, $a_2$
again could be 00, 01, 10, 11, etc. So if I put down a specific one,
then I have a specific path. So this is one possible path from $i$ to
$f$, and that path has a certain probability, which is obtained by
multiplying out the corresponding elements of your $[W]$ matrix. But
then there is, of course many, many paths, why? Because at each stage
I've got four possibilities. So as you go down the list, you have so
many possibilities, so many paths, a very large number of paths, and
each one has a certain probability and the overall probability that we
observe is a sum of the probabilities over all those paths.

#### Fig. [3.45](#fig:fig3_5_10){reference-type="ref" reference="fig:fig3_5_10"} {#fig.-figfig3_5_10}

Now, how do you actually calculate them? Well, it's probably much more
convenient to multiply out the matrices if you could have written them
down, but then they are huge matrices. So what we are really doing in
our sampling methods is we're saying look, doing this entire summation
by multiplying matrices, that's impossible, that's too hard.

So instead what we'll do is, we'll try to find which ones are the paths
with the highest probabilities, and we'll add them up and hopefully,
that will get us close enough to the correct answer. So these different
algorithms for sampling, like the Metropolis algorithm or Gibbs
sampling, all of these in the end I think are saying that, I can't do
this summation exactly, but I'll try to have an algorithm, so that I
pick out the ones with the highest probabilities and then I'll sum them
up, and try to get to the right answer.

![Sum over paths.](./Week3_5/figure10.jpg){#fig:fig3_5_10
width="\\textwidth"}

But one important conceptual value of this view is in connecting to the
quantum world. As we will see in Chapter 5, quantum problems are
described by a quantum transition matrix $U$ which is of size
$2^n \times 2^n$ just like the classical counterpart $W$ we have been
discussing. However, unlike $W$, it's elements are not positive numbers
but are complex numbers and instead of the probability distribution $P$
we have a complex probability amplitude or wavefunction $\psi$ whose
squared magnitude gives the probability.

But the mathematics is very similar and we can express the final
wavefunction as a sum over Feynman paths. Indeed you will see this
concept of Feynman paths more often in the context of quantum problems.
But there's a very big difference, between adding probabilities and
adding probability amplitudes. Probabilities are always positive and so
when you add them up, they tend to converge relatively easily, because
it's all positive numbers that you're adding up. But if you're adding
complex numbers or even numbers that are both positive and negative, you
can get a small number by adding and subtracting huge numbers, like if
you had $+100$ and $-99$ and they give you $1$, that's a harder number
to get it right, because you miss one sample, and you get a totally
wrong answer.

So these things don't converge easily, and that is where the strength of
quantum computing lies. Quantum bits or q-bits can actually do these
summations "instinctively\". It is as if they kind of sense all these
paths and add up their complex amplitudes, and behave accordingly. A
classical sampling algorithm in order to figure out all these
cancellations, would actually have to sum many, many samples to get it
right. The challenge of quantum computing, however, is that in order to
sum complex amplitudes accurately it needs stringent control of the
phase of different paths, and there is a worldwide effort to achieve
that with different physical representations of q-bits. By contrast,
$p$-$bits$ can be built with existing technology operating at room
temperature.

### Quiz

#### Question 1

A system with just one spin has a transition matrix given by W =\
$\left [ \begin{array}{r r}
0.1 & \ 0.3  \\
0.9 & \ 0.7  \\
\end{array} \right ]$

It evolves from an initial state 0 at t, to a final state at t+2 after 2
time steps. What is the probability that it took the path
$0 \rightarrow 1 \rightarrow 1$?[^49]

#### Question 2

A system of three spins evolves from an intial state 000 at $t$ to a
final state 111 at t+10 after ten steps. How many Feynman paths leading
from an initial 0 to a final 1. [^50]

#### Question 3

A system of four spins evolves from an intial state 0000 at $t$ to a
final state 1111 at t+10 after ten steps. How many Feynman paths leading
from an initial 0 to a final 1. [^51]

## Fig. [3.46](#fig:fig3_6_2){reference-type="ref" reference="fig:fig3_6_2"}: 5-minute summary {#fig.-figfig3_6_2-5-minute-summary}

This is [Chapter 3 summary: Watch youtube video, after
2:05](https://www.youtube.com/watch?v=eQCxUi3yFmw)

In week 3, we introduced this transition matrix method. In Chapter 2 we
had these two methods, namely the direct Boltzmann probabilities, and
the sampling method. Now, in Chapter 3 we have introduced a third method
based on the transition matrix from which also you could calculate the
stationary probability distribution. We first use it to discuss the
sampling method, why it works, why it is important to update $p$-$bits$
sequentially and not simultaneously. Then in the fourth lecture, we
talked about the Bayesian networks which are widely used and behave very
differently from the Boltzmann networks that we largely focus on.

![Week 2.](./Week3_6/Picture2.png){#fig:fig3_6_2 width="\\textwidth"}

Finally, we talked about Feynman paths which gives you a nice conceptual
picture, of how to think about these probabilistic circuits using $W$
matrices and it provides you a conceptual bridge to our next topic,
which is about quantum computing where instead of probabilities evolving
through stochastic $W$ matrices, we have complex probability amplitudes
or wavefunctions evolving through unitary $U$ matrices.

# Quantum Boltzmann Law

## Quantum Spins

This is [Lecture 4.1: Watch youtube
video](https://www.youtube.com/watch?v=7niePxinYAg)

Now, Chapters 4 and 5, that's the quantum part of this course. Loosely
speaking, they are the quantum counterparts of Chapters 2 and 3.
Mathematically, as you'll see in this chapter we'll introduce this
equation, which looks like a lot like the classical Boltzmann Law. It's
just that instead of a probability distribution function, we have this
density matrix. And instead of energy you have the energy matrix or the
Hamiltonian.

And in chapter 5, we'll introduce this quantum transition matrix which
loosely corresponds to the classical transition matrix, where you had a
probability distribution function that evolved with time. Here you have
a wave function that evolves with time. Anyway, so let's get started
with the quantum Boltzmann law.

### Figs. [4.1](#fig:fig4_1_1){reference-type="ref" reference="fig:fig4_1_1"}-[4.3](#fig:fig4_1_3){reference-type="ref" reference="fig:fig4_1_3"}: Classical spin {#figs.-figfig4_1_1-figfig4_1_3-classical-spin}

#### Fig. [4.1](#fig:fig4_1_1){reference-type="ref" reference="fig:fig4_1_1"}: {#fig.-figfig4_1_1}

So how do you go from this Classical Boltzmann Law to what I call this
Quantum Boltzmann Law? Now, in order to make this transition, it is
convenient to start from the bipolar representation. If you remember in
lecture 2.4, we introduced this bipolar representation, which is
equivalent to the binary representation which we commonly used in
chapters 2 and 3. In binary representation the spin has the values $1$
and $0$, whereas in the bipolar representation it has the values $+1$
and $-1$. Now, for the purposes of making this transformation to the
Quantum Boltzmann law, the bipolar one is more convenient, it
corresponds more directly, okay? So this is where we'll start.

![Classical binary and bipolar
representations](./Week4_1/Picture1.png){#fig:fig4_1_1
width="\\textwidth"}

#### Fig. [4.2](#fig:fig4_1_2){reference-type="ref" reference="fig:fig4_1_2"} {#fig.-figfig4_1_2}

![Classical bipolar spin versus 3-D
spin](./Week4_1/Picture2.png){#fig:fig4_1_2 width="90%"}

Now, for starters, let's ignore this interaction term and just think of
one spin, right? In lectures 3 and 4 of this chapter we'll pick up the
interactions. For the moment, let's just focus on one spin. But what we
want to describe now is quantum spins. And the best example of that is a
single electron because every electron is actually like a little magnet
but it's a quantum magnet, as we mentioned in the Prologue, see
Fig.[0.2](#fig0_3){reference-type="ref" reference="fig0_3"}. And what
I'll try to describe in this lecture is what that means and how you
describe it.

So this elementary magnet you might think, okay, I've got this electron
it has no particular preferred direction. Unlike a magnet where you
could say okay, this is the long axis. Well, the electron has no
particular axis, it could point in any direction. And so you might say,
well, what I really need to do is take my basic description that I had
before and turn it into a 3D spin, something where the magnetization of
the magnetic moment can have a three components $m_x$, $m_y$, and $m_z$,
and instead of this one parameter $h$, allow her $h_x$ and $h_y$ and
$h_z$. I could write the energy as say $\vec{h}\cdot\widehat{m}$.

But a quantum magnet is neither a classical bipolar magnet or a
classical 3-D magnet, you could say it is something in-between.

#### Fig. [4.3](#fig:fig4_1_3){reference-type="ref" reference="fig:fig4_1_3"} {#fig.-figfig4_1_3}

![What we expect to see for classical 3-D
spin](./Week4_1/figure3.jpg){#fig:fig4_1_3 width="\\textwidth"}

![Experiment shows that a quantum spin can point in any 3D direction,
but any measurement will yield a bipolar
result!](./Week4_1/Picture4.png){#fig:fig4_1_4 width="90%"}

What would we expect to see if the electron were a 3-D classical spin?
Suppose we put all $h$'s equal to 0, then the energy is equal to 0,
which means regardless of which direction this elementary magnet points,
the energy is the same. And so you can apply Boltzmann Law and say, all
directions have equal energy and hence equal probability. Well, so if I
went in and measured a particular component of the spin or the magnetic
moment, say the $z$-component or the $x$-component or the $y$-component,
you'd think that you'd get all values between $-1$ and $+1$. Because
after all the magnet could be pointing in any direction, and so
$z$-component could have any value, between the extremes.

### Figs. [4.4](#fig:fig4_1_4){reference-type="ref" reference="fig:fig4_1_4"}-[4.5](#fig:fig4_1_5){reference-type="ref" reference="fig:fig4_1_5"}: Quantum spins {#figs.-figfig4_1_4-figfig4_1_5-quantum-spins}

#### Fig. [4.4](#fig:fig4_1_4){reference-type="ref" reference="fig:fig4_1_4"}: {#fig.-figfig4_1_4}

Well, what 100 years ago, Stern and Gerlach reported this experiment,
which essentially revolutionized our conception of electron (see Fig.
[4.4](#fig:fig4_1_4){reference-type="ref" reference="fig:fig4_1_4"}),
and what they showed was that when they measured $m_x$ or $m_z$ or
$m_y$, there's only two values $-1$ and $+1$, not this continuous
spectrum of values. In short, a quantum spin can point in any 3D
direction, but any measurement will yield a bipolar result!

Of course, in science, facts come first, and so if the facts don't fit
the math, then you have to change the math. So what is the new math that
will fit the new facts?

#### Fig. [4.5](#fig:fig4_1_5){reference-type="ref" reference="fig:fig4_1_5"}: {#fig.-figfig4_1_5}

![Quantum Spin.](./Week4_1/Picture5.png){#fig:fig4_1_5 width="90%"}

So that's how the quantum theory started. And in the quantum theory
then, the $m$, this magnetic moment gets replaced by a operator
$\vec{\sigma}$, which as you'll see is a $2\times2$ matrix. So instead
of $\vec{h}\cdot\, \widehat{m}$, you write this energy matrix or what's
called the Hamiltonian matrix $H$, which is $\vec{h}\cdot\vec{\sigma}$
(see Fig. [4.5](#fig:fig4_1_5){reference-type="ref"
reference="fig:fig4_1_5"}).

Now, what is this $\vec{\sigma}$? Well, we have these three Pauli spin
matrices, one corresponding to each direction, $\sigma_z$, $\sigma_x$
and $\sigma_y$, and these are the three matrices and so
$\vec{h}\cdot\vec{\sigma}$ means $h_x\sigma_x+h_y\sigma_y+h_z\sigma_z$
and when you measure any quantity, let's say you want to know, I
measured $m_z$, what values will I get? And the answer is the
measurement will only yield eigenvalues of the corresponding operator.
So what are the eigenvalues?

Well, for $\sigma_z$ since its diagonal, it's easy to see the
eigenvalues it's $+1$ and $-1$, whatever is on the diagonal. But what
about $\sigma_x$? Well, it's not as easy to see, but you can check for
the eigenvalues and the answer is still $+1$ and $-1$ (see Fig.
[4.5](#fig:fig4_1_5){reference-type="ref" reference="fig:fig4_1_5"}).
And if you look at $\sigma_y$, it looks different, but here too the
eigenvalues are $+1$ and $-1$. So whether you measure $m_z$ or $m_x$ or
$m_y$, what you'll measure will be the eigenvalues of the corresponding
operator and those are $-1$ and $+1$. And that obviously fits the fact
here.

### Fig. [4.6](#fig:fig4_1_6){reference-type="ref" reference="fig:fig4_1_6"}: Density matrix {#fig.-figfig4_1_6-density-matrix}

![Density Matrix](./Week4_1/Picture6.png){#fig:fig4_1_6
width="\\textwidth"}

Now, quantitatively how do we predict probabilities of measuring $-1$
and $+1$? So that is where this density matrix comes in (see Fig.
[4.6](#fig:fig4_1_6){reference-type="ref" reference="fig:fig4_1_6"}). So
classically the probability was as you know, related to the energy. Now
we have a density matrix, which is $\exp{(-H)}$, $H$ being this energy
matrix or Hamiltonian matrix.

A little side note. This $H$ matrix is Hermitian. And Hermitian means
that the matrix is equal to it's conjugate transpose. So if you look at
the $(i,j)$ component, it is equal to the complex conjugate of the
$(j,i)$ component. So all these three spin matrices you will notice are
Hermitian. $\sigma_z$ is Hermitian because there isn't any off-diagonal
element and $h_{ii}$ and the diagonal elements $h_{11}$ or $h_{22}$,
those are all real. So they are of course, equal to their complex
conjugate. And $\sigma_x$ again you'll notice 1 is equal to its complex
conjugate and here also in $\sigma_y$, $-i$ is equal to the complex
conjugate of $+i$. So $H$ is Hermitian, and so is $\rho$ which is
obtained by exponentiating this $H$, and I should note that this
exponentiation is in a matrix sense, not an element by element sense.
And these will become clear when we look at the actual examples.

Now, if you write out this matrix, then this Hermitian matrix, it will
always have the form shown: there will be real quantities $a,b$ on the
diagonal. The off-diagonal elements can be complex, but then they'll be
complex conjugates, $c$ and $c^*$.

### Figs. [4.7](#fig:fig4_1_7){reference-type="ref" reference="fig:fig4_1_7"}-[4.10](#fig:fig4_1_10){reference-type="ref" reference="fig:fig4_1_10"}: Predicting measurements {#figs.-figfig4_1_7-figfig4_1_10-predicting-measurements}

#### Figs. [4.7](#fig:fig4_1_7){reference-type="ref" reference="fig:fig4_1_7"}: {#figs.-figfig4_1_7}

Now, these diagonal elements basically give you the probability of
measuring $m_z$ equals $+1$ or $-1$ (see Fig.
[4.7](#fig:fig4_1_7){reference-type="ref" reference="fig:fig4_1_7"}).
Now, what about $m_x$ and $m_y$? Well, you might be tempted to say that
I should look at the off diagonal terms. Well, no, that won't quite work
because after all, these off-diagonal elements are complex and they
cannot be interpreted as probability.

![Predicting Measurements](./Week4_1/Picture7.png){#fig:fig4_1_7
width=".75\\textwidth"}

![Predicting Measurements
(contd.)](./Week4_1/Picture8.png){#fig:fig4_1_8 width="\\textwidth"}

#### Fig. [4.8](#fig:fig4_1_8){reference-type="ref" reference="fig:fig4_1_8"} {#fig.-figfig4_1_8}

The general rule for predicting measured values is the following. Given
any quantity $S$, there is a corresponding operator $S_{op}$. And the
way you find the average value of that quantity is by taking the *trace*
of this operator times the density matrix and when you take *trace*, it
doesn't matter in what order you multiply the matrices. So you could
multiply the density matrix times the operator, answer would be the
same. So if you wanted $m_x$, well, you take whatever density matrix you
have and multiply it by the operator representing $m_x$, which is
$\sigma_x$, and then take the *trace* and you'd have the average value.
Same procedure if you want $m_y$, except that you use the operator
representing $m_y$, which is $\sigma_y$.

Now, what if I wanted to predict the value of the correlation between
$m_x$ and $m_y$? So I go and measure both $m_x$ and $m_y$, and I want to
know the average value of the product. And you might say, well, that's
simple, I could define the operator for $m_x m_y$ as $\sigma_x\sigma_y$.
Well, not quite, because what's not clear is whether I should use
$\sigma_x\sigma_y$ or $\sigma_y\sigma_x$? And now when you are talking
of numbers like $m_x$ and $m_y$, of course, the order doesn't matter,
but here we have matrices. With matrices, $A$ times $B$ is not
necessarily equal to $B$ times $A$. And in this case, actually it isn't,
you can check it out. If you take $\sigma_x$ times $\sigma_y$, you'll
get $+i\sigma_z$. And if you take $\sigma_y$ times $\sigma_x$, you'll
get $-i\sigma_z$, and neither of these is actually Hermitian, anyway. So
the bottom line is if you really wanted to know the expectation value of
$m_xm_y$, the quantum theory I just described to you wouldn't give you
an answer? Well, then how do we use quantum theory?

And the answer is that well, experimentally there is no way to measure
$m_x$ and $m_y$ simultaneously. If you could, then you see quantum
theory would essentially fail. But it stands on the general experimental
fact that for these elemental magnets, there is no way to measure two
components simultaneously. You can either measure $x$ or $y$ or $z$, but
not any two of them. In general, whenever you have two operators, if
they do not commute, meaning if $AB$ is not equal to $BA$, then you
cannot measure them simultaneously.

#### Fig. [4.9](#fig:fig4_1_9){reference-type="ref" reference="fig:fig4_1_9"} {#fig.-figfig4_1_9}

![Useful Property](./Week4_1/Picture9.png){#fig:fig4_1_9 width="80%"}

Note that the Pauli spin matrices have this cyclic property shown in the
figure. This is a very useful property that often comes in handy.

#### Fig. [4.10](#fig:fig4_1_10){reference-type="ref" reference="fig:fig4_1_10"} {#fig.-figfig4_1_10}

![Finding Z](./Week4_1/Picture10.png){#fig:fig4_1_10
width="\\textwidth"}

Now, one last thing, and that is to calculate the probability, as you
know, you also need to figure out the constant in front. And in the
classical case, the idea is that all probabilities must add up to $1$.
And so this constant $Z$ is actually the sum of all the exponentials.
The corresponding thing for the quantum law is, that you see that
diagonal elements of the density matrix they represent a probability,
and they must add up to $1$, which means the trace of $\rho$ must be
equal to $1$. And that leads to the condition that $Z$ should be equal
to $\text{Trace}\left(\exp{(-H)}\right)$.

So to sum up then what we did in this lecture was introduced this
quantum version of the energy, which gives us this Hamiltonian matrix
$H$. And you can use this matrix to find the density matrix which is
like the quantum version of probability. And once you have the density
matrix, you can predict the expected measured value of any quantity: For
whatever quantity you're interested in, you have to figure out the
corresponding operator and then find the trace of the opertaor times the
density matrix. In the next lecture we'll look at an example of a one
q-bit system and apply the rules we just laid down.

### Quiz

#### Question 1

Suppose the density matrix is given by

$\rho = \frac{1}{2} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ 1  \\
\end{array} \right ]$\
What is the expected value $\langle m_x \rangle$ of the spin in the
x-direction?[^52]

#### Question 2

Suppose the density matrix is given by

$\rho = \frac{1}{2} \left [ \begin{array}{r r}
+1 & \ -1  \\
-1 & \ +1  \\
\end{array} \right ]$\
What is the expected value $\langle m_x \rangle$ of the spin in the
x-direction?[^53]

#### Question 3

Consider the Pauli spin matrices

$\sigma_x = \left [ \begin{array}{r r}
+1 & \ 0  \\
0 & \ -1  \\
\end{array} \right ]$, $\sigma_y = \left [ \begin{array}{r r}
0 & \ -i  \\
+i & \ 0  \\
\end{array} \right ]$, $\sigma_z = \left [ \begin{array}{r r}
0 & \ 1  \\
1 & \ 0  \\
\end{array} \right ]$\
What is the matrix $\sigma_x \sigma_y - \sigma_y \sigma_x$?[^54]

## One q-bit system

This is [Lecture 4.4: Watch youtube
video](https://www.youtube.com/watch?v=bg9EZaytvQ8)

In the last lecture, we introduced this quantum energy matrix or the
Hamiltonian matrix where you replace the classical spin variable with a
spin operator, $\sigma$, with three components $\sigma_z$, $\sigma_x$,
and $\sigma_y$, each one of which is a two by two matrix. You can
calculate the quantum probability matrix or what's called the density
matrix, $\rho=(1/Z)\exp{(-H)}$ from $H$, and knowing the operator $S$
for a particular observable $S$, you can calculate its expectation value
from $\textit{trace} [\rho S]$.

Now, what we'll do in this lecture is work out a specific example which
should give you a more concrete feeling for how this whole thing works.

### Fig. [4.11](#fig:fig4_2_1){reference-type="ref" reference="fig:fig4_2_1"}: Hamiltonian {#fig.-figfig4_2_1-hamiltonian}

![Hamiltonian.](./Week4_2/figure1.jpg){#fig:fig4_2_1
width="\\textwidth"}

Now, for a single q-bit, the energy matrix is given by,
$H=\vec{h}\cdot\vec{\sigma}$, which you can write as,
$H= h_x \sigma_x + h_y \sigma_y + h_z \sigma_z$. Now for this example,
we'll assume that $h_y$ is 0. You could put in a nonzero $h_y$ as well,
it's just that algebra looks more messy, so we'll put that to 0 for this
discussion, and assume that $\vec{h}$ lies in the $z$-$x$ plane,
pointing in some direction $\theta$ from the $z$-axis.

So what does the energy matrix look like then? A little algebra leads us
to the result shown with $h \cos{\theta}$ on the diagonal and
$h \sin{\theta}$ off diagonal.

### Figs. [4.12](#fig:fig4_2_2){reference-type="ref" reference="fig:fig4_2_2"}-[4.14](#fig:fig4_2_4){reference-type="ref" reference="fig:fig4_2_4"}: Density matrix {#figs.-figfig4_2_2-figfig4_2_4-density-matrix}

#### Fig. [4.12](#fig:fig4_2_2){reference-type="ref" reference="fig:fig4_2_2"}: {#fig.-figfig4_2_2}

![Density Matrix](./Week4_2/figure2.jpg){#fig:fig4_2_2
width="\\textwidth"}

Now, so we have written down the energy matrix, now to find the density
matrix, that's this probability matrix, we need to evaluate this
quantity, $(1/Z)\exp{(-H)}$ (see Fig.
[4.12](#fig:fig4_2_2){reference-type="ref" reference="fig:fig4_2_2"}).
So how would we do that? We need the $\exp{(-H)}$. Now, this question is
how do we evaluate $\exp{(-\vec{h}\cdot\vec{\sigma})}$? Remember, this
exponentiation is not in an element by element sense, it is in the
matrix sense.

Now, the general approach to finding any function of a matrix works like
this, given a matrix $M$, you first diagonalize it. You find the
transformation, $VMV^{\dagger}$ that will turn it into a diagonal
matrix. These transformations work also in reverse that is from diagonal
matrix you can go back to the original by applying $V ^{\dagger}$ and
then $V$, in that order, $M=V^{\dagger} DV$. Remember we are writing
this $V ^{\dagger}$ to denote Hermitian conjugate, which is the
conjugate transpose.

Now, the way you proceed to find any function is the following, that
given a diagonal matrix, the function is simply the functions of the
diagonal elements and the off diagonal stays 0 (see Fig.
[4.12](#fig:fig4_2_2){reference-type="ref" reference="fig:fig4_2_2"}).
So after you have transformed it, So you find the function in the
transformed bases and then transform it back. So this is a general
procedure for finding any function.

Of course, if you're calculating things numerically, you do not have to
worry about this. There's a command in MATLAB^®^ or in Python that will
do just that. It's EXPM, that if you leave out the M, just say EXP, then
it will get you the element by element exponentiation, which is not what
we want, we want the EXPM.

Anyway, we are trying to do this analytically without invoking numerical
computations. Then what you can show with some algebra is that any
function of this quantity $-\vec{h}\cdot\vec{\sigma}$ can be written as,
$f(-\vec{h}\cdot\vec{\sigma})=[I]((f(h)+f(-h))/2) - [\vec{h}\cdot\vec{\sigma}] ((f(h)-f(-h))/2h)$.

#### Fig. [4.13](#fig:fig4_2_3){reference-type="ref" reference="fig:fig4_2_3"}: {#fig.-figfig4_2_3}

![Density Matrix.](./Week4_2/figure3.jpg){#fig:fig4_2_3
width="\\textwidth"}

So if we use this relation along with the result we obtained earlier for
${\vec{h}\cdot\vec{\sigma}}$ we get the result shown:
$\exp{(-\vec{h}\cdot\vec{\sigma})} = [I]\cosh{(h)}-([-\vec{h}\cdot\vec{\sigma}]/h)\sinh{(h)}$.

#### Fig. [4.14](#fig:fig4_2_4){reference-type="ref" reference="fig:fig4_2_4"}: {#fig.-figfig4_2_4}

![Finding Z.](./Week4_2/Picture4.png){#fig:fig4_2_4 width="\\textwidth"}

Finally to get the density matrix, I also need to know this number in
front $Z$, and what is $Z$? Well, I need to take the trace of
$\exp{(-\vec{h}\cdot\vec{\sigma})}$. Now, what is the ? Well, for the
identity matrix, the trace is 2, it's 1 plus 1. For all these $\sigma$
matrices, the is 0. So the trace of $\exp{(-\vec{h}\cdot\vec{\sigma})}$
is $2 \cosh{(h)}$, and that's the Z. So now, we can write down the
density matrix $\rho$ as shown.

### Figs. [4.15](#fig:fig4_2_5){reference-type="ref" reference="fig:fig4_2_5"}-[4.17](#fig:fig4_2_8){reference-type="ref" reference="fig:fig4_2_8"}: Predicting $m_z$ {#figs.-figfig4_2_5-figfig4_2_8-predicting-m_z}

#### Fig. [4.15](#fig:fig4_2_5){reference-type="ref" reference="fig:fig4_2_5"}: {#fig.-figfig4_2_5}

![Predicting $m_z$.](./Week4_2/figure5.jpg){#fig:fig4_2_5
width="\\textwidth"}

![Predicting $P_{+z}$ and
$P_{-z}$.](./Week4_2/figure7.jpg){#fig:fig4_2_7 width="\\textwidth"}

Now, we can file that away, because this density matrix is what we need
to calculate any quantity of interest. We'll look at different operators
and how to find the expected value, and how to predict the results of
measurements of different quantities.

Let us say you want to know the average value of $m_z$. Okay, then I am
supposed to take the of $\sigma_z$ times the density matrix and when I
multiply those two quantities take the trace I get
$\rho_{11}- \rho_{22}$. From our result for the density matrix we know
that $\rho_{11}=0.5(1-\tanh{(h)}\cos{\theta})$ and
$\rho_{22}=0.5(1+\tanh{(h)}\cos{\theta})$ and the difference is
$\langle m_z \rangle = -tanh(h) cos(\theta)$.

#### Fig. [4.16](#fig:fig4_2_7){reference-type="ref" reference="fig:fig4_2_7"} {#fig.-figfig4_2_7}

So we have seen that $m_z$ = $\rho_{11}- \rho_{22}$. Now, one thing I
should point out is that you could interpret $\rho_{11}$ and $\rho_{22}$
as the probability that the spin will have a value $+1$ and $-1$
respectively. How do you see that? By writing down the operators
representing the probability of the spin being $+1$ or $-1$ as shown. We
then get $P_{+z} = \rho_{11}$ and $P_{-z} = \rho_{22}$ and the
difference is what gives you the average value $\langle m_z \rangle$.

#### Fig. [4.17](#fig:fig4_2_8){reference-type="ref" reference="fig:fig4_2_8"} {#fig.-figfig4_2_8}

![Predicting
$\langle m_{x} \rangle$.](./Week4_2/figure8.jpg){#fig:fig4_2_8
width="\\textwidth"}

One more example. Suppose you want the average value of $m_x$, then you
take the operator for $m_x$ namely $\sigma_x$, multiply it by the
density matrix and take the as shown. In this case, you can show that
what you'll get is $\rho_{12}+\rho_{21}$, now, those it will depend on
the off diagonal terms, and we'll add it up, add those two, and you'll
get this answer, $-\tanh{(h)}\sin{\theta}$, that would be
$\langle m_x \rangle$.

So the point I am trying to make is that any question you want to ask in
this quantum framework, what you have to do is figure out the
corresponding operator. And then you can multiply it with the density
matrix and take the , and you'd have your answer, that's the message.

### Quiz

#### Question 1

A single quantum spin has a Hamiltonian matrix
$H = \overrightarrow{h}\cdot\overrightarrow{\sigma}$. If $h_z= h_x=0$
,$h_y \neq 0$ , what is \[H\]?[^55]

#### Question 2

A single quantum spin has a Hamiltonian matrix
$H = \overrightarrow{h}\cdot\overrightarrow{\sigma}$. If $h_z= 0$
,$h_x \neq 0$, $h_y \neq 0$ , what is \[H\]?[^56]

#### Question 3

The density matrix is given by

$\rho = \frac{1}{2} \left [ \begin{array}{r r}
1-tanh(h) cos(\theta) & \ -tanh(h) sin(\theta)  \\
-tanh(h) sin(\theta) & \ 1+tanh(h) cos(\theta)  \\
\end{array} \right ]$

What is the expectation value $\langle m_z \rangle$?[^57]

## Spin-Spin Interactions

This is [Lecture 4.3: Watch youtube
video](https://www.youtube.com/watch?v=pIN7onHvAxg)

In the first two lectures we have seen how we can write down the energy
or Hamiltonian matrix for one quantum spin, and use it to obtain the
density matrix, from which we can calculate the expectation value of any
quantity $S$ if we can write down the operator $S_{op}$ corresponding to
it. In this lecture we will see how we write down the energy matrix for
multiple spins with interactions, which can then be used to calculate
the density matrix and make predictions.

### Figs. [4.18](#fig:fig4_3_1){reference-type="ref" reference="fig:fig4_3_1"}-[4.19](#fig:fig4_3_2){reference-type="ref" reference="fig:fig4_3_2"}: Interaction Hamiltonian {#figs.-figfig4_3_1-figfig4_3_2-interaction-hamiltonian}

#### Figs. [4.18](#fig:fig4_3_1){reference-type="ref" reference="fig:fig4_3_1"}: {#figs.-figfig4_3_1}

In the last two lectures, we wrote the energy for just one spin. If
there are two non-interacting spins, then it's easy, you just add the
second one. The classical picture would be
$\widetilde{E}=\overrightarrow{h_1}\cdot\hat{m}_1 + \overrightarrow{h_2}\cdot\hat{m}_2$,
and the corresponding quantum picture would be
$H=\overrightarrow{h_1}\cdot\overrightarrow{\sigma_1} + \overrightarrow{h_2}\cdot\overrightarrow{\sigma_2}$.

![Interactions.](./Week4_3/figure1.jpg){#fig:fig4_3_1
width="\\textwidth"}

If you want to include interactions, then classically you would add $J$
times this interaction term times $\hat{m}_1\cdot\hat{m}_2$.
Correspondingly in the quantum picture you'd have
$\overrightarrow{\sigma_1}\cdot\overrightarrow{\sigma_2}$.

#### Fig. [4.19](#fig:fig4_3_2){reference-type="ref" reference="fig:fig4_3_2"}: {#fig.-figfig4_3_2}

![Interactions.](./Week4_3/Picture2.png){#fig:fig4_3_2
width="\\textwidth"}

Now if you write it out, you will see all the components,
$h_{1x}\sigma_{1x}$, etc. and here, $\vec{\sigma_1}\cdot\vec{\sigma_2}$
means $\sigma_{1x}\sigma_{2x}$, $\sigma_{1y}\sigma_{2y}$,
$\sigma_{1z}\sigma_{2z}$. By the way I've written $J_x$, $J_y$, $J_z$
because in general, those three could be different, although in Fig.
[4.19](#fig:fig4_3_2){reference-type="ref" reference="fig:fig4_3_2"} I
had assumed the same $J$ for all three components.

Okay, now, the tricky part is that actually when you have two spins,
this energy matrix is $2^2\times2^2$. If it were $n$ spins, it will be
$2^n$ by $2^n$. So it's a matrix in this $2^2$ space, whereas the
matrices we had written down earlier, those were $2\times2$ matrices,
the Pauli spin matrices. So question is, how do we write down these
2-spin matrices, which are $4\times4$? If we knew how to do that, then
after that, it's straightforward again. You have the energy matrix, you
can calculate density matrix, and then calculate any operator.

### Figs. [4.20](#fig:fig4_3_3){reference-type="ref" reference="fig:fig4_3_3"}-[4.21](#fig:fig4_3_4){reference-type="ref" reference="fig:fig4_3_4"}: 2-spin matrices {#figs.-figfig4_3_3-figfig4_3_4-2-spin-matrices}

#### Fig. [4.20](#fig:fig4_3_3){reference-type="ref" reference="fig:fig4_3_3"}: {#fig.-figfig4_3_3}

So supposing we want to write $\sigma_{1x}$, which means the x-directed
spin of spin 1. So for 1, I have $\sigma_x$ but for 2, I do nothing
which is represented by the identity matrix. So the corresponding
operators are $\sigma_x$ and $I$, but you have to take the Kronecker
product of the two: kron($\sigma_x$,$I$).

Now, how does this Kronecker product work? It's not a matrix product.
With matrix products, if you took a $2 \times 2$ matrix and multiply by
another $2 \times 2$ matrix, you would have got another $2 \times 2$
matrix, but when you take this Kronecker product or tensor product, you
actually get a $4 \times 4$ matrix, using the procedure shown.

![2-spin Matrices.](./Week4_3/figure3.jpg){#fig:fig4_3_3
width="\\textwidth"}

#### Fig. [4.21](#fig:fig4_3_4){reference-type="ref" reference="fig:fig4_3_4"}: {#fig.-figfig4_3_4}

Now, if you want $\sigma_{2x}$, which means I want the $x$ component of
the spin two, then you see it's a little different, we want
kron($I$,$\sigma_x$), since I have labeled the order of the spins in my
mind as 1 and then 2. And the point to note is that for the Kronecker
product, the order matters: $kron(I,\sigma_x) \neq kron(\sigma_x,I)$. Of
course, if you're using MATLAB or Python, that's what the computer would
do for you and give you the $4 \times 4$ matrices, which are different
for $\sigma_{1x}$ and $\sigma_{2x}$ as shown.

![2-spin Matrices.](./Week4_3/figure4.jpg){#fig:fig4_3_4
width="\\textwidth"}

### Figs. [4.22](#fig:fig4_3_5){reference-type="ref" reference="fig:fig4_3_5"}-[4.26](#fig:fig4_3_9){reference-type="ref" reference="fig:fig4_3_9"}: Product matrices {#figs.-figfig4_3_5-figfig4_3_9-product-matrices}

#### Fig. [4.22](#fig:fig4_3_5){reference-type="ref" reference="fig:fig4_3_5"}: {#fig.-figfig4_3_5}

Once we have the $4 \times 4$ matrices representing $\sigma_{1x}$ and
$\sigma_{2x}$, finding their product $\sigma_{1x}\sigma_{2x}$ is
straightforward matrix multiplication. What if I multiply them in
reverse order, $\sigma_{2x}\sigma_{1x}$? Interestingly, you end up with
the same matrix at the end, indicating that the matrices $\sigma_{1x}$
and $\sigma_{2x}$ $\textit{commute}$. Indeed you would have got the same
answer if you had taken the Kronecker product
$kron(\sigma_{x},\sigma_{x})$.

The fact that we get the same matrix for both $\sigma_{1x}\sigma_{2x}$
and $\sigma_{2x}\sigma_{1x}$ means that we can identify it as the
operator for $m_{1x}m_{2x}$ without any ambiguity. Experimentally the
question we are asking is, what is the expectation or average value of
the product of the measurement of $x$ spin on spin 1 and $x$ spin on
spin 2? When I measure the $x$ spin of spin 1, I get $+1$ or $-1$, and
the same for the $x$ spin of spin 2, and I want to know what is the
average value of the product. Well, to answer this question I should be
using the operator $\sigma_{1x}\sigma_{2x}$ = $\sigma_{2x}\sigma_{1x}$.

![$\sigma_{1x}\sigma_{2x}$ and
$\sigma_{2x}\sigma_{1x}$](./Week4_3/figure5.jpg){#fig:fig4_3_5
width="\\textwidth"}

#### Fig. [4.23](#fig:fig4_3_6){reference-type="ref" reference="fig:fig4_3_6"}: {#fig.-figfig4_3_6}

Now, what if I wanted to know the $x$ spin on 1 and the $y$ spin on 2?
Well, then the operator would be like $\sigma_x\times\sigma_y$, or you
could write $\sigma_{1x}\sigma_{2y}$ or $\sigma_{2y}\sigma_{1x}$. You
can multiply them in either order and again you get the same answer. And
it is exactly the matrix you would have got if you just Kroneckered
$\sigma_x$ and $\sigma_y$. So this is how you would write the operator
for answering questions about measurements of $x$ spin on 1 and $y$ spin
on 2: $\langle m_{1x} m_{2y} \rangle$

![$\sigma_{1x}\sigma_{2y}$ =
$\sigma_{2y}\sigma_{1x}$](./Week4_3/figure6.jpg){#fig:fig4_3_6
width="\\textwidth"}

#### Fig. [4.24](#fig:fig4_3_7){reference-type="ref" reference="fig:fig4_3_7"}: {#fig.-figfig4_3_7}

Now, you might say, well, what if I want to know the $x$ spin and $y$
spin, but on spin 2, both on spin 2? Now, if you remember from our first
lecture, this is something quantum mechanics says you cannot do because
you can never measure the two components on the same spin and indeed, if
you try to write the operator for this, you'd get in trouble. We end up
with different matrices for $\sigma_{2x}\sigma_{2y}$ and for
$\sigma_{2y}\sigma_{2x}$.

Actually one is the negative of the other. You could show is that one is
$+i \sigma_{2z}$, and the other is $-i \sigma_{2z}$, and this is related
to the identity I had mentioned in Lecture 4.1, that
$\sigma_x\sigma_y = +i \sigma_z$ and $\sigma_y\sigma_x = -i \sigma_z$.
Although we are writing $4 \times 4$ matrices, it's basically what you
would have expected just for one spin. Here as you may have noticed, all
our measurements are on spin 2 and spin 1 is just going along for the
ride.

Anyway the bottom line is that there's no unambiguous way of defining a
proper operator to answer questions about $\langle m_{2x}m_{2y} \rangle$
since the corresponding operators do not commute. And so we cannot
answer such questions. That is fine because it turns out that
experimentally too you cannot measure both $x$ and $y$ components of the
same spin.

![$\sigma_{2x}\sigma_{2y}$ $\neq$
$\sigma_{2y}\sigma_{2x}$](./Week4_3/figure7.jpg){#fig:fig4_3_7
width="\\textwidth"}

#### Fig. [4.25](#fig:fig4_3_8){reference-type="ref" reference="fig:fig4_3_8"}: {#fig.-figfig4_3_8}

To sum up, when operators do not commute, like $\sigma_{2x}$ and
$\sigma_{2y}$, we cannot measure the corresponding quantities $m_{2x}$
and $m_{2y}$ simultaneously and we cannot define an operator for the
product $m_{2x}m_{2y}$.\
But when operators do commute, like $\sigma_{1x}$ and $\sigma_{2y}$, the
corresponding quantities $m_{1x}$ and $m_{2y}$ can be measured
simultaneously and we can define an operator for the product
$m_{1x}m_{2y}$ and use it to answer questions regarding it.

![$m_{1x}m_{2y}$ versus
$m_{2x}m_{2y}$](./Week4_3/Picture8.png){#fig:fig4_3_8
width="\\textwidth"}

#### Fig. [4.26](#fig:fig4_3_9){reference-type="ref" reference="fig:fig4_3_9"}: {#fig.-figfig4_3_9}

Getting back to the original 2-spin problem with interactions, we now
have everything we need. We have seen is how to write $\sigma_{1x}$,
$\sigma_{2x}$, $\sigma_{1y}$, $\sigma_{2y}$, $\sigma_{1z}$,
$\sigma_{2z}$. Each of these are $4 \times 4$ matrices and we can
combine them as needed using straightforward matrix algebra to obtain
the composite $H$ matrix. Once you have $H$, you could find the
probability or density matrix which we could use to find the expectation
value for any measured quantity $S$ as long as we can wirte down the
corresponding operator $S_{op}$.

![We have everything we need for the two interacting spin
problem](./Week4_3/Picture9.png){#fig:fig4_3_9 width="\\textwidth"}

### Fig. [4.27](#fig:fig4_3_10){reference-type="ref" reference="fig:fig4_3_10"}: n-spin matrices {#fig.-figfig4_3_10-n-spin-matrices}

In principle, this is how you could talk about an $n$-spin system also.
If you had $n$ spins with pairwise or two-body interactions then the
general expression would be something like this,
$H=\sum_{r=1}^{n}{\overrightarrow{h_r}\cdot\overrightarrow{\sigma_r}}+(1/2)\sum_{r \neq q}^{n}{\sum_{q=1}^{n}{J_{rq}\overrightarrow{\sigma_r}\cdot\overrightarrow{\sigma_q}}}$
and each one of these sigmas would actually be a $2^n \times 2^n$
matrix.

For example, suppose you had a 4-spin system and you want to know what
is $\sigma_{2x}$. Well, then, the $\sigma_{2x}$ matrix would be like a
Kronecker product of $I\times \sigma_x \times I \times I$ giving a
$16 \times 16$ matrix at the end.

![Writing n-spin matrices](./Week4_3/figure10.jpg){#fig:fig4_3_10
width="\\textwidth"}

### Figs. [4.28](#fig:fig4_3_11){reference-type="ref" reference="fig:fig4_3_11"}-[4.29](#fig:fig4_4_9){reference-type="ref" reference="fig:fig4_4_9"}: Why quantum computers? {#figs.-figfig4_3_11-figfig4_4_9-why-quantum-computers}

#### Figs. [4.28](#fig:fig4_3_11){reference-type="ref" reference="fig:fig4_3_11"}: {#figs.-figfig4_3_11}

![Exponential growth in matrix
size](./Week4_3/Picture11.png){#fig:fig4_3_11 width="\\textwidth"}

So in principle, that's all there is to it. In practice, of course, the
problem gets huge as $n$ gets bigger because of this exponential problem
that I had mentioned before that as $n$ grows, $2^n$ power grows
exponentially and that is what makes it practically difficult to deal
with large quantum spin problems in general (see Fig.
[4.28](#fig:fig4_3_11){reference-type="ref" reference="fig:fig4_3_11"}).
That is, in a way, the basic rationale for building a quantum computer.

#### Fig. [4.29](#fig:fig4_4_9){reference-type="ref" reference="fig:fig4_4_9"} {#fig.-figfig4_4_9}

![$H_2$ Molecule.](./Week4_4/figure9.jpg){#fig:fig4_4_9 width="85%"}

As an example, for a hydrogen molecule one of the simpler models would
lead to a Hamiltonian with four spins, $\sigma_0$, $\sigma_1$,
$\sigma_2$, and $\sigma_3$, as shown. So it's a four spin system, and
each one of the matrices appearing here would be $2^4 \times 2^4$. We
could write out the $16 \times 16$ Hamiltonian matrix, find the density
matrix and calculate the properties you're interested in.

On the other hand, you could build a 4-bit quantum computer to solve
this problem. Of course, in this case, the direct calculation isn't too
hard, because the matrices are $16 \times 16$, but this goes up
exponentially. When you have bigger molecules and you want to calculate
the structure, the direct calculation would involve huge matrices of
size $2^n$, but if you build a relatively small quantum computer with
just $n$ qubits, and in principle it could solve the problem for you.

Of course the challenge is how to engineer all these interactions. That
how do you make sure that the interaction between say the $z$ component
of the second spin, and the $z$ component of the third spin is indeed
$g_{11}$, etc. That is the part that is hard to engineer, that is the
challenge that people face when actually trying to build quantum
computer. But the driving vision is that a 40 q-bit quantum computer
could solve a 40 spin problem, something that would ordinarily involve
$10^{12} \times 10^{12}$ matrices!

### Quiz

#### Question 1

An operator for a 2-spin system is given by
$\left [ \begin{array}{r r r r}
0 & \ 0 & \ 1 & \ 0 \\
0 & \ 0 & \ 0 & \ 1 \\
1 & \ 0 & \ 0 & \ 0 \\
0 & \ 1 & \ 0 & \ 0 \\
\end{array} \right ]$

Can you write it as the Kronecker product of the identity matrix and/or
the Pauli spin matrices $\sigma_x, \sigma_y, \sigma_z?$[^58]

#### Question 2

An operator for a 2-spin system is given by
$\left [ \begin{array}{r r r r}
+1 & \ 0 & \ 0 & \ 0 \\
0 & \ -1 & \ 0 & \ 0 \\
0 & \ 0 & \ -1 & \ 0 \\
0 & \ 0 & \ 0 & \ +1 \\
\end{array} \right ]$

Can you write it as the Kronecker product of the identity matrix and/or
the Pauli spin matrices $\sigma_x, \sigma_y, \sigma_z?$[^59]

#### Question 3

An operator for a 2-spin system is given by
$\left [ \begin{array}{r r r r}
0 & \ 0 & \ 0 & \ -i \\
0 & \ 0 & \ +i & \ 0 \\
0 & \ -i & \ 0 & \ 0 \\
+i & \ 0 & \ 0 & \ 0 \\
\end{array} \right ]$

Can you write it as the Kronecker product of the identity matrix and/or
the Pauli spin matrices $\sigma_x, \sigma_y, \sigma_z?$[^60]

## Two q-bit system

This is [Lecture 4.4: Watch youtube
video](https://www.youtube.com/watch?v=-TGnKrQI27k)

Now that we have established the basic framework for the quantum
description, let us consider a two q-bit system described by an energy
operator of this form,
$H=\overrightarrow{h_1}\cdot\overrightarrow{\sigma_1}+ \overrightarrow{h_2}\cdot\overrightarrow{\sigma_2} + J\overrightarrow{\sigma_1}\cdot\overrightarrow{\sigma_2}$.
and work out some of the consequences. Hopefully this will give you a
better feeling of how these things work.

### Figs. [4.30](#fig:fig4_4_2){reference-type="ref" reference="fig:fig4_4_2"}-[4.31](#fig:fig4_4_3){reference-type="ref" reference="fig:fig4_4_3"}: Hamiltonian {#figs.-figfig4_4_2-figfig4_4_3-hamiltonian}

#### Figs. [4.30](#fig:fig4_4_2){reference-type="ref" reference="fig:fig4_4_2"}: {#figs.-figfig4_4_2}

Let us assume that all the one spin terms
$\overrightarrow{h_1}, \overrightarrow{h_2}, \overrightarrow{h_3}$ are
zero and consider just the interaction term
$J\overrightarrow{\sigma_1}\cdot\overrightarrow{\sigma_2}$ which is the
sum of three terms
$J(\sigma_{1x}\sigma_{2x} + \sigma_{1y}\sigma_{2y} + \sigma_{1z}\sigma_{2z})$.
Following the procedure discussed in the last lecture we write out the
$4 \times 4$ matrices for each of the terms.

![Writing J$\overrightarrow{\sigma_1}\cdot\overrightarrow{\sigma_2}$ in
matrix form.](./Week4_4/figure2.jpg){#fig:fig4_4_2 width="\\textwidth"}

#### Fig. [4.31](#fig:fig4_4_3){reference-type="ref" reference="fig:fig4_4_3"}: {#fig.-figfig4_4_3}

So now, if we want to write out the total matrix, we have to add up
these three matrices. The items on the diagonal come from
$\sigma_{1z}\sigma_{2z}$, because the other two have all 0's on the
diagonal, while the off-diagonal terms come from the other two
$\sigma_{1x}\sigma_{2x}$ and $\sigma_{1y}\sigma_{2y}$.

![Writing J $\overrightarrow{\sigma_1}\cdot\overrightarrow{\sigma_2}$ in
matrix form(contd.)](./Week4_4/figure3.jpg){#fig:fig4_4_3
width="\\textwidth"}

### Figs. [4.32](#fig:fig4_4_4){reference-type="ref" reference="fig:fig4_4_4"}-[4.33](#fig:fig4_4_5){reference-type="ref" reference="fig:fig4_4_5"}: Ising spins {#figs.-figfig4_4_4-figfig4_4_5-ising-spins}

#### Fig. [4.33](#fig:fig4_4_5){reference-type="ref" reference="fig:fig4_4_5"}: {#fig.-figfig4_4_5}

Now what we need to do is, find the density matrix which is
$\exp{(-H)}$. If we ignore the off diagonal terms, which came from
$\sigma_x$ and $\sigma_y$, then this would be equivalent to doing just
classical spins, sometimes referred to as Ising spins. You'd then have a
purely diagonal matrix. It is easy then to write down the exponential as
shown, with $\exp{(-J)}$, $\exp{(+J)}$, $\exp{(+J)}$, and $\exp{(-J)}$
on the diagonal, all the rest being zero.

![Classical or Ising spins](./Week4_4/figure4.jpg){#fig:fig4_4_4
width="95%"}

![Classical or Ising spins](./Week4_4/figure5.jpg){#fig:fig4_4_5
width="95%"}

#### Fig. [4.33](#fig:fig4_4_5){reference-type="ref" reference="fig:fig4_4_5"}: {#fig.-figfig4_4_5-1}