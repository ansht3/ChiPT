![Classical or Ising spins](./Week4_4/figure4.jpg){#fig:fig4_4_4
width="95%"}

![Classical or Ising spins](./Week4_4/figure5.jpg){#fig:fig4_4_5
width="95%"}

#### Fig. [4.33](#fig:fig4_4_5){reference-type="ref" reference="fig:fig4_4_5"}: {#fig.-figfig4_4_5-1}

So in this limit when you have ignored the $\sigma_x$ and $\sigma_y$
terms, we just get what we'd have got in the classical case that we
looked at in chapter 2. The heights for the states $\{0 1\}$ and
$\{1 0\}$ are $\sim \exp{(+J)}$, which means if $J$ is a positive
quantity, these would be the tall peaks. The heights for $\{0 0\}$ and
$\{1 1\}$ are $\sim \exp{(-J)}$, and of course, if $J$ were negative,
these would be the peaks. Easy to understand this, positive J makes it
energetically favorable for the two spins to be antiparallel
($m_1m_2 < 0$), while a negative J makes it favorable to be parallel
($m_1m_2 > 0$). These are often referred to as antiferromagnetic and
ferromagnetic interaction respectively.

### Figs. [4.34](#fig:fig4_4_6){reference-type="ref" reference="fig:fig4_4_6"}-[4.35](#fig:fig4_4_8){reference-type="ref" reference="fig:fig4_4_8"}: Quantum spins {#figs.-figfig4_4_6-figfig4_4_8-quantum-spins}

#### Fig. [4.34](#fig:fig4_4_6){reference-type="ref" reference="fig:fig4_4_6"}: {#fig.-figfig4_4_6}

