# -*- coding: utf-8 -*-
"""
Created on Tue May 15 19:01:55 2018

@author: Admin
"""
import imgproc
from memory_profiler import profile
import matplotlib.pyplot as plt
import csv
import numpy as np
#@profile
def computer_RGB_SV(vis_image,idx):
    #vis_image = 'D:/Users/Admin/Downloads/testSet/strain1/0184 Uni Nebraska Rice 1_023538-S_2013-09-08_05-16-05_460864'
    plant = imgproc.Image(vis_image)
    
    base = plant.save("base")
    #plant.show("base")
    
    plant.convertColor("bgr", "gray")
    #plant.show("grayscale")
    
    plant.gaussianBlur((5, 5))
    #plant.show("blur")
    
    plant.adaptiveThreshold(255, "mean", "binary", 15, 3)
    #plant.show("adaptive threshold")
    
    plant.bitwise_not()
    #plant.show("invert")
    
    plant.convertColor("gray", "bgr")
    plant.bitwise_and("base")
    #plant.show("recolor")
    
    plant.morphology("open", "rect", (3, 3))
    #plant.show("morph")
    
    logic1 = '((((r max g) max b) - ((r min g) min b)) > 40)' 
    logic2 = '((b - g) < 30)'
    plant.colorFilter(logic1 + 'and' + logic2, [plant.y - 350, -1, -1, -1])
    #plant.show("filter")
    plant.save("filter")
    
    plant.convertColor("bgr", "gray")
    plant.threshold(0)
    plant.medianBlur(5)
    plant.bitwise_not()
    binary = plant.save("binary")
    #plant.show("binary")
    plant.restore("filter")
    
    plant.contourCut("binary", basemin = 500, resize = False)
    final = plant.save("final")
    #plant.write(f'/Mask/RGB SV2/{idx}-final.png')
    #plt.imshow(final);
    PSA = plant.extractPixels()
    ConA_SV, ConC_SV = plant.extractConvexHull()
    MinC_SV = plant.extractMinEnclosingCircle()
    Ci_SV = np.pi * MinC_SV[1]
    CL_SV = plant.extractLongestAxis()
    MinR_sv = plant.extractMinEnclosingRectangle()
    
    final = []; binary = []; base = []; 
    del final; del binary; del base; del logic1; del logic2; del vis_image;
    plant.exit();
    return PSA, CL_SV, Ci_SV, ConA_SV, ConC_SV , MinC_SV, MinR_sv 

def RGB_SV(vis_image,idx):
    sv = []
    sv1_PSA, sv1_CL_SV, sv1_Ci_SV, sv1_ConA_SV, sv1_ConC_SV , sv1_MinC_SV, sv1_MinR_sv = computer_RGB_SV(vis_image + '/RGB SV1/0_0.png',idx)
    sv2_PSA, sv2_CL_SV, sv2_Ci_SV, sv2_ConA_SV, sv2_ConC_SV , sv2_MinC_SV, sv2_MinR_sv = computer_RGB_SV(vis_image + '/RGB SV2/0_0.png',idx)     
    sv.extend([sv1_PSA, sv1_CL_SV, sv1_Ci_SV, sv1_ConA_SV, sv1_ConC_SV , sv1_MinC_SV, sv1_MinR_sv, sv2_PSA, sv2_CL_SV, sv2_Ci_SV, sv2_ConA_SV, sv2_ConC_SV , sv2_MinC_SV, sv2_MinR_sv ])
    return sv


#@profile    
def RGB_TV(vis_image,idx):
    plant = imgproc.Image(vis_image + '/RGB TV/0_0.png')
    base = plant.save("base")
    #plant.show("base")
    
    logic = '(((g - r) > 15) and (b < g))'
    plant.colorFilter(logic)
    plant.crop([582,1553,577,1622])
    filter_img = plant.save('filter')
    
    PSA = plant.extractPixels()

    
    #plant.write(f'/Mask/RGB TV/{idx}-final.png')
    
    base = []; filter_img = [];
    del base; del filter_img; del logic
    plant.exit();
    tv = []; tv.extend([PSA])
    return tv
    
if __name__ == '__main__':
    file = open('testadd.txt','rt')
    lines = file.read().strip().split('\n')

    with open('Draft.csv', "w") as f:        
        #configure writer to write standard csv file
        #writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer = csv.writer(f,lineterminator='\n')
        for idx, l in enumerate(lines):
            img_path = l.strip()
            
            sv = RGB_SV(img_path,idx)
            tv = RGB_TV(img_path,idx)
            trait = []
            trait.extend([img_path])
            trait.extend(sv)
            trait.extend(tv)
            
            writer.writerow(trait)

