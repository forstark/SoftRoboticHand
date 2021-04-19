# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 17:49:20 2021

@author: nguye
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA
import cmath
import math



'''workbook = xlrd.open_workbook('Profil.xlsx')
SheetNameList = workbook.sheet_names()
for i in np.arange( len(SheetNameList) ):
    print( SheetNameList[i] )

worksheet = workbook.sheet_by_name(SheetNameList[0])
num_rows = worksheet.nrows 
num_cells = worksheet.ncols 
print( 'num_rows, num_cells', num_rows, num_cells )

curr_row = 0
while curr_row < num_rows:
    row = worksheet.row(curr_row)
    #print row, len(row), row[0], row[1]
    print( 'Row: ', curr_row )
    print( row, len(row), row[0] )
    curr_cell = 0
    while curr_cell < num_cells:
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        cell_type = worksheet.cell_type(curr_row, curr_cell)
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        print( ' ', cell_type, ':', cell_value )
        curr_cell += 1
    curr_row += 1'''
    
f = open("Profil.txt")
f.readline()
data = np.loadtxt(f, delimiter='\t')
data = 10*np.array(data,dtype="float32")
'''print(data[0])'''


X = data[:,0]
Y = data[:,1]
X = X.reshape(-1,1)
Y = Y.reshape(-1,1)
print("valeurs de X",X)
print("valeurs de Y",Y)
plt.figure()
plt.plot(X,Y)
plt.show()

'''Setting parameters'''
Nt = data.shape
print("Nt = ",Nt)
strN = str(Nt[0])
print("strN = ", strN)
N = np.array(strN, dtype='int')
print("N = ",N)

C1 = np.zeros((N,2),float)
C2 = np.zeros((N,2),float)

r1_prime = np.zeros((N,2),float)
r2_prime = np.zeros((N,2),float)

r1_prime_prime = np.zeros((N,2),float)
r2_prime_prime = np.zeros((N,2),float)

K1 = np.zeros((N,1),float)
K2 = np.zeros((N,1),float)

'''Computation of end points, end tangents and curve Length'''

'''points initial et final'''
q0 = data[0]
q1 = data[N-1]
print("q0 = ",q0)
print("q1 = ",q1)

'''vecteurs'''
t0 = data[1]-data[0]
t1 = data[N-1]-data[N-2]
print("t0 = ",t0)
print("t1 = ",t1)

'''longueur de la courbe'''
L0 = 0
for i in range (1,400):
        L0 += LA.norm((data[i]-data[i-1]))
print("L0 = ",L0)

''' Computation of canonical form of inputs data'''
q0_c = complex(q0[0],q0[1])
q1_c = complex(q1[0],q1[1])
print("q0_c = ",q0_c)
print("q1_c = ",q1_c)

t0_c = (complex(t0[0],t0[1]))/LA.norm(t0)
t1_c = (complex(t1[0],t1[1]))/LA.norm(t1)
print("t0_c = ",t0_c)
print("t1_c = ",t1_c)

z = q1_c - q0_c
print("z = ", z)
l = abs(z)
print("l = ",l)
alpha = cmath.phase(z)
print ("alpha = ", alpha)

di = (t0_c*np.conj(z))/l
df = (t1_c*np.conj(z))/l
Le  = L0/l

'''Computation of orientation'''
theta0 = cmath.phase(di);
theta1 = cmath.phase(df);

thetam = 0.5*(theta0+theta1);
dtheta = 0.5*(theta1-theta0);

c0 = math.cos(0.5*theta0);
c1 = math.cos(0.5*theta1);

s0 = math.sin(0.5*theta0);
s1 = math.sin(0.5*theta1);

'''Computation of coeficient'''
a2 = 2*(math.sin(dtheta))**2
a1 = 6*((math.cos(dtheta)-3)*Le + (3*math.cos(dtheta)-1)*math.cos(thetam))
a0 = 36*(Le**2-1)

discr = (a1**2)-4*a2*a0

z_ = (-a1-np.sqrt(discr))/(2*a2)                   

w =  np.sqrt(z_)

'''Cheking satisfaction condition'''
Pz = 60*(Le+1)-((15*c0**2) + (15*c1**2) - 10*c0*c1)*z_
Qz = 60*(Le-1)-((15*s0**2) + (15*s1**2) - 10*s0*s1)*z_

Mu_m = -1.0
Mu_p = +1.0
Mu = [Mu_m, Mu_p] 

Nu_m = -1.0
Nu_p = +1.0
Nu = [Nu_m, Nu_p] 

cond = 5*(c0*s1 + c1*s0 - 3*c0*s0 - 3*c1*s1)*z_

Status = np.zeros((2,2),float)
mn = np.zeros((2,2),float)

