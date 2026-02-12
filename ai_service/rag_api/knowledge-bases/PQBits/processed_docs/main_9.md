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
PPSL=reshape(PSL,16,64);

X=[0:2^Nv-1];

figure(1) % Boltzmann
bar(X',[sum(PP)'],0.75)
set(gca,'Fontsize',24)
grid on
xlim([-1 64])

figure(10) % Boltzmann
bar3(PP,0.25)
set(gca,'XTickLAbel', {0:15} )
set(gca,'xticklabelrotation', 90)
set(gca,'YTickLabel', [0:63] )
set(gca,'yticklabelrotation', 90)
set(gca,'Fontsize',0.1)
grid on
zlim([0 0.1])

figure(2) % Sampling
bar(X',[sum(PPSL)'],0.75)
set(gca,'Fontsize',24)
grid on

figure(20) % sampling
bar3(PPSL,0.25)
set(gca,'XTickLAbel', {0:15} )
set(gca,'xticklabelrotation', 90)
set(gca,'YTickLabel', [0:63] )
set(gca,'yticklabelrotation', 90)
set(gca,'Fontsize',0.1)
grid on
zlim([0 0.1])
```

[Matlab]{.smallcaps} code for Fig.
[4.42](#fig:fig4_5_8){reference-type="ref" reference="fig:fig4_5_8"},
Lecture 4.5:

``` {.octave language="Octave"}
% Max-cut problem Annealing, Classical and quantum
clear all
rng(1)

E0=1; hx=15; % Change these parameters

N2=3;
A=randi(10,N2); A= A-diag(diag(A)); A=A+A';
B=randi(10,N2); B= B-diag(diag(B)); B=B+B';
Z=0*ones(N2,N2);

