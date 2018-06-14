# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:53:31 2018

@author: Admin
"""
import math
import cv2
import numpy as np, matplotlib.pyplot as plt


outf = open('result.txt', 'w')
def my_func(test_add, gt_add):
    obj = cv2.imread(test_add, cv2.IMREAD_GRAYSCALE)
    gt = cv2.imread(gt_add, cv2.IMREAD_GRAYSCALE)
    
#    obj = obj[460:1857,520:1953]
#    gt = gt[460:1857,520:1953]
    
    p1 = cv2.countNonZero(obj)
    p2 = cv2.countNonZero(gt)

    outf.write('{}\n'.format(float(math.fabs(p1 - p2))*100/p2));

file1 = open('GT.txt','rt')
lines1 = file1.read().strip().split('\n')    


for idx in range(len(lines1)):
    if(idx % 10 == 0):
        print(idx)
    gt_path = lines1[idx]
    test_path= "C:/Users/Admin/workspace/Cereal/Analyze/RGB/mask/" +f'{idx}.png'
    my_func(test_path, gt_path)

    
with open('result.txt') as f:
    content = f.readlines();
    content = [float(x.strip('\n')) for x in content]

score = 100 - sum(content)/float(len(content))
print(score)