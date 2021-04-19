
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
from numpy import linalg as LA




img = cv2.imread("Ressources/ballon2.jpg", cv2.IMREAD_UNCHANGED)

print('Original Dimensions : ', img.shape)

cv2.imshow(" image", img)


#grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



ret, thresh = cv2.threshold(img_gray, 240, 215, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

img_copy = img.copy()


cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)

strokeList=[] # liste où l'on va stoker les  coordonnées x,y

Xcontour = []
Ycontour = []

Xcontour2=[]
Ycontour2=[]



for i in range(0,len(contours)):
    for c in contours[i]:
        x = c[0][0]
        y = c[0][1]

        coord = (x, y)
        strokeList.append(coord)
        Xcontour.append(x)
        Ycontour.append(y)
        if x!=min(Xcontour): #enleve les 4 points aux extremité
            if  x!=max(Xcontour):
                if y != min(Ycontour):
                    if y != max(Ycontour):
                        #plt.plot(x, y, "or")
                        Xcontour2.append(x) # se debarasser des extremités des listes
                        Ycontour2.append(y)


xg=round(sum(Xcontour2)/len(Xcontour2))
yg=round(sum(Ycontour2)/len(Ycontour2))


NewXcontour=[]
NewYcontour=[]

positif=[]
negatif=[]
k=0

for i in range(0,len(Xcontour2)):
        Xnew= Xcontour2[i]-xg
        Ynew= Ycontour2[i]-yg
        coordnew=(Xnew,Ynew)
        NewXcontour.append(Xcontour)
        NewYcontour.append(Ycontour)
        if Xnew> 0:
            positif.append(coordnew)
        if Xnew <= 0:
            negatif.append(coordnew)


Xg=xg-xg
Yg=yg-yg


k=0
t=0


for i in range(0,len(positif)-1):
    for j in range(0,len(positif)-i):
        if positif[i][1]>positif[i+j][1]:
            t=positif[i+j]
            positif[i+j]=positif[i]
            positif[i]=t
        if positif[i][1]==positif[i+1][1]:
            if positif[i][0] > positif[i+1][0]:
                k=positif[i+1]
                positif[i+1]=positif[i]
                positif[i]=k



for i in range(0,len(negatif)-1):
    for j in range(0,len(negatif)-i):
        if negatif[i][1]>negatif[i+j][1]:
            t=negatif[i+j]
            negatif[i+j]=negatif[i]
            negatif[i]=t
        if negatif[i][1] == negatif[i+1][1]:
            if negatif[i][0] < negatif[i+1][0]:
                k = negatif[i+1]
                negatif[i + 1] = negatif[i]
                negatif[i] = k

image = cv2.circle(img_copy, (xg,yg), 1, (0,0,0), 3) # trace du centre de gravité

print(positif)
print(negatif)

cv2.imshow('resultat', img_copy)

plt.figure()
plt.grid(True)

Xp=0
Yp=0
Xn=0
Yn=0

for i in range (0,len(positif)):
    Xp = positif[i][0]
    Yp = positif[i][1]
    plt.plot(Xp,Yp,"or")

for i in range(0,len(negatif)):
    Xn= negatif[i][0]
    Yn= negatif[i][1]
    plt.plot(Xn, Yn, "og")

plt.axis([-300,300,-300,300])
plt.plot(Xg,Yg,"oy")
plt.show()


cv2.waitKey(0)






valeurs = np.zeros((len(positif),2),float)
for i in range(0,len(positif)):
    valeurs[i]=positif[i]
print(valeurs)
print(valeurs.shape)

X = valeurs[:, 0]
Y = valeurs[:, 1]
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)
print("valeurs de X", X)
print("valeurs de Y", Y)
plt.figure()
plt.plot(X, Y)
plt.show()


Nt = valeurs.shape
print("Nt = ", Nt)
strN = str(Nt[0])
print("strN = ", strN)
N = np.array(strN, dtype='int')
print("N = ", N)

C1 = np.zeros((N, 2), float)
C2 = np.zeros((N, 2), float)

r1_prime = np.zeros((N, 2), float)
r2_prime = np.zeros((N, 2), float)

