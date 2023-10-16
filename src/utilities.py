import cv2
import pandas as pd
import numpy as np
import sys
import os
import re


def read_from_file(file_name):
    if file_name[-4:] == '.txt':
        picture = np.loadtxt(file_name)
        length = int(np.sqrt(len(picture)))
        if np.abs(int(length) - length) < 1e-3:
            picture = picture.reshape([length, length])
            if (picture <= 1).all():
                picture *= 255
                picture = picture.astype(np.uint8)
                return picture
            else:
                raise ValueError("input value should between 0 and 1")
        else:
            raise ValueError("input picture is not square")
    else:
        raise ValueError("input file is not .txt file")


def binarize_picture(picture, threshold):
    ret, bi_picture = cv2.threshold(picture, threshold, 255, cv2.THRESH_BINARY)
    return bi_picture

def count_grains(picture, threshold):
    num_objects,labels,stats,centroids= cv2.connectedComponentsWithStats(picture)
    bl = stats[:,-1]>threshold  
    stats = stats[bl]
    num_objects = len(bl)
    centroids=centroids[bl]
    centroids=centroids.astype(np.uint16) 

    area = stats[:,-1].sum()
    average_area = area/num_objects
    return num_objects, average_area


def draw_threshold(picture, gray_range=[180,210], area_range=8):
    if isinstance(gray_range, list):
        if isinstance(area_range, list):
            raise TypeError("gray range and area range should not be 0 at the same time")
        thresholds = list(range(gray_range[0], gray_range[1]))
        for t in thresholds:
            bi_picture = binarize_picture(picture, threshold) 
            num, ave_area = count_grains(bi_picture, area_range)  

        fig, ax = plt.subplots()
        ax.plot(threshold, num)
        ax.set_xlabel('threshold')
        ax.set_ylabel('num')
        fig.savefig('gray_reference.png')


        
    else:
        if not isinstance(area_range, list):
            raise TypeError("area range should list in this case")

        area_candidates = list(range(area_range[0], area_range[1]))
        for a in area_candidates:
            bi_picture = binarize_picture(picture, gray_range) 
            num, ave_area = count_grains(bi_picture, a)  

        fig, ax = plt.subplots()
        ax.plot(threshold, num)
        ax.set_xlabel('threshold')
        ax.set_ylabel('num')
        fig.savefig('area_reference.png')

        


    




    


