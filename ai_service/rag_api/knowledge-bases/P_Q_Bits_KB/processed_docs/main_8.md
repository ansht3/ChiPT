![2-bit Hadamards](./Week5_2/figure5.jpg){#fig:fig5_2_5
width="\\textwidth"}

#### Fig. [5.17](#fig:fig5_2_6){reference-type="ref" reference="fig:fig5_2_6"}: {#fig.-figfig5_2_6}

![Hadamard gate, compact
expression](./Week5_2/figure6.jpg){#fig:fig5_2_6 width="90%"}

Now, it's convenient to express this property concisely because Hadamard
gates are widely used in many of these quantum circuits. We label these
columns as 0, 1, 2, 3 which is like the decimal equivalent of the binary
representation. So we could name the columns of $(U_H \times U_H)$ as
$h_0$, $h_1$, $h_2$, $h_3$. What's $h_0$\" It is this
$(+1 \ +1 \ +1 \ +1)^T$ multiplied by a half. What's $h_1$, well, it's
$(+1 \ -1 \ +1 \ -1)^T$ again multiplied by a half and so on.

We also define something like a delta function, $\delta_0$ means you
only have $+1$ in the $(00)$ position, $\delta_1$ means you will only
have $+1$ in the $(01)$ position, and so on. When you apply the Hadamard
gate to a wave function that looks like $\delta_k$, meaning a $+1$ in
the $k$ position you get the $h_k$ which represents the column $k$ of
$(U_H \times U_H)$. Apply the Hadamard gate again to $h_k$ and you get
back $\delta_k$.

### Fig. [5.18](#fig:fig5_2_7){reference-type="ref" reference="fig:fig5_2_7"}: Example with three q-bits {#fig.-figfig5_2_7-example-with-three-q-bits}

![Hadamard, 3-bit example](./Week5_2/figure7.jpg){#fig:fig5_2_7
width="90%"}

These relations summarize the property of Hadamard gates and
interestingly it can be extended beyond just two q-bits. If you had say
3 q-bits, then the overall matrix obtained from the Kronecker product of
three elementary Hadamard matrices,
$\bf{U_H}$$=U_H \times U_H \times U_H$, is an $8 \times 8$ matrix. Once
again we can define $\{h_k\}$, $\{\delta_k\}$ with $k$ running from 0 to
7. With ten q-bits, the composite matrix would be of size
$1024 \times 1024$, and we would have $k$ running from 0 to 1023. But in
the end we still have $\bf{U_H}$$\delta_k = h_k$ and
$\bf{U_H}$$h_k = \delta_k$.\
In the next two lectures we will talk about two classic quantum
algorithms both of which make use of Hadamard gates to take a 0 state
and spread it out and then later bring it back.

### Quiz

#### Question 1

A Hadamard gate $\frac{1}{\sqrt{2}} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ -1  \\
\end{array} \right ]$. acts on a wavefunction $\left \{ \begin{array}{r}
1 \\
0 \\
\end{array} \right \}$.

What is the final wavefunction $\psi$?[^72]

#### Question 2

A Hadamard gate $\frac{1}{\sqrt{2}} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ -1  \\
\end{array} \right ]$. acts on a wavefunction $\left \{ \begin{array}{r}
0 \\
1 \\
\end{array} \right \}$.

What is the final wavefunction $\psi$?[^73]

#### Question 3

Two Hadamard gates $\frac{1}{\sqrt{2}} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ -1  \\
\end{array} \right ]$. act separately on two spins with a composite
wavefunction $\left \{ \begin{array}{r}
0 \\
1 \\
0 \\
0 \\
\end{array} \right \}$.

What is the final wavefunction $\psi$?[^74]

## Grover search {#Sec:Grover}