id_mu = np.zeros(2,int)
id_nu = np.zeros(2,int)

k=0
for i in range (0,2):
    for j in range (0,2):
        mn[i,j]= Mu[i]*Nu[j]
        Status[i,j]= np.sqrt(Pz)*np.sqrt(Qz)*mn[i,j]
        if ((Status[i,j]- cond) <= 0.001):
            id_mu[k] = i
            id_nu[k] = j
    k+=1

print(mn,Status)
print("id_mu : ",id_mu,"/ id-nu : ", id_nu)

'''Computation u, v and w'''
u = np.zeros(2,float)
v = np.zeros(2,float)

for k in range (0,2):
    u[k] = (-3*(c0+c1)*w + Mu[id_mu[k]]*np.sqrt(Pz))/4
    v[k] = (-3*(s0+s1)*w + Nu[id_nu[k]]*np.sqrt(Qz))/4
print("u : ",u, "/ v : ",v)

'''Computation w0, w1, w2'''
w0 = w*complex(c0,s0)
w1 = np.zeros(2,complex)
w1[0] = complex(u[0],v[0])
w1[1] = complex(u[1],v[1])
w2 = w*complex(c1,s1)


'''Computation w0_c, w1_c, w2_c'''
w0_c = np.sqrt(l)*complex(math.cos(0.5*alpha),math.sin(0.5*alpha))*w0
w1_c = np.sqrt(l)*complex(math.cos(0.5*alpha),math.sin(0.5*alpha))*w1
w2_c = np.sqrt(l)*complex(math.cos(0.5*alpha),math.sin(0.5*alpha))*w2


'''Computation of control point'''
P0 = q0_c
P1 = P0 + (1/5)*(w0_c)**2
P2 = P1 + (1/5)*(w0_c*w1_c)
P3 = P2 + (1/15)*(2*(w1_c)**2 + w0_c*w2_c)
P4 = P3 + (1/5)*(w1_c*w2_c)        
P5 = P4 + (1/5)*(w2_c)**2

pc1 = [P0, P1, P2[0], P3[0], P4[0], P5[0]]
pc2 = [P0, P1, P2[1], P3[1], P4[1], P5[1]]

pc1b = np.zeros(6,dtype = complex)
pc2b = np.zeros(6,dtype = complex)


pc1real = np.zeros(6,float)
pc1imag = np.zeros(6,float)
pc2real = np.zeros(6,float)
pc2imag = np.zeros(6,float)

for i in range(0,len(pc1)):
    pc1b[i] = pc1[i]
    pc2b[i] = pc2[i]
    pc1real[i] = pc1[i].real
    pc1imag[i] = pc1[i].imag
    pc2real[i] = pc2[i].real
    pc2imag[i] = pc2[i].imag
    

PC1 = np.zeros((6,2),float)
PC2 = np.zeros((6,2),float)

PC1[:,0] = pc1real
PC1[:,1] = pc1imag
     
PC2[:,0] = pc2real
PC2[:,1] = pc2imag

'''Curve Interpolation'''
LOD = 400
x1= np.zeros((N,1),float)
y1= np.zeros((N,1),float)
BEZ = np.array([[1,0,0,0,0,0],[-5,5,0,0,0,0],[10,-20,10,0,0,0],[-10,30,-30,10,0,0],[5,-20,30,-20,5,0],[-1,5,-10,10,-5,1]])
print(BEZ)
r1_x=[]
r1_y=[]

r2_x=[]
r2_y=[]

r1_x_prime = []
r1_y_prime = []
r1_z_prime = []

r2_x_prime = []
r2_y_prime = []
r2_z_prime = []

r1_x_prime_prime = []
r1_y_prime_prime = []

r2_x_prime_prime = []
r2_y_prime_prime = []

