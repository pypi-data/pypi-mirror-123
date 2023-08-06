#From the paper:
#Evolutionary Clustering and Community Detection Algorithms for Social Media Health Surveillance
#Heba Elgazzar, Kyle Spurlock, Tanner Bogart
#2020

import numpy as np
#Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 0.1038/s41586-020-2649-2. (Publisher link).
import matplotlib.pyplot as plt
#Hunter, J. D. (2007). Matplotlib: a 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95. doi:10.1109/mcse.2007.55.
from sklearn.metrics import pairwise_distances
#Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., . . . Duchesnay, E. (2011). Scikit-learn: machine learning in python (M. Braun, Ed.). The Journal of Machine Learning Research, 12, 2825-2830. Retrieved November 16, 2020, from jmlr.org.
import community as community_louvain
#Aynaud, T. (2020). python-louvain x.y: Louvain algorithm for community detection. GitHub. https://github.com/taynaud/python-louvain.
import networkx as nx
#Hagberg, A., Swart, P., & S Chult, D. (2008, August). Exploring network structure, dynamics, and function using networkx. Proceedings of the 7th Python in Science Conference, 11-16. Retrieved November 16, 2020, from www.osti.gov.

class EvoLouvain:
    def __init__(self): #constructor
        self.current_time = 0 #the current generation step of the class
        self.previous_gen = [] #holds the previous generations distance matrix
        self.modularities = [] #Modularities per timesteps
        self.times = []
        
    def showPlot(self, current_gen, partition, modularity, alpha): #Displays the plots of the clustered generation
        plt.scatter(current_gen[:,0], current_gen[:,1], c = list(partition.values()), cmap = 'tab20') #(x, y, cluster_ labels, colour_map for clusters)
        title = r'Louvain Generation-{g} Alpha-{a} Modularity-{m}'.format(g = self.current_time, a = alpha, m = "%.5f" % modularity)
        plt.title(title)
        plt.savefig('{t}.png'.format(t = title))
        plt.show() #Show the graph
    
    def applySmoothing(mat1, mat2, alpha): #Adding two matrices
        mat1, mat2 = (1-alpha)*mat1, alpha*mat2
        ysize, xsize = mat2.shape #Get inverse of shape of second matrix
        mat1[0:ysize, 0:xsize] += mat2 #Add elements of mat2 to mat1 on index (0,0)
        return mat1
    
    def callLouvain(self, X, t_intervals, alpha, show_mod = False): #member function that performs the evolutionary clustering
        seen_times = [] #these are the time steps we have currently moved through
        for time in t_intervals: #For each time step in our unique times
            self.current_time = time #Set the class time to this time
            seen_times.append(time) #Add the current_time to our already viewed times
            
            current_gen = X.loc[X['Time'].isin(seen_times)] #Check which values in our data match the current time step
            current_gen = current_gen.iloc[:,[0,1]].values #Convert the dataframe with the time column into a 2-D array with the coordinate points
            
            dist_cg = pairwise_distances(current_gen) #Calculate the distance matrix of our coordinate points using pairwise distance
            dist_cg = EvoLouvain.convert_matrix(dist_cg) #Remove distant links
            
            if time == 0: #If we are at the first step, there is no previous generation to consider
                dist_cg = dist_cg #Otherwise take distance matrix as normal
            else: #If we are past the first time step, there is a previous generation we must consider
                #dist_cg = EvoLouvain.addAtPos(((1-alpha)*dist_cg), ((alpha)*self.previous_gen))
                dist_cg = EvoLouvain.applySmoothing(dist_cg, self.previous_gen, alpha)
            
            G = nx.from_numpy_matrix(dist_cg) #Get NetworkX graph
            partition = community_louvain.best_partition(G)#Find the best partition at time step
            
            modularity = 0
            try:
                modularity = community_louvain.modularity(partition, G) #Retrieve modularities
            except(ValueError):
                print("Can't compute modularity for this partition.")
            
            if (show_mod):
                print('Generation {g} modularity: {m}'.format(g = self.current_time, m = modularity))

            self.modularities.append(modularity) #Store these for possible visualization later
            self.times = seen_times
            
            self.previous_gen = dist_cg #Set the current generations distance matrix to the previous gen since we have passed it

            if time in [100, int(np.median(t_intervals)), t_intervals[-1]]: #If the time has either started, is in the middle, or at the end:
                EvoLouvain.showPlot(self, current_gen, partition, modularity, alpha) #Take our current gen coordinates and the predicted labels and plot them
    
    def convert_matrix(dist): #Introducing sparsity into distance matrix, loose similarity
        dist[(dist < 10) & (dist != 0)] = 3
        dist[(dist > 10) & (dist < 20)] = 2
        dist[(dist > 20) & (dist < 30)] = 1
        dist[dist > 30] = 0
        return dist