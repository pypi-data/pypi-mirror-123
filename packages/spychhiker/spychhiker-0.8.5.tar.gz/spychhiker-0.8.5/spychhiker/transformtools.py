#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 07:54:59 2020

@author: benjamin
"""

import numpy as np
import numpy.matlib
import scipy.signal
import statsmodels.api as sm
import h5py
from sklearn import linear_model
from .prosody import Contour
from .ola import *

def findelements(a, b):
    # find indices of elements in a that contains elements in b
    nB = len(b)
    idx = []
    
    for k in range(nB):
        bTmp = b[k]
        idxTmp = [i for i,x in enumerate(a) if x==bTmp]
        if idxTmp != []: 
            if idx == []:
                idx = idxTmp
            else:
                idx = np.concatenate((idx, idxTmp)).astype(int)
                
    return idx

def get_distribution_from_keys(f, key):
    
    y = f[key][()]
    pdf = []
    pdf_bins = []
    
    if len(y) == 3:
        y = y[0]
    
    if len(y) == 4:    
        for k in y:
            pdfTmp, bins_tmp = np.histogram(k, 25, density=True)
            pdf.append(sm.nonparametric.lowess(pdfTmp, np.arange(25),
                                          frac=0.2,
                                          return_sorted=False))
            pdf_bins.append(bins_tmp)
    else:
        pdfTmp, bins_tmp = np.histogram(y, 25, density=True)
        pdf.append(sm.nonparametric.lowess(pdfTmp, np.arange(25),
                                      frac=0.2,
                                      return_sorted=False))
        pdf_bins.append(bins_tmp)
    return pdf, pdf_bins

def get_distribution_from_file(dist_file):    
    
    f = h5py.File(dist_file, 'r')
    a = dict.fromkeys(f.keys(), 0)
    for k in f.keys():        
        a[k] = get_distribution_from_keys(f, k)
        
    return a

def get_pros_modif_factor_from_dist(dist):
    fact_med = random_smpl(dist, 'med_pitch', lim=[0.5,2])
    fact_span = random_smpl(dist, 'span_pitch', lim=[0.25,3])
    fact_dur = random_smpl(dist, 'duration', lim=[1/1.8,1.8])
    return fact_med, fact_span, fact_dur

def parse_align_file(align_file):
    f = open(align_file, 'r', encoding='Latin 1')
    lines = f.readlines()
    keys = ['utterance_id', 'channel', 'start', 'dur', 'phone']
    rlist = {"utterance_id":[], "channel":[], "start":[], "dur":[], "phone":[]}
    
    for curr_line in lines:
        for ks, curr_split in enumerate(curr_line.split(' ')):
            rlist[keys[ks]].append(curr_split.replace('\n', ''))
    return rlist

def parse_txt_file(txt_file):
    f = open(txt_file, 'r', encoding='Latin 1')
    lines = f.readlines()
    utt_id = [x[:x.find(' ')] for x in lines]
    utt_txt = [x[x.find(' ') + 1:] for x in lines]
    return utt_id, utt_txt

def parse_rlist_file(rlist_file):
    f = open(rlist_file, 'r', encoding='Latin 1')
    lines = f.readlines()
    keys = ['speaker_id', 'utterance_id', 'path_to_utterance', 
            'channel', 'start', 'end']
    rlist = {"speaker_id":[], "utterance_id":[], "path_to_utterance":[], 
             "channel":[], "start":[], "end":[]}
    
    for curr_line in lines:
        for ks, curr_split in enumerate(curr_line.split(' ')):
            rlist[keys[ks]].append(curr_split.replace('\n', ''))
    return rlist

def parse_slist_file(slist_file):
    f = open(slist_file, 'r', encoding='Latin 1')
    lines = f.readlines()
    keys = ['speaker_id', 'utterance_id', 'path_to_utterance', 
            'path_to_segmentation']
    slist = {"speaker_id":[], "utterance_id":[], "path_to_utterance":[], 
             "path_to_segmentation":[]}
    
    for curr_line in lines:
        for ks, curr_split in enumerate(curr_line.split(' ')):
            slist[keys[ks]].append(curr_split.replace('\n', ''))
    return slist

def random_its(pdf, pdf_bins, N=1):
    
    x = np.linspace(min(pdf_bins[1:]), max(pdf_bins[1:]), 10000)
    f1 = scipy.interpolate.interp1d(pdf_bins[1:], pdf)
    y = f1(x)
    
    cdf = np.cumsum(y/sum(y))
    R = np.random.uniform(0, 1, N)
    return [x[np.argwhere(cdf == min(cdf[(cdf - r) > 0]))[0][0]] for r in R]

def random_smpl(dist, key, k=0, lim=None):
    
    pdf = dist[key][0][k]
    pdf_bins = dist[key][1][k]
      
    fact = random_its(pdf, pdf_bins, 1)[0]
    if lim is not None:
        while fact > lim[1] or fact < lim[0]:
            fact = random_its(pdf, pdf_bins, 1)[0]
    return fact

def read_dictionary_file(dict_file):
    
    f = h5py.File(dict_file, 'r')
    A_dict = f['dictionary'][()]
    phones = f['phonemes'][()]
    info = f["type"][()]
    
    return A_dict, phones, info

def read_spk_model(model):
    
    f = h5py.File(model, 'r')
    W_mask = f['mask_dict'][()]
    W_nominal = f['nominal_dict'][()]
    
    return W_nominal, W_mask

def sparse_transform(features, W_nominal, W_mask):    
    
    clf = linear_model.Lasso(alpha=1e-3, tol=1e-10, max_iter=100000,
                                 positive=True)    
    clf.fit(W_nominal, features)
    W = clf.coef_.T
    #X_nom = W_nominal @ W
    #Rs = features - X_nom
    return W_mask @ W + np.mean(features, 0, keepdims=True)

def transform_sparse_audio(Sp, W_source, W_target, output_audio, isFlat=False,
                           isNorm=False):
    
    nb_feat, nb_atoms = W_source.shape
    nwin = (nb_feat - 1) * 2
    novlp = int(nwin * 3 / 4)
    Sp.sparse_transform(W_source, W_target, isFlat=isFlat, isNorm=isNorm)
    Sp.savespeech(output_audio, "normalized")    
    
    return len(Sp.signal) / Sp.sampling_frequency
   
def transform_formant(formants, dil_fact, trans_fact=np.ones(4)):  
    fr_out = formants.copy()
    f_mean = np.mean(formants.frequency, 1).squeeze()   
    detrend_freq = ((fr_out.frequency - f_mean.reshape(-1,1)) *
                        (1 - dil_fact.reshape(-1,1)))
    trans_freq = (f_mean * trans_fact).reshape(-1,1)
    new_freq = detrend_freq + trans_freq
    fr_out.frequency = new_freq  
    return fr_out

def transform_formant_from_dist(Fr, dist, rndmize=True):
    
    Fr_out = Fr.copy()
    for k in range(4):
        
        if rndmize:
            fact_med = random_smpl(dist, 'med_formant', k=k, lim=[0.5,2])
            fact_span = random_smpl(dist, 'span_formant', k=k, lim=[0.25,3])
        else:
            fact_med = dist["med_formant"][k]
            fact_span = dist["span_formant"][k]
        
        fTmp = Fr_out.frequency[k,:]
        Cont = Contour('values', fTmp, 'time_points', Fr_out.time_vector)
        try:
            Cont.getbaselines()
            Cont.changespan(fact_span)
        except:
            Cont = Contour('values', fTmp, 'time_points', Fr_out.time_vector)
                
        Cont.values *= fact_med 
        Fr_out.frequency[k,:] = Cont.values
    
    return Fr_out

def transform_pitch(pitch, fact_med, fact_span):
    
    pitch_out = pitch.copy()    
    pitch_out.getcontour()
    if fact_span != 1:
        try:
            pitch_out.changespan(fact_span)
        except:
            pitch_out = pitch.copy()
            pitch_out.getcontour()
    if fact_med != 1:
        pitch_out.values *= fact_med
     
    return pitch_out