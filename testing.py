
from PIL import Image
import random
import numpy
import pdb

from PIL import Image

import array
import logging

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot

import math

from matplotlib.patches import Rectangle







class Testing(object):
    def __init__(self, image, boundary):
        self.image =image
        self.pixel_map = [] 
        self.boundary = boundary
        self.image_width = 0
        self.image_height = 0
        self.positive_sample = []

        self.output_image =  Image.open(self.image)
        self.output_map = self.output_image.load()


    def openImage(self):
        self.pixel_map = Image.open(self.image).load()
        self.image_width, self.image_height = Image.open(self.image).size
    

    def seperate_minority_majority(self, selected_cluster_no):
        village = 0
        non_village = 0

        for j in range(self.image_width):
            for k in range(self.image_height):
                not_village_pixel = True
                x = 0
                for i in range(len(self.boundary)/2):
                    x = i * 2

                    status = False
                    for no in selected_cluster_no:
                        # print "no ", no, x, len(self.boundary)
                        if x != no and (x+1) != no:
                            # print "************************* ", x
                            status = True


                    if status:

                        # print "------------>", x, i , cluster_no_2, len(self.boundary)
                       
                        # print self.boundary[x], self.boundary[x+1]
                        if self.pixel_map[j,k][0] > self.boundary[x][0] and self.pixel_map[j,k][1] > self.boundary[x][1] and self.pixel_map[j,k][2] > self.boundary[x][2] and self.pixel_map[j,k][0] < self.boundary[x+1][0] and self.pixel_map[j,k][1] < self.boundary[x+1][1] and self.pixel_map[j,k][2] < self.boundary[x+1][2]:
                            self.positive_sample.append(j)
                            self.output_map[j,k] = (255, 0, 0)
                            village=village+1
                            not_village_pixel= False
                            break


                if not_village_pixel:
                    non_village = non_village+1

        print "original image",  village,non_village

        self.output_image.show()


    def minimumOverlapOutpu(self, selected_cluster_no):

        village = 0
        non_village = 0

        for j in range(self.image_width):
            for k in range(self.image_height):
                not_village_pixel = True
                x = 0
                
                for i in selected_cluster_no:
                    x = i * 2
                

                    
                        # print self.boundary[x], self.boundary[x+1]
                    if self.pixel_map[j,k][0] > self.boundary[x][0] and self.pixel_map[j,k][1] > self.boundary[x][1] and self.pixel_map[j,k][2] > self.boundary[x][2] and self.pixel_map[j,k][0] < self.boundary[x+1][0] and self.pixel_map[j,k][1] < self.boundary[x+1][1] and self.pixel_map[j,k][2] < self.boundary[x+1][2]:
                        self.positive_sample.append(j)
                        self.output_map[j,k] = (255, 0, 0)
                        village=village+1
                        not_village_pixel= False
                        break
                    # else:
                    #     self.output_map[j,k] = (255, 255, 255)


                if not_village_pixel:
                    non_village = non_village+1

        print "original image",  village,non_village

        self.output_image.show()


