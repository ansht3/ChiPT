#### Figs. [2.33](#fig:fig2_3_9){reference-type="ref" reference="fig:fig2_3_9"}-[2.35](#fig:fig2_3_11){reference-type="ref" reference="fig:fig2_3_11"}: Constraints through energy {#figs.-figfig2_3_9-figfig2_3_11-constraints-through-energy}

![Imposing constraint through
energy](./Week2_3/figure9.jpg){#fig:fig2_3_9 width="\\textwidth"}

![Imposing constraint through
energy](./Week2_3/figure10.jpg){#fig:fig2_3_10 width="\\textwidth"}

![Imposing constraint through
energy](./Week2_3/figure11.jpg){#fig:fig2_3_11 width="\\textwidth"}

So, that is where we have to put in a constraint into the problem. We
have to figure out a way so that whenever the number in the two groups,
when the number of 1s is not equal to the number of 0s, there is a large
energy cost to it. Remember, in all optimization problems there is a
cost function, you see what the problem does is try to minimize that
cost. Of course, in these Boltzmann circuits, in these things what is
minimized is the energy, so energy is the cost function. So the way you
do it is (see Fig. [2.33](#fig:fig2_3_9){reference-type="ref"
reference="fig:fig2_3_9"}), I could add a term like this
$(\sum_{r}{s_r}-(n/2))^2$ to the energy. Now I already have something
and I'm going to add another term, and what is this term? It says that
well, when I add up the values of all the spins, the answer should be
equal to half the total number, so if I add 6, the answer should be 3.
Then you can see that these, $\{1 1 0 0 1 0\}$ and $\{0 0 1 1 0 1\}$,
when I add them all up, I get 3. But these ones, $\{0 0 0 0 0 0\}$ and
$\{1 1 1 1 1 1\}$, when I add them up, I get 0 here, $\{0 0 0 0 0 0\}$,
and I get six there, $\{1 1 1 1 1 1\}$, so those are not acceptable,

If I add a term like this $(\sum_{r}{s_r}-(n/2))^2$ to the energy, it
will discriminate against those solutions. So again, we want to get it
back into this canonical form. The algebra is shown in Figs.
[2.33](#fig:fig2_3_9){reference-type="ref" reference="fig:fig2_3_9"},
[2.34](#fig:fig2_3_10){reference-type="ref" reference="fig:fig2_3_10"}
and [2.35](#fig:fig2_3_11){reference-type="ref"
reference="fig:fig2_3_11"}.

#### Fig. [2.36](#fig:fig2_3_12){reference-type="ref" reference="fig:fig2_3_12"} {#fig.-figfig2_3_12}

In the final result in Fig.[2.35](#fig:fig2_3_11){reference-type="ref"
reference="fig:fig2_3_11"} we have weighted the new constraint terms
with a constant $K$ which we can choose depending on how strongly I want
to enforce the constraint. Sure enough now if I do the simulation (see
Fig. [2.36](#fig:fig2_3_12){reference-type="ref"
reference="fig:fig2_3_12"}), by including the $K$, what we'll find is,
well, when $K$ was 0, we had these two extra peaks. But once we put in
the $K$, we only get the two peaks that we want. And to what extent
these unwanted peaks are suppressed will depend on what $K$ I use. So
here I use the $K$ of 4, if I had used something less like one or half,
then they wouldn't be completely suppressed. We would still see some of
it.

![State space response with (K=4) and without (K=0) constraint, MATLAB
code included at end of book](./Week2_3/figure12.jpg){#fig:fig2_3_12
width="\\textwidth"}

#### Figs. [2.37](#fig:fig2_3_13){reference-type="ref" reference="fig:fig2_3_13"}-[2.38](#fig:fig2_3_14){reference-type="ref" reference="fig:fig2_3_14"}: From min-cut to max-cut {#figs.-figfig2_3_13-figfig2_3_14-from-min-cut-to-max-cut}

So this is what you might call the min-cut problem as we discussed (see
Fig. [2.37](#fig:fig2_3_13){reference-type="ref"
reference="fig:fig2_3_13"}). So this is where you're trying to minimize
the energy of cutting the two groups apart, okay? Now, if you want to
solve the max cut problem, then what you do is you just add a minus sign
because an energy that minimizes something if you put a minus sign then
it will maximize it. So let's say you have 1, so you prefer 1 relative
to 10 but then if you put a minus sign, then of course you'll prefer
$-10$ relative to $-1$.

#### Fig. [2.37](#fig:fig2_3_13){reference-type="ref" reference="fig:fig2_3_13"} {#fig.-figfig2_3_13}

![From min-cut to max-cut, same MATLAB code as
Fig.[2.36](#fig:fig2_3_12){reference-type="ref"
reference="fig:fig2_3_12"}](./Week2_3/figure13.jpg){#fig:fig2_3_13
width="90%"}

#### Fig. [2.38](#fig:fig2_3_14){reference-type="ref" reference="fig:fig2_3_14"} {#fig.-figfig2_3_14}

![Max-cut](./Week2_3/figure14.jpg){#fig:fig2_3_14 width="90%"}

So you just have to add the $-1$. You don't change anything about the
term that has the $K$ in it because that is intended to ensure that you
have the same number of 0's and 1's in both groups. So now if you do
that, sure enough, you solve the max-cut problem and we'll get a
different set of peaks and now in this case the groups are 2 3 4 is one
group and 1 5 6 is the other group, $\{0 1 1 1 0 0\}$ and
$\{1 0 0 0 1 1\}$. So in other words (see Fig.
[2.38](#fig:fig2_3_14){reference-type="ref" reference="fig:fig2_3_14"}),
you like to keep the 2 3 and 4 together and 1 5 and 6 together, and you
can kind of see why, if you look at the connection matrix. You see,
there's a 12 that connects 1 and 2. So you want to put 1 and 2 in
separate groups so that when you cut it, you're cutting a 12. And
remember, this is the max-cut problem, where you want to cut as much as
possible.

Anyway, the bottom line is that (see Fig.
[2.39](#fig:fig2_3_15){reference-type="ref" reference="fig:fig2_3_15"}),
you could solve the min-cut problem or the max-cut problem just by
changing the sign of the second term. The first term is just for
imposing the constraint that you should have equal number of 0's and
1's.

### Figs. [2.39](#fig:fig2_3_15){reference-type="ref" reference="fig:fig2_3_15"}-[2.40](#fig:fig2_3_16){reference-type="ref" reference="fig:fig2_3_16"}: Summary {#figs.-figfig2_3_15-figfig2_3_16-summary}

#### Fig. [2.39](#fig:fig2_3_15){reference-type="ref" reference="fig:fig2_3_15"}: {#fig.-figfig2_3_15}

![x, w in matrix notation](./Week2_3/figure15.jpg){#fig:fig2_3_15
width="\\textwidth"}

Our final result for $x$ and $w$ can be written compactly in matrix form
as shown in Fig. [2.39](#fig:fig2_3_15){reference-type="ref"
reference="fig:fig2_3_15"}. For example, $w_{rq}=2K \mp 4C_{rq}$ becomes
$w = \mp 4[C]$ in matrix notation, and so on.

#### Fig. [2.40](#fig:fig2_3_16){reference-type="ref" reference="fig:fig2_3_16"}: {#fig.-figfig2_3_16}

So, summing up then what we're trying to show in this lecture is how you
can use probabilistic circuits to solve constrained optimization
problems (see Fig. [2.40](#fig:fig2_3_16){reference-type="ref"
reference="fig:fig2_3_16"}). And I showed it using this example of
min-cut and max-cut. You have a graph with a connection matrix, and the
point is how to divide it into two groups so that when you cut, you cut
as few connections as possible. Or as many connections as possible. And
you could easily go from one problem to the other by changing the sign
of the second term. And this constraint term weighted by the constant
$K$ tries to make the two groups be of equal size.

![Summary](./Week2_3/Picture2.jpg){#fig:fig2_3_16 width="\\textwidth"}

Finally I should note that in this lecture I chose the mincut / maxcut
problem because it translates straightforwardly to a cost or energy
function of the form $\widetilde{E}$ of the form $s^Tx + 0.5 s^Tws$.
Things may not be as straightforward if we consider otherwise
optimization problems, like say the traveling salesman problem (TSP): A
salesman has to visit say $N$ cities in sequence. Which route
corresponds to the shortest overall path? This problem can be translated
to $E=s^Tx + 0.5 s^Tws$, but it requires $N^2$ $p$-$bits$. More
efficient approaches are well-known and routinely used. It remains to be
seen if the TSP problem can be translated to $p$-$bit$ networks in a way
that would provide an improvement over established methods.

### Quiz

#### Question 1

The energy of a system of n classical spins (s is a binary variable with
two values 0 and 1) is given by
$\widetilde{E} = \big(s^T x + 0.5 \ s^T w s \big) \times E_0$.\
Suppose $x_r = -(n-1)$,\
$w_{rq} = 2$ if $r \neq q$ and $w_{rq} = 0$ if $r = q$.\
Which states have the highest probability?[^32]

#### Question 2

The energy of a system of 4 classical spins (s is a binary variable with
two values 0 and 1) is given by
$\widetilde{E} = \big(s^T x + 0.5 \ s^T w s \big) \times E_0$.\
Consider a graph with a connection matrix given by\
$C = \left [ \begin{array}{r r r r}
0 & \ 1 & \ 0 & \ 0 \\
1 & \ 0 & \ 0 & \ 0 \\
0 & \ 0 & \ 0 & \ 1 \\
0 & \ 0 & \ 1 & \ 0 \\
\end{array} \right ]$\
Suppose we choose $w_{rq} = -4 C_{rq}$ and $x_r = 2$.\
What are the highest probability peaks?[^33]

## Inference

This is [Lecture 2.4: Watch youtube
video](https://www.youtube.com/watch?v=LmW8-ugzM1c)

In the last lecture I used the mincut / maxcut problem because it
translates straightforwardly to a cost or energy function of the form
$\widetilde{E}$ of the form $s^Tx + 0.5 s^Tws$. However, as I mentioned
at the end, not all problems are quite as straightforward. In general we
may want an arbitrary set of peaks as shown in Fig.
[2.41](#fig:fig2_4_2){reference-type="ref" reference="fig:fig2_4_2"}.
Powerful learning algorithms have been developed to find the appropriate
$x$ and $w$ and in the next lecture I will try to give you an example.
In this lecture let me just try to give you an idea of how such
arbitrary peaks in state space could help us address practical
applications, assuming we have some way to learn the necessary $x$ and
$w$.

### Figs. [2.41](#fig:fig2_4_2){reference-type="ref" reference="fig:fig2_4_2"}-[2.45](#fig:fig2_4_7){reference-type="ref" reference="fig:fig2_4_7"}: Logic gates {#figs.-figfig2_4_2-figfig2_4_7-logic-gates}

#### Figs. [2.41](#fig:fig2_4_2){reference-type="ref" reference="fig:fig2_4_2"}: {#figs.-figfig2_4_2}

![Generating arbitrary peaks in state
space](./Week2_4/Picture1.jpg){#fig:fig2_4_2 width="\\textwidth"}

Okay, so, these peaks are just randomly chosen actually with nothing in
particular in mind (see Fig.
[\[fig:fig2_4_3\]](#fig:fig2_4_3){reference-type="ref"
reference="fig:fig2_4_3"}). Each peak is labeled with a 6-digit binary
number like say $\{000101\}$. Now this is something you could view as a
truth table, that is if you are familiar with logic gates in electrical
engineering or digital circuits. They usually have a truth table for
inputs and outputs.

#### Fig. [2.42](#fig:fig2_4_4){reference-type="ref" reference="fig:fig2_4_4"}: {#fig.-figfig2_4_4}

![Clamping inputs for the problem in Fig.
[2.41](#fig:fig2_4_2){reference-type="ref"
reference="fig:fig2_4_2"}.](./Week2_4/figure2.jpg){#fig:fig2_4_4
width="90%"}

Once $x$ and $w$ have been designed to give us these peaks, we could
operate the $p$-$bit$ network like a digital circuit in the sense that
you could go in and apply an input and look at the output. So whenever I
put an input say $\{011\}$, I'll get this output $\{101\}$.

Now how do you apply input? Well, you have to clamp these three bits to
$\{011\}$. So how do you clamp it? Well, because left to itself of
course they would be fluctuating all over the place, but you say well,
no these three bits needs to be $\{011\}$. So how do you do that? Well,
in your bias vector, $x$ you add a big positive number to clamp it to 0
and a big negative number to clamp it to 1.

Once you clamp your input, you could then go and look at the output
because you see originally, all of these six peaks were equally likely,
they all had low energies they had high probability. But now that you
have clamped it in the sense you have made it energetically favorable
for this to be $\{011\}$, the output will just lock into one of them.
And then you can read it and call that your output.

#### Figs. [2.43](#fig:fig2_4_5){reference-type="ref" reference="fig:fig2_4_5"} and [2.44](#fig:fig2_4_6){reference-type="ref" reference="fig:fig2_4_6"} {#figs.-figfig2_4_5-and-figfig2_4_6}

So that looks just like a digital circuit. But it's really a very
different kind of like digital circuit in the sense that it is much more
versatile. It can work backwards and forwards in different ways.

![Redefining input and output as 4+2 instead of
3+3](./Week2_4/figure4.jpg){#fig:fig2_4_5 width="80%"}

![Clamping example for the problem in Fig.
[2.43](#fig:fig2_4_5){reference-type="ref"
reference="fig:fig2_4_5"}.](./Week2_4/Picture3.jpg){#fig:fig2_4_6
width="80%"}

For example (see Fig. [2.43](#fig:fig2_4_5){reference-type="ref"
reference="fig:fig2_4_5"}), what we could do is to define the first four
$p$-$bits$ as inputs and the last two as outputs. So these first four,
that's what is on this axis. So four of them give you 16 numbers, which
I have written in decimal, rather than write it out as $\{0001\}$, I've
written it as $1$. So the first line $\{0001\}$ that's $1$. Next is
$\{0100\}$ that's like a 4 and so on.

So now you can think of the first four bits as your input and the last
two as your output. So, you could now go in and clamp the input (see
Fig. [2.44](#fig:fig2_4_6){reference-type="ref"
reference="fig:fig2_4_6"}), you could say, okay, the input is, let's
say, seven which is like $\{0111\}$. Now, what will happen then is the
output will go to the corresponding value on this side. So instead of
having all these six peaks like I'd shown before, now you'll just have
one peak and that peak you can now read output which is $\{01\}$.

#### Fig. [2.45](#fig:fig2_4_7){reference-type="ref" reference="fig:fig2_4_7"}: {#fig.-figfig2_4_7}

![Multiple inputs consistent with a clamped output
](./Week2_4/Picture4.jpg){#fig:fig2_4_7 width="\\textwidth"}

An even more interesting thing is that our $p$-$circuit$ can actually
work backwards an tell us all possible inputs that could have produced a
particular output. So what you could do is you could go in and say I'll
clamp the output to $\{01\}$ (see Fig.
[2.45](#fig:fig2_4_7){reference-type="ref" reference="fig:fig2_4_7"}).
How do I do that? Well, take the last two bits and put in a big bias
there, positive if you want a 0, negative if you want a 1 as we have
discussed. The original truth table, of course had all six
possibilities. But after clamping, only the three that correspond to
$\{01\}$ on the output will show up. That gives us all three possible
inputs 1, 4 and 7.

So I just clamped the output and the circuit gives me all three possible
inputs that correspond to that particular output. This is something that
a normal digital circuit would never do. They all work in one direction.
You put inputs, you get outputs. But here you can run it the other way
as well.

### Fig. [2.46](#fig:fig2_4_8){reference-type="ref" reference="fig:fig2_4_8"}: Image classification {#fig.-figfig2_4_8-image-classification}

Another use for $p$-$circuits$ could be for image classification (see
Fig. [2.46](#fig:fig2_4_8){reference-type="ref"
reference="fig:fig2_4_8"}). To see this note that what I called the
input, $\{0001\}$, could represent a series of black and white pixels
{black, black, black and white}. So in that sense, a binary input could
define an image like say a handwritten digit as shown, and what the
output could do is to classify them as 0, 1, 2 etc.

Now of course, real images have many bits because usually something like
this will have 28 pixels on one side and 28 pixels on the other side. So
it's a total of 784 pixels. And you'd have to indicate whether each
pixel is a 1 or 0 whether it's bright or dark. The $p$-$circuit$ could
take a binary string with 784 digits and classify it as one of ten
decimal numbers. image classification.

![Image Classification](./Week2_4/figure7.jpg){#fig:fig2_4_8
width="\\textwidth"}

The question is how do I design my $x$ and $w$ so that it will be able
to recognize all the different ways people write say a $4$ and classify
them all as four. And you want to make sure that you have actually
learned the images and haven't just memorized them meaning that you come
out with $x$ and $w$ that recognizes the training images very well, but
if you showed it something a little different, it may not recognize it
at all. So usually, you'd have a set of training images, but then you
test it with other images, which are not exactly the same but a little
different and if the $x$ and $w$ have been properly chosen, then not
only will it have memorized the training images, but also have learned
how to recognize the testing images. So these are among the many issues
you would discuss in a proper machine learning course, but we won't be
going into it. Right now the main point I wanted to make is that for a
lot of applications like invertible logic, image classification, etc.
what you want is to design your $x$ and $w$ in such a way that you get
these multiple peaks in your $2^n$ space that solve the problem at hand.

### Figs. [2.47](#fig:fig2_4_11){reference-type="ref" reference="fig:fig2_4_11"}-[2.48](#fig:fig2_4_12){reference-type="ref" reference="fig:fig2_4_12"}: A simple learning rule {#figs.-figfig2_4_11-figfig2_4_12-a-simple-learning-rule}

#### Figs. [2.47](#fig:fig2_4_11){reference-type="ref" reference="fig:fig2_4_11"}: {#figs.-figfig2_4_11}

In general then the problem amounts to you're given a set of peaks that
you want (see Fig. [2.47](#fig:fig2_4_11){reference-type="ref"
reference="fig:fig2_4_11"}), which we can call the truth table, $[t]$.
The number of columns in $[t]$ is the number of $p$-$bits$, n and the
number of rows is the number of peaks, $[n_t]$. Given $[t]$, how do I
write $x$ and $w$.

Next lecture we'll discuss learning in more detail. Let me just finish
up this lecture by giving you a simple rule that you could use to write
$x$ and $w$ in terms of $t$. This rule is of limited utility in the
sense it works when you have just a few lines in your truth table, but
you get in trouble if you have too many lines. But it's a nice simple
place to start from.

It is easier to state the learning rule in the bipolar representation
which is different from the binary representation we have been using. So
let me first explain this new representation. In any case this
representation is used a lot in the physics literature and so it is good
to be able to relate to it.

![Bipolar representation](./Week2_4/figure10.jpg){#fig:fig2_4_11
width="\\textwidth"}

So what is this bipolar representation? The idea is that, so far we've
been doing binary where $s$ is the variable and it's 0 or 1. Now, you
could instead have used a bipolar representation where instead of $0$
and $1$, it's actually $-1$ and $+1$ and as I said that's widely used in
this physics literature. Now, a truth table in binary $[t]$ can be
transformed to bipolar using the rule $t_m=2t-1$, which means if an
element in $t$ is 1, you get $+1$ in $[t_m]$, if $t$ is 0, you get $-1$.

Now, you could write the energy function, we had written it earlier in
terms of $s$ and $x$, $\widetilde{E}=s^{\rm T}x+(1/2)s^{\rm T}ws$, and
this $w$, instead of $s$, you could have $m$ which is the bipolar
representation, and then the corresponding bias and weight matrices I'll
write as $h$ and $J$, $\widetilde{E}=m^{\rm T}h+(1/2)m^{\rm T}Jm$,
following what is often done in the physics literature. So these are two
expressions, $\widetilde{E}=s^{\rm T}x+(1/2)s^{\rm T}ws$ and
$\widetilde{E}=m^{\rm T}h+(1/2)m^{\rm T}Jm$, which should give you the
same energy because you're still trying to solve the same problem. As we
will see, a little algebra gets us to a simple expression for
interconverting back and forth between $x$,$w$ and $h$,$J$.

#### Fig. [2.48](#fig:fig2_4_12){reference-type="ref" reference="fig:fig2_4_12"} {#fig.-figfig2_4_12}

The simple learning rule I mentioned earlier is easy to state in the
bipolar representation: $J=(-1/n^t)t_m^{\rm T}t_m$, whereas
$h=(-1/n^t)t_m^{\rm T}\widetilde{\mathbf{1}}$, where
$\widetilde{\mathbf{1}}$ is a $n_t \times 1$ column vector containing
all 1's. I've put a tilde on $\widetilde{\mathbf{1}}$ because it has
$n_t$ number of rows, whereas the 1 vector appearing in
$-J\mathbf{1}-J^{\rm T}\mathbf{1}$ without a tilde has $n$ rows.

In the next lecture I will try to motivate where this rule comes
from[^34] and how some of the recent work on the so-called modern
Hopfield networks seeks to go beyond it. For the moment let us just
focus on how we use this simple rule.

Suppose we are given a truth table $t$ in binary representation. To use
the learning rule stated above in bipolar representation, We first
convert to $t_m = 2t-1$, then write $h$ and $J$ using the rule stated
above, and then convert to $x$, $w$ using these relations,
$x=2h-J\mathbf{1}-J^{\rm T}\mathbf{1}$ and $w=4J$. How these relations
are obtained is explained in the next few slides.

![Simple learning rule in bipolar
representation](./Week2_4/figure11.jpg){#fig:fig2_4_12
width="\\textwidth"}

### Figs. [2.49](#fig:fig2_4_13){reference-type="ref" reference="fig:fig2_4_13"}-[2.50](#fig:fig2_4_15){reference-type="ref" reference="fig:fig2_4_15"}: Binary-bipolar interconversion {#figs.-figfig2_4_13-figfig2_4_15-binary-bipolar-interconversion}

![Converting $h$,$J$ to $x$,$w$](./Week2_4/Picture5.jpg){#fig:fig2_4_13
width="\\textwidth"}

![Interconverting $x$,$w$ and
$h$,$J$](./Week2_4/figure14.jpg){#fig:fig2_4_15 width="\\textwidth"}

Figs. [2.49](#fig:fig2_4_13){reference-type="ref"
reference="fig:fig2_4_13"} and
[2.50](#fig:fig2_4_15){reference-type="ref" reference="fig:fig2_4_15"}
show the algebra needed to obtain the expressions connecting $h$, $J$ to
$x$,$w$. The basic approach is to start from the bipolar energy
expression $\widetilde{E}=m^{\rm T}h+(1/2)m^{\rm T}Jm$, insert $m=2s-1$,
and then compare with the binary energy expression
$\widetilde{E}=s^{\rm T}x+(1/2)s^{\rm T}ws$.

Similarly you can also figure out the reverse transformation (see Fig.
[2.50](#fig:fig2_4_15){reference-type="ref" reference="fig:fig2_4_15"})
that you could use if you are given $w$, $x$ and you want to find $J$,
$h$.

### Quiz

#### Question 1

The energy of a system of 2 classical spins in bipolar notation ($m$ is
a bipolar variable with two values -1 and +1) is given by

$\widetilde{E} = m^T h + 0.5 \ m^T J m$

while in terms of a binary variable s with values 0 and 1,

$\widetilde{E} = s^T x + 0.5 \ s^T w s$\
Suppose $h = \left \{ \begin{array}{r}
0 \\
0 \\
\end{array} \right \}$ and $J = \left [ \begin{array}{r r}
0 & \ 1 \\
1 & \ 0 \\
\end{array} \right ]$\
What is the choice of $\{x\}$ and $[w]$ that will give the same values
of $\widetilde{E}$ for all configurations?[^35]

#### Question 2

The energy of a system of 3 classical spins in bipolar notation ($m$ is
a bipolar variable with two values -1 and +1) is given by

$\widetilde{E} = m^T h + 0.5 \ m^T J m$

What choice of h and \[J\] will give us only two peaks at
$\{+1  -1  +1\}$ and at $\{-1  +1  -1\}$?[^36]

## Learning

This is [Lecture 2.5: Watch youtube
video](https://www.youtube.com/watch?v=33wS2A6slxM)

### Figs. [2.51](#fig:fig2_5_2){reference-type="ref" reference="fig:fig2_5_2"}: Learning rule #1 {#figs.-figfig2_5_2-learning-rule-1}

![Learning rule \# 1](./Week2_5/Figure1a.png){#fig:fig2_5_2
width="\\textwidth"}

In the last lecture, we showed why it would be interesting to be able to
create arbitrary peaks in your state space response, because you could
use that for interesting applications like invertible logic and image
classification. The state space response can be described by a truth
table like the one in Fig. [2.51](#fig:fig2_5_2){reference-type="ref"
reference="fig:fig2_5_2"}, each row describing a particular peak. The
number of columns, that's the number of $p$-$bits$ that you have, six in
this case, and we have six peaks, as well. But those two don't have to
be equal.

Using $h$,$J$ from the learning rule stated in
Fig.[2.48](#fig:fig2_4_12){reference-type="ref"
reference="fig:fig2_4_12"} we can write the energy function in terms of
the quantity $P_k$ which tells us how much overlap the current state $m$
with each row $k$ of the truth table. Any Boltzmann machine minimizes
$E$ which corresponds to maximizing $P_k + (1/2) P_k^2$. This seems
reasonable since our purpose is to maximize the overlap with the truth
table described by $P_k$. This rule often works well when you have many
more bits than there are peaks.

A recent development is the $\textit{modern Hopfield network}$ that
replaces $P_k + (1/2) P_k^2$ with higher powers of $P_k$, or even an
exponential function $e^{P_k}$. These higher powers tend to favor
solutions that maximize one of the $P_k$ in comparison to those that
give medium values for multiple $P_k$. This is desirable since we really
want solutions that strongly match a particular line of the truth table,
and not those that have a medium match with many lines. This seems like
a promising approach but is still a work in progress. We will not
discuss it further.

### Figs. [2.52](#fig:fig2_5_3){reference-type="ref" reference="fig:fig2_5_3"}-[2.55](#fig:fig2_5_6){reference-type="ref" reference="fig:fig2_5_6"}: Average value and correlation matrix {#figs.-figfig2_5_3-figfig2_5_6-average-value-and-correlation-matrix}

Let us talk about a different learning rule that has been widely used.
The quantities $h$,$J$ in the old rule play an important role in this
new rule. First let's look at this quantity
$h= -(1/n_T)t_m^{\rm T}\widetilde{\mathbf{1}}$ (see Fig.
[2.52](#fig:fig2_5_3){reference-type="ref" reference="fig:fig2_5_3"}). A
little reflection will tell you that it can be written as
$\langle m_r\rangle=\sum_{k=1}^{n_t}{(1/n_t)[t_m]_{k,r}}$, which can be
interpreted as the value of each $p$-$bit$ averaged over all rows of the
truth table.

![Average Value](./Week2_5/figure2.jpg){#fig:fig2_5_3 width="90%"}

![Average Value and Correlation
Matrix](./Week2_5/Picture5.jpg){#fig:fig2_5_4 width="90%"}

#### Fig. [2.53](#fig:fig2_5_4){reference-type="ref" reference="fig:fig2_5_4"} {#fig.-figfig2_5_4}

Now similarly, if you look at that second thing, the one that is the
expression for the $J$ matrix, $-(1/n_T)t_m^{\rm T}t_m$, that involves a
product of $t_m$'s, product of two of them. Again, mathematically, you
could write it this way,
$\langle m_rm_q\rangle=\sum_{k=1}^{n_t}{(1/n_t)[t_m]_{k,r}[t_m]_{k,q}}$.
What it tells you is, the average value of the product of what you have
for the $r$-th $p$-$bit$ and what you have for the $q$-th $p$-$bit$ so
you could call that the correlation matrix, correlation between the
$r$-th and $q$-th bits, $m_r$, $m_q$, averaged over all lines of the
truth table.

#### Fig. [2.54](#fig:fig2_5_5){reference-type="ref" reference="fig:fig2_5_5"} {#fig.-figfig2_5_5}

![Average Value and Correlation
Matrix](./Week2_5/figure4.jpg){#fig:fig2_5_5 width="\\textwidth"}

We defined the average value and correlation matrix in terms of the
dream response,the one that has the six peaks exactly where you want
them. Now, in general, if you just took any network, of course, it would
have peaks all over the place. All the different configurations would
have some probability and you could still define an average value which
would look just like this
$\langle m_r\rangle=\sum_{k=1}^{n_t}{(1/n_t)[t_m]_{k,r}}$ except that,
now it's not that there's only six lines of your truth table which
contribute, it's like every configuration contributes and so that you
have to put in the probability of that configuration, the equilibrium
probability, and then sum over all possible all $2^n$ configurations,
$\langle m_r\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}}$. The same with the
correlation matrix, you'd have to sum over all $2^n$ configurations,
$\langle m_rm_q\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}[t_m]_{i,q}}$ to
get the correct correlation values.

#### Figs. [2.55](#fig:fig2_5_6){reference-type="ref" reference="fig:fig2_5_6"} {#figs.-figfig2_5_6}

Now, so in general, in a particular problem (see Fig.
[2.55](#fig:fig2_5_6){reference-type="ref" reference="fig:fig2_5_6"}),
the situation is like this. There is a target that you have in mind, you
want to get a certain $\langle m_r \rangle$, and a certain
$\langle m_rm_q \rangle$, but you don't have it because you don't have
the correct weight matrices, the $h$ and $J$. Instead, what you have is
giving you some junk and that junk has a corresponding average value and
average correlations. So this is what you have,
$\langle m_r\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}}$ and
$\langle m_rm_q\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}[t_m]_{i,q}}$, and
this, $\langle m_r\rangle=\sum_{k=1}^{n_t}{(1/n_t)[t_m]_{k,r}}$ and
$\langle m_rm_q\rangle=\sum_{k=1}^{n_t}{(1/n_t)[t_m]_{k,r}[t_m]_{k,q}}$,
is what you'd really like to do.

![Average and correlations: Target and
actual](./Week2_5/Picture3.jpg){#fig:fig2_5_6 width="\\textwidth"}

### Figs. [2.56](#fig:fig2_5_7){reference-type="ref" reference="fig:fig2_5_7"} - [2.58](#fig:fig2_5_9){reference-type="ref" reference="fig:fig2_5_9"}: Learning rule \# 2 {#figs.-figfig2_5_7---figfig2_5_9-learning-rule-2}

How do you get from where you are to where you want to be? Well, that's
where you have the learning rule. The learning rule tells you that if
the target average is bigger than the actual, then you should decrease
the $h$ value corresponding to that neuron. It's a decrease, so that
means if this what's inside if it's positive, then the delta should be
negative. That's why the minus sign, and this $\varepsilon$ is what you
call a learning parameter,
$\Delta h_r=-\varepsilon (\langle m_r\rangle_{target}-\langle m_r\rangle_{actual})$.
See, try to keep it small but not too small. I'll explain why this works
in a minute.

The other rule is how do I adjust the weight matrix values? Well, there
again, you look at the correlations and if the target is bigger than the
actual, then you reduce the corresponding $J$. So that's the rule, you
see. And what you do is to start from some arbitrary $h$ and $J$, where
you got this mess of a response and then if you keep iterating, you'll
eventually get to your target where you really want to be.

![Learning Rule \# 2](./Week2_5/Picture2.jpg){#fig:fig2_5_7
width="\\textwidth"}

![Learning Rule](./Week2_5/figure7.jpg){#fig:fig2_5_8
width="\\textwidth"}

#### Fig. [2.57](#fig:fig2_5_8){reference-type="ref" reference="fig:fig2_5_8"} {#fig.-figfig2_5_8}

Why does this work? Well think of it like this. Suppose the target value
is bigger than the actual, then what you really want to do is do
something, so that the actual increases. So how do you make the actual
increase? Well, what I claim is decreasing $h$ will do it. Why? Because
you see $h$ appears in this energy expression,
$\widetilde{E}=\sum_{r}{h_rm_r}+(1/2)\sum_{r,q}{J_{rq}m_rm_q}$ and a
positive $h$ puts an energy penalty towards being $+1$. So, if I
decrease $h$, $+1$ will become more probable relative to $-1$. So
overall, the average value of $m$ will want to increase because there's
more $+1$'s then $-1$'s. That's exactly what we want to see, because the
actual is less than the target, And the same argument goes with the
$J$s, you see again if you look at the energy expression, if you want to
increase the correlation, what you should do is decrease this
corresponding $J$.

I should mention here that we have written the energy as
$\widetilde{E}=\sum_{r}{h_rm_r}+(1/2)\sum_{r,q}{J_{rq}m_rm_q}$. Often in
the physics literature, they define energy with an extra minus sign
here. If you do that, it would reverse the signs in the learning rule,
but the basic logic is the same.

In the literature you'll see more rigorous derivations of the learning
rules, but what I wanted to show you here is how you can intuitively
understand why it works. There are other details like, sometimes people
add a term that they called regularization. They don't want the weights
$J$ to increase too much. So they put an energy penalty, towards being
too large
$\Delta J_{rq}=-\varepsilon (\langle m_rm_q\rangle_{target}-\langle m_rm_q\rangle_{actual} + \lambda J_{rq})$.

#### Fig. [2.58](#fig:fig2_5_9){reference-type="ref" reference="fig:fig2_5_9"} {#fig.-figfig2_5_9}

Now, how do you actually implement it? It means that at every step you
have to evaluate the bias and correlation matrix for the target and the
actual, and then use them to learn. Now for the target, it's relatively
easy, Why? Because I just have to do these summations,
$\langle m_r\rangle=\sum_{k=1}^{n_t}{P_k[t_m]_{k,r}}$ and
$\langle m_rm_q\rangle=\sum_{k=1}^{n_t}{P_k[t_m]_{k,r}[t_m]_{k,q}}$,
over my desired peaks, and there's only 6 of them or 10 of them, maybe
100 of them.

But it's much harder to evaluate the actual. It requires me to do a sum
over $2^n$ terms, $\langle m_r\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}}$
and $\langle m_rm_q\rangle=\sum_{i=1}^{2^n}{p_i[t_m]_{i,r}[t_m]_{i,q}}$,
and as I've mentioned many times, the $2^n$ can be a huge number. So, in
this context, what you really want to do is not really evaluate this
entire sum, but use the sampling method, the one that works in $n$
space, but you have to take enough samples, so that you get a accurate
idea of these average values. And that often can be time consuming. In
the literature, often the target is called the data, actual is called
the model, data is easy to evaluate, model needs to be approximated.

![Learning Rule](./Week2_5/figure8.jpg){#fig:fig2_5_9
width="\\textwidth"}

### Fig. [2.59](#fig:fig2_5_10){reference-type="ref" reference="fig:fig2_5_10"}: Learning a full adder {#fig.-figfig2_5_10-learning-a-full-adder}

![Full adder: Truth table and response with learned bias (x) and weight
(w), MATLAB code included at end of
book](./Week2_5/Picture1.png){#fig:fig2_5_10 width="\\textwidth"}

So here's an example of learning a truth table (see Fig.
[2.59](#fig:fig2_5_10){reference-type="ref" reference="fig:fig2_5_10"}),
where the truth table I took is that corresponding to a full adder,
which means it has three inputs, and it produces two outputs, a sum and
a carry term. So this is a system with five $p$-$bits$. I'm writing it
in binary notation. The details aren't important. Basically I've got
five bits, so there are 32 possibilities, and I want to have eight peaks
in my answer which I have labeled with their corresponding decimal
values. So that's what I've shown : the red ones are the peaks I want.

At first, I start with $h=0$, $J=0$ so that all 32 values from 0 to 31
are equally probable. And then gradually as you learn, you adjust the
$h$ and the $J$ and the reds pick up gradually, the blues go down as you
can see in the video.\
[Watch Videoclip: .. 13:00 to
15:00](https://www.youtube.com/watch?v=33wS2A6slxM)\
Learning a full adder : Courtesy of Jan Kaiser

### Figs. [2.60](#fig:fig2_5_11){reference-type="ref" reference="fig:fig2_5_11"}-[2.62](#fig:fig2_5_13){reference-type="ref" reference="fig:fig2_5_13"}: Learning with hidden units {#figs.-figfig2_5_11-figfig2_5_13-learning-with-hidden-units}

#### Figs. [2.60](#fig:fig2_5_11){reference-type="ref" reference="fig:fig2_5_11"}: {#figs.-figfig2_5_11}

![Introducing hidden units, same code as Fig.
[2.59](#fig:fig2_5_10){reference-type="ref"
reference="fig:fig2_5_10"}](./Week2_5/figure10.jpg){#fig:fig2_5_11
width="\\textwidth"}

Before finishing up, let me mention a few ideas to indicate the richness
of this subject. Suppose instead of 6 peaks with the 6 bits, we wanted
10 peaks. So then you'd find that if we just use the straight forward
learning method, it may not work too well. Often what people do is, they
introduce a set of hidden bits, ones I don't look at. So I want these 10
peaks, but these ten peaks correspond to the 6 visible units, and not
these other four that are hidden that I don't even look at. But the $h$,
$J$ matrices involve all ten units. How do I train them?

The learning rule is still the same but remember to get the learning
rule of course, I have to evaluate these average values. Now it's a
little more harder to do this evaluation for the hidden bits because
when I specify the peaks in terms of the visible units. As far as the
hidden units are concerned, I don't really care what they are. So I'm
not really specifying them at all and there is no target value. Even
that has to be evaluated by sampling.

#### Fig. [2.61](#fig:fig2_5_12){reference-type="ref" reference="fig:fig2_5_12"} {#fig.-figfig2_5_12}

![Introducing hidden units, MATLAB code included at end of
book](./Week2_5/Picture6.jpg){#fig:fig2_5_12 width="\\textwidth"}

Here's an example that we ran with this where you had 10 peaks (see Fig.
[2.61](#fig:fig2_5_12){reference-type="ref" reference="fig:fig2_5_12"})
with six visible units, and four hidden units. I have used a
two-dimensional representation with the $2^6=64$ visible configurations
on one axis, and $2^4=16$ hidden configurations on the other, giving a
total of $2^10-1024$ configurations in all. Now if you look from the
visible side I got 10 Peaks, but each one is located at a different
point in the hidden axis. But of course, I hadn't specified anything for
the hidden axes. It's not like I told it to have the peak there. It just
figured that out on its own. So in a way as if the hidden layer, found
some patterns in the data that you showed it, and classified them in
some way, as if it labeled the data and this is generally what people
refer to as unsupervised learning. Not like someone took the data and
labeled it but it, discovered the patterns and labeled it for itself.

Another thing you often hear in this field is about generative models.
The idea that well you show it a few images and train it, but then after
that, if you let it run it will generate new images which will look like
what you had and will have patterns in common with it, but these are not
things that it had seen before. So I'm telling you all this just to give
you a rough idea of the richness of this topic, but if you want to
explore that you need to take a real course on machine learning.

#### Fig. [2.62](#fig:fig2_5_13){reference-type="ref" reference="fig:fig2_5_13"} {#fig.-figfig2_5_13}

One final note. One of the problems you have with Boltzmann machines is
that when you try to scale it up the training gets to be difficult.
Boltzmann machines, are always undirected, that is $w_{ij}=w_{ji}$. It
goes equally both ways.

Now the training process is actually easier if you have directed
connections. So a lot of the action in the field of machine learning is
based on directed networks, the ones where the interactions are one way
if $w_{ij}\neq 0$ then $w_{ji}=0$. And for directed networks, the energy
function does not come naturally as it does for Boltzmann machines. But
there is a lot of work on defining energy-based models for such directed
networks. One of these will be evident after we discuss transition
matrices and Feynman paths in the next chapter.

![Directed networks are easier to
train](./Week2_5/Picture7.jpg){#fig:fig2_5_13 width="\\textwidth"}

### Quiz

#### Question 1

A network of 3 spins shows two peaks, one at $\{+1  -1  +1\}$ and one at
$\{-1  +1  -1\}$.\
What is the matrix describing the average correlations
$\langle m_r  m_q  \rangle$?[^37]

#### Question 2

Suppose for a given network, $\langle m_r  m_q  \rangle = 0.5$ while our
target value for $\langle m_r  m_q  \rangle$ is 0.4. How should we
change the parameters in order to train the network?[^38]

#### Question 3

Suppose for a given network, $\langle m_r  m_q  \rangle = 0.5$ while our
target value for $\langle m_r  m_q  \rangle$ is 0.7. How should we
change the parameters in order to train the network?[^39]

## Fig. [2.63](#fig:fig3_6_1){reference-type="ref" reference="fig:fig3_6_1"}: 5-minute summary {#fig.-figfig3_6_1-5-minute-summary}

This is [Chapter 2 summary: Watch youtube video, until
2:05](https://www.youtube.com/watch?v=eQCxUi3yFmw)

In Lecture 1.1, we started by introducing this sampling method. Is time
sampling, which works in this $n$-space, but allows us to get accurate
results for the response in the $2^n$ space. As you know, one of the
basic points I've always stressed is, how $2^n$ can be huge when you
scale up.

In Lecture 1.2, we discussed how you can control the response in this
$2^n$ space, by adjusting the bias and weight $x$ and $w$, which are in
$n$ space.

![Summary of Lectures 2.1-2.5](./Week2_5/Picture4.png){#fig:fig3_6_1
width="\\textwidth"}

In Lecture 2.3 we talked about how you could design $x$ and $w$ to solve
useful problems that we generally refer to as constrained optimization.
We took a very specific example, this max cut and min cut problem, where
the translation to $x$, $w$ is straightforward.

In Lectures 2.4 and 2.5 we talked about a general approach for designing
$x$ and $w$ to give us arbitrary peaks in the $2^n$ space, which could
be used for a new kind of logic and image classification for example.

# Transition Matrix {#Sec:Transition}

## Markov Chain Monte Carlo

This is [Lecture 3.1: Watch youtube
video](https://www.youtube.com/watch?v=fHC8yptupSQ)

We started in Chapter 1 with the general Boltzmann law opertaing in
$2^n$ space and then in Chapter 2 introduced the sampling method which
operates in $n$ space. Now we'll introduce a third method, which
operates in $2^n$ space, but as you'll see, it gives us a lot of insight
into how the sampling method works and leads to this concept of Feynman
paths, which is useful in connecting to the world of quantum computing.

### Figs. [3.1](#fig:fig3_1_3){reference-type="ref" reference="fig:fig3_1_3"}-[3.4](#fig:fig3_1_6){reference-type="ref" reference="fig:fig3_1_6"}: Transition matrix {#figs.-figfig3_1_3-figfig3_1_6-transition-matrix}

#### Fig. [3.1](#fig:fig3_1_3){reference-type="ref" reference="fig:fig3_1_3"}: Definition {#fig.-figfig3_1_3-definition}

![Transition Matrix.](./Week3_1/figure3.jpg){#fig:fig3_1_3
width="\\textwidth"}

So what is this third method? Well, the idea is that if you have a
system in some configuration $\{111001\}$ denoted by $i$. You want to
know what will happen at the next time step. And the answer is that in a
probabilistic circuit, it will go to different configurations $j$ with
different probabilities. (see Fig.
[3.1](#fig:fig3_1_3){reference-type="ref" reference="fig:fig3_1_3"}).
And those are the probabilities that should appear in the $i$-th column
of the transition matrix $[W]$. So the $i$-th column, the column tells
you what's the input, that is what the configuration was at time $t$.
And $j$-th row then tells you the probability that the system will go
from $i$ on to $j$.

In general, you can take the probability distribution function at a time
$t$. Multiply it by $W$, and it will give you the new probability
distribution at time $t+1$, $[W]{pdf(t)}={pdf(t+1)}$. So, this matrix
kind of propagates your probability distribution function from one time
point to the next (see Fig. [3.1](#fig:fig3_1_3){reference-type="ref"
reference="fig:fig3_1_3"}).

#### Fig. [3.2](#fig:fig3_1_4){reference-type="ref" reference="fig:fig3_1_4"}: Properties {#fig.-figfig3_1_4-properties}

Matrices of this type appear in diverse fields and are generally called
stochastic matrices which have some very useful properties.

![Properties of stochastic matrix](./Week3_1/Picture1.jpg){#fig:fig3_1_4
width="\\textwidth"}

One such property is that every column must add up to 1. Why is that?
Well, because each column represents the probability that the system
will go to some state $j$, given that it is in $i$ at this time. But of
course it must go somewhere, which means if I add up all the $j$'s, the
answer should be 1, $\sum_{j}{W_{ji}}=1$.

#### Fig. [3.3](#fig:fig3_1_5){reference-type="ref" reference="fig:fig3_1_5"} {#fig.-figfig3_1_5}

Another important property is that it has an eigenvalue equal to one.
This is a huge matrix $2^n$ by $2^n$. So, it has $2^n$ eigenvalues. But
one of these actually the largest one, is equal to 1. To show this takes
a little discussion. First consider the transpose of the $W$ matrix. For
the $W$ matrix, the columns add up to 1, so for the transpose, it is the
row that adds up to 1: So, $\sum_{j}{[W^{\rm T}]_{ij}}$.

Now what that means is that a constant vector, all of whose components
are equal to a particular number $c$, is actually an eigenvector of the
transpose matrix W, $[W^{\rm T}]$ with an eigenvalue of 1.

![$W^T$ has one eigenvalue equal to
1](./Week3_1/figure5.jpg){#fig:fig3_1_5 width="\\textwidth"}

#### Fig. [3.4](#fig:fig3_1_6){reference-type="ref" reference="fig:fig3_1_6"} {#fig.-figfig3_1_6}

![$W^T$ and W have the same eigenvalues though not necessarily the same
eigenvectors](./Week3_1/figure6.jpg){#fig:fig3_1_6 width="\\textwidth"}

Now, I am of course, interested not in $W$ transpose, $W^{\rm T}$, but
in $W$, and then there is this theorem that you may remember from
somewhere in linear algebra. That $W$ and $W^{\rm T}$ have the same
eigenvalues though not necessarily the same eigenvectors. Eigenvectors
could be same but don't have to be. But the point is they will always
have the same eigenvalues.

So, what we can deduce is that since $W^{\rm T}$ has eigenvalue 1 and
eigenvector $C$, $W$ must also have an eigenvector, but not necessarily
$C$, we'll call it $P$, with an eigenvalue of 1 such that $[W]{P}={P}$.

### Figs. [3.5](#fig:fig3_1_7){reference-type="ref" reference="fig:fig3_1_7"}-[3.9](#fig:fig3_1_12){reference-type="ref" reference="fig:fig3_1_12"}: Stationary Distribution {#figs.-figfig3_1_7-figfig3_1_12-stationary-distribution}

#### Figs. [3.5](#fig:fig3_1_7){reference-type="ref" reference="fig:fig3_1_7"}: {#figs.-figfig3_1_7}

Now, this $P$ is what you could call the stationary distribution. Why is
that? Well, this $W$ matrix as we discussed takes the probability
distribution function from one point in time and propagates it to the
next point. So if at a given time $t$ you have a distribution $P$, then
$[W]{P}={P}$. So at $t+1$ also you'll have the same distribution. In
other words, the distribution, once it reaches $P$, will stay that way
forever and so you call it a stationary distribution.

![Stationary Distribution.](./Week3_1/figure7.jpg){#fig:fig3_1_7
width="\\textwidth"}

#### Fig. [3.6](#fig:fig3_1_9){reference-type="ref" reference="fig:fig3_1_9"} {#fig.-figfig3_1_9}

![Converging to a stationary
distribution.](./Week3_1/figure9.jpg){#fig:fig3_1_9 width="\\textwidth"}

Now what if initially at time $t$, the distribution was something else.
I'll call that $Q$. Well, the answer is that after a few time steps, and
we'll talk about how many, the probability distribution function will
converge to $P$.

Why is that? Well, one way to think is, take the $Q$ and write it in
terms of the eigenvectors of the $W$ matrix. So, as I said $P$ is one of
the eigenvectors with eigenvalue 1. Let's say there's another
eigenvector $A$ with eigenvalue $\lambda$ and of course, there'll be
many more eigenvectors and some eigenvalues will even be complex. But
here, just for illustrative purposes, I'm considering one other. The
argument we'll make will apply to all of these other eigenvectors.

Now, you see, if at time $t$ we have ${P}+{A}$, then what will happen at
time $t+1$? Well, it will get multiplied by $W$, and ${W}{P}$ will give
me ${P}$, but ${W}{A}$ will give me $\lambda {A}$. Why? Because ${A}$ is
also an eigenvector of ${W}$, but with an eigenvalue $\lambda$.