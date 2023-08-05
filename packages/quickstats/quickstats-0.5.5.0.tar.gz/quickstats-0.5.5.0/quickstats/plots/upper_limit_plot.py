from typing import Optional, Union, Dict, List

import matplotlib.patches as patches
import matplotlib.lines as lines
import pandas as pd
import ROOT

import atlas_mpl_style as ampl

from quickstats.plots.template import single_frame, parse_styles, format_axis_ticks
from quickstats.plots import AbstractPlot

class UpperLimitPlot(AbstractPlot):
    
    COLOR_PALLETE = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9'
    }
    
    def __init__(self, data,
                 color_pallete:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]='limit',
                 analysis_label_options:Optional[Union[Dict, str]]='default'):
        super().__init__(color_pallete=color_pallete, styles=styles,
                         analysis_label_options=analysis_label_options)
        self.data = data
        
    def draw(self, xlabel:str="", ylabel:str="", ylim=None, xlim=None,
             log:bool=False, draw_observed:bool=True, observed_marker:Optional[str]='o'):
        ampl.use_atlas_style()
        
        ax = single_frame(styles=self.styles)
        
        indices = self.data.index.values
        exp_limits = self.data['0'].values
        n1sigma_limits = self.data['-1'].values
        n2sigma_limits = self.data['-2'].values
        p1sigma_limits = self.data['1'].values
        p2sigma_limits = self.data['2'].values 
        
        # draw +- 1, 2 sigma bands 
        ax.fill_between(indices, n2sigma_limits, p2sigma_limits, 
                        facecolor=self.color_pallete['2sigma'],
                        label='Expected limit $\pm 2\sigma$')
        ax.fill_between(indices, n1sigma_limits, p1sigma_limits, 
                        facecolor=self.color_pallete['1sigma'],
                        label='Expected limit $\pm 1\sigma$')
        
        if log:
            draw_fn = ax.semilogy
        else:
            draw_fn = ax.plot
        
        
        if draw_observed:
            obs_limits = self.data['obs'].values
            draw_fn(indices, obs_limits, 'k', label='Observed limit (95% CL)', 
                    marker=observed_marker)
            draw_fn(indices, exp_limits, 'k--', label='Expected limit (95% CL)')
        else:
            draw_fn(indices, exp_limits, 'k', label='Expected limit (95% CL)')        
        
        ax.set_xlabel(xlabel, **self.styles['xlabel'])
        ax.set_ylabel(ylabel, **self.styles['ylabel'])
        format_axis_ticks(ax, **self.styles['axis'])
        
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)
        
        if self.analysis_label_options is not None:
            ampl.draw_atlas_label(**self.analysis_label_options)

        # border for the legend
        border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
        
        handles, labels = ax.get_legend_handles_labels()
        if draw_observed:
            handles = [handles[0], handles[1], (handles[3], border_leg), (handles[2], border_leg)]
            labels  = [labels[0], labels[1], labels[3], labels[2]]
        else:
            handles = [handles[0], (handles[2], border_leg), (handles[1], border_leg)]
            labels  = [labels[0], labels[2], labels[1]]
        ax.legend(handles, labels, **self.styles['legend'])
        return ax