from scipy.optimize import fsolve
import casadi as ca
import numpy as np
import matplotlib.pyplot as plt

def fun(variables, A1, Lc, kv, P1, P_out, C) :
    (x,y) = variables
    eqn_1 = (A1/Lc)* ((1.5 * P1) - y)
    eqn_2 = (C**2)/2 * (x - 0.5 * kv * np.sqrt(y - P_out))
    return [eqn_1, eqn_2]

A1 = (2.6)*(10**-3)
Lc = 2
kv = 0.38
P1 = 8.5
P_out = 5
C = 479

result = fsolve(fun, (0, 10), args = (A1, Lc, kv, P1, P_out, C)) 
print(result)

a = result[0]
b = result[1]
np.random.seed(42)
intervalo = [np.linspace(0,400,1000), np.linspace(400,800,1000),np.linspace(800,1200,1000),np.linspace(1200,1600,1000),np.linspace(1600,2000,1000)]
x = ca.MX.sym('x', 2)
alpha = ca.MX.sym('alpha', 1)
x0_values = []
x1_values = []


for i in range(0,5):  
    if i ==0:
        alpha0 = 0.5
    else:
        alpha0 = np.random.uniform(0.2, 0.8)
    
    rhs = ca.vertcat((A1/Lc)*((1.5 * P1) - x[1]), (C**2)/2 * (x[0] - alpha * kv * np.sqrt(x[1] - P_out)))
    ode = {'x' : x, 'ode' : rhs, 'p' : alpha }

    F = ca.integrator('F','cvodes', ode, intervalo[i][0], intervalo[i])
    
    sol = F(x0 = [a, b], p = alpha0)

    xf_values = np.array(sol["xf"])

    aux1, aux2 = xf_values
    x0_values.append(aux1)
    x1_values.append(aux2)
    a = aux1[-1]
    b = aux2[-1]


plt.figure()
for i in range(0,5):
    plt.plot(intervalo[i], np.squeeze(x0_values[i]), label='x0(t)')
plt.grid(True)
plt.show()

plt.figure()
for i in range(0,5):
    plt.plot(intervalo[i], np.squeeze(x1_values[i]), label='x0(t)')
plt.grid(True)
plt.show()