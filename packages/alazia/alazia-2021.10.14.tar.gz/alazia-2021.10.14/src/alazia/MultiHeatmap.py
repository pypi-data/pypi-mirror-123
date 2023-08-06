#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Multistage heatmap.py
@Time    :   2021/10/14 17:29:19
@Author  :   Youqi Liu
@Version :   0.1.1
@Contact :   liuyouqi@westlakeomics.com
'''


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd



def MultiHeatmap(data: pd.DataFrame,
                 infodf: pd.DataFrame,
                 clist: list,
                 cmap='RdYlBu_r',
                 pos=(1, 0, 0.13, 0.8),
                 colors_ratio=0.02,
                 method='complete',
                 metric='euclidean',
                 row_cluster=True,
                 col_cluster=False,
                 P=2):
    """Heatmap of multi-tier labels

    Args:
        data (pd.DataFrame): The matrix that has been dealt with the expression, such as zscore.
        infodf (pd.DataFrame): Multi-classification information matrix whose index is matrix sample name.
        clist (list): A list of color bars, using dictionary types for discrete variables and colorMap 
                      strings for continuous variables.
        cmap (str, optional): colormap of Heatmap. Defaults to 'RdYlBu_r'.
        pos (tuple, optional): position of colorbars. Defaults to (1, 0, 0.13, 0.8).
        colors_ratio (float, optional): [description]. Defaults to 0.02.
        method (str, optional): [description]. Defaults to 'complete'.
        metric (str, optional): [description]. Defaults to 'euclidean'.
        row_cluster (bool, optional): [description]. Defaults to True.
        col_cluster (bool, optional): [description]. Defaults to False.
        P (int, optional): [description]. Defaults to 2.
    """ 
    def _colorbar(axes, value, cmap='RdYlBu_r',
                    clrnorm=plt.Normalize(0, 1),
                    realnorm=plt.Normalize(0, 1),
                    xmin=0.1, xmax=0.4,
                    ymin=0.1, ymax=0.9, ystep=0.001, P=2,nc=4):
        for y in np.arange(ymin, ymax, ystep):
            axes.plot([xmin, xmax], [y, y], color=plt.get_cmap(cmap)(clrnorm(y)))
        for y in np.arange(ymin, ymax+(ymax-ymin)/nc, (ymax-ymin)/nc):
            axes.text(xmax+0.05, y-0.05,
                    format(clrnorm(y)*(realnorm.vmax-realnorm.vmin)+realnorm.vmin,'.'+str(P)+'f'))
        axes.text(xmax, ymax+0.05, value)


    def _groupbar(axes, value, cdict,
                    xmin=0.1, xmax=0.4,
                    ymin=0, ymax=1, yjust=1.5):
        _i = 0
        for group, color in cdict.items():
            axes.add_patch(patches.Rectangle((xmin, ymin+(ymax-ymin)/len(cdict)*_i),
                                            xmax-xmin, (ymax-ymin)/len(cdict), color=color))
            axes.text(xmax+0.05, ymin+(ymax-ymin)/len(cdict) *
                    (_i+1)-(ymax-ymin)/len(cdict)/yjust, group)
            _i += 1
        axes.text(xmax, ymax+0.05, value)
    values, colors, xmins, xmaxs, ymins, ymaxs = [], [], [], [], [], []

    for i in range(infodf.shape[1]):
        value = infodf.columns[i]
        values.append(value)
        if infodf.shape[1]<=4:
            if i == 0:
                xmins.append(1.1)
                xmaxs.append(1.4)
            else:
                xmins.append(0.1)
                xmaxs.append(0.4)
            ymins.append(0.1-i)
            ymaxs.append(0.9-i)
        else:
            if i == 0:
                xmins.append(1.1)
                xmaxs.append(1.4)
            else:
                if i%2==0:
                    xmins.append(1.1)
                    xmaxs.append(1.4)
                else:
                    xmins.append(0.1)
                    xmaxs.append(0.4)
            ymins.append(0.1-int((i+1)/2))
            ymaxs.append(0.9-int((i+1)/2))
        if type(clist[i]) == dict:
            lut = clist[i].copy()
        elif type(clist[i]) == str:
            lut = dict(zip(infodf[value].unique(),
                           [plt.get_cmap(clist[i])(plt.Normalize(infodf[value].min(),
                                                                 infodf[value].max())(tmp)) for tmp in infodf[value].unique()]))
        colors.append(list(infodf[value].map(lut)))
    colordf = pd.DataFrame(colors, index=infodf.columns,
                           columns=infodf.index).T

    mysns = \
        sns.clustermap(data=data,
                       method=method,
                       metric=metric,
                       row_cluster=row_cluster,
                       col_cluster=col_cluster,
                       cmap=cmap,
                       col_colors=colordf,
                       row_colors=None,
                       yticklabels=False,
                       xticklabels=False,
                       cbar_pos=None,
                       colors_ratio=colors_ratio
                       )
    mysns.ax_heatmap.set_ylabel('')
    axes = mysns.fig.add_subplot(mysns.gs[0, 0])
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['left'].set_color('none')
    axes.spines['bottom'].set_color('none')
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_xlim(0, 2)
    axes.set_ylim(-3.5, 1.5)
    axes.set_position(pos=pos)

    clrnorm = plt.Normalize(0.1, 0.9)
    realnorm = plt.Normalize(data.min().min(), data.max().max())
    if plt.get_cmap(cmap).N<10:
        _colorbar(axes, '', clrnorm=clrnorm, realnorm=realnorm, cmap=cmap,nc=plt.get_cmap(cmap).N)
    else:
        _colorbar(axes, '', clrnorm=clrnorm, realnorm=realnorm, cmap=cmap)
    for i in range(infodf.shape[1]):
        if type(clist[i]) == dict:
            _groupbar(
                axes, values[i], clist[i], xmins[i], xmaxs[i], ymins[i], ymaxs[i])
        elif type(clist[i]) == str:
            clrnorm = plt.Normalize(ymins[i], ymaxs[i])
            realnorm = plt.Normalize(
                infodf[values[i]].min(), infodf[values[i]].max())
            _colorbar(
                axes, values[i], clist[i], clrnorm, realnorm, xmins[i], xmaxs[i], ymins[i], ymaxs[i], P=P)


if __name__ == '__main__':
    matrix = [list(np.random.random(5))+\
              list(np.random.random(5)*(-1)) 
              if j%2==0 and j>1000 else
              list(np.random.random(5)*(-1))+\
              list(np.random.random(5)) for j in range(2000)]
    data = pd.DataFrame(matrix,
                        index=['Protein'+str(i) for i in range(2000)],
                        columns=['Sample'+str(i)  for i in range(10)])

    infodf = pd.DataFrame([[17+i for i in range(10)],
                           ['M']*5+['F']*5,
                           ['KO']*6+['WT']*4, 
                           ['H']*3+['M']*4+['L']*3],
                          index=['ages', 'gender', 'tissue', 'symptom'],
                          columns=data.columns,).T

    clist = ['PuRd',
             {'F': plt.get_cmap('Set1')(0), 'M': plt.get_cmap('Set1')(1)},
             {'KO': plt.get_cmap('Set2')(0), 'WT': plt.get_cmap('Set2')(1)},
             {'H': plt.get_cmap('Set3')(0),'M': plt.get_cmap('Set3')(1),
              'L': plt.get_cmap('Set3')(2)}
             ]

    # data :zscore,fillna
    MultiHeatmap(data, infodf, clist,P=0,colors_ratio=0.015)