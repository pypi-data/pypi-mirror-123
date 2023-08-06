#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#packages environment
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import error, spaces, utils
#from gym.utils import seeding
#import statsmodels.api as sm
#import statsmodels.formula.api as smf
import pandas.testing as tm
import math
from sklearn.linear_model import LogisticRegression
from scipy.stats import truncnorm

#Gym environment - continuous

class UpdateEnv1(gym.Env):
  def __init__(self):
    self.size = 2000
    #get initial values for theta's
    #fit logit model to data
    self.df = pd.DataFrame(dict(
            Xs=truncnorm.rvs(a=0,b=math.inf,size=self.size),
            Xa=truncnorm.rvs(a=0,b=math.inf,size=self.size),
            Y=np.random.binomial(1, 0.2, self.size)))
    self.model = LogisticRegression(fit_intercept=False).fit(self.df[["Xs", "Xa"]], np.ravel(self.df[["Y"]]))

    #extract theta parameters from the fitted logistic
    self.thetas = np.array([self.model.coef_[0,0] , self.model.coef_[0,1]]) #thetas[0] coef for Xs, thetas[1] coef for Xa

    #set range for obs space
    #? not all values should be equaly likely to be sampled, this is missing here
    #? can I restrict the sampling space when an episode is run?
    self.minXa1 = pd.to_numeric(min(self.df[["Xa"]].values.flatten()))
    self.minXs1 = pd.to_numeric(min(self.df[["Xs"]].values.flatten()))
    
    self.maxXa1 = pd.to_numeric(max(self.df[["Xa"]].values.flatten()))
    self.maxXs1 = pd.to_numeric(max(self.df[["Xs"]].values.flatten()))
    
    self.min_Xas=np.array([np.float32(self.minXa1), np.float32(self.minXs1)])
    self.max_Xas=np.array([np.float32(self.maxXa1), np.float32(self.maxXs1)])


    #set range for action space
    self.high_th = np.array([4, 4])
   
    #set ACTION SPACE
    #space.box handles continuous action space
    #it needs values for the bounds and the shape: low, high, shape (as in a tensor)
    #the bounds for a logit transformation of X's are 0, 1 (or min and max of the logit transform with initial values for theta)
    self.action_space = spaces.Box(
            low = np.float32(-self.high_th),
            high = np.float32(self.high_th))
    
    #set OBSERVATION SPACE
    #it is made of values for Xa, Xs for each observation
    self.observation_space = spaces.Box(low=self.min_Xas, 
                                   high=self.max_Xas, 
                                   dtype=np.float32)
    
    #set an initial state
    self.state=None 

    #introduce some length
    self.horizon=200
 

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]    

#take an action with the environment
#it returns the next observation, the immediate reward, whether the episode is over (done) and additional information    
#"action" argument is one value in the range of the action space (logit transform)
  def step(self, action):

    #theta0, theta1 = action    
        
    patients1= self.patients #shape (50, 2), 1st column Xs, 2nd column Xa
    rho1 = (1/(1+np.exp(-(np.matmul(patients1, action[:, None])))))  #prob of Y=1  # (sizex2) x (2x1) = (size, 1)
    rho1 = rho1.squeeze() # shape: size, individual risk
    Xa = patients1[:, 1] # shape: size
    g2 = ((Xa) + 0.5*((Xa)+np.sqrt(1+(Xa)**2)))*(1-rho1**2) + ((Xa) - 0.5*((Xa)+np.sqrt(1+(Xa)**2)))*(rho1**2)
    Xa = g2 # 50
    
    #calculate reward
    #get new coefficients given the covariate Xa has changed by running logit 
    Y = np.random.binomial(1, 0.2, (self.size, 1))
    patients2 = np.hstack([Y, np.reshape(patients1[:, 0], (self.size,1)), np.reshape(Xa, (self.size,1))]) #Y, Xs, Xa
    #run logit model to get coefficients, because their risk has changed (or use acitons to get risk using just new Xa??)
    model2 = LogisticRegression(fit_intercept=False).fit(patients2[:, 1:3], np.ravel(patients2[:, 0].astype(int)))
    thetas2 = np.array([model2.coef_[0,0] , model2.coef_[0,1]]) #thetas2[0]: coef for Xs, thetas2[1] coef for Xa
    
    patients3 = patients2[:, 1:3]
    rho3 = (1/(1+np.exp(-(np.matmul(patients3, thetas2[:, None])))))  #prob of Y=1 # (sizex3) x (3x1) = (size, 1)
    rho3 = rho3.squeeze() # shape: size, individual risk
    
    #transform rho3 in a list to print individual risk (and not just mean risk of the hospitak's patient)
    rho3_list = rho3.tolist()
    self.mean_r = np.mean(rho3)
    
    #check if horizon is over, otherwise keep on going
    if self.horizon <= 0:
      done = True
    else:
      done = False
    #set the reward equal to the mean hospitalization rate
    reward = self.mean_r 
        
    self.state = self.patients[self.random_indices, :].reshape(2,) #not sure if with or without reshape
    
    #without action - simple logit on inital (non-intervened) dataset with Y, old Xa, Xs
    patients4 = np.hstack([Y, self.patients]) #shape (50, 3), 1st column of Y, 2nd columns Xs, 3rd column Xa
    model4 = LogisticRegression(fit_intercept=False).fit(patients4[:, 1:3], np.ravel(patients4[:, 0].astype(int)))
    thetas4 = np.array([model4.coef_[0,0] , model4.coef_[0,1]]) #thetas4[0]: coef for Xs, thetas4[1] coef for Xa
    rho4 = (1/(1+np.exp(-(np.matmul(patients1, thetas4[:, None])))))  #prob of Y=1  #(sizex3) x (3x1) = (size, 1) #use patients1 because it's fine, it has self.patients
    rho4 = rho4.squeeze() # shape: size, individual risk
    rho4_list = rho4.tolist()
    reward4 = np.mean(rho4)
 
    
    #reduce the horizon
    self.horizon -= 1
    
    #set placeholder for infos
    info ={}    
    return self.state, reward,  reward4, thetas4, done, {}

#reset state and horizon    
  def reset(self):
    self.horizon = 200
    
    #define dataset of patients with actionable covariate Xa and non-actionable covariate Xs
    self.patients = truncnorm.rvs(a=0, b= math.inf,size=(self.size,2)) #shape (size, 2), 1st columns is Xs, second is Xa
    
       
    self.random_indices = np.random.choice(self.size, size=1, replace=False)
    self.state = self.patients[self.random_indices, :].reshape(2,) #not sure if with or without reshape

    
    
    return self.state

