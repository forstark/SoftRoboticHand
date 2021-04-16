import cv2
import numpy as np
#import scipy as sp
import scipy.ndimage
import matplotlib.pyplot as plt
import pandas as pd
import math
#///////////////////////////////////////////////////////////////////




img = cv2.imread("Ressources/banane.jpg", cv2.IMREAD_UNCHANGED)

print('Original Dimensions : ', img.shape)

cv2.imshow(" image", img)


#grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#afficher l'image en gris

cv2.imshow("image en gris", img_gray)


#contours
#ret, thresh = cv2.threshold(img_gray, 215, 100, cv2.THRESH_BINARY)

#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


ret, thresh = cv2.threshold(img_gray, 230, 215, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

img_copy = img.copy()

#for contours in contours:
    #cv2.drawContours(img_copy, contours,-1, (0, 255, 0),4)

cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)




figure=plt.figure()

plt.grid(True)

strokeList=[]

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
                        plt.plot(x, y, "or")
                        Xcontour2.append(x) # se debarasser des extremités des listes
                        Ycontour2.append(y)

xg=round(sum(Xcontour2)/len(Xcontour2))
yg=round(sum(Ycontour2)/len(Ycontour2))

plt.plot(xg,yg,"oy")
plt.show()
#Xnew=np.zeros((len(Xcontour2),1),float)
#Ynew=np.zeros((len(Ycontour2),1),float)

Centre=plt.figure()
plt.grid(True)

NewXcontour=[]
NewYcontour=[]
for i in range(0,len(Xcontour2)):
        Xnew= Xcontour2[i]-xg
        Ynew= Ycontour2[i]-yg
        plt.plot(Xnew,Ynew,"or" )
        NewXcontour.append(Xcontour)
        NewYcontour.append(Ycontour)

Xg=xg-xg
Yg=yg-yg

a=max(NewXcontour)
b=max(NewYcontour)


plt.plot(Xg,Yg,"og")

image = cv2.circle(img_copy, (xg,yg), 1, (0,0,0), 3)

plt.axis([-300,300,-300,300])
cv2.imshow('resultat', img_copy)

plt.show()

cv2.waitKey(0)

