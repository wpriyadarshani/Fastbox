
from PIL import Image
import random
import numpy
import pdb
from PIL import Image
import array
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
import math
from matplotlib.patches import Rectangle

#import FCM class
import FCM
import testing

def calcDistance(a, b):
        dis1 = pow((a[0]-b[0]),2.0)
        dis2 = pow((a[1]-b[1]),2.0)
        dis3 = pow((a[2]-b[2]),2.0)
        dis4 = pow((a[3]-b[3]),2.0)

        sumation = dis1 + dis2 + dis3 + dis4
        result = numpy.sqrt(sumation)
        return result


class Initial_Clustering(object):
  
    def __init__(self, image, image_GT):
        #save image names
        self.org_image = image
        self.GT_image = image_GT

        #save pixel maps
        self.org_pixel_map = []
        self.GT_pixel_map = []
        self.output_pixel_map = []
        self.output_image = 0
       
        self.village_pixels = []
        self.village_pixel_location = []

        self.centroids = []

        self.non_village_pixels = []
        self.cluster1 = []
        self.cluster2= []
        self.cluster3 = []
        self.image_width = 0
        self.image_height = 0
      
    def openImages(self):
        #load pixels
        self.GT_pixel_map = Image.open(self.GT_image).load()
        self.org_pixel_map = Image.open(self.org_image).load()

        self.output_image = Image.open(self.org_image)
        self.output_pixel_map = self.output_image.load()

        print "GT ", self.GT_pixel_map[0,0]
        print "Org ", self.org_pixel_map[0,0]

        self.image_width, self.image_height = Image.open(self.GT_image).size



    def get_village_pixels(self):
        #select only village pixels for the clustering
        for i in range(self.image_width):
            for j in range(self.image_height):
               
                #match with exact white pixel
                if calcDistance(self.GT_pixel_map[i,j], self.GT_pixel_map[16,33]) == 0.0: 


                    if (self.org_pixel_map[i,j][0]-53)<10.0 and (self.org_pixel_map[i,j][1] - 53)<10.0:
                        print "catched ", self.org_pixel_map[i,j], i, j

                    elif (self.org_pixel_map[i,j][0]-76)<10.0 and (self.org_pixel_map[i,j][1] - 76)<10.0:
                        print "catched ", self.org_pixel_map[i,j], i, j
                    else:
                        #get the original image village pixel values
                        self.village_pixels.append(self.org_pixel_map[i,j])
                        #get the village village pixel locations
                        self.village_pixel_location.append((i,j))

                else:
                    self.non_village_pixels.append(self.org_pixel_map[i,j])

        return self.village_pixels, self.non_village_pixels



    def run_fcm(self):
        f = FCM.FCM(self.village_pixels)
        centroids = f.run()

        clusters = f.devidPixelsToClusters()

        for i in centroids:
            self.centroids.append(i)
       
        return self.centroids, clusters

    def showClustering(self, name):
        for idx, pixel in enumerate(self.village_pixels):
            shortest = float('Inf')
            for cluster in self.centroids:

                distance = calcDistance(cluster, pixel)

                if distance < shortest:
                    shortest = distance
                    nearest = cluster


            self.output_pixel_map[int(self.village_pixel_location[idx][0]), int(self.village_pixel_location[idx][1])] = (int(nearest[0]),int(nearest[1]),int(nearest[2]),255) 
           
        self.output_image.save(name)


