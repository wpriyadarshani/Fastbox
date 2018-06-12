
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


class Cluster(object):
    def __init__(self):
        self.centroid = None # define centroid for particular cluster



class FCM(object):
    def __init__(self, pixels, k = 5, m = 2.0, epsilon = 0.01, max_fcm_iteration =100):
        self.pixels = pixels
        self.k = k
        self.epsilon = epsilon
        self.max_fcm_iteration = max_fcm_iteration
        self.clusters = []
        self.max_diff = 10.0
        self.s = len(pixels)
        self.m = m
        self.degree_of_membership = []
        self.clusters_pixels = [[] for i in range(k)] 
       

    def run(self):

        print " length of pixels ", len(self.pixels)

        for i in range(self.s):
            self.degree_of_membership.append(numpy.random.dirichlet(numpy.ones(self.k), size=1))

        randomPixels = random.sample(self.pixels, self.k)

        #initialize the clusters
        self.clusters = [None for i in range(self.k)]

        for idx in range(self.k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = randomPixels[idx]

        #run FCM algorithm
        iterations = 0

        while self.shouldExitFCM(iterations) is False:
            print "FCM Iteration -------------->", iterations  
            self.calculate_centre_vector()
            self.update_membership()
            iterations += 1
          
        return [cluster.centroid for cluster in self.clusters]

    def shouldExitFCM(self, iteration):
        if self.max_diff < self.epsilon:
            return True

        if self.max_fcm_iteration < iteration:
            return True

        return False

    def get_new_value(self, i, j):
        sum = 0.0
        val = 0.0
        p = (2 * (1.0) / (self.m - 1))  # cast to float value or else will round to nearst int
        for k in self.clusters:
            num = self.calcDistance(i, j)
            denom = self.calcDistance(i, k.centroid)
            val = num / denom
            val = pow(val, p)
            sum += val
        return (1.0 / sum)

    def update_membership(self):
        self.max_diff = 0.0

        for idx in range(self.k):
            for i in range(self.s):
                new_uij = self.get_new_value(self.pixels[i], self.clusters[idx].centroid)
                # if (i == 0):
                #     print "This is the Updatedegree centroid :", idx, self.clusters[idx].centroid
                diff = new_uij - self.degree_of_membership[i][0][idx]

                if (diff > self.max_diff):
                    self.max_diff = diff
                self.degree_of_membership[i][0][idx] = new_uij
        return self.max_diff



    # Calculates the centroids using degree of membership and fuzziness.
    def calculate_centre_vector(self):
        for cluster in range(self.k):
            sum_numerator = [0,0,0,0]
            sum_denominator = 0.0
            for i in range(self.s):
                pow_uij= pow(self.degree_of_membership[i][0][cluster], self.m)
                sum_denominator +=pow_uij
                
                num= (pow_uij * self.pixels[i][0], pow_uij * self.pixels[i][1], pow_uij * self.pixels[i][2], 255)

                sum_numerator[0] = num[0] + sum_numerator[0]
                sum_numerator[1] = num[1] + sum_numerator[1] 
                sum_numerator[2] = num[2] + sum_numerator[2] 
                sum_numerator[3] = num[3] + sum_numerator[3] 

            updatedcluster_center = (sum_numerator[0]/sum_denominator, sum_numerator[1]/sum_denominator, sum_numerator[2]/sum_denominator,255)

            self.clusters[cluster].centroid = updatedcluster_center

    def normalization(self):
        for i in range(self.s):
            max = 0.0
            highest_index = 0
            for j in range(self.k):
                if (self.degree_of_membership[i][0][j] > max):
                    max = self.degree_of_membership[i][0][j]
                    highest_index = j
            for j in range(self.k):

                if (j != highest_index):
                    self.degree_of_membership[i][0][j] = 0
                else:
                    self.degree_of_membership[i][0][j] = 1

    def devidPixelsToClusters(self):

        self. normalization()

        for i in range(self.s):
            if self.degree_of_membership[i][0][0] == 1:
                self.clusters_pixels[0].append(self.pixels[i])
            elif self.degree_of_membership[i][0][1] == 1:
                self.clusters_pixels[1].append(self.pixels[i])
            elif self.degree_of_membership[i][0][2] == 1:
                self.clusters_pixels[2].append(self.pixels[i])
            elif self.degree_of_membership[i][0][3] == 1:
                self.clusters_pixels[3].append(self.pixels[i])
            elif self.degree_of_membership[i][0][4] == 1:
                self.clusters_pixels[4].append(self.pixels[i])
           
      
       
        return self.clusters_pixels

    def calcDistance(self, a, b):
        dis1 = pow((a[0]-b[0]),2.0)
        dis2 = pow((a[1]-b[1]),2.0)
        dis3 = pow((a[2]-b[2]),2.0)
        dis4 = pow((a[3]-b[3]),2.0)

        sumation = dis1 + dis2 + dis3 + dis4
        result = numpy.sqrt(sumation)
        return result