for i in range (0,LOD):
    
    t= (i)/(LOD-1)
    
    r1_x =np.dot([1, t, t**2, t**3, t**4, t**5],np.dot(BEZ,(PC1[:,0].T)))
    r1_y =np.dot([1, t, t**2, t**3, t**4, t**5],np.dot(BEZ,(PC1[:,1].T)))

    C1[i,0]= r1_x 
    C1[i,1]= r1_y 
        
    
    r2_x =np.dot([1, t, t**2, t**3, t**4, t**5],np.dot(BEZ,(PC2[:,0].T)))
    r2_y =np.dot([1, t, t**2, t**3, t**4, t**5],np.dot(BEZ,(PC2[:,1].T)))
    
    C2[i,0]= r2_x 
    C2[i,1]= r2_y 
    
    r1_x_prime = np.dot([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4],np.dot(BEZ,(PC1[:,0].T)))
    r1_y_prime = np.dot([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4],np.dot(BEZ,(PC1[:,1].T)))
  
    r1_prime[i,0] = r1_x_prime
    r1_prime[i,1] = r1_y_prime
 
    r2_x_prime = np.dot([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4], np.dot(BEZ,(PC2[:,0].T)))
    r2_y_prime = np.dot([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4], np.dot(BEZ,(PC2[:,1].T)))

    r2_prime[i,0] = r2_x_prime
    r2_prime[i,1] = r2_y_prime
    
    
    r1_x_prime_prime = np.dot([0, 0, 2, 6*t, 12*t**2, 20*t**3], np.dot(BEZ,(PC1[:,0].T)))
    r1_y_prime_prime = np.dot([0, 0, 2, 6*t, 12*t**2, 20*t**3], np.dot(BEZ,(PC1[:,1].T)))
    
    r1_prime_prime[i,0] = r1_x_prime_prime
    r1_prime_prime[i,1] = r1_y_prime_prime
    
    r2_x_prime_prime = np.dot([0, 0, 2, 6*t, 12*t**2, 20*t**3],np.dot(BEZ,(PC2[:,0].T)))
    r2_y_prime_prime = np.dot([0, 0, 2, 6*t, 12*t**2, 20*t**3],np.dot(BEZ,(PC2[:,1].T)))
    
    
    r2_prime_prime[i,0] = r2_x_prime_prime
    r2_prime_prime[i,1] = r2_y_prime_prime
    
    K1[i] = (LA.norm (np.cross(r1_prime[i],r1_prime_prime[i]))) / (LA.norm(r1_prime[i]))**3
    
    K2[i] = (LA.norm(np.cross(r2_prime[i],r2_prime_prime[i]))) / (LA.norm(r2_prime[i]))**3
   
    
    
''' Computing length and absolute rotation'''

def moyenne(n):
    somme = sum(n)
    nbr_element = len(n)
    moyenne = somme / nbr_element
    return moyenne

Pc = np.zeros(6,float)

R1=0
R2=0
l1=0
l2=0
    
for i in range (1,LOD):
    l1 = l1 + np.sqrt((C1[i,0] - C1[i-1,0])**2+(C1[i,1]-C1[i-1,1])**2)
    l2 = l2 + np.sqrt((C2[i,0] - C2[i-1,0])**2+(C2[i,1]-C2[i-1,1])**2)
    R1 = R1+0.5*abs(K1[i])**2
    R2 = R2+0.5*abs(K2[i])**2
    
if R1< R2:
        Pts = C1
        Pc = PC1
        L_r=l1
        R = R1
        K= moyenne(K1)    
else :
        Pts = C2
        Pc = PC2
        L_r=l2
        R = R2
        K = moyenne(K2)    
    
plt.figure()
plt.title('Tracé de la courbure')
plt.plot(Pts[:,0],Pts[:,1],'r*', label = "courbure")
plt.plot(data[:,0],data[:,1],'b', label = "contours")
plt.plot(Pc[:,0],Pc[:,1],'g*', label = "Points de contrôle")
plt.legend()
plt.show()  
    


'''Finger material and geometry properties (in USI)'''
E   = 0.36e6
courbure = 10*K

'''Finger 1'''
#Finger Geometry (in USI)
e1   = 3e-3
e3   = 2.5e-3
ht1  = 27e-3           
B1   = 40e-3               
H1   = (30e-3)+e1                                             
t1   = 3e-3            #longeur

h1   = ht1             #H-2*e1
b1   = B1-2*e1
d12  = h1/2+ e1/2      #H/2
S11z = B1*H1 - b1*h1

I11  = ((B1*H1**3)-(b1*h1**3))/12
I11z = I11 + (S11z*d12**2)

d2   =  0.5*11.5e-3+e1/2
S12z = (18e-3)*(25e-3)-(11.5e-3)*(19e-3)

I12  = ((25e-3)*(18e-3)**3-(19e-3)*(11.5e-3)**3)/12
I12z = I12 + (S12z*(d2)**2)


vol1 = S11z*15e-3
vol2 = S12z*4e-3

Im1 = (4*vol1*I11z + 3*vol2*I12z)/(4*vol1+3*vol2)
Ioz1=Im1

'''ACUATION'''
#P1=55000


'''Calculation of the End bending moment1'''
#s = area section of the finger, r = shape factor

r1 = np.sqrt(b1/h1)
s1 = b1*h1
a1 = np.sqrt(s1)

Geom_const=((a1**2)*((0.5*a1+(t1+e3)*r1)/r1))
P=E*Ioz1*courbure*(Geom_const**-1)/(1-Ioz1*courbure*(Geom_const**-1))

    
    
   
    
    