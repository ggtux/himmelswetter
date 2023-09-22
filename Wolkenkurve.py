from numpy import sign
from math import exp,log10,pow

K1 = 33.
K2 = 0.
K3 = 4.
K4 = 10.
K5 = 100.
K6 = 0.
K7 = 0.

Tir = 12.
Tamb = 18.
Tsky = Tir-Tamb

if abs((K2/10-Tamb)) < 1:
    T67= sign(K6)*sign(Tamb-K2/10)*abs((K2/10-Tamb))
else:
     T67=K6/10*sign(Tamb-K2/10)*(log10(abs((K2/10-Tamb)))/log10(10)+K7/100)

Td=(K1/100)*(Tamb-K2/10)+(K3/100)*pow(exp(K4/1000*Tamb),(K5/100))+T67
Tsky=Tir-Td
print(Tir,Tamb,Td,Tsky)