class InitialBoundary(object):
    def __init__(self, image, centroids):
        self.org_image = image
        self.org_pixel_map = []
        self.centroids = centroids
        self.boundary = []
        self.init_boundary = []
        self.positive_sample = []

        self.output_image =  Image.open(self.org_image)
        self.output_map = self.output_image.load()
        self.new_cluster = [[] for i in range(5)] 

        self.image_width = 0
        self.image_height = 0



    def run(self):
        self.org_pixel_map = Image.open(self.org_image).load()
        self.image_width, self.image_height = Image.open(self.org_image).size

   
   #return lower and upper boundary of initial clusters
    def findBoundary(self, clusters, non_village_pixels):
        new_cluster = [[] for i in range(5)] 

        fig = plt.figure()

        #initialize color list
        colors = ["red", "green", "blue","orange", "purple", "pink" ,"DarkRed", "Salmon", "Violet", "Orchid"]

        #normalize the pixel features
        for idx in range(len(clusters)):
            print idx
            for i in clusters[idx]:
                #normalize features
                new_cluster[idx].append([i[0]/255.0, i[1]/255.0, i[2]/255.0])


        #display non-village pixels
        r_n = []
        g_n = []
        b_n = []
        for i in non_village_pixels:
            #normalize features
            r_n.append(i[0]/255.0)
            g_n.append(i[1]/255.0)
            b_n.append(i[2]/255.0)

        plt.scatter(r_n,g_n,edgecolors='none', color = "yellow")


        #DRAW rectangles
        currentAxis = plt.gca()

        x = 0
        for i in new_cluster:
            r = []
            g = []
            b = []
            for j in i:
                r.append(j[0])
                g.append(j[1])
                b.append(j[2])

            plt.scatter(r,g,edgecolors='none', color = colors[x])
            x = x+1

            #draw boxes
            #find out boarders of the boxes
            r.sort()
            g.sort()
            b.sort()

            currentAxis.add_patch(Rectangle((r[0], g[0]), (r[-1]- r[0]), (g[-1]- g[0]), fill=None, alpha=1))

            #un-normalized features for returning , lower boundary and upper boundary
            self.init_boundary.append(([r[0] * 255.0, g[0] * 255.0, b[0] * 255.0], [r[-1] * 255.0, g[-1]* 255.0, b[-1]* 255.0]))
           
        # pyplot.show()
        pyplot.savefig("plot.png")
        return self.init_boundary



    def getMajorityPixelsCount(self, boundary, non_village_pixels):
        # print boundary[0], boundary[1]
        count =0
        for j in non_village_pixels:
                if j[0] > boundary[0][0] and j[1] > boundary[0][1] and j[2] > boundary[0][2] and j[0] < boundary[1][0] and j[1] < boundary[1][1] and j[2] < boundary[1][2]:
                    count = count+1

        return count

    def newClusterBoundary(self, cluster_new, non_village_pixels, plt_name):

        new_boundary = []

        colors = ["red", "green", "blue","orange", "purple", "pink" ,"DarkRed", "Salmon", "Violet", "Orchid"]

        fig = plt.figure()

        
        #display non-village pixels
        r_n = []
        g_n = []
        b_n = []
        for i in non_village_pixels:
            r_n.append(i[0]/255.0)
            g_n.append(i[1]/255.0)
            b_n.append(i[2]/255.0)

        plt.scatter(r_n,g_n,edgecolors='none', color = "yellow")



        new_cluster = [[] for i in range(5)]

        for idx in range(len(cluster_new)):
            print idx
            for i in cluster_new[idx]:
                new_cluster[idx].append([i[0]/255.0, i[1]/255.0, i[2]/255.0])

        currentAxis = plt.gca()
        
        x = 0
        for i in new_cluster:
            r = []
            g = []
            b = []
            for j in i:
                r.append(j[0])
                g.append(j[1])
                b.append(j[2])

            plt.scatter(r,g,edgecolors='none', color = colors[x])
            x = x+1

            #draw boxes

            r.sort()
            g.sort()
            b.sort()

            currentAxis.add_patch(Rectangle((r[0], g[0]), (r[-1]- r[0]), (g[-1]- g[0]), fill=None, alpha=1))

            #un-normalized features for returning
            new_boundary.append(([r[0] * 255.0, g[0] * 255.0, b[0] * 255.0], [r[-1] * 255.0, g[-1]* 255.0, b[-1]* 255.0]))
          


        # pyplot.show()
        pyplot.savefig(plt_name)
        return new_boundary

    def output_boundary_based(self, boundary):
        for j in range(self.image_width):
            for k in range(self.image_height):
                for i in range(len(boundary)):

                    # print boundary[i][0]
                    if (self.output_map[j,k][0] > boundary[i][0][0] and self.output_map[j,k][0] < boundary[i][1][0]) and (self.output_map[j,k][1] > boundary[i][0][1] and self.output_map[j,k][1] < boundary[i][1][1]) and (self.output_map[j,k][2] > boundary[i][0][2] and self.output_map[j,k][2] < boundary[i][1][2]):  
                        
                        # print self.boundary[x], self.boundary[x+1], self.output_map[j,k]

                        self.output_map[j,k] = (255, 0, 0)
                       
                        
        self.output_image.show()










    def reset(self):
        self.boundary = []
        self.new_cluster = [[] for i in range(15)]


    

    def findOutMajorityPixels(self, non_village_pixels):

        non_village_pixel_count_clusters = []
        copy = []

        for i in range(len(self.boundary)/2):
            x = i * 2
            print self.boundary[x], self.boundary[x+1]

            count = 0

            for j in non_village_pixels:
                if j[0] > self.boundary[x][0] and j[1] > self.boundary[x][1] and j[2] > self.boundary[x][2] and j[0] < self.boundary[x+1][0] and j[1] < self.boundary[x+1][1] and j[2] < self.boundary[x+1][2]:
                    count = count+1

            non_village_pixel_count_clusters.append(count)
            copy.append(count)


        for i in non_village_pixel_count_clusters:
            print "pixel count", i

        #find out the max cluster
       
        non_village_pixel_count_clusters.sort()
        print non_village_pixel_count_clusters[-2], non_village_pixel_count_clusters[-1]

        number_1 = 0
        number_2 = 0
        number_3 = 0

        for i in range(len(non_village_pixel_count_clusters)):
            if non_village_pixel_count_clusters[-1]==copy[i]:
                number_1 = i

            if non_village_pixel_count_clusters[-2]==copy[i]:
                number_2 = i

            if non_village_pixel_count_clusters[-3]==copy[i]:
                number_3 = i

            
        print number_1, number_2
        #get relevant cluster

        return self.new_cluster[number_1], self.new_cluster[number_2], self.new_cluster[number_3], number_1, number_2, number_3

    def findMinimumBoundaryOverlapCluster(self, non_village_pixels):

        non_village_pixel_count_clusters = []
        copy = []

        for i in range(len(self.boundary)/2):
            x = i * 2
            print self.boundary[x], self.boundary[x+1]

            count = 0

            for j in non_village_pixels:
                if j[0] > self.boundary[x][0] and j[1] > self.boundary[x][1] and j[2] > self.boundary[x][2] and j[0] < self.boundary[x+1][0] and j[1] < self.boundary[x+1][1] and j[2] < self.boundary[x+1][2]:
                    count = count+1

            non_village_pixel_count_clusters.append(count)
            copy.append(count)


        for i in non_village_pixel_count_clusters:
            print "pixel count", i

        #find out the max cluster
       
        non_village_pixel_count_clusters.sort()
        print non_village_pixel_count_clusters[-2], non_village_pixel_count_clusters[-1]

        number_1 = 0
        number_2 = 0
        number_3 = 0
        number_4 = 0
        

        for i in range(len(non_village_pixel_count_clusters)):
            if non_village_pixel_count_clusters[0]==copy[i]:
                number_1 = i
            elif non_village_pixel_count_clusters[1]==copy[i]:
                number_2 = i
            elif non_village_pixel_count_clusters[2]==copy[i]:
                number_3 = i
            elif non_village_pixel_count_clusters[3]==copy[i]:
                number_3 = i

         
            
        print number_1, 
        #get relevant cluster

        return number_1, number_2, number_3, number_4


    def output(self, selected_cluster_no):

        # print "output start -------------########################################"

        village = 0
        non_village = 0

        

        for j in range(self.image_width):
            for k in range(self.image_height):
                not_village_pixel = True
                for i in range(len(self.boundary)/2):
                    x = 0
                    x = i * 2

                    status = False
                    for no in selected_cluster_no:
                        # print "no ", no, x, len(self.boundary)
                        if x != no and (x+1) != no:
                            # print "************************* ", x
                            status = True


                    if status:
                        # print x, x+1, len(self.boundary), len(self.boundary)/2
                        if (self.output_map[j,k][0] > self.boundary[x][0] and self.output_map[j,k][0] < self.boundary[x+1][0]) and (self.output_map[j,k][1] > self.boundary[x][1] and self.output_map[j,k][1] < self.boundary[x+1][1]) and (self.output_map[j,k][2] > self.boundary[x][2] and self.output_map[j,k][2] < self.boundary[x+1][2]):  
                                # print self.boundary[x], self.boundary[x+1], self.output_map[j,k]

                            self.output_map[j,k] = (255, 0, 0)
                            village=village+1
                            not_village_pixel = False
                            break

                if not_village_pixel:
                    non_village = non_village+1

     

       
        self.output_image.show()

    def minimumOverlapOutpu(self, selected_cluster_no):

        # print "output start -------------########################################"

        village = 0
        non_village = 0

        

        for j in range(self.image_width):
            for k in range(self.image_height):
                not_village_pixel = True

                for i in selected_cluster_no:
                    x = i * 2

                        # print x, x+1, len(self.boundary), len(self.boundary)/2
                    if (self.output_map[j,k][0] > self.boundary[x][0] and self.output_map[j,k][0] < self.boundary[x+1][0]) and (self.output_map[j,k][1] > self.boundary[x][1] and self.output_map[j,k][1] < self.boundary[x+1][1]) and (self.output_map[j,k][2] > self.boundary[x][2] and self.output_map[j,k][2] < self.boundary[x+1][2]):  
                                    # print self.boundary[x], self.boundary[x+1], self.output_map[j,k]

                        self.output_map[j,k] = (255, 0, 0)
                        village=village+1
                        not_village_pixel = False
                        break

                if not_village_pixel:
                    non_village = non_village+1

       
        self.output_image.show()

            