r1_prime_prime = np.zeros((N, 2), float)
r2_prime_prime = np.zeros((N, 2), float)

K1 = np.zeros((N, 1), float)
K2 = np.zeros((N, 1), float)




q0 = valeurs[0]
q1 = valeurs[N - 1]
print("q0 = ", q0)
print("q1 = ", q1)


t0 = valeurs[1] - valeurs[0]
t1 = valeurs[N - 1] - valeurs[N - 2]
print("t0 = ", t0)
print("t1 = ", t1)


L0 = 0
for i in range(1, len(valeurs)):
    L0 += LA.norm((valeurs[i] - valeurs[i - 1]))
print("L0 = ", L0)


q0_c = complex(q0[0], q0[1])
q1_c = complex(q1[0], q1[1])
print("q0_c = ", q0_c)
print("q1_c = ", q1_c)

t0_c = (complex(t0[0], t0[1])) / LA.norm(t0)
t1_c = (complex(t1[0], t1[1])) / LA.norm(t1)
print("t0_c = ", t0_c)
print("t1_c = ", t1_c)

z = q1_c - q0_c
print("z = ", z)
l = abs(z)
print("l = ", l)
alpha = cmath.phase(z)
print("alpha = ", alpha)

di = (t0_c * np.conj(z)) / l
df = (t1_c * np.conj(z)) / l
Le = L0 / l


theta0 = cmath.phase(di);
theta1 = cmath.phase(df);

thetam = 0.5 * (theta0 + theta1);
dtheta = 0.5 * (theta1 - theta0);

c0 = math.cos(0.5 * theta0);
c1 = math.cos(0.5 * theta1);

s0 = math.sin(0.5 * theta0);
s1 = math.sin(0.5 * theta1);


a2 = 2 * (math.sin(dtheta)) ** 2
a1 = 6 * ((math.cos(dtheta) - 3) * Le + (3 * math.cos(dtheta) - 1) * math.cos(thetam))
a0 = 36 * (Le ** 2 - 1)

discr = (a1 ** 2) - 4 * a2 * a0

z_ = (-a1 - np.sqrt(discr)) / (2 * a2)

w = np.sqrt(z_)


Pz = 60 * (Le + 1) - ((15 * c0 ** 2) + (15 * c1 ** 2) - 10 * c0 * c1) * z_
Qz = 60 * (Le - 1) - ((15 * s0 ** 2) + (15 * s1 ** 2) - 10 * s0 * s1) * z_

Mu_m = -1.0
Mu_p = +1.0
Mu = [Mu_m, Mu_p]

Nu_m = -1.0
Nu_p = +1.0
Nu = [Nu_m, Nu_p]

cond = 5 * (c0 * s1 + c1 * s0 - 3 * c0 * s0 - 3 * c1 * s1) * z_

Status = np.zeros((2, 2), float)
mn = np.zeros((2, 2), float)

id_mu = np.zeros(2, int)
id_nu = np.zeros(2, int)

k = 0
for i in range(0, 2):
    for j in range(0, 2):
        mn[i, j] = Mu[i] * Nu[j]
        Status[i, j] = np.sqrt(Pz) * np.sqrt(Qz) * mn[i, j]
        if ((Status[i, j] - cond) <= 0.001):
            id_mu[k] = i
            id_nu[k] = j
    k += 1

print(mn, Status)
print("id_mu : ", id_mu, "/ id-nu : ", id_nu)


u = np.zeros(2, float)
v = np.zeros(2, float)

for k in range(0, 2):
    u[k] = (-3 * (c0 + c1) * w + Mu[id_mu[k]] * np.sqrt(Pz)) / 4
    v[k] = (-3 * (s0 + s1) * w + Nu[id_nu[k]] * np.sqrt(Qz)) / 4
print("u : ", u, "/ v : ", v)


w0 = w * complex(c0, s0)
w1 = np.zeros(2, complex)
w1[0] = complex(u[0], v[0])
w1[1] = complex(u[1], v[1])
w2 = w * complex(c1, s1)


w0_c = np.sqrt(l) * complex(math.cos(0.5 * alpha), math.sin(0.5 * alpha)) * w0
w1_c = np.sqrt(l) * complex(math.cos(0.5 * alpha), math.sin(0.5 * alpha)) * w1
w2_c = np.sqrt(l) * complex(math.cos(0.5 * alpha), math.sin(0.5 * alpha)) * w2


