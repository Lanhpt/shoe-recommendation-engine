#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:06:50 2019

@author: griggles
"""


import pandas as pd
import mat4py


class Munger():
    
    def __init__(self, feature_vector_path='data/4096_vals.csv', dir_data='data/ut-zap50k-data/', dir_imgs='data/ut-zap50k-images/', 
                 file_meta='meta-data.csv', file_img_paths='image-path.mat'):
        self.dir_imgs = dir_imgs
        self.dir_data = dir_data
        self.file_meta = file_meta
        self.file_img_paths=file_img_paths
        
        self.feature_vector_path=feature_vector_path
        
        
        
    def _build_meta_df(self):
        df = pd.read_csv(self.dir_data + self.file_meta)
        df.index = df['CID']
        self.df = df
        
    def _adhoc_corrections(self, string):
        string = string.replace('/T.U.K./', '/T.U.K/')
        string = string.replace('/Neil M./', '/Neil M/')
        string = string.replace('/Aquatalia by Marvin K./', '/Aquatalia by Marvin K/')
        string = string.replace("/Levi's Shoes/", "/Levi's&#174; Shoes/")
        string = string.replace("/Levi's Kids/", "/Levi's&#174; Kids/")
        string = string.replace('/W.A.G./', '/W.A.G/')
        string = string.replace('/L.A.M.B./', '/L.A.M.B/')
        return string

    
    def _append_img_paths(self):
        img_paths = mat4py.loadmat(self.dir_data + self.file_img_paths)
        img_paths = list(map(lambda x: self.dir_imgs + x[0], img_paths['imagepath']))
        self.df['img_path'] = img_paths
        self.df['img_path'] = self.df['img_path'].apply(self._adhoc_corrections)
        
        #remove this random one that doesn't appear in files
        self.df = self.df[~self.df['img_path'].str.contains("/Pablosky Kids/")]
        
    def munge(self):
        print('Returning meta_data dataframe followed by feature_space_dataframe for ', self.feature_vector_path)
        self._build_meta_df()
        self._append_img_paths()
        feature_df = pd.read_csv(self.feature_vector_path, index_col='CID')
        return self.df, feature_df
        
        
        
    

        
    
        