if __name__ == "__main__":

    #training
    c = Initial_Clustering("T6.png", "GT_T6.png")
    c.openImages()
    village_pixels, non_village_pixels = c.get_village_pixels()

    #initially run FCM to devide clusters
    centroids, clusters= c.run_fcm()


    #find initial boundary of the initial clusters
    initial = InitialBoundary("T7.png", centroids)
    initial.run()
    boundary = initial.findBoundary(clusters , non_village_pixels)

    threshold = 50

    maj_pix = []
    updated_boundary = []

    for i in range(len(boundary)):
        #get the majority pixel count in the boundary
        majority_pixel_count = initial.getMajorityPixelsCount(boundary[i], non_village_pixels)
        
        print majority_pixel_count
        maj_pix.append(majority_pixel_count)

        #check if it is in the threshold

        if majority_pixel_count<threshold:
            print "less ", i
            updated_boundary.append(boundary[i])
        else:
            #run FCM for particular cluster
            

            if len(clusters[i]) > 5:
                f = FCM.FCM(clusters[i])
                centroids = f.run()
                clusters_updated = f.devidPixelsToClusters()

                #get the updated boundary
                updated_boundary_fcm = initial.newClusterBoundary(clusters_updated , non_village_pixels, "1.png")

                for j in range(len(updated_boundary_fcm)):
                    update_majority_pixel_count = initial.getMajorityPixelsCount(updated_boundary_fcm[j], non_village_pixels)

                    maj_pix.append(update_majority_pixel_count)

                    
                    if update_majority_pixel_count<threshold:
                        updated_boundary.append(updated_boundary_fcm[j])
                    else:
                        if len(clusters_updated[i]) > 5:
                            print "starting FCM for ", i
                            f2 = FCM.FCM(clusters_updated[i])
                            centroids = f2.run()
                            clusters_updated_2 = f2.devidPixelsToClusters()

                            #get the updated boundary
                            updated_boundary_fcm_2 = initial.newClusterBoundary(clusters_updated_2 , non_village_pixels, "1.png")

                            for x in range(len(updated_boundary_fcm_2)):
                                update_majority_pixel_count_2 = initial.getMajorityPixelsCount(updated_boundary_fcm_2[x], non_village_pixels)

                                maj_pix.append(update_majority_pixel_count_2)

                                print majority_pixel_count
                                if update_majority_pixel_count_2<threshold:
                                    updated_boundary.append(updated_boundary_fcm_2[x])


    for i in updated_boundary:
       print "updated_boundary", i

    # for i in maj_pix:
    #     print i

    initial.output_boundary_based(updated_boundary)

 