P0 = q0_c
P1 = P0 + (1 / 5) * (w0_c) ** 2
P2 = P1 + (1 / 5) * (w0_c * w1_c)
P3 = P2 + (1 / 15) * (2 * (w1_c) ** 2 + w0_c * w2_c)
P4 = P3 + (1 / 5) * (w1_c * w2_c)
P5 = P4 + (1 / 5) * (w2_c) ** 2

pc1 = [P0, P1, P2[0], P3[0], P4[0], P5[0]]
pc2 = [P0, P1, P2[1], P3[1], P4[1], P5[1]]

pc1b = np.zeros(6, dtype=complex)
pc2b = np.zeros(6, dtype=complex)

pc1real = np.zeros(6, float)
pc1imag = np.zeros(6, float)
pc2real = np.zeros(6, float)
pc2imag = np.zeros(6, float)

for i in range(0, len(pc1)):
    pc1b[i] = pc1[i]
    pc2b[i] = pc2[i]
    pc1real[i] = pc1[i].real
    pc1imag[i] = pc1[i].imag
    pc2real[i] = pc2[i].real
    pc2imag[i] = pc2[i].imag

PC1 = np.zeros((6, 2), float)
PC2 = np.zeros((6, 2), float)

PC1[:, 0] = pc1real
PC1[:, 1] = pc1imag

PC2[:, 0] = pc2real
PC2[:, 1] = pc2imag


LOD = len(valeurs)
x1 = np.zeros((N, 1), float)
y1 = np.zeros((N, 1), float)
BEZ = np.array(
    [[1, 0, 0, 0, 0, 0], [-5, 5, 0, 0, 0, 0], [10, -20, 10, 0, 0, 0], [-10, 30, -30, 10, 0, 0], [5, -20, 30, -20, 5, 0],
     [-1, 5, -10, 10, -5, 1]])
print(BEZ)
r1_x = []
r1_y = []

r2_x = []
r2_y = []

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

for i in range(0, LOD):
    t = (i) / (LOD - 1)

    r1_x = np.dot([1, t, t ** 2, t ** 3, t ** 4, t ** 5], np.dot(BEZ, (PC1[:, 0].T)))
    r1_y = np.dot([1, t, t ** 2, t ** 3, t ** 4, t ** 5], np.dot(BEZ, (PC1[:, 1].T)))

    C1[i, 0] = r1_x
    C1[i, 1] = r1_y

    r2_x = np.dot([1, t, t ** 2, t ** 3, t ** 4, t ** 5], np.dot(BEZ, (PC2[:, 0].T)))
    r2_y = np.dot([1, t, t ** 2, t ** 3, t ** 4, t ** 5], np.dot(BEZ, (PC2[:, 1].T)))

    C2[i, 0] = r2_x
    C2[i, 1] = r2_y

    r1_x_prime = np.dot([0, 1, 2 * t, 3 * t ** 2, 4 * t ** 3, 5 * t ** 4], np.dot(BEZ, (PC1[:, 0].T)))
    r1_y_prime = np.dot([0, 1, 2 * t, 3 * t ** 2, 4 * t ** 3, 5 * t ** 4], np.dot(BEZ, (PC1[:, 1].T)))

    r1_prime[i, 0] = r1_x_prime
    r1_prime[i, 1] = r1_y_prime

    r2_x_prime = np.dot([0, 1, 2 * t, 3 * t ** 2, 4 * t ** 3, 5 * t ** 4], np.dot(BEZ, (PC2[:, 0].T)))
    r2_y_prime = np.dot([0, 1, 2 * t, 3 * t ** 2, 4 * t ** 3, 5 * t ** 4], np.dot(BEZ, (PC2[:, 1].T)))

    r2_prime[i, 0] = r2_x_prime
    r2_prime[i, 1] = r2_y_prime

    r1_x_prime_prime = np.dot([0, 0, 2, 6 * t, 12 * t ** 2, 20 * t ** 3], np.dot(BEZ, (PC1[:, 0].T)))
    r1_y_prime_prime = np.dot([0, 0, 2, 6 * t, 12 * t ** 2, 20 * t ** 3], np.dot(BEZ, (PC1[:, 1].T)))

    r1_prime_prime[i, 0] = r1_x_prime_prime
    r1_prime_prime[i, 1] = r1_y_prime_prime

    r2_x_prime_prime = np.dot([0, 0, 2, 6 * t, 12 * t ** 2, 20 * t ** 3], np.dot(BEZ, (PC2[:, 0].T)))
    r2_y_prime_prime = np.dot([0, 0, 2, 6 * t, 12 * t ** 2, 20 * t ** 3], np.dot(BEZ, (PC2[:, 1].T)))

    r2_prime_prime[i, 0] = r2_x_prime_prime
    r2_prime_prime[i, 1] = r2_y_prime_prime

    K1[i] = (LA.norm(np.cross(r1_prime[i], r1_prime_prime[i]))) / (LA.norm(r1_prime[i])) ** 3

    K2[i] = (LA.norm(np.cross(r2_prime[i], r2_prime_prime[i]))) / (LA.norm(r2_prime[i])) ** 3




