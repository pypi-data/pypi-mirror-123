#From the paper:
#Evolutionary Clustering and Community Detection Algorithms for Social Media Health Surveillance
#Heba Elgazzar, Kyle Spurlock, Tanner Bogart
#2020

import numpy as np
#Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 0.1038/s41586-020-2649-2. (Publisher link).
import matplotlib.pyplot as plt
#Hunter, J. D. (2007). Matplotlib: a 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95. doi:10.1109/mcse.2007.55.
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances
#Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., . . . Duchesnay, E. (2011). Scikit-learn: machine learning in python (M. Braun, Ed.). The Journal of Machine Learning Research, 12, 2825-2830. Retrieved November 16, 2020, from jmlr.org.

class EvoDBSCAN:
    def __init__(self):
        self.current_time = 0 #The current generation step of the class
        self.previous_gen = [] #Holds the previous generations distance matrix
        self.clusters = [] #Number of clusters
        self.noise = [] #Number of noise points
    
    def showPlot(self, current_gen, labels, noise, alpha): #Displays the plots of the clustered generation
        plt.scatter(current_gen[:, 0], current_gen[:, 1], c = labels, cmap = 'tab20') #(x, y, cluster_labels, colour_map for clusters)
        plt.scatter(current_gen[labels == -1, 0], current_gen[labels == -1 , 1], c = 'black') #Plot noise
        title = 'EvoDBSCANv1 Generation-{t} Alpha-{a} Noise-{n}'.format(t = self.current_time, a = alpha, n = noise)
        plt.title(title) #Title of the graph, displays the current generation step
        plt.savefig('{t}.png'.format(t = title))
        plt.show() #Show the graph
    
    def callDBSCAN(self, X, t_intervals, alpha, beta, show_eps = False): #Member function that performs the evolutionary clustering
        seen_times = [] #These are the time steps we have currently moved through
        
        for time in t_intervals: #For each time step in our unique times
            eps = 0 #Initialize epsilon (radius measure)
            
            self.current_time = time #Set the class time to this time
            seen_times.append(time) #Add the current_time to our already viewed times
            
            current_gen = X.loc[X['Time'].isin(seen_times)] #Check which values in our data match the current time step
            current_gen = current_gen.iloc[:,[0,1]].values #Convert the dataframe with the time column into a 2-D array with the coordinate points 
            
            dist_cg = pairwise_distances(current_gen) #Calculate the distance matrix of our coordinate points using pairwise distance
            
            if time == 0: #If we are at the first step, there is no previous generation to consider for our epsilon value
                if len(current_gen < 2): #If there is only one sample at first gen, median will be 0 since distance will be 0
                    eps = 1e-5 #Small value to avoid skewing radius
                else:
                    eps = ((np.median(np.unique(dist_cg))/beta)) #Find the median distance in the list of unique distances and divide it by 10
            else: #If we are past the first time step, there is a previous generation we must consider
                eps = ((1-alpha)*np.median(np.unique(dist_cg)))/beta + (alpha*np.median(np.unique(self.previous_gen)))/beta #Calculate the epsilon using both the current median unique distance, as well as the previous generation's distance
            
            if show_eps:
                print('Generation {g} epsilon: {e}'.format(g = self.current_time, e = eps))
            
            dbscan = DBSCAN(eps, min_samples = 2) #Create the dbscan object
            labels = dbscan.fit_predict(current_gen) #Find the cluster labels of our current generation
            noise = list(labels).count(-1)
            
            self.clusters.append(len(set(labels)) - (1 if -1 in labels else 0))
            self.noise.append(noise)
            
            self.previous_gen = dist_cg #Set the current generations distance matrix to the previous gen since we have passed it
            
            if time in [100, int(np.median(t_intervals)), t_intervals[-1]]: #If the time has either started, is in the middle, or at the end:
                EvoDBSCAN.showPlot(self, current_gen, labels, noise, alpha) #Take our current gen coordinates and the predicted labels and plot them

    def callSTATIC(self, X, beta): #Normal DBSCAN where epsilon is static and points are taken at once
        X = X.iloc[:,[0,1]].values
        dist_cg = pairwise_distances(X)
        eps = np.median(np.unique(dist_cg))/beta
        
        dbscan = DBSCAN(eps, min_samples = 2)
        labels = dbscan.fit_predict(X) #Find the cluster labels of our current generation
        self.clusters = len(set(labels)) - (1 if -1 in labels else 0)
        self.noise = list(labels).count(-1)
        
        #Plotting
        plt.scatter(X[:,0], X[:,1], c = labels, cmap = 'tab20') #(x, y, cluster_labels, colour_map for clusters)
        plt.scatter(X[labels == -1, 0], X[labels == -1 , 1], c = 'black') #Plot noise
        title = 'Full Static EvoDBSCANv1 Noise-{n}'.format(n = self.noise)
        plt.title(title)
        plt.savefig('{t}.png'.format(t = title))
        plt.show()