Now, if you keep the $x$ and $y$ terms, then you will get something that
looks a little different (see Fig.
[4.34](#fig:fig4_4_6){reference-type="ref" reference="fig:fig4_4_6"}).
Qualitatively it's still similar in that positive $J$ accentuates $(01)$
and $(10)$ while a negative J accentuates $(00)$ and $(11)$.

But in the quantum case, firstly, you will notice that for positive $J$,
the $(01)$ and $(10)$ seem taller with respect to $(00)$ $(11)$ than in
the classical case. But the result for negative J is more striking, it
doesn't matter how big you make $J$, $(01)$ and $(10)$ never get
suppressed beyond a factor of two. It is always half of this (see Fig.
[4.34](#fig:fig4_4_6){reference-type="ref" reference="fig:fig4_4_6"}).
By contrast, in the classical case, with negative $J$, $(01)$ and $(10)$
get suppressed exponentially as $J$ gets more negative.

#### Fig. [4.35](#fig:fig4_4_8){reference-type="ref" reference="fig:fig4_4_8"} {#fig.-figfig4_4_8}

It is straightforward to see the mathematical origin of this difference
by performing the matrix exponentiation of the full $H$ matrix,
$e^{-H}$. Earlier we ignored the off-diagonal terms in $H$ and got a
diagonal matrix with $\exp{(-J)}$, $\exp{(+J)}$, $\exp{(+J)}$ and
$\exp{(-J)}$ along the diagonal. When we include the off-diagonal terms
in $H$ the extremes still remain $\exp{(-J)}$, but in the middle we have
a matrix as shown. The probabilities of $(01)$ and $(10)$ are given by
$a = (e^{-J} + e^{+3J})/2$.

So based on this, you can understand what I had mentioned before, namely
that for $J << 0$, the $(01)$ and $(10)$ peaks tend to half the $(00)$
and $(11)$ peaks, since $a \rightarrow e^{-J}/2$.

This quantum problem appears in many contexts and are often discussed in
terms of what are called singlet and triplet states, but we will not
discuss the physics any further. Our purpose is simply to illustrate the
overall quantum methodology, which is straightforward to implement on
MATLAB or Python even after including more details like the single spin
terms,
$\overrightarrow{h_1}, \overrightarrow{h_2}, \overrightarrow{h_3}$ that
we ignored at the outset.

![Comparing Ising to quantum spins](./Week4_4/figure6.jpg){#fig:fig4_4_6
width="95%"}

![Two quantum spins](./Week4_4/figure8.jpg){#fig:fig4_4_8 width="95%"}

### Quiz

#### Question 1

An operator for a 2-spin system is given by
$\left [ \begin{array}{r r r r}
+1 & \ 0 & \ 0 & \ 0 \\
0 & \ -1 & \ 2 & \ 0 \\
0 & \ 2 & \ -1 & \ 0 \\
0 & \ 0 & \ 0 & \ +1 \\
\end{array} \right ]$

Can you write it in terms of the $4 \times 4$ matrices like
$\sigma_{1x}$, $\sigma_{2y}$ etc?[^61]

#### Question 2

Suppose for a 2-spin system we have
$e^{-H} = \left [ \begin{array}{r r r r}
10 & \ 0 & \ 0 & \ 0 \\
0 & \ 5 & \ 5 & \ 0 \\
0 & \ 5 & \ 5 & \ 0 \\
0 & \ 0 & \ 0 & \ 10 \\
\end{array} \right ]$

What is the expectation value $\langle m_{1x} \rangle?$[^62]

#### Question 3

An operator for a 2-spin system is given by
$\left [ \begin{array}{r r r r}
0 & \ 0 & \ 0 & \ 1 \\
0 & \ 0 & \ 1 & \ 0 \\
0 & \ 1 & \ 0 & \ 0 \\
1 & \ 0 & \ 0 & \ 0 \\
\end{array} \right ]$

Can you write it in terms of the $4 \times 4$ matrices like
$\sigma_{1x}$, $\sigma_{2y}$ etc?[^63]

## Quantum Annealing

This is [Lecture 4.5: Watch youtube
video](https://www.youtube.com/watch?v=TEUU7oRilWY)

In Lecture 5.3 I had mentioned that one use for a system of quantum
spins, this what you might call generally adiabatic quantum computer,
would be chemical structure calculations, which can be cast in the form
of $H$ matrix describing the interactions of many spins. But as we
noted, the challenge there is how to implement the complex interactions
in the actual hardware. Now, in this lecture, what we'll talk about a
possible application known as $\textit{quantum annelaing}$ on which
there has been a lot of work because this requires relatively simple
interactions. Even without a quantum computer the principle itself could
be useful when implemented on a conventional computer, something that is
referred to as $\textit{simulated quantum annealing.}$

### Figs. [4.36](#fig:fig4_5_2){reference-type="ref" reference="fig:fig4_5_2"}-[4.38](#fig:fig4_5_4){reference-type="ref" reference="fig:fig4_5_4"}: Why anneal? {#figs.-figfig4_5_2-figfig4_5_4-why-anneal}

#### Fig. [4.36](#fig:fig4_5_2){reference-type="ref" reference="fig:fig4_5_2"}: {#fig.-figfig4_5_2}

Now, let me start from a problem that we discussed in Chapter 2 where we
talked about this problem of optimization using classical spins. The
idea was how to design the interactions so that the lowest energy state
indicates the solution to some problem we're interested in and we used
the min cut or max cut problem as an illustration. So the idea was, if
you have say a bunch of nodes, I show six nodes, of which some are
connected strongly and some are not connected and there's a connection
matrix describing these connections. The problem is to find a way of
separating them into two separate groups of three nodes each, such that
the connections that you are cutting when you break them apart is a
minimum or is a maximum. We showed that there is a simple way to choose
the bias terms $x$ and the interaction terms $w$, given the connection
matrix, such that the lowest energy solutions will solve the problem
you're interested in.

![Constrained Optimization.](./Week4_5/figure2.jpg){#fig:fig4_5_2
width="90%"}

![Re-plotting in 1D](./Week4_5/figure3.jpg){#fig:fig4_5_3 width="90%"}

#### Fig. [4.37](#fig:fig4_5_3){reference-type="ref" reference="fig:fig4_5_3"} {#fig.-figfig4_5_3}

Now going forwards, what we'll be trying to do is translating this into
a quantum system seeing what that can add to this story. But before we
go on, let me just re-plot this graph, not as a two dimensional thing,
but in one dimension. What I mean is, here the way we did it is we had
eight states on each axis. Instead we plot it with all $64$ items on a
single axis, The two solutions then look like a 13 and a 50, obtained by
converting the binary number to a decimal one.

#### Fig. [4.38](#fig:fig4_5_4){reference-type="ref" reference="fig:fig4_5_4"} {#fig.-figfig4_5_4}

Now in solving problems of this type, there is a common difficulty that
I didn't talk about earlier. This is is not a problem you'd encounter
with six $p$-$bits$ usually, but with many $p$-$bits$ what could often
happen is that as you try to find the lowest energy states when you're
sampling, you could get stuck in other states which are not really the
lowest energy. If you take many, many samples, wait a long time,
theoretically it should always get there, but with a reasonable number
of samples, it often may be difficult to lock in on the right answers.

![Annealing](./Week4_5/Picture4.png){#fig:fig4_5_4 width="90%"}

So one solution that people use is what's called annealing (see Fig.
[4.38](#fig:fig4_5_4){reference-type="ref" reference="fig:fig4_5_4"}).
They multiply the energy by a number $E_0$, which is slowly turned up
from zero. When $E_0$ is 0, all states are equally probable and then as
you increase $E_0$, gradually the correct peaks rise up. In chapter 1 we
saw that for physical systems, $\widetilde{E}=E/kT$ and by analogy one
could view our $E_0$ as $1/kT$ so that we are kind of starting at a high
temperature and gradually lowering it. That is the origin of this word
annealing. In physical systems, when people are trying to grow a
crystal, a solid often gets stuck in higher energy states with many
defects in it, and one way to get rid of defects is to anneal by
lowering the temperature slowly. In this case, of course, we are not
changing the physical temperature, we are just changing the energy
function $\widetilde{E}$ through the constant $E_0$.

### Figs. [4.39](#fig:fig4_5_5){reference-type="ref" reference="fig:fig4_5_5"}-[4.40](#fig:fig4_5_6){reference-type="ref" reference="fig:fig4_5_6"}: Translating to quantum spins {#figs.-figfig4_5_5-figfig4_5_6-translating-to-quantum-spins}

#### Fig. [4.39](#fig:fig4_5_5){reference-type="ref" reference="fig:fig4_5_5"}: {#fig.-figfig4_5_5}

Now, what we want to talk about is the quantum version of this, and as I
had noted earlier, when translating to quantum spins, it's more
convenient to work from the bipolar formulation. So we do this in two
steps as shown, first from binary to bipolar
(Fig.[4.39](#fig:fig4_5_5){reference-type="ref"
reference="fig:fig4_5_5"}), and then from bipolar to the quantum model
with z-spins only (Fig.[4.40](#fig:fig4_5_6){reference-type="ref"
reference="fig:fig4_5_6"}).

Note that $m_r,m_q$ becomes $\sigma_{zr},\sigma_{zq}$, and the point is
that the coefficients $h$ and $J$ remain unchanged from what they were
in Chapter 2.

![Translating binary to bipolar](./Week4_5/Picture5.png){#fig:fig4_5_5
width="90%"}

![Translating bipolar to quantum with z-spins
only](./Week4_5/Picture6.png){#fig:fig4_5_6 width="90%"}

### Fig. [4.41](#fig:fig4_5_7){reference-type="ref" reference="fig:fig4_5_7"}: Add transverse term {#fig.-figfig4_5_7-add-transverse-term}

Of course, if that was all, then you'd say, well, why do I even want to
do it? The classical one is much simpler, we can go from there. But what
the quantum one lets you also do is add other terms to it that are not
in the $z$ direction. So you could for example add a term like this,
$\sum_{r=1}^{n}{h_{xr}\sigma_{xr}}$, which correspond to an energy term
that involves the $m_x$ component.

![Add x-spin term](./Week4_5/figure7.jpg){#fig:fig4_5_7
width="\\textwidth"}

Now, the way classical annealing works is that you start with $E_0=0$,
so all configurations have the same energy and then gradually you
increase $E_0$, and the peaks gradually rise up. With quantum annealing
what you could do is to could keep $E_0$ fixed, whatever your normal
value is, but you gradually decrease this transverse $h_x$ from a large
value. This is something you couldn't have done with your classical
spins.

### Fig. [4.42](#fig:fig4_5_8){reference-type="ref" reference="fig:fig4_5_8"}: Classical versus quantum annealing {#fig.-figfig4_5_8-classical-versus-quantum-annealing}

Now, just to give you an example, with $E_0=1$ and $h_{xr} =0$ we have
this solution I've shown before, two peaks at 13 and 50. In classical
annealing you could approach the final result by starting with
$E_0=0.04$ and increasing to $E_0=1$, while in quantum annealing you
could start with $h_{xr} =15$ and work your way down to $h_{xr} =0$. As
you can see both have qualitatively the same effect, start with lots of
peaks and gradually lock down to the desired ones.

![Classical versus quantum annealing, MATLAB code included at end of
book](./Week4_5/figure8.jpg){#fig:fig4_5_8 width="\\textwidth"}

But why would you think that quantum annealing might be better than
classical annealing? Well, there is a theorem that says that when you
gradually change a parameter in your Hamiltonian, if you do it slowly
enough, that if initially it was in some ground state, then it will stay
there and eventually you will actually get to the ground state. But in
the classical case, there is really no theorem that guarantees that you
will get to the ground state.

Now in practice how well this will work, how slowly you have to go to
actually take advantage of these? These are all still debated and pretty
much up in the air. So there have been demonstrations of various kinds,
there's a lot of work that has gone into this, but the motivation is
that quantum annealing might allow you to get to the ground state faster
and more reliably than the classical one.

### Figs. [4.43](#fig:fig4_5_9){reference-type="ref" reference="fig:fig4_5_9"}-[4.44](#fig:fig4_5_10){reference-type="ref" reference="fig:fig4_5_10"}: How the transverse term works {#figs.-figfig4_5_9-figfig4_5_10-how-the-transverse-term-works}

#### Figs. [4.43](#fig:fig4_5_9){reference-type="ref" reference="fig:fig4_5_9"}: {#figs.-figfig4_5_9}

Now, why does the $x$ term have the same effect as lowering $E_0$,
namely making all states equally likely? Well, one way to think about it
is to recall from Lecture 4.1 that the expectation value of $m_z$ is
given by $-\tanh{(h)}\cos{(\theta)}$. So if you put an $h$ in the $x$
direction corresponding to $\theta$ being 90 degrees, then
$\cos{(\theta)}$ being 0, it says that the expectation value of $m_z$ is
0 (see Fig. [4.43](#fig:fig4_5_9){reference-type="ref"
reference="fig:fig4_5_9"}).

What that means is that with large $h_{xr}$, for each spin $r$, both
$+1$ and $-1$ states are equally likely, which makes all states kind of
equally probable.

![How the x-term works](./Week4_5/figure9.jpg){#fig:fig4_5_9
width="\\textwidth"}

#### Fig. [4.44](#fig:fig4_5_10){reference-type="ref" reference="fig:fig4_5_10"}: Density matrix to wavefunction {#fig.-figfig4_5_10-density-matrix-to-wavefunction}

![Density Matrix to wavefunction](./Week4_5/figure10.jpg){#fig:fig4_5_10
width="\\textwidth"}

You can get a little more insight if you actually go from density
matrices to wave functions, which is not always possible, and in the
next week we'll discuss this much more. For the moment we note that if
you put a large $h$ at 90 degrees, the density matrix takes a simple
form that can be factorized to give us a wavefunction $\psi$ such that
$\rho = \psi \psi^{+}$.

As we'll discuss next week, there are systems where you can take the
density matrix and factorize it, and in that case, you can think in
terms of a wave function, which is a little easier because it's just got
two components as opposed to the density matrix, which is a matrix.

With wavefunctions, the squared magnitude of the first component tells
you the probability of up ($m_z=+1$) and the second one tells you the
probability of down ($m_z=-1$). In this case the two components of the
wavefunction are equal indicating that up and down states are equally
likely.

Next chapter we'll see more of wavefunctions ..

### Quiz

#### Question 1

A classical spin system has an energy function given by\
$\widetilde{E} = \sum_{r=1}^{n}{b_{r} s_{r}} + \frac{1}{2} \sum_{r \neq q}^{n} \sum_{q=1}^{n}{w_{rq}s_{r} s_{q}}$\
in binary representation 0, 1 (using $b_r$ instead of our usual $x_r$ to
avoid confusion with the coordinate x).\
In bipolar representation it is given by\
$\widetilde{E} = \sum_{r=1}^{n}{h_{r} m_{r}} + \frac{1}{2} \sum_{r \neq q}^{n} \sum_{q=1}^{n}{J_{rq} m_{r} m_{q}}$\
What is the Hamiltonian matrix for the corresponding quantum spin
system?[^64]

#### Question 2

A quantum spin system has a Hamiltonian matrix given by\
$H = E_0 \times \sum_{r=1}^{n}{h_{zr} \sigma_{zr}} + \frac{1}{2} \sum_{r \neq q}^{n} \sum_{q=1}^{n}{J_{rq} \sigma_{zr} \sigma_{zq}} + \sum_{r=1}^{n}{h_{xr} \sigma_{xr}}$\
How would you implement classical annealing on this system?[^65]

#### Question 3

A quantum spin system has a Hamiltonian matrix given by\
$H = E_0 \times  \sum_{r=1}^{n}{h_{zr} \sigma_{zr}} + \frac{1}{2} \sum_{r \neq q}^{n} \sum_{q=1}^{n}{J_{rq} \sigma_{zr} \sigma_{zq}} + \sum_{r=1}^{n}{h_{xr} \sigma_{xr}}$\
How would you implement quantum annealing on this system?[^66]

## EPR experiment {#Sec:EPR}

In this chapter we have introduced the quantum methodology: To every
observable $S$, there is a corresponding operator $S_{op}$ and knowing
the density matrix $\rho$ we can find the average value of measurements
from the relation $trace[\rho S_{op}]$. Let us end this chapter with an
example that shows that the methodology is straightforward to apply, but
understanding the results can take much longer!

### Fig. [4.45](#fig:fig4_6_1){reference-type="ref" reference="fig:fig4_6_1"}: Problem statement {#fig.-figfig4_6_1-problem-statement}

![A pair of electrons is initially prepared in some state: their spins
are then measured respectively along two arbitrary directions
$\hat{n_1}$ and $\hat{n_2}$. Problem is to predict the averages of each
measurement and the average of their product. The operators
corresponding to these observables are
indicated.](./Week4_6/Picture1.png){#fig:fig4_6_1 width="90%"}

The problem we consider is the following. A pair of electrons is
initially prepared in some state and their spins are then measured
respectively along two arbitrary directions $\hat{n_1}$ and $\hat{n_2}$.
Problem is to predict the averages of the measurements of
$\vec{m}\cdot \hat{n}_1$, $\vec{m}\cdot \hat{n}_2$ and their product
$(\vec{m}\cdot \hat{n}_1) (\vec{m}\cdot \hat{n}_2)$. The operators
corresponding to these three observables are obtained from the
$2 \times 2$ matrices obtained by replacing $\vec{m}$ with
$\vec{\sigma}$. But before we write down the observables let us talk
about the initial states we consider and their density matrices.

### Fig. [4.46](#fig:fig4_6_3){reference-type="ref" reference="fig:fig4_6_3"}: Density matrix {#fig.-figfig4_6_3-density-matrix}

We consider four separate initial states: First is the state $(01)$ with
spin 1 pointing along $+\hat{z}$ and spin 2 pointing along $-\hat{z}$.
The corresponding density matrix has only one non-zero element for
$[01,01]$. Second is the state $(10)$ with the spins reversed. The
density matrix now has its non-zero element for $[10,10]$. Third is a
state that is a $50-50$ mixture of the two, and the corresponding
density matrix is a $50-50$ combination of the last two. We will refer
to it as the $\textit{classical mixture state}$.

![Four different initial states that we consider and the corresponding
density matrices](./Week4_6/Picture3.png){#fig:fig4_6_3
width="\\textwidth"}

These three initial states are all classical states that we have
included to provide a contrast to the fourth state which is the
$\textit{quantum entangled state}$ that the EPR experiment is actually
about. Earlier in this chapter we saw that a pair of electrons when
subject to a large antiferromagnetic interaction ($J>>0$) go to a ground
state with a density matrix as shown having two additional
$\textit{off-diagonal}$ terms compared to the third initial state. In
this case the density matrix can actually be factorized to give a
wavefunction $\psi = \{0 \ +1 \ -1 \ 0\}^T /\sqrt{2}$ indicating that it
is a superposition of $(01)$ and $(10)$ with a negative sign.

### Fig. [4.47](#fig:fig4_6_2){reference-type="ref" reference="fig:fig4_6_2"}: Operators for observables {#fig.-figfig4_6_2-operators-for-observables}

Next we write down the operators corresponding to the three observables
in the problem. The $4 \times 4$ matrix corresponding to
$\vec{m}\cdot \hat{n}_1$ is obtained by replacing $\vec{m}$ with the
$2 \times 2$ spin matrix $\vec{\sigma}$, and then taking the Kronecker
product with the identity matrix representing spin 2. Similarly the
matrix corresponding to $\vec{m}\cdot \hat{n}_2$ is obtained from the
Kronecker product of $I$ with $\vec{\sigma}\cdot \hat{n}_2$. Finally the
matrix corresponding to the product
$(\vec{m}\cdot \hat{n}_1) (\vec{m}\cdot \hat{n}_2)$ is obtained from the
matrix product of the two $4 \times 4$ matrices we just wrote down.
Alternatively we could take the Kronecker product of the $2 \times 2$
matrices $\vec{\sigma}\cdot \hat{n}_1$ and
$\vec{\sigma}\cdot \hat{n}_2$.

![Operators corresponding to the three observables we
consider](./Week4_6/Picture2.png){#fig:fig4_6_2 width="\\textwidth"}

### Fig. [4.48](#fig:fig4_6_4){reference-type="ref" reference="fig:fig4_6_4"}: Predicting the averages {#fig.-figfig4_6_4-predicting-the-averages}

Now that we have both the density matrices $\rho$ and the operators
$S_{op}$ for each observables $S$, we are ready to compute the
predictions for the average value from the relation
$trace[\rho S_{op}]$. Note that all the density matrices have non-zero
elements only in the middle $2 \times 2$ block indicated in red in Figs.
[4.46](#fig:fig4_6_3){reference-type="ref" reference="fig:fig4_6_3"} and
[4.47](#fig:fig4_6_2){reference-type="ref" reference="fig:fig4_6_2"}.
Although the matrices are $4 \times 4$, we only need to consider the
$2 \times 2$ sections indicated, making the algebra fairly simple.

![Predicted results for the average value of the three observables for
each of the initial states](./Week4_6/Picture4a.png){#fig:fig4_6_4
width="90%"}

![Predicted histogram for the three observables for each of the initial
states whose averages are shown in Fig.
[4.48](#fig:fig4_6_4){reference-type="ref" reference="fig:fig4_6_4"}. On
the right there are four bars, the red ones (uu and dd) contributing +1,
and the blue ones (ud and du) contributing -1. On the left there are two
bars, the red (u) contributing +1 and the blue (d) contributing -1.
](./Week4_6/Picture5a.png){#fig:fig4_6_5 width="95%"}

### Fig. [4.49](#fig:fig4_6_5){reference-type="ref" reference="fig:fig4_6_5"}: Interpreting the results {#fig.-figfig4_6_5-interpreting-the-results}

To interpret the results it is useful to consider the actual histogram
of results that is experimentally observed from which the average values
in Fig. [4.48](#fig:fig4_6_4){reference-type="ref"
reference="fig:fig4_6_4"} are to be calculated. For example, the average
value of $\vec{m}\cdot \hat{n}_1$ is given as $c_1 = cos \theta_1$.
Experimentally one measures some spins that are up (u) along $\hat{n}_1$
and contribute $+1$ and some spins that are down (d) and contribute
$-1$. The fraction of spins contributing $+1$ is
$p_1 \equiv cos^2(\theta_1/2)$, while the fraction contributing $-1$ is
$q_1 \equiv sin^2(\theta_1/2)$, so that the average value is
$p_1-q_1 = c_1$ as shown in Fig.
[4.49](#fig:fig4_6_5){reference-type="ref" reference="fig:fig4_6_5"}.

You might say well it's nice that $p_1$ and $q_1$ give us the right
average $c_1$ we calculated directly from the operator
$\vec{\sigma} \cdot \hat{n}_1$. But isn't there a operator that would
let me calculate $p_1$, the number of up's directly. Indeed we could do
that using the operator $(I + \vec{\sigma} \cdot \hat{n}_1)/2$ as I had
mentioned earlier (see Fig. [4.16](#fig:fig4_2_7){reference-type="ref"
reference="fig:fig4_2_7"}). We would then have obtained
$(1+c_1)/2 = p_1$.[^67]

Anyway, from this picture we can understand the results for the first
two initial conditions and see how we get the average values of
$\pm c_1$ and $\mp c_2$, and their product gives the average of the
product or the correlation $-c_1 c_2$. If we take the average of the
first two we get the third, which makes good sense since the third case,
the classical mixture state, is a $50-50$ mixture of the first two. This
is all quite understandable.

What is intriguing is the correlation histogram for the fourth case, the
quantum entangled state, where the fraction of {ud} $\&$ {du}
measurements contributing $-1$ is $(1+\hat{n}_1 \cdot \hat{n}_2)/2$ and
the fraction of {uu} $\&$ {dd} measurements contributing $+1$ is
$(1-\hat{n}_1 \cdot \hat{n}_2)/2$, giving an average of
$-\hat{n}_1 \cdot \hat{n}_2$.

Consider first the case when both measurements are in the same
direction, that is, $\hat{n}_1$=$\hat{n}_2$. Each measurement will
produce a sequence of random $up$ and $down$ results, but the two
results will then be exactly anti-correlated. Something like this\
Electron 1:
$\{ u\ u \ d \ u \ d \ d \ u \ u \ u \ d \ d \ u \ d \ u \ u \ d \cdot \cdot \}$\
Electron 2:
$\{ d \ d \ u \ d \ u \ u \ d \ d \ d \ u \ u \ d \ u \ d \ d \ u \cdot \cdot  \}$\
And as long as $\hat{n}_1$=$\hat{n}_2$$\equiv \hat{n}$, this will be
true no matter what direction $\hat{n}$ we choose! This means that one
observer could make a measurement on one spin and immediately predict
the result of the other person's measurement which could be happening
far away at another location. Does that mean information is getting
transmitted instantaneously? Not really. Each person's measurement looks
like a random sequence of $up$ and $down$ that the other person has no
control over. The magical correlation between them is evident only if
they get together and compare notes, but that does not let them transmit
any information.

### Figs. [4.50](#fig:fig4_6_6){reference-type="ref" reference="fig:fig4_6_6"}: Why is it surprising? {#figs.-figfig4_6_6-why-is-it-surprising}

Nevertheless one still wonders how correlations like this can be
enforced between two remote measurements. With
$\hat{n}_1 \neq \hat{n}_2$ the result is even more intriguing: the
correlations are determined by $\hat{n}_1 \cdot \hat{n}_2$ even though
both $\hat{n}_1$ and $\hat{n}_2$ can be chosen arbitrarily.

But you might say that a correlation is also observed for the classical
$50-50$ mixture, the one that shows a correlation of $-c_1c_2$. Why
isn't that surprising? $\textit{Answer:}$ $c_1 c_2$ is equal to
$(\hat{n}_1 \cdot \hat{z})$ times $(\hat{n}_2 \cdot \hat{z})$ which has
a simple common sense interpretation. One electron is polarized along
$+\hat{z}$, another along $-\hat{z}$, the two observers measure the
components along $\hat{n}_1$ and $\hat{n}_2$ respectively and it does
not matter which observer sees which electron, the product is always
negative $- (\hat{n}_1 \cdot \hat{z})$ $\times$
$(\hat{n}_2 \cdot \hat{z})$.

It is as if you took two marbles, one white and one black, chose one
randomly and gave it to A, and gave the other to B. A and B traveled
elsewhere and looked at their marbles, and sure enough their colors are
anti-correlated. Nothing surprising here !

The quantum case is different. The electrons were not pointing
$+\hat{z}$ or $-\hat{z}$ when they left the source. They were neither
black nor white. Two independent observers chose two arbitrary
directions $\hat{n}_1$ and $\hat{n}_2$ to measure their blackness or
whiteness and their correlation is determined by
$\hat{n}_1$$\cdot$$\hat{n}_2$, no role is played by any property that
the each electron may have carried with it from the source.

![Comparing $S$ for the classical 50-50 mixture and the quantum
entangled states.](./Week4_6/Figure6.png){#fig:fig4_6_6 width="95%"}

There is a rich literature on Bell's inequalities and related topics
exploring different ways to pin down the surprising nature of quantum
entanglement. For example the CHSH[^68] inequality is based on the
quantity $S$ calculated from an experiment where one observer measures
the spin randomly along one of two directions $\hat{n}_1$ or
$\hat{n}'_1$ and the other observers does the same with two other
directions $\hat{n}_2$ or $\hat{n}'_2$ as shown in the figure. For
simplicity let us just consider the case with the directions equally
spaced by an angle $\theta = \pi/4$ from each other. The quantum
entangled state we discussed then leads to an $S$ of $2 \sqrt{2}$. Our
classical $50-50$ mixture on the other hand gives an $S$ that is only
half as big.

Your first reaction may be to say that we have arbitrarily chosen the
$\hat{z}$ direction to coincide with $\hat{n}_1$. Maybe a different
choice would have given a larger $S$? Interestingly with
$\theta = \pi/4$ we get the same answer irrespective of our choice of
$\hat{z}$ though it takes a little more algebra to see it.

Perhaps one could replace $\hat{z}$ with an elaborate set of hidden
variables that none of us know about and which control the correlations
in a way that leads to the large $S$ expected for the quantum entangled
state? It has been shown that a certain class of hidden variable models
will always obey the CHSH inequality $S \leq 2$ and cannot explain the
values exceeding 2 that have been demonstrated experimentally, work that
was recognized in 2022 with the physics Nobel prize.

## Fig. [4.51](#fig:fig5_6_1){reference-type="ref" reference="fig:fig5_6_1"}: 5-minute summary {#fig.-figfig5_6_1-5-minute-summary}

This is [Chapter 4 summary: Watch youtube video, upto
2:20](https://www.youtube.com/watch?v=JiESPuChnOM)

![Chapter 4 summary](./Week4_5/Picture11.png){#fig:fig5_6_1
width="\\textwidth"}

In this chapter, we started by making this transition from classical
spins to quantum spins starting from the bipolar representation, and
replacing $m$'s with $\sigma$'s which are $2 \times 2$ matrices, known
as the Pauli spin matrices. So what used to be an energy function now
becomes an energy matrix which you call the Hamiltonian matrix and
that's what you use when you want to describe quantum spins.

Just as with classical spins, you find the probability from the energy,
but now we find the probability matrix or the density matrix from the
energy matrix. Then if you want to predict what the result of a
particular measurement will be, that's when you need the operator
corresponding to what you are trying to observe and then take the
$\textit{trace}$ of its product with the density matrix.

The first two lectures illustrated the approach with one spin, while the
next two lectures illustrated it with two-spin systems. The principles
can be extended straightforwardly to n-spin systems for arbitrary $n$,
the real difficulty being that the matrices are of size
$2^n \times 2^n$, which increases exponentially with $n$. Hence the
interest in building quantum computers whose natural physics can perform
the computation for us. However, implementing arbitrary interactions
presents a formidable challenge. Finally, in the last lecture we talked
about quantum annealing, which is one approach that people have been
working on to use quantum systems to improve classical optimization
circuits.

In Section [4.6](#Sec:EPR){reference-type="ref" reference="Sec:EPR"} we
used the methods introduced in this chapter to discuss the celebrated
EPR (Einstein-Podolsky-Rosen) experiment that has intrigued generations
of scientists. Our aim is to convey that although the quantum approach
is straightforward and can be implemented readily, \"understanding\" the
results can be much more challenging, even for a simple two q-bit
system.

# Quantum Transition Matrix {#Sec:Quantum Transition}

## Adiabatic to Gated Computing

This is [Lecture 5.1: Watch youtube
video](https://www.youtube.com/watch?v=FmJayetRXKw)

What we discussed in chapter 4 you could call adiabatic quantum
computing, which assumes that the quantum system is in equilibrium with
some reservoir. And in that case it is convenient to describe things in
terms of the density matrix. In this chapter we will make the transition
to what is called gated computing, where we'll talk more in terms of
wave functions.

### Figs. [5.1](#fig:fig5_1_1){reference-type="ref" reference="fig:fig5_1_1"}-[5.8](#fig:fig5_1_8){reference-type="ref" reference="fig:fig5_1_8"}: Density matrix and wavefunction {#figs.-figfig5_1_1-figfig5_1_8-density-matrix-and-wavefunction}

#### Fig. [5.1](#fig:fig5_1_1){reference-type="ref" reference="fig:fig5_1_1"}: {#fig.-figfig5_1_1}

In the last chapter we set up the general framework for discussing
quantum spins, of how you write the energy matrix, the density matrix,
and deduce the expectation values of observables. We did this by
extending the concepts from classical spins, which we had introduced in
chapters 1-3. When translating to quantum, we didn't have to bring up
all those deep thoughts about reservoirs and the Boltzmann law, we just
went from the energy function to this energy matrix.

But of course, the physical picture is still the same, the system
interacts continually with the reservoir, which keeps it in equilibrium.
Now, if we were to start from the full system plus reservoir, then we'd
have a density matrix, that would also involve the reservoir states as
shown in Fig. [5.1](#fig:fig5_1_1){reference-type="ref"
reference="fig:fig5_1_1"}. The reservoir could be in state 1, state 2
etc, an enormous number of states, because reservoirs are usually huge
things with many degrees of freedom. The density matrix that we've been
calculating is like the sum of all these diagonal elements corresponding
to individual states of the reservoir, and it all comes out naturally in
our equilibrium calculations, because we're using this framework that we
inherited from classical statistical mechanics.

![Density Matrix](./Week5_1/figure1.jpg){#fig:fig5_1_1 width="95%"}

#### Fig. [5.2](#fig:fig5_1_2){reference-type="ref" reference="fig:fig5_1_2"}: {#fig.-figfig5_1_2}

Suppose instead we were dealing with an isolated system, then you see
we'd be looking at only one of the density matrices along the diagonal
in Fig. [5.1](#fig:fig5_1_1){reference-type="ref"
reference="fig:fig5_1_1"}. In that case, you can write the density
matrix as a product of what's called a wave function, so
$\rho_{ij}=\psi_i{\psi_j}^*$. This is much simpler, of course, because
$\rho_{ij}$ is a matrix, whereas $\psi$ is a column vector (see Fig.
[5.2](#fig:fig5_1_2){reference-type="ref" reference="fig:fig5_1_2"}).
But when you're trying to discuss an open system, you see, we have a sum
over all the reservoir states and in that case, the $\rho_{ij}$ cannot
be simply factorized this way, which is why you really need the density
matrix and that's what we'd been doing in the last chapter.

![Density matrix and wavefunction](./Week5_1/figure2.jpg){#fig:fig5_1_2
width="\\textwidth"}

#### Fig. [5.3](#fig:fig5_1_3){reference-type="ref" reference="fig:fig5_1_3"}: {#fig.-figfig5_1_3}

![Density matrix and wavefunction](./Week5_1/figure3.jpg){#fig:fig5_1_3
width="\\textwidth"}

But for an isolated system, the density matrix can be written as the
product of a column vector $\psi$ and its conjugate transpose,
$\psi^{\dagger}$, a row vector. In this chapter we'll be talking more
about an isolated system, and how it evolves in time. In that case, you
can talk in terms of the wave function, which is simpler, because it's
got just $N$ components, whereas, the density matrix has $N^2$
components. But when reservoirs are involved, you cannot have this
factorization, which is why we hadn't talked about wave functions in the
last chapter.

#### Fig. [5.4](#fig:fig5_1_4){reference-type="ref" reference="fig:fig5_1_4"}: {#fig.-figfig5_1_4}

![Single q-bit: Density matrix and wavefunctions
($\theta = 0$)](./Week5_1/figure4.jpg){#fig:fig5_1_4
width="\\textwidth"}

Now, just to understand this distinction between density matrices and
wavefunctions a little better, let's go back to the equilibrium density
matrix for one q-bit that we discussed in Lecture 4.2 (Fig.
[4.15](#fig:fig4_2_5){reference-type="ref" reference="fig:fig4_2_5"}),
in the presence of a $\vec{h}$ pointing along $\theta$.

Now, suppose $\theta = 0$, that means that this bias term is all in the
$z$ direction, and you put a large h, so that $tanh(h) \approx 1$. Now
you can simplify the density matrix $\rho$ and factorize it into
$\{0\quad +1\}^T$ times $\{0 \quad+1\}$ as shown. You can check this out
when you multiply it, you'll will get this matrix. So now you have the
wave function. $\{0 \quad+1\}$, and you could interpret it by saying,
that this quantum spin is all in the $-1$ state , it's pointing
downwards and that makes sense, because you're putting a large bias term
in the $z$ direction, which means, that if this were to point upwards,
it would have a very big energy, and so, it wants to point downwards.

#### Fig. [5.5](#fig:fig5_1_5){reference-type="ref" reference="fig:fig5_1_5"}: {#fig.-figfig5_1_5}

![Single q-bit: Density matrix and wavefunctions
($\theta = \pi$)](./Week5_1/figure5.jpg){#fig:fig5_1_5 width="90%"}

What if you put a large $H$ in the opposite direction, that's
$\theta = \pi$. Well in that case, $\cos{\theta}$ is -1, $\tanh{(h)}$ is
still $\approx 1$. Proceeding as before we can factorize the density
matrix to obtain the wavefunction as $\{+1 \quad0\}$, which shows you
that the spin is all in the $+1$ state, pointing up. So if you put $H$
pointing downwards, the spin will point upwards. Incidentally, I should
mention that in a lot of the literature, people define the $H$ with an
additional minus sign here, and so their conclusions may be the opposite
of ours. we are coming to, could be the exact opposite of what you might
see in some of the literature. This is just to warn you, if you're
trying to correlate this with what you might see elsewhere.

Anyway, but the main point here is, that when you get into one of these
pure states, you can easily factorize.

#### Fig. [5.6](#fig:fig5_1_6){reference-type="ref" reference="fig:fig5_1_6"}: {#fig.-figfig5_1_6}

![Single q-bit: Density matrix and wavefunctions
($\theta = \pi/2$)](./Week5_1/figure6.jpg){#fig:fig5_1_6
width="\\textwidth"}

What if I put a large $h$ in the $x$ direction? Now, you see
$cos{\theta}=0$ leading to a more complicated density matrix, but it can
still be factorized giving a wavefunction $\{+1 \quad-1\}$. So what this
wave function tells you is that the probability of being up or down is
equal, you see, it's $+1$. Remember, there's a half in the density
matrix, so I should have a $1/\sqrt{2}$ multiplying each one of the
wavefunctions, which I have left out for clarity.

But the important point I wanted to make is, that this actually
represents a spin in the $-x$ direction (see Fig.
[5.6](#fig:fig5_1_6){reference-type="ref" reference="fig:fig5_1_6"}), as
you might expect, since you're putting a big $h$ along positive $x$,
making the spin point to negative $x$. But a negative $x$ is actually a
superposition of up and down.

This is a little bit like vectors, it is just that the angles are twice
as big. We know that for a vector pointing at 45 degrees, you can think
of it as a superposition of a vertical vector and a horizontal vector.
But what used to be 45 degrees for vectors becomes 90 degrees for
spinors. So it's a superposition of up and down which are each at 90
degrees to the original.

#### Fig. [5.7](#fig:fig5_1_7){reference-type="ref" reference="fig:fig5_1_7"}: {#fig.-figfig5_1_7}

![Single q-bit: Density matrix and wavefunctions
($h = 0$)](./Week5_1/figure7.jpg){#fig:fig5_1_7 width="\\textwidth"}

Now, let us look at a case where the density matrix cannot be
factorized. Suppose $h$ equals 0. and the spin can be up or down,
because they both have the same energy. The density matrix looks like an
identity matrix multiplied by $1/2$. And the thing is, you can try this
out. You $\textbf{cannot}$ write it as $\{\psi\} \{\psi\}^{\dagger}$.

What you can do, however, is to write it as the sum of two factorizable
terms as shown, one represents a pure $up$ state, and the other a pure
$down$ state. So there is no unique wave function in this case, it is
$50\%$ of one, and $50\%$ of the other. You might say, well, couldn't I
have just added these two wave functions? No, then I would get
$\{1\quad 1$ which we know represents an x-polarized spin. What we
actually have here is what you might call an unpolarized collection of
electrons. Those are not the same thing, just as unpolarized light is
not the same as 45 degree polarized light, it's the same with electrons.

#### Fig. [5.8](#fig:fig5_1_8){reference-type="ref" reference="fig:fig5_1_8"}: {#fig.-figfig5_1_8}

One more thing as we move from density matrices to wavefunctions
assuming it is factorizable. Earlier we wrote the rule for calculating
expectation values by taking the trace of the corresponding operator
with the density matrix. Assuming that the density matrix can be
factorized, we can rewrite this rule in terms of wavefunctions as shown.
Note that we have made use of the property that when you take a trace of
product of a, b, and c, you can permute these in cyclic order, and it
stays the same.

![Density matrix to wavefunctions](./Week5_1/figure8.jpg){#fig:fig5_1_8
width="\\textwidth"}

### Figs. [5.9](#fig:fig5_1_9){reference-type="ref" reference="fig:fig5_1_9"}-[5.10](#fig:fig5_1_10){reference-type="ref" reference="fig:fig5_1_10"}: Quantum transition matrix {#figs.-figfig5_1_9-figfig5_1_10-quantum-transition-matrix}

#### Fig. [5.9](#fig:fig5_1_9){reference-type="ref" reference="fig:fig5_1_9"}: {#fig.-figfig5_1_9}

![Quantum transition matrix](./Week5_1/figure9.jpg){#fig:fig5_1_9
width="\\textwidth"}

In gated quantum computing, we will be talking about the time evolution
of isolated quantum systems using the same Hamiltonian $H$ that we used
in Chapter 4. But is Chapter 4, we wanted the density matix $e^{-H}$,
but now we want the the quantum transition matrix $U = e^{-iH}$, which
evolves the wavefunctions from time $t$ to $t+1$.

#### Fig. [5.10](#fig:fig5_1_10){reference-type="ref" reference="fig:fig5_1_10"}: {#fig.-figfig5_1_10}

![Quantum transition matrix](./Week5_1/figure10.jpg){#fig:fig5_1_10
width="\\textwidth"}

You could compare the quantum transition matrix $U$ with its classical
counterpart $W$ from Chapter 3. $W$ describes the evolution of
probabilities, whereas, the $U$ describes the evolution of wave
functions. Probabilities have the property that when you add up all the
components, it must be 1, and so, to ensure that the probability stays
normalized, $W$ has the property that every column must add up to 1. So
that's called a stochastic matrix.

For the quantum case, the $\psi$'s don't add up to 1. What adds up to 1
is the sum of the squares, which can be written as, which means that
$\{\psi\}^{\dagger} \{\psi\} = 1$. What you can show is, that in order
to ensure this, the matrix $U$, must be unitary. Just as $W$ must be a
stochastic matrix with columns adding up to one, $U$ must be a unitary
matrix, with $UU^{\dagger}$ = $U^{\dagger}U$ = 1.

By the way note the subtle difference between $\{\psi\}^{\dagger} \psi$
and what we wrote for the density matrix after factorizing, namely
$\{\psi\} \{\psi\}^{\dagger}$. If $\{\psi\}$ is an $N \times 1$ column
vector, then the former is a number, while the latter is an $N \times N$
matrix. The former should equal one, while it's the $\textit{trace}$ of
the latter that should equal one.

### Fig. [5.11](#fig:fig5_1_11){reference-type="ref" reference="fig:fig5_1_11"}: Quantum gates {#fig.-figfig5_1_11-quantum-gates}

![Quantum Gates.](./Week5_1/figure12.jpg){#fig:fig5_1_11
width="\\textwidth"}

What we'll be doing this week then, is talk about quantum gates, which
work on isolated systems where the wave functions are gradually
transformed in time. By the way, it's convenient to draw the time axis
from right to left, instead of left to right, because then the order of
multiplication of matrices comes naturally.

Quantum gates will let you transform the wave function from an initial
state as you go along and its classical equivalent might be the Bayesian
networks we talked about briefly in Lecture 3.4 which transformed the
probability density function. But these are very different from
adiabatic quantum computing whose classical equivalent would be our
Boltzmann networks.

The transformation of wavefunctions is described by the quantum
transition matrix $U$ and the challenge is to design them so that they
do something useful. That is what we will talk about in the next three
lectures.

### Quiz

#### Question 1

Suppose the density matrix is given by
$\frac{1}{2} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ 1  \\
\end{array} \right ]$.

What is the corresponding wavefunction $\psi$?[^69]

#### Question 2

Suppose the density matrix is given by
$\frac{1}{2} \left [ \begin{array}{r r}
1 & \ -i  \\
+i & \ 1  \\
\end{array} \right ]$.

What is the corresponding wavefunction $\psi$?[^70]

#### Question 3

What is the property that a properly normalized wavefunction $\psi$ must
have?[^71]

## Hadamard Gates

This is [Lecture 5.2: Watch youtube
video](https://www.youtube.com/watch?v=TAkUuw-1tBc)

In the last lecture, we outlined this transition from density matrices
to wavefunctions as we go from adiabatic to gated quantum computing. The
next three lectures will be about how we use quantum gates to do useful
interesting things. They all have this structure where you apply one
gate after another sequentially: we draw the time axis going to the left
so that you start with a wave function at the right and multiply by the
$U$ from these different gates to obtain a final wave function.

### Figs. [5.12](#fig:fig5_2_1){reference-type="ref" reference="fig:fig5_2_1"}-[5.13](#fig:fig5_2_2){reference-type="ref" reference="fig:fig5_2_2"}: Transition matrix for H-gate {#figs.-figfig5_2_1-figfig5_2_2-transition-matrix-for-h-gate}

#### Fig. [5.12](#fig:fig5_2_1){reference-type="ref" reference="fig:fig5_2_1"}: {#fig.-figfig5_2_1}

![Transition matrix for Hadamard
Gate](./Week5_2/figure1.jpg){#fig:fig5_2_1 width="\\textwidth"}

Now, one gate that's very interesting and important that's widely used
is this Hadamard gate whose $U$ matrix is shown. Just a $2 \times 2$
matrix, but note that one element is $-1$, something you never see with
classical $W$ matrices.

Now if the initial state is say up, then if you multiply it with this
$U$ you get a superposition of up and down. If the initial state is down
and you multiply it with this $U$ again you will get a superposition but
now the down component will have a negative sign. Now if you ask for the
probabilities the negative sign doesn't matter because we square the
wavefunction to get the probability, which in either case is $50\%$ up
and $50\%$ down.

#### Fig. [5.13](#fig:fig5_2_2){reference-type="ref" reference="fig:fig5_2_2"}: {#fig.-figfig5_2_2}

![Classical Analog of H-gate](./Week5_2/figure2.jpg){#fig:fig5_2_2
width="\\textwidth"}

It is interesting to compare with a classical probabilistic gate with a
$W$ that would give essentailly the same result as one Hadamard
gate.This $W$ will transform an initial probability distribution
function that is all up or all down into half up and half down. So you
might say why are we talking about the Hadamard gate? In effect it's
doing much the same thing as the classical version. Well, they look the
same because we are looking at the effect after one gate. The difference
is striking when you apply the gate twice.

### Figs. [5.14](#fig:fig5_2_3){reference-type="ref" reference="fig:fig5_2_3"}: Two Hadamards in series {#figs.-figfig5_2_3-two-hadamards-in-series}

![Two Hadamards operating
sequentially](./Week5_2/figure3.jpg){#fig:fig5_2_3 width="\\textwidth"}

So if you apply the same gate again, the effect is to multiply again
with the same matrix. So it's the same $U$ again and the interesting
thing about the Hadamard gate is that $U^2$ is actually the identity
gate, you can multiply it out and check. What that means is when you
apply it twice you get back what you started with because it's basically
like an identity matrix multiplying the original wavefunction. So if
started all up, you end up being all up and if you started all down you
end up being all down.

By contrast in the classical case if we apply that same gate again you
will again get 50-50. No change in the classical case, but a big chane
in teh quantum case. This is the very remarkable thing that this
negative term in $U$ is able to accomplish. When you apply the gate once
it spreads out, but apply it twice and it comes back.

### Figs. [5.15](#fig:fig5_2_4){reference-type="ref" reference="fig:fig5_2_4"}-[5.17](#fig:fig5_2_6){reference-type="ref" reference="fig:fig5_2_6"}: Example with two q-bits {#figs.-figfig5_2_4-figfig5_2_6-example-with-two-q-bits}

#### Fig. [5.15](#fig:fig5_2_4){reference-type="ref" reference="fig:fig5_2_4"}: {#fig.-figfig5_2_4}

Now, let's consider what happens when you have, 2-bits and you apply
this Hadamard gate individually to each bit. We could think of it as a
composite system which has four states, and these two individual
Hadamard gates can be described by a single transformation matrix which
is a $4 \times 4$ matrix obtained from the Kronecker product of the two
individual $2 \times 2$ matrices.

![2-bit Hadamards](./Week5_2/figure4.jpg){#fig:fig5_2_4
width="\\textwidth"}

#### Fig. [5.16](#fig:fig5_2_5){reference-type="ref" reference="fig:fig5_2_5"}: {#fig.-figfig5_2_5}

So if you start out all in the $(00)$ state then what would you get? We
get what is in the first column of the $U_H \times U_H$ matrix, that's
the way matrix multiplication works. If we start in the $(01)$ state, we
get the second column and so on. Since the different columns are all the
same except for the signs, the histogram in any case would have all four
states equally probable. But as we noted earlier with one q-bit, the
magic of the Hadamard gate shows up when you apply it twice. You get
back what you started with, since $(U_H \times U_H)^2$ is the identity
matrix as you can check. So that's the amazing thing about this Hadamard
gate, applied once it spreads out looks like all the information is
lost. But apply it twice and it comes right back where you started.

![2-bit Hadamards](./Week5_2/figure5.jpg){#fig:fig5_2_5
width="\\textwidth"}

#### Fig. [5.17](#fig:fig5_2_6){reference-type="ref" reference="fig:fig5_2_6"}: {#fig.-figfig5_2_6}

![Hadamard gate, compact
expression](./Week5_2/figure6.jpg){#fig:fig5_2_6 width="90%"}