C = [A Z;Z' B]./2;

    N=length(C); u=ones(N,1);
    ctr=randperm(N); C=C(ctr,ctr);

K=5; % enforcing equal number in each group
M=+1; % +1 for min-cut, -1 for max-cut

X=[0:2^N-1]; 

w= 2*K - M*4*C; w= w - diag(diag(w));
x = -K*(N-1) + M*C*u + M*C'*u;

    % Bipolar
    J = 0.25 * w;
    h = 0.5*x + 0.125 * w * u + 0.125 * w' * u;

% % % % Quantum

sx=[0 1;1 0]; sy=[0 -1i;+1i 0]; sz=[+1 0;0 -1]; s0=[1 0;0 1];

s1z=kron(sz,kron(s0,kron(s0,kron(s0,kron(s0,s0)))));
s2z=kron(s0,kron(sz,kron(s0,kron(s0,kron(s0,s0)))));
s3z=kron(s0,kron(s0,kron(sz,kron(s0,kron(s0,s0)))));
s4z=kron(s0,kron(s0,kron(s0,kron(sz,kron(s0,s0)))));
s5z=kron(s0,kron(s0,kron(s0,kron(s0,kron(sz,s0)))));
s6z=kron(s0,kron(s0,kron(s0,kron(s0,kron(s0,sz)))));

s1x=kron(sx,kron(s0,kron(s0,kron(s0,kron(s0,s0)))));
s2x=kron(s0,kron(sx,kron(s0,kron(s0,kron(s0,s0)))));
s3x=kron(s0,kron(s0,kron(sx,kron(s0,kron(s0,s0)))));
s4x=kron(s0,kron(s0,kron(s0,kron(sx,kron(s0,s0)))));
s5x=kron(s0,kron(s0,kron(s0,kron(s0,kron(sx,s0)))));
s6x=kron(s0,kron(s0,kron(s0,kron(s0,kron(s0,sx)))));

H= h(1)*s1z + h(2)*s2z + h(3)*s3z + h(4)*s4z + h(5)*s5z + h(6)*s6z...
+ J(1,2)*s1z*s2z + J(1,3)*s1z*s3z + J(1,4)*s1z*s4z + J(1,5)*s1z*s5z + J(1,6)*s1z*s6z...
+ J(2,3)*s2z*s3z + J(2,4)*s2z*s4z + J(2,5)*s2z*s5z + J(2,6)*s2z*s6z...
+ J(3,4)*s3z*s4z + J(3,5)*s3z*s5z + J(3,6)*s3z*s6z...
+ J(4,5)*s4z*s5z + J(4,6)*s4z*s6z + J(5,6)*s5z*s6z...
+ hx*s1x + hx*s2x + hx *s3x + hx*s4x + hx*s5x + hx*s6x;

rho=expm(-E0*H); rho=rho./trace(rho);

Q=diag(abs(rho));

% % % % Plot

figure(20)
bar(X',[Q],0.5,'r')
set(gca,'Fontsize',16)
grid on
ylim([0 max(Q)+0.005])
legend('quantum model')

% % % % Classical Boltzmann calculation, works only for hx=0
for ii= 1:2^N
    n=de2bi(ii-1,N,'left-msb')';
    E(ii) = n' * x + 0.5 * n' * w * n ;
end
P=exp(-E0*E); P=P./sum(P);

figure(2)
bar(X',[flip(P)'],0.5,'k')
set(gca,'Fontsize',24)
grid on
ylim([0 max(P)+0.005])
legend('classical model')
```

[Matlab]{.smallcaps} code for Fig.
[5.22](#fig:fig5_3_4){reference-type="ref" reference="fig:fig5_3_4"},
Lecture 5.3:

``` {.octave language="Octave"}
% Grover search
clear all

n=10; % # of q-bits
N=2^n;  NT=40; % Number of iterations

k=N/2; % Target configuration
R=eye(N); R(k,k)=-1; %U_Q

H=[1 1;1 -1]./sqrt(2); HH=H;
for ii=1:n-1
    HH=kron(HH,H);
end

% Diffusion matrix
DD=-eye(N,N); DD(1,1)=+1; D=HH*DD*HH; % UH * U0 * UH

% Alternative expression for diffusion matrix
% D=-eye(N)+(2/N)*ones(N);

psi=ones(N,1)./sqrt(N); % Initial wavefunction created by first Hadamard
phi(:,1) = psi.^2;
for ii=2:NT
    psi=D*R*psi; % Grover iteration
    phi(:,ii)=psi.^2;
end

hold on
h=plot(phi(k,:),'ko-');
set(gca,'fontsize',[20])
xlabel('Number of cycles')
ylabel('Amplitude of target')
grid on
```

[Matlab]{.smallcaps} code for Figs.
[5.31](#fig:fig5_4_2){reference-type="ref" reference="fig:fig5_4_2"} and
[5.32](#fig:fig5_4_3){reference-type="ref" reference="fig:fig5_4_3"},
Lecture 5.4:

``` {.octave language="Octave"}
% Factorizing F, by finding the period of a^x mod(F) 
clear all

n=4;N=2^n;

a=7; F=15; aa=a;
for ii=0:20
  m(ii+1)= mod(aa, F);
  aa= a*m(ii+1);
end

X=[0:20];

h=plot(X,m,'r-o');
set(h,'Linewidth',2.0)
set(gca,'fontsize',[32])
grid on

r=4;
[gcd(a^(r/2)-1,F) gcd(a^(r/2)+1,F)]
```

[^1]: We will talk in terms of binary units or bits (d=2), but one could
    generalize to units with $d$ states leading to a space with $d^n$
    components.

[^2]: Magnetoresistive Random Access Memory

[^3]: Note that similar experiments can be done with polarized photons
    instead of spin-polarized electrons but the spots then have
    strengths $\sim cos^{2} \theta$ and $\sim sin^{2} \theta$.
    Mathematically the difference comes from the use of $vectors$ for
    photon polarizations as opposed to $spinors$ for electron spin
    polarizations. In these notes we will focus on the latter.

[^4]: Although an electron is a quantum magnet it is difficult to do
    this experiment with electrons because they are charged particles
    with strong repulsive forces that will mask what we are looking for.
    Instead the experiments are done with neutral atoms having a net
    magnetic moment coming from unpaired electrons.

[^5]: on [nanoHUB](https://nanohub.org/courses/FON2), on
    [edX](https://www.edx.org/course/introduction-to-quantum-transport)

[^6]: These are discussed in Sections
    [5.3](#Sec:Grover){reference-type="ref" reference="Sec:Grover"} and
    [5.4](#Sec:Shor){reference-type="ref" reference="Sec:Shor"}
    respectively

[^7]: In quantum computing $d$-valued units are sometimes referred to as
    qudits

[^8]: more generally, complex elements

[^9]: This so-called sign problem is discussed in Section
    [5.5.3](#Sec:Sign){reference-type="ref" reference="Sec:Sign"}.

[^10]: 256

[^11]: $(1-f_1) (1-f_2)$

[^12]: $\mu$

[^13]: Because this law reflects a property of the reservoir, not the
    system

[^14]: Because the reservoir then has more energy and hence more
    available states.

[^15]: $p_{i} = (1/Z) \times e^{(E_i - \mu N_i)/kT}$

[^16]: 0

[^17]: $nk \ \ell n 3$

[^18]: $8k \ \ell n 2$

[^19]: \(a\) Free energy goes down, (b) overall entropy of system +
    reservoir goes up

[^20]: $\Delta N (\mu_1-\mu_2)/T$

[^21]: $\Delta E (1/T_2 - 1/T_1)$

[^22]: Method 1 requires us to evaluate $2^{10}$ probabilities,\
    while Method 2 requires us to evaluate 10 probabilities

[^23]: $2 \varepsilon + U$

[^24]: $3 \varepsilon + 3U$

[^25]: $n_r$ takes on the value 1 with probability $f_r$, and the value
    0 with probability $1 - f_r$

[^26]: $\widetilde{x_3} = x_3 + n_1 n_2$

[^27]: $\{01\} and \{10\}$

[^28]: Magnetoresistive Random Access Memory

[^29]: $\widetilde{x}_4 = -1 + 2n_3$

[^30]: {0101},{1010},{1001}

[^31]: Note that the $[C]$ matrix elements are all positive numbers

[^32]: Those having equal number of zeros and ones

[^33]: {0000}, {1111}, {0011} and {1100}

[^34]: Interested readers can look up $\textit{Hebbian learning}$.

[^35]: $x = \left \{ \begin{array}{r}
    -2 \\
    -2 \\
    \end{array} \right \}$ and $J = \left [ \begin{array}{r r}
    0 & \ 4 \\
    4 & \ 0 \\
    \end{array} \right ]$

[^36]: $h = \left \{ \begin{array}{r}
    0 \\
    0 \\
    0 \\
    \end{array} \right \}$ and $J = \left [ \begin{array}{r r r}
    0 & \ +2 & \ -2 \\
    +2 & \ 0  & \ +2 \\
    -2 & \ +2 & \ 0 \\
    \end{array} \right ]$

[^37]: $\left [ \begin{array}{r r r}
    +1 & \ -1 & \ +1 \\
    -1 & \ +1 & \ -1 \\
    +1 & \ -1 & \ +1 \\
    \end{array} \right ]$

[^38]: Increase $J_{rq}$

[^39]: Decrease $J_{rq}$

[^40]: 1,1

[^41]: $\left \{ \begin{array}{r}
    1/3 \\
    2/3 \\
    \end{array} \right \}$

[^42]: $exp(\widetilde{E}_{10}-\widetilde{E}_{00})$

[^43]: $exp(\widetilde{E}_{11}-\widetilde{E}_{01})$

[^44]: Recall that the eigenvector of $W$ with an eigenvalue of 1
    represents the stationary distribution.

[^45]: sample one at a time in any order

[^46]: It will go to 11, then come back to 00, then oscillate back and
    forth

[^47]: The spins are updated one at a time in parent-child order

[^48]: $\{0 \ 0.5 \ 0.5 \  0\}$

[^49]: $0.9 \times 0.7 = 0.63$

[^50]: $8^9$

[^51]: $16^9$

[^52]: +1

[^53]: -1

[^54]: -2i $\sigma_z = \left [ \begin{array}{r r}
    -2i & \ 0  \\
    0 & \ +2i  \\
    \end{array} \right ]$

[^55]: $\left [ \begin{array}{r r}
    0 & \ -i h_y  \\
    +i h_y & \ 0  \\
    \end{array} \right ]$

[^56]: $\left [ \begin{array}{r r}
    0 & \ h_x -i h_y  \\
    h_x +i h_y & \ 0  \\
    \end{array} \right ]$

[^57]: $-tanh(h)cos \theta$

[^58]: $\sigma_x \times I$

[^59]: $\sigma_z \times \sigma_z$

[^60]: $\sigma_x \times \sigma_y$

[^61]: $\sigma_{1x}\sigma_{2x}+\sigma_{1y}\sigma_{2y}+\sigma_{1z}\sigma_{2z}$

[^62]: $0$

[^63]: $\sigma_{1x}\sigma_{2x}$

[^64]: $H = \sum_{r=1}^{n}{h_{r} \sigma_{zr}} + \frac{1}{2} \sum_{r \neq q}^{n} \sum_{q=1}^{n}{J_{rq} \sigma_{zr} \sigma_{zq}}$

[^65]: Slowly changing $E_0$ from a low value to a large value

[^66]: Slowly changing $h_{xr}$ from a large value to a small value

[^67]: Incidentally you might have noticed that we are getting
    $p_1 = cos^2 (\theta_1/2)$ for the probability of detecting an upsin
    along $\hat{n}_1$ which is at an angle $\theta_1$ to the direction
    of the spin $\hat{z}$. With photons the answer would have been
    $p_1 = cos^2 \theta_1$, obtained from the square of the dot product
    $\hat{n}_1 \cdot \hat{z}$. Photon polarization is represented by
    vectors and the dot product gives $cos \theta_1$. But electron spin
    is represented by spinors and the \"dot product\" gives
    $cos (\theta_1/2)$.

[^68]: Clauser-Horne-Shimony-Holt

[^69]: $\frac{1}{\sqrt{2}} \left [ \begin{array}{r}
    1  \\
    1  \\
    \end{array} \right ]$

[^70]: $\frac{1}{\sqrt{2}} \left [ \begin{array}{r}
    1  \\
    i  \\
    \end{array} \right ]$

[^71]: $\psi^\dagger \psi = 1$

[^72]: $\frac{1}{\sqrt{2}} \left \{ \begin{array}{r}
    1  \\
    1  \\
    \end{array} \right \}$

[^73]: $\frac{1}{\sqrt{2}} \left \{ \begin{array}{r}
    +1  \\
    -1  \\
    \end{array} \right \}$

[^74]: $\frac{1}{2} \left \{ \begin{array}{r}
    +1  \\
    -1  \\
    +1  \\
    -1  \\
    \end{array} \right \}$

[^75]: $\sim 2^{10}$

[^76]: 11:3

[^77]: r = period of f(x) = $a^x$ mod(F)

[^78]: Only on the main register, irrespective of the auxiliary register

[^79]: Because for the wrong state half the paths have negative
    amplitudes canceling the other half which have positive amplitudes

[^80]: Because for the wrong state hall the paths have zero amplitude