from typing import Optional, Union, Dict, List

import numpy as np

import ROOT

from quickstats.plots import AbstractPlot
from quickstats.plots.template import single_frame, parse_styles
from quickstats.utils.roostats_utils import get_hypotest_data

import atlas_mpl_style as ampl

class TestStatisticDistributionPlot(AbstractPlot):
    
    COLOR_PALLETE = {
        'null': 'b',
        'alt': 'r'
    }
        
    def __init__(self, result:ROOT.RooStats.HypoTestResult,
                 color_pallete:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]='default',
                 analysis_label_options:Optional[Union[Dict, str]]='default'):
        super().__init__(color_pallete=color_pallete, styles=styles,
                         analysis_label_options=analysis_label_options)
        self.result = result
        self.data = get_hypotest_data(self.result)
        
    def draw_distribution(self, ax, data, weight, label:str,
                          color:Optional[str]=None,
                          nbins:int=75, xmax:float=40.):
        n, bins   = np.histogram(data, bins=nbins, range=(0, xmax), 
                                 density=False, weights=weight)
        bin_centers  = 0.5*(bins[1:] + bins[:-1])
        bin_width    = bin_centers[1] - bin_centers[0]
        ax.errorbar(bin_centers, n, color=color, yerr = n**0.5, 
                    **self.styles['errorbar'])

    def draw(self, xlabel:str="", ylabel:str="",
             logy:bool=True, nbins:int=75, xmax:float=40.):
        ampl.use_atlas_style()
        ax = single_frame(logy=logy, styles=self.styles)
        # draw test statistic distribution for null hypothesis
        self.draw_distribution(ax, 
                               self.data['null']['data'],
                               self.data['null']['weight'],
                               self.color_pallete['null'],
                               label="$f(\tilde{q}_{\mu}|\mu)$ toys",
                               nbins=nbins, xmax=xmax)
        # draw test statistic distribution for alternative hypothesis
        self.draw_distribution(ax, 
                               self.data['alt']['data'],
                               self.data['alt']['weight'],
                               self.color_pallete['alt'],
                               label="$f(\tilde{q}_{\mu}|0)$ toys",
                               nbins=nbins, xmax=xmax)
        ax.set_xlim([0, xmax])
        ax.set_xlabel("$\tilde{q}_{\mu}$", **self.styles['xlabel'])
        ax.set_ylabel("Number of Entries", **self.styles['ylabel'])
        
        return ax