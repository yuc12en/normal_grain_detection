import cv2
import pandas as pd
import numpy as np



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


if __name__ == "__main__":
    file_name = "../../data/300.txt"
    from matplotlib import pyplot as plt

    # read
    picture = read_from_file(file_name)

    # binarize
    # bi_picture = binarize_picture(picture, 127)
    
    # count
    # num, ave_area = count_grains(bi_picture, 8)

    threshold = list(range(1,151))
    nums = []
    for t in threshold:
        print(t)
        bi_picture = binarize_picture(picture, t)
        num, ave_area = count_grains(bi_picture, 8)
        nums.append(nums)

    fig, ax = plt.subplots()
    ax.plot(threshold, nums)
    fig.savefig("binary_threshold.png")


    # print("number of grains:" + str(num))

    # print("average area:" + str(ave_area))
    
                