def moyenne(n):
    somme = sum(n)
    nbr_element = len(n)
    moyenne = somme / nbr_element
    return moyenne


Pc = np.zeros(6, float)

R1 = 0
R2 = 0
l1 = 0
l2 = 0

for i in range(1, LOD):
    l1 = l1 + np.sqrt((C1[i, 0] - C1[i - 1, 0]) ** 2 + (C1[i, 1] - C1[i - 1, 1]) ** 2)
    l2 = l2 + np.sqrt((C2[i, 0] - C2[i - 1, 0]) ** 2 + (C2[i, 1] - C2[i - 1, 1]) ** 2)
    R1 = R1 + 0.5 * abs(K1[i]) ** 2
    R2 = R2 + 0.5 * abs(K2[i]) ** 2

if R1 < R2:
    Pts = C1
    Pc = PC1
    L_r = l1
    R = R1
    K = moyenne(K1)
else:
    Pts = C2
    Pc = PC2
    L_r = l2
    R = R2
    K = moyenne(K2)

plt.figure()
plt.title('Tracé de la courbure')
plt.plot(Pts[:, 0], Pts[:, 1], 'r*', label="courbure")
plt.plot(valeurs[:, 0], valeurs[:, 1], 'b', label="contours")
plt.plot(Pc[:, 0], Pc[:, 1], 'g*', label="Points de contrôle")
plt.legend()
plt.show()


E = 0.36e6
courbure = 10*K


# Finger Geometry (in USI)
e1 = 3e-3
e3 = 2.5e-3
ht1 = 27e-3
B1 = 40e-3
H1 = (30e-3) + e1
t1 = 3e-3  # longeur

h1 = ht1  # H-2*e1
b1 = B1 - 2 * e1
d12 = h1 / 2 + e1 / 2  # H/2
S11z = B1 * H1 - b1 * h1

I11 = ((B1 * H1 ** 3) - (b1 * h1 ** 3)) / 12
I11z = I11 + (S11z * d12 ** 2)

d2 = 0.5 * 11.5e-3 + e1 / 2
S12z = (18e-3) * (25e-3) - (11.5e-3) * (19e-3)

I12 = ((25e-3) * (18e-3) ** 3 - (19e-3) * (11.5e-3) ** 3) / 12
I12z = I12 + (S12z * (d2) ** 2)

vol1 = S11z * 15e-3
vol2 = S12z * 4e-3

Im1 = (4 * vol1 * I11z + 3 * vol2 * I12z) / (4 * vol1 + 3 * vol2)
Ioz1 = Im1


# P1=55000



# s = area section of the finger, r = shape factor

r1 = np.sqrt(b1 / h1)
s1 = b1 * h1
a1 = np.sqrt(s1)

Geom_const = ((a1 ** 2) * ((0.5 * a1 + (t1 + e3) * r1) / r1))
P = E * Ioz1 * courbure * (Geom_const ** -1) / (1 - Ioz1 * courbure * (Geom_const ** -1))

print("courbure = ", courbure)
print("P = ", P)