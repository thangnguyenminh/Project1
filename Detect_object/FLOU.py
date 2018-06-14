# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:12:03 2018

@author: Admin
"""
import matplotlib.pyplot as plt
import ih.imgproc
import cv2
import numpy as np


def myfunc(flou,idx):
    plant = ih.imgproc.Image(flou + '/FLUO SV1/0_0.png')
    
    plant.colorFilter("(((((((r - g) < 30) and (((r + g) + b) < 110)) or ((((r + g) + b) > 110) and ((r - g) < 50))) or (((r - g) < 25) and ((g - r) < 25))) or (g > 60)) not 1)")
    pot_filter_1 = plant.save('pot_filter_1')
    
    
    #plant.colorFilter("(((r + g) + b) > 120)")
    #pot_filter_2 = plant.save('pot_filter_2')
    #
    #plant.colorFilter("((r - g) > 10)")
    #main_filter = plant.save('main_filter')
    
    #plant.show('pot_filter_1')
    binary = cv2.inRange(pot_filter_1.copy(), np.array([0, 0, 1], np.uint8), np.array([255, 255, 255], np.uint8))
    
    image, contours,hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, 2)
    obj_contours = contours.copy(); obj_hierarchy = hierarchy
    
    # Loai bo nhung contours cua background
    for i, _cont_ in enumerate(contours):
        if (_cont_[:,:,1][0] > 1230) or (_cont_[:,:,1][0] >= 1337):
        #if (_cont_[:,:,1][0] > 1230):
            del contours[i]
            hierarchy = np.delete(hierarchy, i, 1)
            
    
    ### Find biggest area
    # =============================================================================
    #if len(contours) != 0:
    #     # draw in blue the contours that were founded
    #    cv2.drawContours(output, contours, -1, 255, 3)
    # 
    #     #find the biggest area
    #    c = max(contours, key = cv2.contourArea)
    #    c = np.array(c); contours = np.array(contours);
    #    h_max_index = 0;
    #    for i in np.ndindex(contours.shape):
    #        if contours[i].shape == c.shape:
    #            h_max_index = i;
    #            break;
    #    h_max = hierarchy[:,h_max_index,:]
    #     
    #    contours = list(contours)
    #     # draw the book contour (in green)    
    #     #x,y,w,h = cv2.boundingRect(c)
    #     #cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
    # =============================================================================
        
    ix, iy = np.shape(binary)    
    size = ix, iy, 3
    
    # =============================================================================
    # Allows user to cut objects to the ROI (all objects completely outside ROI will not be kept)
    
    background = np.zeros(size, dtype=np.uint8)
    w_back = background + 255    
    background1 = np.zeros(size, dtype=np.uint8)
    background2 = np.zeros(size, dtype=np.uint8)
    
    cv2.drawContours(background1, obj_contours, -1, (255, 255, 255), -1, lineType=8, hierarchy=obj_hierarchy)
    roi_points = np.vstack(contours)
    cv2.fillPoly(background2, [roi_points], (255, 255, 255))
    obj_roi = cv2.multiply(background1, background2)
    kept_obj = cv2.cvtColor(obj_roi, cv2.COLOR_RGB2GRAY)
    mask = np.copy(kept_obj)
    # =============================================================================
    
    # Tach bien doi tuong
    final = cv2.bitwise_and(pot_filter_1, obj_roi, mask=mask)
    
    # Lap day mau vao ROI
    final_buff = final[800:1196,230:736]
    output_buff = pot_filter_1[800:1196,230:736]
    final2 = cv2.bitwise_or(output_buff,final_buff )
    final[800:1196,230:736] = final2
    
    # =============================================================================
    # show the images
#    plt.figure(1)
#    plt.subplot(211)
#    plt.imshow(final)
#     
#    plt.subplot(212)
#    plt.imshow(obj_roi)
#    plt.show()
    # =============================================================================
    cv2.imwrite(f'{idx}.png', final)
    del background,background1,background2, binary;
    del contours, final, final2, final_buff;
    del hierarchy;
    del i, image, ix;
    del kept_obj, mask;
    del obj_contours, obj_hierarchy, obj_roi, output_buff;
    del pot_filter_1, roi_points, size, w_back;
    plant.exit()


if __name__ == '__main__':
    file = open('../../testadd.txt','rt')
    lines = file.read().strip().split('\n')
    for idx, l in enumerate(lines):
      if (idx% 10 == 0):
          print(idx)
      img_path = l.strip()
      myfunc(img_path,idx)

