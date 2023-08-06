# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2021

@author: Scott Mutchler
'''
import folium
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import json
from math import radians, cos, sin, asin, sqrt
from folium import plugins
from folium.features import DivIcon

def type_check(variable: object, interested_type: object):
    """
    Generic function that will allow us to check the types of variables
    being passed to other functions to ensure nothing weird is going to happen
    due to variable types

    Parameters
    ----------
    variable : object
        variable name of interest
    interested_type : object
        the type of object you want to be sure the variable is

    Raises
    ------
    TypeError
        if the variable type and the interested_type type do not match, this
        error is thrown that shows the type that is expected and the type that
        is actually passed

    Returns
    -------
    None.

    """
    if not isinstance(variable, interested_type):
        raise TypeError('Expected {0}; got {1}'.format(str(interested_type.__name__), 
                                                       str(type(variable).__name__)))
    else:
        pass

class CenterOfGravityModel(object):
    '''
    Center of Gravity Model - Essentially weighted k-means for lat/long 
    '''
    
    def __init__(self, options: dict):
      """
      Initiation function
      """
      type_check(options, dict)
      self.options = options
        # store models after training for later scoring
      self.models = dict()
      print("Using options:")
      print(options)
        
    
    def train(self, frame: pd.DataFrame) -> pd.DataFrame:
      """
      Calls trainSingleFrame function on each split specified in the options['splitCol'] column
      """
      type_check(frame, pd.DataFrame)
      
      assert (self.options['latCol'] in frame.columns) , "latCol not found in frame columns"
      assert (self.options['lonCol'] in frame.columns) , "lonCol not found in frame columns"
      assert (self.options['splitCol'] in frame.columns) , "splotCol not found in frame columns"
      assert (self.options['weightCol'] in frame.columns) , "weightCol not found in frame columns"
      
      self.models = dict()
        
      frames = list(frame.groupby(by=self.options['splitCol']))

      for frame in frames:
          frame = frame[1]
          frame.reset_index(drop=True, inplace=True)
          self.trainSingleFrame(frame)
      return 
        
    
    
    def trainSingleFrame(self, frame: pd.DataFrame) -> pd.DataFrame:
      """
      Runs a kmeans model and assigns it to the value in the self.models dictionary
      under the key that corresponds to the scenario name
      """
      type_check(frame, pd.DataFrame)
      splitVal = frame[self.options['splitCol']][0]
      print('Training split: ', splitVal)
        
      xcols = [self.options['latCol'], self.options['lonCol']]
      x = frame[xcols]
      weights = frame[self.options['weightCol']]
      kmeans = KMeans(n_clusters=self.options['numClusters'], random_state=self.options['randomSeed']).fit(x, sample_weight=weights)
        
      self.models[splitVal] = kmeans
      
      return 
    
    def score(self, frame: pd.DataFrame) -> pd.DataFrame:
      """
      Calls scoreSingleFrame for each scenarios specififed in the options['splitCol'] column
      """
      type_check(frame, pd.DataFrame)
      frames = list(frame.groupby(by=self.options['splitCol']))
        
      outputFrame = None
      for frame in frames:
          frame = frame[1]
          frame.reset_index(drop=True, inplace=True)
          frame = self.scoreSingleFrame(frame)
          outputFrame = frame if outputFrame is None else outputFrame.append(frame, ignore_index=True)
        
      return outputFrame
    
    def haversine(self, lat1:float, lon1:float, lat2:float, lon2:float) -> float:
      """
      Haversine function, returns distance in miles
      """
      type_check(lat1, float)
      type_check(lon1, float)
      type_check(lat2, float)
      type_check(lon2, float)
      R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km
        
      dLat = radians(lat2 - lat1)
      dLon = radians(lon2 - lon1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)
        
      a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
      c = 2*asin(sqrt(a))
        
      return R * c
    
    def scoreSingleFrame(self, frame: pd.DataFrame) -> pd.DataFrame:
      """
      Assigns clusters and identifies centroids of each cluster via the kmeans algorithm
      """
      type_check(frame, pd.DataFrame)
      splitVal = frame[self.options['splitCol']][0]
      print('Scoring split: ', splitVal)
        
      xcols = [self.options['latCol'], self.options['lonCol']]
      x = frame[xcols]
      weights = frame[self.options['weightCol']]
      kmeans = self.models[splitVal]
        
      frame[self.options['clusterAssignmentCol']] = kmeans.predict(x, sample_weight=weights)
      frame[self.options['centroidsCol']] = json.dumps(kmeans.cluster_centers_.tolist())
        
      haversineDistances = list()
      for index, row in frame.iterrows():
          centroid = kmeans.cluster_centers_.tolist()[row[self.options['clusterAssignmentCol']]]
          dist = self.haversine(row[self.options['latCol']], row[self.options['lonCol']], centroid[0], centroid[1])
          haversineDistances.append(dist)
        
      frame[self.options['distanceCol']] = haversineDistances
        
      return frame
  
def createMap(data: pd.DataFrame, options: dict) -> folium.Map():
    """
    Creates a folium map with all of the layers present in the CenterOfGravityModel output dataframe
    
    Parameters
    ----------------------------------------------
    data
    
    A pandas dataframe of the form produced by the CenterOfGravityModel class (see examples)
    
    Outputs
    ----------------------------------------------
    Outputs a folium map with all the layers outlined in the the CenterOfGravityModel output
    
    """
    type_check(data, pd.DataFrame)
    type_check(options, dict)
    the_map = folium.Map(location=data[[options['latCol'], options['lonCol']]].mean(),
               fit_bounds=[[data[options['latCol']].min(),
                            data[options['lonCol']].min()], 
                           [data[options['latCol']].max(),
                            data[options['lonCol']].max()]])
    
    scenarios = list(data[options['splitCol']].unique())
    
    for i in scenarios:
      x = folium.FeatureGroup(name= i + ' Heat Map')
      color_dict = {0: 'white', 1 : options['scenarioColors'][i]}
      #colormap = cm.linear.Blues_05.scale(z_min, z_max)
      #colors = cm.LinearColormap(colors=['red','lightblue'])#, index=[90,100],vmin=90,vmax=100)
      scenario_data = data[data[options['splitCol']] == i].copy()
      heat_data = scenario_data[[options['latCol'],options['lonCol'],options['weightCol']]].copy()
      
      hm = plugins.HeatMap(heat_data, min_opacity=0.4, gradient = color_dict)#, gradient = options['scenarioColors'][i])
      hm.add_to(x)
      x.add_to(the_map)                                   
    
    for i in scenarios:
        x = folium.FeatureGroup(name = i)
        
        scenario_data = data[data[options['splitCol']] == i].copy()
        
        for _, row in scenario_data.iterrows():
                        folium.CircleMarker(location=[row[options['latCol']], 
                                  row[options['lonCol']]],
                        radius=(25*(row[options['weightCol']]-scenario_data[options['weightCol']].mean())/(scenario_data[options['weightCol']].max() - scenario_data[options['weightCol']].min())),
                        #radius = (row[options['weightCol']] ** 0.6),
                        fill_color=options['scenarioColors'][i],
                        fill_opacity=0.6,
                        color = False,
                        tooltip=str(row[options['label']])+' '+str(row[options['splitCol']]) + ' ' + str(row[options['weightCol']])).add_to(x)
                
        x.add_to(the_map)
                
    for i in scenarios:
        clusters = list(data[data[options['splitCol']] == i]['X_CLUSTER'].unique())
        
        if len(clusters) == 1:
          pass
        else:
          for j in clusters:
              x = folium.FeatureGroup(name = i + "-cluster-" + str(j))
        
              scenario_data = data[data[options['splitCol']] == i].copy()
        
              for _, row in scenario_data.iterrows():
                          folium.CircleMarker(location=[row[options['latCol']], 
                                    row[options['lonCol']]],
                          radius=(25*(row[options['weightCol']]-scenario_data[options['weightCol']].mean())/(scenario_data[options['weightCol']].max() - scenario_data[options['weightCol']].min())),
                          #radius = (row[options['weightCol']] ** 0.6),
                          fill_color=options['scenarioColors'][i],
                          fill_opacity=0.6,
                          color = False,
                          tooltip=str(row[options['label']])+' '+str(row[options['splitCol']]) + ' ' + str(row[options['weightCol']])).add_to(x)
                
              x.add_to(the_map)
            
    for i in scenarios:
        x = folium.FeatureGroup(name = i + "-centroids")
        
        scenario_data = data[data[options['splitCol']] == i].reset_index().copy()
        
        centroids = json.loads(scenario_data['X_CENTROIDS'][0])
        
        for j in centroids:
            folium.CircleMarker(location=[float(j[0]), float(j[1])],
                               radius = 13,
                               #fill_color = options['scenarioColors'][i],
                               fill_color = options['centroidOptions'][i]['color'],
                               color = False,
                               fill_opacity = 1).add_to(x)
            
            
            #this text is for eventually adding labels to the centroids
            text = options['centroidOptions'][i]['text']
            
            folium.map.Marker(
                [j[0] + 0.1, j[1] + 0.3],
                icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html='<div style="font-size: 16pt">%s</div>' % text,
                
                  )).add_to(x)
            
        x.add_to(the_map)
        
    
      
      
    control = folium.LayerControl()
    control.add_to(the_map)
    
    return the_map

def populateMapOptions(options:dict, map_options:dict, data: pd.DataFrame) -> dict:
  """
  This function automatically populates the scenarioColors and centroidOptions values of the options dictionary to be passed to the createMap function
  
  Input
  -------------------------------------------
  Options dictionary of the form to be passed to the createMap function (see example)
  
  Options dictionary of the form to be passed to the CenterOfGravityModel (see example)
  
  Pandas dataframe of the type produced by the CenterOfGravityModel class (see example)
  
  Output
  -------------------------------------------
  Options dictionary of the form to be passed to the createMap function, but with
  the scenarioColors and centroidOptions values populated automatically with defaults
  """
  type_check(options, dict)
  type_check(map_options, dict)
  type_check(data, pd.DataFrame)
  scenarios = list(data[options['splitCol']])
  scenColors = {}
  colors = list(['red', 'green', 'blue', 'black', 'orange'])
  counter = 0
  for i in scenarios:
    scenColors[i] = colors[counter%5]
    counter = counter + 1
  
  map_options['scenarioColors'] = scenColors
  
  centroidOptions = {}
  for i in scenarios:
    x = {'color': 'black', 'text':i} #once reverse geocoding comes online we will use it in the createMap function to replace the null value under the text key
    centroidOptions[i] = x
  
  map_options['centroidOptions'] = centroidOptions
  
  return map_options