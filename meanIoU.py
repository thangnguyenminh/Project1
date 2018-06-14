# -*- coding: utf-8 -*-
"""
Created on Wed May 3 16:42:48 2018

@author: Admin
"""

import numpy as np
import cv2

#@profile
def my_func(gt_addr, pred_addr):
    def classification(obj):
        obj_bg = []
        obj_fg = []
        rows = obj.shape[0]
        cols = obj.shape[1]
        for i in range(rows):
            for j in range(cols):
                if(obj.item(i,j) == 0 ):
                    obj_bg.append([i,j])
                else:
                    obj_fg.append([i,j])
        return obj_bg, obj_fg
    
    def multidim_intersect(arr1, arr2):
        arr1 = np.array(arr1)
        arr2 = np.array(arr2)
        arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
        #print(f'arr1_view = {arr1_view}')
        arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
        intersected = np.intersect1d(arr1_view, arr2_view)
        return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])
    
    def meanIoU(gt_bg, gt_fg ,pred_bg, pred_fg ):
        M11 = 0; M01 = 0; M10 = 0;
        M11 = multidim_intersect(gt_fg,pred_fg).shape[0];
        M01 = multidim_intersect(gt_bg,pred_fg).shape[0];
        M10 = multidim_intersect(gt_fg,pred_bg).shape[0];
        denominator = M11 + M01 + M10
        #print(f'M11 = {M11} and M01 = {M01} and M10 = {M10}')
        return float(float(M11)/denominator)
    
    gt = cv2.imread(gt_addr);
    gt = gt[582:1553,577:1622]
    gt = cv2.cvtColor(gt, cv2.COLOR_RGB2GRAY)
    pred = cv2.imread(pred_addr)
    pred = pred[582:1553,577:1622]
    pred = cv2.cvtColor(pred, cv2.COLOR_RGB2GRAY)
    gt_bg, gt_fg = classification(gt)
    pred_bg, pred_fg = classification(pred)
    IoU = meanIoU(gt_bg, gt_fg ,pred_bg, pred_fg );
    gt_bg.clear();gt_fg.clear(); pred_bg.clear();pred_fg.clear();
    gt = []; pred = [];
    del gt_bg[:];del gt_fg[:];del pred_bg[:];del pred_fg[:];
    return IoU
if __name__ == '__main__':
    file = open('GT.txt','rt')
    lines = file.read().strip().split('\n')
    for idx, l in enumerate(lines):
        if(idx % 10 == 0):
            print(idx)
        img_path = l.strip()
        IoU = []
        temp = my_func(img_path,"C:/Users/Admin/workspace/Cereal/Analyze/RGB/mask/" +f'{idx}.png')
        print(temp)
        IoU.append(temp)
        del temp
    
