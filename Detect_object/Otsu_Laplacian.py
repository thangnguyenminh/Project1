# -*- coding: utf-8 -*-
"""
Created on Wed May 16 05:19:27 2018

@author: Admin
"""
import os
import gc
import cv2
import matplotlib.pyplot as plt
import numpy as np
#from memory_profiler import profile

#@profile
def histogram(img):
    w = img.shape[0]
    h = img.shape[1]
    hist = np.zeros((256))
    
    for i in np.arange(w):
        for j in np.arange(h):
            a = img.item(i,j)
            hist[a] += 1
    
    return hist

def nguong_toan_cuc(img, epsilon):
    hist = histogram(img)
    bins = np.array([i for i,h in enumerate(hist) if h != 0])
    thresh_all = 124
    delta_T = 1
    while(delta_T > epsilon):
        G1 = np.array([i for i in bins if i >= thresh_all])
        G2 = np.array([i for i in bins if i < thresh_all])
        
        m1 = np.mean(G1)
        m2 = np.mean(G2)
        
        T = float(m1+m2)/2
        delta_T= abs(T - thresh_all)
        thresh_all = T
        if delta_T > epsilon:
            break
    return thresh_all




# =============================================================================
# cpy = img
# thresh = nguong_toan_cuc(cpy,0.01)
# thresh1,cpy = cv2.threshold(cpy, thresh,255, cv2.THRESH_BINARY)
# # Otsu's thresholding after Gaussian filtering
# blur = cv2.GaussianBlur(cpy,(5,5),0)
# plt.hist(blur.ravel(),256,[0,256]); plt.show();
# ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# =============================================================================
# =============================================================================
# plt.subplot(221)
# plt.imshow(img)
# plt.subplot(222)
# plt.imshow(th3)
# plt.subplot(223)
# plt.hist(img.ravel(),256,[0,256]);
# plt.subplot(224)
# plt.hist(th3.ravel(),256,[0,256]); plt.show()
# =============================================================================
@profile
def my_func():
    print('Hello')
    img = cv2.imread('1-6.png')
    cpy = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    blur1 = cv2.GaussianBlur(img,(5,5),0)
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    laplacian = np.absolute(laplacian)
    laplacian = laplacian.astype(np.uint8)
    blur1 = cv2.GaussianBlur(laplacian,(5,5),0)
    retVal1, thresh1 = cv2.threshold(blur1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('thresh1',thresh1)
    mask_inv = cv2.bitwise_not(thresh1)
    #thresh1 = thresh1[1404:2138,649:1393]
    mask_inv = mask_inv[1404:2138,649:1393]
    draft = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)
    draft[1404:2138,649:1393] = 255
    img_wise = cv2.bitwise_and(draft,thresh1,mask_inv)
    cv2.imshow('img_wise_pre',img_wise)

    #retVal2, thresh2 = cv2.threshold(img_wise,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #thresh1 = thresh1[1404:2138,649:1393]
    #thresh2 = thresh2[1404:2138,649:1393]
    

    # Mask image
    #masked = cv2.bitwise_or(cpy, img_wise, mask = img_wise);
    masked = cpy and img_wise
    cv2.imshow('Masked',masked)
    #Create inverted mask for background
    img_wise = cv2.bitwise_not(img_wise)
    cv2.imshow('img_wise',img_wise)
    # Invert the background so that it is white
    white_mask = cv2.bitwise_not(masked, mask = img_wise)
    cv2.imshow('white_mask',white_mask)
    # Add image 
    white_masked = cv2.add(masked, white_mask) 
    cv2.imshow('white_masked',white_masked)
    del blur1,  draft, img_wise, laplacian, masked, mask_inv, white_mask, white_masked
    #del retVal1, retVal2
    gc.collect()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 

if __name__ == '__main__' :
    my_func()