This is [Lecture 5.3: Watch youtube
video](https://www.youtube.com/watch?v=sZmvr7q0y0A)

### Figs. [5.19](#fig:fig5_3_1){reference-type="ref" reference="fig:fig5_3_1"}-[5.22](#fig:fig5_3_4){reference-type="ref" reference="fig:fig5_3_4"}: Grover cycle {#figs.-figfig5_3_1-figfig5_3_4-grover-cycle}

#### Figs. [5.19](#fig:fig5_3_1){reference-type="ref" reference="fig:fig5_3_1"}: Classical versus Grover search {#figs.-figfig5_3_1-classical-versus-grover-search}

In the last lecture, we introduced this Hadamard gate, and this magical
property that when you apply it once to a delta function, you spread it
out over all the components. But you apply it a second time, you again
get back the $\delta$. This is the property that is widely used in many
quantum circuits and in this lecture, we'll see how it is used in
Grover's algorithm along with other gates.

![An unstructured classical search needs $\sim N$ queries, Grover search
needs $\sim \sqrt(N)$ queries.](./Week5_3/Figure1.png){#fig:fig5_3_1
width="\\textwidth"}

The problem is something like this. We have a database with small $n$
bits, which can host capital $N=2^n$ configurations, and of these $2^n$
configurations, there is one which is the correct answer. That's the
target that we want to find out of a total of $2^n$ configurations and
$N$ increases exponentially with $n$, so that with say 40 bits, you have
like a trillion configurations, a lot to search from.

Now, classically, how many tries would you need? Well, the idea is that
you'd go at it sequentially. You could say, okay, is this the right one?
No. Is this the right one? No. Till you get a yes. If you're lucky, your
first query would be the right one, so you'd have your answer in one
query. If you're unlucky, it would take you $N$ queries. On the average,
it would be half of $N$, the point is it is of the order of $N$. But
Grover's algorithm gives us a way to get an answer in $\sqrt{N}$ queries
(see Fig. [5.19](#fig:fig5_3_1){reference-type="ref"
reference="fig:fig5_3_1"}). That can be a huge improvement when $N$ is
large.

#### Fig. [5.20](#fig:fig5_3_2){reference-type="ref" reference="fig:fig5_3_2"}: Grover cycle, Step 1, Hadamard {#fig.-figfig5_3_2-grover-cycle-step-1-hadamard}

![Step 1 of Grover cycle: Hadamard](./Week5_3/figure2.jpg){#fig:fig5_3_2
width="\\textwidth"}

So how does this work? For this discussion, we will assume $n=2$ with
$N=4$ but you will see that it applies to any arbitrary number $n$. So
the composite Hadamard matrix working on this two q-bit system will be
written by the Kronecker product ${\bf{U_H}}=U_H \times U_H$. Now, if
you come in with a $\{00\}$, so the initial wave function looks like
$\delta_0= \{+1 \ 0 \ 0 \ 0\}^T$ and on applying the Hadamard gate, we
get this first column, $h_0= 1/\sqrt{N} \{1 \ 1 \ 1 \ 1\}^T$. To keep it
general I'm writing $1/\sqrt{N}$ instead of setting $N=4$.

#### Fig. [5.21](#fig:fig5_3_3){reference-type="ref" reference="fig:fig5_3_3"}: Grover cycle: Step 2, Query {#fig.-figfig5_3_3-grover-cycle-step-2-query}

![Step 2 of Grover cycle: Query](./Week5_3/figure3.jpg){#fig:fig5_3_3
width="\\textwidth"}

Now comes the query. What it does is, that when you ask for the answer
about the target, it will flip the sign of the target component as
shown. Now if this were a course on quantum computing, the next question
we'd be discussing is, how do you build the circuit that does this
query? Can you do it with just a few circuits of the order of small $n$,
or would you need $\sim 2^n$ circuits to do it? Actually, it's a fairly
straightforward circuit using what are called controlled gates that you
could use to implement this, but we won't go into that.

Okay, but the point is, supposing we had this circuit which flips the
sign of the target every time we query it. How could we then identify
the target? Because just flipping the sign doesn't help me. Because you
see, in the end, when I'm making a measurement, I measure probabilities,
I don't measure amplitudes. So the fact that this amplitude is $-1$
doesn't mean a thing, because as far as probabilities are concerned, all
four look equally probable. So I can't really tell what happened.

So what happens next is there's a sequence of gates that are applied,
which turn this simple flipping into a measurable thing, which means
what happens after I apply these three gates, which I'll explain, the
target becomes enhanced relative to the background, and the background
is suppressed a little bit (see Fig.
[5.21](#fig:fig5_3_3){reference-type="ref" reference="fig:fig5_3_3"}).
Of course, if any one is enhanced, the rest must be suppressed in order
to keep the normalization right, because overall, the sum of squares
must be 1. So the point is every time you run this, the amplitude of the
target, that is the correct answer, goes from $1/\sqrt{N}$ to
$3/\sqrt{N}$. I'll show that in a minute, it's not obvious.

#### Fig. [5.22](#fig:fig5_3_4){reference-type="ref" reference="fig:fig5_3_4"}: Grover cycle: Step 3 {#fig.-figfig5_3_4-grover-cycle-step-3}

![The target amplitude increases in every cycle, reaches a maximum and
continues to oscillate which we have not shown. MATLAB code included at
end of book](./Week5_3/Picture4.png){#fig:fig5_3_4 width="75%"}

So in every cycle this enhancement occurs and if you apply the
enhancement a number of times, then finally the target amplitude will
become big enough that you will be easily able to detect it. How many
would you need? Well, since it goes up by $2/\sqrt{N}$ every time,
roughly speaking you need $\sim \sqrt{N}$ application cycles to build it
up to $\sim 1$, at which point you can measure it and get your answer.

I have plotted the amplitude of the target as a function of the number
of cycles and if you have say 6 bits, then you can see the number of
cycles goes up to 1 rather quickly in less than 10 cycles and then
actually comes down again. If you had 8 bits, it takes about 20 cycles.
If you have 10 bits, it takes a little less than 30 cycles, and roughly
you can see that the peak value occurs when the number of cycles is
$\sqrt{N}$. So that's the point, for the Grover iteration the number of
cycles which means the number of queries is of the order of $\sqrt{N}$,
which is a big improvement over classical searches which require $N$
queries. We will now work out a quantitative description that describes
the results in Fig.[5.22](#fig:fig5_3_4){reference-type="ref"
reference="fig:fig5_3_4"} accurately. It will also show why the target
amplitude increases at first, but eventually starts to decrease. Indeed
we will see that with more cycles it continues to oscillate, which is
not shown.

### Figs. [5.23](#fig:fig5_3_5){reference-type="ref" reference="fig:fig5_3_5"}-[5.28](#fig:fig5_3_14){reference-type="ref" reference="fig:fig5_3_14"}: Quantitative analysis {#figs.-figfig5_3_5-figfig5_3_14-quantitative-analysis}

#### Fig. [5.23](#fig:fig5_3_5){reference-type="ref" reference="fig:fig5_3_5"}: Role of Query {#fig.-figfig5_3_5-role-of-query}

So how does this work? We are starting with something that's in the 0
state, and that's what we have named $\delta_0$. When you apply a
Hadamard, the $\delta_0$ becomes $h_0$ as we discussed in the last
lecture.\
Now, what does the query do? It takes the target element and flips it.
You could write that as $h_0$, where all elements are positive and
subtract $-2$ from the target component, giving us
$h_0-(2\delta_t/\sqrt{N})$. That's what we get after applying the query.

![Grover output after query](./Week5_3/figure5.jpg){#fig:fig5_3_5
width="80%"}

![Grover output after full cycle](./Week5_3/figure6.jpg){#fig:fig5_3_6
width="80%"}

#### Fig. [5.24](#fig:fig5_3_6){reference-type="ref" reference="fig:fig5_3_6"}: The full cycle {#fig.-figfig5_3_6-the-full-cycle}

Next in the Grover cycle, we have this sequence $\bf{U_H}$$U_0$
$\bf{U_H}$. What does the first Hadamard do? That's easy, as we have
discussed, Hadamard takes $\delta$ and turns it into $h$, takes $h$ and
turns it into a $\delta$. So after the first $\bf{U_H}$ we have
$\delta_0-2 h_t/\sqrt{N}$.

Next, we have this $U_0$ gate and its job is to flip the sign of all the
elements except for the first one. So the first one stays what it is,
but all the elements are flipped. Again, if this was a course about
quantum computing, we'd talk about the kind of circuits you could use to
actually do that. You'd need one of these controlled gates, but we won't
go into it.

The question is, what does $U_0$ do to what we had, namely to
$\delta_0-(2h_t/\sqrt{N})$? Well, if you think about it, the $\delta_0$
is unaffected. Why? Because in $\delta_0$ the only non-zero element is
the first one and we are doing nothing to the first one anyway.

Now, what about the $h_t$? Well, if you just flipped the sign of all its
elements, $-2h_t/\sqrt{N}$ would become $+2h_t/\sqrt{N}$. But then you
flipped all the signs except for the first one, so you need another term
to account for that. You can show that this actually amounts to
subtracting this $\delta_0$, and the $4/N$ comes from $(2/\sqrt{N})^2$.
So after applying $U_0$ we have $(1-4/N)\delta_0+(2h_t/\sqrt{N})$.

Next, we have another Hadamard and that's again easy because Hadamards
just turn $\delta$'s into $h$ and $h$'s into $\delta$. So at the end of
the cycle, we have turned an initial $h_0$ into
$(1-4/N)h_0+(2\delta_t/\sqrt{N})$.

So we have two terms. The $h_0$ is $+1$ everywhere. That's the
background and in the course of a cycle, it has been reduced by a factor
$1-4/N$. And then there is $\delta_t$, that's the target, which got
enhanced by $2/\sqrt{N}$. So that's what we had said a Grover cycle
does. It enhances the amplitude of the target from $1/\sqrt{N}$ to
$3/\sqrt{N}$ and suppresses the background to compensate.

#### Fig. [5.25](#fig:fig5_3_10){reference-type="ref" reference="fig:fig5_3_10"}: Transformation of $a_k,b_k$ in each cycle {#fig.-figfig5_3_10-transformation-of-a_kb_k-in-each-cycle}

Note, however, that in this case the cycle started with an initial state
that contained just $h_{0}$. That is true of the first cycle but
subsequent cycles will start with a combination of $h_{0}$ and
$\delta_{t}$ and so we also need to know what the Grover cycle does to
an initial $\delta_{t}$. We will not go through the detailed arguments
but the final result is shown in the Figure. We start with $a_0 = 1$,
$b_0 =0$ and the $(k+1)^{th}$ Grover cycle transforms $a_k, b_k$ into
$a_{k+1},b_{k+1}$ as shown.

![Transformation of $a_k,b_k$ in each
cycle](./Week5_3/Picture10a.png){#fig:fig5_3_10 width="80%"}

#### Fig. [5.26](#fig:fig5_3_11){reference-type="ref" reference="fig:fig5_3_11"}: Transformation from $a_k,b_k$ to $A_k,B_k$ {#fig.-figfig5_3_11-transformation-from-a_kb_k-to-a_kb_k}

We have described the wavefunction at each stage in terms of two
components $h_0$ and $\delta_t$ but you can check that they are NOT
orthogonal. The transformation properties of each Grover cycle can be
made to look much cleaner if we subtract out the overlap with $\delta_t$
from $h_0$ to construct $\widetilde{h_0}$.\
We now have a different set of coefficients $A_k,B_k$ which are related
to the old ones $a_k,b_k$ at any value of $k$ by the relations shown.

![We construct $\widetilde{h_0}$ from $h_0$ such that it is orthogonal
to $\delta_t$. This changes the coefficients $a_k,b_k$ to $A_k,B_k$ as
shown](./Week5_3/Picture11.png){#fig:fig5_3_11 width="75%"}

#### Fig. [5.27](#fig:fig5_3_12){reference-type="ref" reference="fig:fig5_3_12"}: Transformation of $A_k,B_k$ in each cycle {#fig.-figfig5_3_12-transformation-of-a_kb_k-in-each-cycle}

We can now combine the transformation rules for $a_k,b_k$ and $A_k,B_k$
with the rule for the evolution of $a_k,b_k$ in each cycle, to obtain
the rule for the evolution of $A_k,B_k$ in each cycle. Note that the
resulting transformation matrix is a unitary one that can be written in
the form of rotation matrix, as if $A_k,B_k$ from an orthogonal $x-y$
coordinate system and each Grover cycle rotates the coordinates by
$\theta$. This simple transformation law is what we were seeking, the
reason why we went to the trouble of constructing $\widetilde{h_0}$ from
$h_0$ such that it was orthogonal to the other component $\delta_t$.

![Transformation of $A_k,B_k$ in each
cycle](./Week5_3/Picture12.png){#fig:fig5_3_12 width="\\textwidth"}

#### Fig. [5.28](#fig:fig5_3_14){reference-type="ref" reference="fig:fig5_3_14"}: Final solution after $k$ cycles  {#fig.-figfig5_3_14-final-solution-after-k-cycles}

![Number of cycles $K$ needed for peak target
amplitude](./Week5_3/Picture14a.png){#fig:fig5_3_14 width="\\textwidth"}

Now that transformation property of each cycle has been reduced to a
rotation, it is easy to see what $k$ cycles will do: it will rotate the
amplitudes by $k \theta$. When do we get a peak in the target amplitude?
When $sin \ K \theta = 1$ which leads to a simple expression for K if we
assume large $N$, so that $N-1 \approx N$ and
$sin \ \theta \approx \theta$. This describes the numerical results in
Fig.[5.22](#fig:fig5_3_4){reference-type="ref" reference="fig:fig5_3_4"}
accurately and shows why the target amplitude $sin \ k \theta$ is
oscillatory as a function of the nunber of cycles $k$. .

### Fig. [5.29](#fig:fig5_3_8){reference-type="ref" reference="fig:fig5_3_8"}: Summary {#fig.-figfig5_3_8-summary}

Now, you may want to look at all the gates that were required to
implement one Grover cycle. The Hadamard is used repeatedly to turn
$\delta's$ into $h's$ and vice versa. In addition, we have a query gate
that flips the sign of the target component and the $U_0$ gate which
flips all signs except the first component. We have only shown two
q-bits, but the real power of quantum circuits comes when we scale up
the number $n$ of q-bits, because the size of each matrix is
$2^n \times 2^n$. So if this were a course on quantum computing we'd now
talk about how to implement these transformations with controlled gates
so that their complexity increases $\sim n$ and not $\sim 2^n$.

![All gates involved in Grover
iteration](./Week5_3/figure8.jpg){#fig:fig5_3_8 width="\\textwidth"}

Next we'll talk about another seminal algorithm in the quantum
literature, known as Shor's algorithm.

### Quiz

#### Question 1

If a system of 20 quantum spins is used to implement the Grover search
algorithm, how many queries will be needed?[^75]

#### Question 2

If a system of 4 quantum spins is used to implement the Grover search
algorithm, then after one query cycle what will be the amplitude of the
target relative to the background?[^76]

## Shor's Algorithm {#Sec:Shor}

This is [Lecture 5.4: Watch youtube
video](https://www.youtube.com/watch?v=DaTxQ-C-Nis)

In the last lecture, we talked about this Grover search algorithm, which
makes use of quantum transformations to implement an efficient search
algorithm. In this lecture, we'll talk about another celebrated quantum
algorithm, one that allows you to factorize large numbers efficiently.

### Figs. [5.30](#fig:fig5_4_1){reference-type="ref" reference="fig:fig5_4_1"}-[5.32](#fig:fig5_4_3){reference-type="ref" reference="fig:fig5_4_3"}: How the algorithm works {#figs.-figfig5_4_1-figfig5_4_3-how-the-algorithm-works}

#### Fig. [5.30](#fig:fig5_4_1){reference-type="ref" reference="fig:fig5_4_1"}: {#fig.-figfig5_4_1}

The way this works is, supposing I want to factorize a number $F$, then
the first step is to find the period $r$ of the function
$a^x \text{mod}(F)$, where $a$ is a number you can choose arbitrarily,
any number you want, and what you have to find is the period of this
function (see Fig. [5.30](#fig:fig5_4_1){reference-type="ref"
reference="fig:fig5_4_1"}). When $F$ is a big number, the difficult part
is to find the period of this function and that's what the actual
algorithm does, it uses quantum circuits to find the period.

![Shor's Algorithm.](./Week5_4/figure1.jpg){#fig:fig5_4_1
width="\\textwidth"}

#### Figs. [5.31](#fig:fig5_4_2){reference-type="ref" reference="fig:fig5_4_2"}-[5.32](#fig:fig5_4_3){reference-type="ref" reference="fig:fig5_4_3"} {#figs.-figfig5_4_2-figfig5_4_3}

Supposing I'm trying to factorize 15 and I choose $a$ equal to 11 (see
Fig. [5.31](#fig:fig5_4_2){reference-type="ref"
reference="fig:fig5_4_2"}). So $11^0 \text{mod}(15)$ is 1,
$11^1 \text{mod}(15)$, is 11, $11^2 \text{mod}(15)$, that's
$121 \text{mod}(15)$, which is 1 again, and so it keeps oscillating
between 1 and 11. It's a periodic function whose period is 2. Now as I
said, $a$ is not unique, you can choose any $a$. So if you chose $a$
equal 7, then you'd get a different period, 4. In either case you can
find the gcd's as shown and obtain the factors 3 and 5. So that's how
the overall thing works. Now the point is to find this period.

![Finding period of $a^x mod(F)$, MATLAB code included at end of
book](./Week5_4/figure2.jpg){#fig:fig5_4_2 width="\\textwidth"}

![Finding factors of F from period $r$ of $a^x mod(F)$, same MATLAB code
as in Fig. [5.31](#fig:fig5_4_2){reference-type="ref"
reference="fig:fig5_4_2"}](./Week5_4/figure3.jpg){#fig:fig5_4_3
width="\\textwidth"}

### Figs. [5.33](#fig:fig5_4_4){reference-type="ref" reference="fig:fig5_4_4"}-[5.35](#fig:fig5_4_6){reference-type="ref" reference="fig:fig5_4_6"}: Period-finding with a quantum circuit {#figs.-figfig5_4_4-figfig5_4_6-period-finding-with-a-quantum-circuit}

#### Fig. [5.33](#fig:fig5_4_4){reference-type="ref" reference="fig:fig5_4_4"}: {#fig.-figfig5_4_4}

So how does a quantum circuit find the period? As shown, you have a main
register and an auxiliary register each with a certain number of q-bits,
and I've chosen 4 for illustration. Actually you'd need more than that
even to factorize 15. But just to keep it from getting too messy, let me
stick to 4. As you can see, I've already got $2^4=16$ components per
register and it is kind of hard to see the thing clearly. Just so you
can easily recognize which component we are talking about, I've put a
red marker after every four of them. So the 4th one is red, 8th one is
red, and the 12th one is red, and the 16th one is red indicating 0, 1,
2, 3 up to 15.

You start off with both registers in the zero state which means that the
first item has an amplitude of 1, rest are all 0's. The first step is do
the Hadamard transformation and we have discussed it often enough that
you know immediately what to expect. You get our old friend $h_0$ from
the last lecture, having $+1$ everywhere with the $1/\sqrt{2^4}$ in
front. That's the main register and then, of course, we have the
auxiliary register, which is still in the 0 state, what we had named
$\delta_0$ earlier. So the overall state of all eight q-bits is the
Kronecker product of the two registers: $h_0 \times \delta_0$.

We now apply the gate $U_f$ which performs a transformation so that for
the $x$ component of the main register it puts $1$ for the $f(x)$
component of the auxiliary register. For our example $f(x)$ is either 1
or 11, for alternating components of the main register. So the composite
wavefunction splits into two components $\psi_1 \times \delta_1$ +
$\psi_2 \times \delta_{11}$ where $\psi_1$ contains all the components
for which $f(x)=1$ and $\psi_2$ contains the other components for which
$f(x)=11$.

Note that the elements are numbered from 0, so 11 appears at the
$12^{th}$ position which is one of the red-marked elements. As you
probably realize, we get two components, $\psi_1 \times \delta_1$ and
$\psi_2 \times \delta_{11}$ because the period is 2. If the period had
been 4, then I'd have four terms to write. I chose this example so that
I have only two parts and I can write it out cleanly.

![Quantum Circuits.](./Week5_4/Picture4.png){#fig:fig5_4_4
width="\\textwidth"}

#### Fig. [5.34](#fig:fig5_4_5){reference-type="ref" reference="fig:fig5_4_5"}: Quantum Fourier Transform {#fig.-figfig5_4_5-quantum-fourier-transform}

![Quantum Fourier Transform](./Week5_4/Picture5.png){#fig:fig5_4_5
width="\\textwidth"}

Next you apply is what's called the Quantum Fourier Transform, which
takes what we have, namely $\psi_1 \times \delta_1$ +
$\psi_2 \times \delta_{11}$ and operates only on the
$\textit{main register}$ to produce a set of coefficients which are the
Fourier Transform of the original coefficients giving
$\phi_1 \times \delta_1$ + $\phi_2 \times \delta_{11}$, where $\phi_1$
and $\phi_2$ are the Fourier transforms of $\psi_1$ and $\psi_2$
respectively.

Now both parts of our main register $\psi_1$ and $\psi_2$ are periodic
functions with the same period, namely 2. So their Fourier transforms
are essentially the same function except for an overall phase factor
coming from the fact that $\psi_1$ and $\psi_2$ are shifted with respect
to each other. So we could replace $\phi_1$ and $\phi_2$ with a common
function $\phi$ having two peaks and write the composite wavefunction as
$\sim \phi \times (\delta_1 + \delta_{11})$.

Now if you come in and measure the main register, you will see two peaks
and when you see two peaks, you conclude that, $r$ is equal to 2, and
remember, that was the original purpose, to find the period $r$ so that
you can then go ahead and find the factors (see Fig.
[5.34](#fig:fig5_4_5){reference-type="ref" reference="fig:fig5_4_5"}).
In real problems the period will be much longer than two, and
correspondingly many more peaks in the QFT and you may need special
algorithms to find them efficiently.

#### Fig. [5.35](#fig:fig5_4_6){reference-type="ref" reference="fig:fig5_4_6"} {#fig.-figfig5_4_6}

![U-matrix for Quantum Fourier
Transform](./Week5_4/Picture6.png){#fig:fig5_4_6 width="90%"}

Now, what does the $U-matrix$ for this Quantum Fourier Transform look
like? Well, the basic transformation would look something like this.
This is basically the digital Fourier Transform for disrete time samples
that you may have seen before. The first column is all 1's. Next one
goes 1, P, $P^2$, etc. The next one goes 1, $P^2$, $P^4$, etc, where $P$
is the phase factor $exp(+i2\pi/N)$.

### Fig. [5.36](#fig:fig5_4_8){reference-type="ref" reference="fig:fig5_4_8"}: Summary {#fig.-figfig5_4_8-summary}

So overall, the picture is something like this. You start with the zero
state for both registers $\delta_0 \times \delta_0$, apply the Hadamard
to the main register to get $h_0 \times \delta_0$.

Then you apply $U_f$ which anytime there's an $x$ in the main register,
associates it with a $f(x)$ in the auxiliary register. giving a sum over
$r$ terms, r being the period of $f(x)$:
$\sum_{i=0}^{r-1}\psi_i \times \delta_{f(i)}$.

All $\psi_{i}$ have the same Fourier transform $\phi$ except for an
overall phase factor, so when we apply the QFT to the main register we
get $\phi \times \sum_{i=0}^{r-1} \delta_{f(i)}$. Now you look at the
main register and count the number of peaks to obtain the period, $r$.

![Shor's Algorithm](./Week5_4/Picture8.png){#fig:fig5_4_8
width="\\textwidth"}

If this was a course on quantum computing, then the next point we'd be
discussing is, how we implement this QFT transformation and this other
transformation that I talked about, which takes $x$ and associates an
$f(x)$ with the auxiliary register.

So these are things we won't be going into. My main point is to show how
these quantum algorithms make use of interference, make use of complex
numbers to get peaks in the result, peaks that give you the correct
solution in a way that is very different from what you can do with
classical circuits.

### Quiz

#### Question 1

The input wavefunction to the $U_f$ gate in Shor's algorithm can be
written as $\psi \times A$ which is a Kronecker product of the
wavefunction $\psi$ of the main register with that for the auxiliary
register, $A$. After the $U_f$ gate the wavefunction breaks up into r
pieces: $\psi_1 \times A_1$ + $\psi_2 \times A_2$ +
$\cdot \cdot \cdot$ + $\psi_r \times A_r$.\
What is $r$?[^77]

#### Question 2

Which register(s) does the quantum Fourier transform (QFT) in Shor's
algorithm act on?[^78]

## Feynman Paths {#feynman-paths}

This is [Lecture 5.5: Watch youtube
video](https://www.youtube.com/watch?v=xqk-2hZLod4)

In the last few lectures, we have been talking about gated quantum
computing, where the idea is to manipulate the wave function through a
sequence of quantum gates and we just discussed two of the celebrated
quantum algorithms, which do just that. Now, what we want to do in this
lecture is to introduce a different way of looking at what these gates
do in terms of what are called Feynman Paths. But instead of looking at
specific algorithms, we'll try to illustrate the main point by looking
at just the Hadamard gate, the one we introduced Lecture 5.2 and which
is used as part of all these algorithms. This illustrates the basic
point that we want to get across.

### Figs. [5.37](#fig:fig5_5_1){reference-type="ref" reference="fig:fig5_5_1"}-[5.40](#fig:fig5_5_4){reference-type="ref" reference="fig:fig5_5_4"}: Matrix multiplication as a sum of paths {#figs.-figfig5_5_1-figfig5_5_4-matrix-multiplication-as-a-sum-of-paths}

#### Figs. [5.37](#fig:fig5_5_1){reference-type="ref" reference="fig:fig5_5_1"}: Hadamard chain {#figs.-figfig5_5_1-hadamard-chain}

![Hadamard Gate](./Week5_5/figure1.jpg){#fig:fig5_5_1
width="\\textwidth"}

Remember the transformation matrix for a one q-bit Hadamard matrix. The
interesting thing is if you start from all up and you apply it once, it
spreads it out equally between the up and the down states. Then when you
apply it again, it goes back to all up. This spreading and then coming
back, that's usually not something you can do with classical systems and
that's kind of part of the magic of quantum and comes from this negative
sign(s) in the $U$ matrix. We'll talk more about this.

#### Fig. [5.38](#fig:fig5_5_2){reference-type="ref" reference="fig:fig5_5_2"}: {#fig.-figfig5_5_2}

![Matrix multiplication as a sum of
paths](./Week5_5/figure2.jpg){#fig:fig5_5_2 width="\\textwidth"}

Feynman paths give you a different way of looking at it. You could think
of it this way, supposing you start with the 0 state initially and we
know that after applying this Hadamard gate twice, you get back to 0,
and the reason is that if I multiply the two matrices, I get the
identity matrix, which takes me back where I started from.

But as we noted in Fig. [3.45](#fig:fig3_5_10){reference-type="ref"
reference="fig:fig3_5_10"} in the classical context, matrix
multiplication involves summations like
$[AB]_{ij} = \sum_k A_{ik} B_{kj}$ and one can view each term in the
summation as the weight of a path that takes you from $j$ to $i$ and the
sum over all the paths gives you the final answer.

So you could think of it this way that you went from 0 to 0, but through
one of two paths, one path is (000), and the other path is (010). Both
have the same amplitude $1/\sqrt{2}\times1/\sqrt{2}$, that's a 1/2, and
you add them up, you get 1.

Now, consider the other outcome, the one that doesn't happen. Here too
we have two possible paths (100) and (110) but now the amplitudes are
+1/2 and -1/2 and they cancel out. The negative sign comes from $U_{11}$
which is involved in the path (110), but not in (100). So that's the
Feynman path way of thinking, but it is really just a pictorial view of
the underlying matrix math.

#### Fig. [5.39](#fig:fig5_5_3){reference-type="ref" reference="fig:fig5_5_3"} {#fig.-figfig5_5_3}

![Number of paths increases exponentially with circuit
depth](./Week5_5/figure3.jpg){#fig:fig5_5_3 width="\\textwidth"}

Now, if you had many of these Hadamard gates, all applied sequentially,
at time steps 1, 2, all the way to capital $T$, then you see we now have
lots and lots of paths that can be labeled with binary numbers having
$T+1$ digits. Earlier we had $T=2$ and so paths were labeled with three
digits like (010). So now starting from a particular state, say 0, you
have $2^T$ total paths, half of them $2^{T-1}$ end up at 0 and the other
half at 1.

Now, if you had $n$ q-bits, then there would be $2^n$ configurations at
each time step and the total number of paths would be $2^{nT}$. So
that's the number that determines how many paths you have: involves both
the number $n$ of q-bits and the number of time steps or the depth of
the gates, $T$.

#### Fig. [5.40](#fig:fig5_5_4){reference-type="ref" reference="fig:fig5_5_4"}: Quantum versus probabilistic circuit {#fig.-figfig5_5_4-quantum-versus-probabilistic-circuit}

![Quantum versus probabilistic
circuit](./Week5_5/figure4.jpg){#fig:fig5_5_4 width="\\textwidth"}

Now, if you were doing this with a probabilistic circuit, you'd still
have the same number of paths. But the difference is that the amplitudes
for the paths are determined by the classical transition matrix $W$
which has all positive elements. In the quantum case, that amplitudes
are determined by the $U$ matrix where each amplitude is a complex
number.

Does that make a difference? Well, not too much if we are just going to
multiply the matrices. If we're going to write down matrices and
multiply them, then you see, it's not too much more difficult to
multiply complex matrices compared to real matrices. It's a little more
complicated, but not a whole lot. But in practice, you see, as you scale
the problem up, you cannot really afford to write down matrices and
multiply them, why? Because the matrices are $2^n \times 2^n$, and as we
know, as $n$ goes up, this $2^n$ just goes up exponentially, and it's
very soon it's out of control.

### Fig. [5.41](#fig:fig5_5_6){reference-type="ref" reference="fig:fig5_5_6"}: Quantum Monte Carlo {#fig.-figfig5_5_6-quantum-monte-carlo}

![Adapting sampling techniques to quantum
circuits](./Week5_5/Picture6a.png){#fig:fig5_5_6 width="\\textwidth"}

So what do you do? Well, for practical problems, you use sampling
techniques as we discussed in Chapters 2 and 3, which let us operate in
$nT$ space and generate samples in the $2^{nT}$ space. Similarly we
could generate sample paths that start with $0$ as shown and end on a
$0$ or a $1$. In classical sampling we use some algorithm like
Metropolis or Gibbs to select proposals based on the probability ratio
of the proposed path and the current path. In quantum sampling we have
complex path amplitudes whose squared magnitude gives the probability.
We could use the same classical algorithms replacing the probability
ratios with the magnitude of amplitude ratios. But we also have to
replace ordinary samples with $\textit{complex samples}$ whose phase
reflects the $\textit{phase of the path amplitudes}$. That seems
straightforward enough, but replacing positive samples with complex
samples is not as innocent as it sounds. It leads to the well-known sign
problem associated with Quantum Monte Carlo.

### Fig. [5.42](#fig:fig5_5_9){reference-type="ref" reference="fig:fig5_5_9"}: Sign problem {#Sec:Sign}

Actually our illustrative problem with the Hadamard chain presents an
extreme example that clearly shows the difficulty with complex samples.
Consider the two sets of paths shown, assuming just one q-bit ($n=1$),
and a depth 0f $T=10$. So we have $2^10=1024$ paths, $512$ of which end
up at $(0)$ and the other $512$ end up at $(1)$. Interestingly every
path has the same magnitude, $(1/\sqrt2)^{10}$, but some are positive
and some are negative. This is because the amplitude of any path is a
product of ten elements of the $U_H$ matrix, and all elements of this
matrix have the same magnitude $1/\sqrt2$.

![Sign Problem](./Week5_5/Picture9a.png){#fig:fig5_5_9
width="\\textwidth"}

But if both outputs $(0)$ and $(1)$ have $512$ paths leading upto them
all having the same magnitude $(1/\sqrt2)^{10}$, then why do they add up
to $1$ for one and to $0$ for the other? $\textit{Answer:}$ For the
wrong output $(1)$, 256 paths are positive, $256$ are negative, and they
cancel perfectly. For the correct output $(0)$, $272$ paths are
positive, $240$ are negative, giving a a net positive of $32$. Since
each path has a magnitude $(1/\sqrt2)^{10} = 1/32$, they add up to $1$.

This cancellation of paths makes it much harder to get reliable results,
it requires a lot more samples to be able to distinguish between the
correct output (0), $272-240=32$ and the wrong output (1), $256-256$.
Roughly speaking we could say that the signal to noise ratio is
$32/1024$. The situation gets worse as the depth gets larger.

In general the signal to noise ratio is $2^{T/2}/2^{T}=2^{-T/2}$, and to
detect the signal reliably we have to reduce the noise by collecting
lots of samples, $N_s$:
$1/\sqrt{N_s} \sim 2^{-T/2} \rightarrow N_s \sim 2^T$. More generally
the number of samples $\sim 2^{nT}$. But the point is that sampling is
really not getting us any advantage at all. If we are going to collect
$\sim 2^{nT}$ samples, we might as well sum all $\sim 2^{nT}$ exactly.
The strength of the sampling method lies in being able to get accurate
answers with far less samples than the total population of $2^{nT}$
paths. Because all paths in this problem have the same amplitude
(magnitude wise) our method is choosing all paths with equal
probability. This amounts to random sampling and we do not get any of
the advantages that usually come from classic sampling algorithms like
Metropolis or Gibbs.

Now, although we did not discuss it in chapter 4, the density matrix
$\sim e^{-\beta H}$ in adiabatic quantum computing can also be evaluated
by sampling Feynman paths, and in that case people make this distinction
between stoquastic Hamiltonians and non-stoquastic Hamiltonians.
Stoquastic ones are those where all paths have the same sign with no
cancellations, and so sampling is very effective, whereas non-stoquastic
ones are those that involve path cancellation, with its associated sign
problems that we just discussed.

In this chapter we have been focusing on gated quantum computing, which
is based on the quantum transition matrix $U=e^{-iH}$ which is almost
always non-stoquastic. But the most severe sign problems arise when all
elements have the same magnitude like the Hadamard matrix or the
$U-matrix$ for the quantum Fourier transform (QFT),
Fig.[\[fig:fig5_5_13\]](#fig:fig5_5_13){reference-type="ref"
reference="fig:fig5_5_13"}. Our standard sampling algorithms then lead
to essentially random sampling, requiring an enormous number of samples
comparable to the total number of paths.

Problems with severe $sign$ $problems$ like this are precisely the ones
where quantum computers can shine by comparison. In the sampling method,
an output that has zero probability, attracts $2^{T-1}$ samples, which
cancel out to give zero. By contrast a q-bit in a quantum computer would
know $instinctively$ that the net wavefunction for this output is zero,
and not a single sample would reach that output.

Of course, that's true only of the ideal quantum computer, the one
that's noiseless. In the real world, we have to deal with noise because
the quantum computer is in touch with its surroundings, which have noise
that destroys the phase and when the phase is destroyed, the samples
cannot cancel very effectively and give you nulls. It remains to be seen
how much noisy quantum computers can actually help us with problems
having sign problems.

### Quiz

#### Question 1

A Hadamard gate $\frac{1}{\sqrt{2}} \left [ \begin{array}{r r}
1 & \ 1  \\
1 & \ -1  \\
\end{array} \right ]$

acting 20 times in sequence on a wavefunction $\{0\quad 1\}^T$ produces
the same wavefunction $\{0\quad 1\}^T$ at the end.\
$2^{19}$ Feynman paths lead from the specified initial state
$\{0\quad 1\}^T$ to the final state $\{0\quad 1\}^T$.

$2^{19}$ Feynman paths also lead from the specified initial state
$\{0\quad 1\}^T$ to the WRONG final state $\{1\quad 0\}^T$.\
Why is the final probability for the wrong state so much smaller tha
that for the correct state?[^79]

#### Question 2

A Pauli-X gate $\left [ \begin{array}{r r}
0 & \ 1  \\
1 & \ 0  \\
\end{array} \right ]$

acting 20 times in sequence on a wavefunction $\{0\quad 1\}^T$ produces
the same wavefunction $\{0\quad 1\}^T$ at the end.\
$2^{19}$ Feynman paths lead from the specified initial state
$\{0\quad 1\}^T$ to the final state $\{0\quad 1\}^T$.

$2^{19}$ Feynman paths also lead from the specified initial state
$\{0\quad 1\}^T$ to the WRONG final state $\{1\quad 0\}^T$.\
Why is the final probability for the wrong state so much smaller tha
that for the correct state?[^80]

## Fig. [5.43](#fig:fig5_6_2){reference-type="ref" reference="fig:fig5_6_2"}: 5-minute summary {#fig.-figfig5_6_2-5-minute-summary}

[Watch youtube video, after
2:20](https://www.youtube.com/watch?v=JiESPuChnOM)

![Chapter 5 summary](./Week5_6/Picture2.png){#fig:fig5_6_2
width="\\textwidth"}

In this chapter we transitioned to gated computing involving isolated
quantum systems that can be described in terms of its wave function
which is transformed in time according to these quantum gates, applied
sequentially one after the other. In Lecture 5.1 we introduced the
quantum transition matrix $U$ describing this transformation of
wavefunctions. It is also the quantum analog of the classical transition
matrix $W$ in chapter 3.

In Lecture 5.2 we introduced the Hadamard gate which is a very useful
gate and used in many quantum circuits. It also illustrates the basic
magic of quantum circuits, coming from the negative element in $U$ which
allows it to do something very remarkable: If you start from a delta
function distribution, delta function meaning where all the amplitude is
in one particular state and apply a Hadamard gate to it, it spreads out
into a distribution where all components are present, but then you apply
the Hadamard gate again and you come back to the delta function, this is
something that wouldn't happen with probabilistic distributions. Once
you have spread out, it will continue spreading.

In Lecture 5.3 and 5.4 we talked about how this Hadamard gate is
combined with other ideas in two celebrated quantum algorithms, the
Grover's search and Shor's algorithm. Finally, in Lecture 5.5 we talked
about this concept of Feynman Paths, how you can think about all these
quantum gates, or probabilistic circuits within the same framework. What
you get at the end is like a sum of the amplitudes of different paths
and the difference between the quantum and the classical is, in the
classical case all paths have positive amplitudes whereas in the quantum
case they can have negative or even complex amplitudes which can cancel
each other out, and because of this \"sign problem\" the sampling
procedure which is so effective with classical system is trickier to
implement in the case of quantum systems.

But quantum systems in order to perform their magic require all the
phases to be precisely preserved, and in practice you have to deal with
noise and control it. At this time there is worldwide effort and
research trying to see if we can use noisy quantum systems to solve real
world problems more efficiently than their classical counterparts.

# Epilogue {#epilogue .unnumbered}

![In this course, we've brought together concepts from three very
different areas.](./Epilogue/Figure1a.png){#fig:fig5_7_1 width="90%"}

I personally was very intrigued by something I had read over 40 years
ago. It was a comment by Feynman in a paper that actually was one of the
papers that inspired the world of quantum computing. But in that paper
before getting to quantum computing, he introduced the idea of a
probabilistic computer and he made the point that what really makes the
quantum world so different is, it is as if you have negative
probabilities, something that's unknown in our everyday classical world.
And that is the fundamental difference.

This thought seems to be just as true today as it was 40 years ago, and
that is what I've tried to convey in this course using modern examples
from machine learning and quantum computing. I was hoping to give you a
different perspective, showing the connections between these two
different worlds. I hope you find that enjoyable and will have use for
it.

But as I mentioned at the outset, this is a work in progress. Hope to
have a more complete story next time.

# MATLAB codes {#matlab-codes .unnumbered}

[Matlab]{.smallcaps} code for Figs.
[2.36](#fig:fig2_3_12){reference-type="ref" reference="fig:fig2_3_12"}
and [2.37](#fig:fig2_3_13){reference-type="ref"
reference="fig:fig2_3_13"}, Lecture 2.3:

``` {.octave language="Octave"}
% Max-cut problem
clear all
rng(1)

N = 6; C = zeros(N); N2 = N/2;
C(1,2) = 12; C(2,1) = C(1,2);
C(1,5) = 3; C(5,1) = C(1,5);
C(3,4) = 6; C(4,3) = C(3,4);
C(2,5) = 5; C(5,2) = C(2,5);
C(3,6) = 8; C(6,3) = C(3,6);
C(4,6) = 14; C(6,4) = C(4,6);

u=ones(N,1);
% % % %     ctr=randperm(N); C=C(ctr,ctr);
    
X=[0:2^N-1]; Look = 2.^[N-1:-1:0];
I0=1/4; T = 1e6;

K=5*0; % enforcing equal number in each group
M=+1; % +1 for min-cut, -1 for max-cut

w= 2*K - M*4*C; w= w - diag(diag(w));
x = -K*(N-1) + M*C*u + M*C'*u;

% % % % Boltzmann law
    rhos=zeros(N,N); rhom=zeros(N,N); E=zeros(1,2^N);

    for ii= 1:2^N
        n=de2bi(ii-1,N,'left-msb')';
        E(ii) = n' * x + 0.5 * n' * w * n ;
    end
P=exp(-I0*E); P=P./sum(P);

% % % % Sampling method

n=de2bi(1,N,'left-msb')'; %initial state
for ii=1:T
for jj=randperm(N) 

    xx= x(jj) + w(jj,:)*n;    
    f=1/(1+exp(I0*xx));
        n(jj)=0;  if f > rand
                    n(jj)=1; end
end
nn(:, ii)=n;
end

D=Look*nn;
PSL=histcounts(D,[0:2^N]);
PSL=PSL./T;

figure(2)
bar(X',[PSL'],0.75)
set(gca,'Fontsize',24)
grid on

figure(20)
PP=P;
PP=reshape(PP,2^N2,2^N2);
bar3(PP,0.25)
set(gca,'xticklabel', dec2bin([0:2^N2-1]) )
set(gca,'xticklabelrotation', -90)
set(gca,'yticklabel', dec2bin([0:2^N2-1]) )
set(gca,'yticklabelrotation', 90)
set(gca,'Fontsize',14)
grid on
```

[Matlab]{.smallcaps} code for Figs.
[2.59](#fig:fig2_5_10){reference-type="ref" reference="fig:fig2_5_10"}
and [2.60](#fig:fig2_5_11){reference-type="ref"
reference="fig:fig2_5_11"}, Lecture 2.5:

``` {.octave language="Octave"}
%%%% General learning code for Boltzmann machine with hidden units using Boltzmann law
%%%% Jan Kaiser, 6/13/2020

clear all

rng(1)
momentum=0.9*0; epsilon=1e-2; weightcost=1e-4; % learning rate, regularization
NT=1e5; %run time

%%%% Use this to train full adder with no hidden units
Nv = 5; Nh = 0; Nm= Nv + Nh; % visible, hidden
d=zeros(1,2^Nv);    d([0 6 10 13 18 21 25 31]+1)=1; % PDF, full adder

% Nv = 6; Nh = 4; Nm= Nv + Nh; % visible, hidden
% d=zeros(1,2^Nv);    d([5 10 17 24 29 40 48 51 57 62]+1)=1;

df=repelem(d,1,2^Nh);

J=randn(Nm,Nm);J=J-diag(diag(J));J=(J+J')/2; Jinc=zeros(Nm,Nm);
h=zeros(1,Nm); hinc=zeros(1,Nm); tic

for epoch=1:NT
    
    for ii=0:2^Nm-1            
        m=flip(de2bi(ii,Nm))'*2-1; mm(ii+1,:)=m';
        E(ii+1)=-m'*J/2*m-h*m;
    end
    E=E-min(E);
    Pf=exp(-E);Z=sum(Pf); Pf=Pf/Z; % Free phase
    
    for ii=1:2^Nv  %% artificallly normalize for hidden units
        P0(1+(ii-1)*2^Nh:(ii)*2^Nh)=...  
          Pf(1+(ii-1)*2^Nh:(ii)*2^Nh)./sum(Pf(1+(ii-1)*2^Nh:(ii)*2^Nh));
    end 
    Pc=P0.*df; ZZ=sum(Pc); Pc=Pc/ZZ; % Clamped phase
    
%%%% correlations
    Corrf=zeros(Nm,Nm); Corrc=zeros(Nm,Nm);
    for ii=1:Nm
        for jj=1:Nm
            Corrf(ii,jj)=sum(mm(:,ii).*mm(:,jj).*Pf',1);
            Corrc(ii,jj)=sum(mm(:,ii).*mm(:,jj).*Pc',1);
        end
    end
    Corrf = Corrf-diag(diag(Corrf));
    Corrc = Corrc-diag(diag(Corrc));

%%%% bias
    hf=Pf*mm; hc=Pc*mm;

%%%% update 
    Jinc=epsilon*(Corrc-Corrf-weightcost*J) + momentum*Jinc;
    hinc=epsilon*(hc-hf) + momentum*hinc;

    J=J+Jinc; h=h+hinc;  

        Jincrement(epoch)=sum(sum(abs(Jinc)));
        hincrement(epoch)=sum(abs(hinc));  err(epoch)=sum(abs(Pf-Pc));
 
        if mod(epoch,1e3)==0
            disp(['Learning process: ',num2str(epoch/NT*100),'%    ',...
            'Time: ', num2str(toc)])
        end

end

save J

    if Nh==0
        Pfv=Pf; Pcv=Pc;
    end

    if Nh~=0
        Pfv=sum(reshape(Pf,2^Nh,2^Nv));
        Pcv=sum(reshape(Pc,2^Nh,2^Nv));
    end

%%   
%%%% Plot results
figure(1)
bar([0:2^Nv-1],[Pfv(1:2^Nv)',Pcv(1:2^Nv)'],0.5)
set(gca,'Fontsize',12)
legend('learned distribution','target distribution')
ylabel('PDF')
xlabel('configuration')
```

[Matlab]{.smallcaps} code for Fig.
[2.61](#fig:fig2_5_12){reference-type="ref" reference="fig:fig2_5_12"},
Lecture 2.5:

``` {.octave language="Octave"}
% Separating hidden variables
clear all
rng(1)

% 5 10 17 24 29 40 48 51 57 62, 10 peaks
load J % First run previous code with these peaks and save J.mat

Nv=6; N=10; u=ones(N,1);
J = -J; h = -h;
w=4*J; % % % % Bipolar to Binary
x=2*h'-J*u-J'*u;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
I0 = 1/2;
% % % Boltzmann law
for ii= 1:2^N
    n=de2bi(ii-1,N,'left-msb')';
    E(ii) =  n' * x + 0.5 * n' * w * n ;
end
Emin=min(E);
P=exp(-I0*(E-Emin)); P=P./sum(P);
PP=reshape(P,16,64);

% % Sampling
T = 1e4;
Look = 2.^[N-1:-1:0]; 

n=de2bi(1,N,'left-msb')'; %initial state
for ii=1:T
for jj=randperm(N)