# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from scipy import signal
"""
Created on Thu Jan 07 17:13:00 2021

@author: sz394@exeter.ac.uk
"""

class Spec():
    def __init__(self, hz = 10):
        self.hz = hz
        
    def spectra(self, scalar):
        """
        calculate scalar spectra
        Parameters:
        -----------
        scalar: pandas.Series
        Returns:
        --------
        freq: numpy.ndarray frequencies
        psd(spectra): numpy.ndarray power spectral density
        """
        scalar = scalar.interpolate(method = "linear")

        # method 1: welch
        freqs, psd = signal.welch(
            scalar,
            fs = 1/self.hz, # # sample rate
            window = "hamming",   # apply a Hanning window before taking the DFT
            detrend = "constant", # detrend scalar by subtracting the mean
            scaling = "spectrum"
        )

        # # method 2: csd (same to welch)
        # freqs, psd = signal.csd(
        #     scalar, scalar, 
        #     fs = 1/self.hz, # # sample rate,
        #     window = "hamming",   # apply a Hanning window before taking the DFT
        #     detrend = "constant", # detrend scalar by subtracting the mean
        #     scaling = "spectrum" # Selects between computing the power spectral density ('density') where Pxx has units of V**2/Hz and computing the power spectrum ('spectrum') where Pxx has units of V**2, if x is measured in V and fs is measured in Hz.
        # )
        return freqs, psd

    def cospectra(self, wind, scalar):
        """
        calculate scalar cospectra
        Parameters:
        -----------
        wind: pandas.Series
        scalar: pandas.Series
        Returns:
        --------
        freq: numpy.ndarray frequencies
        csd(cospectra): numpy.ndarray power spectral density
        """
        scalar = scalar.interpolate(method = "linear")
        wind = wind.interpolate(method = "linear")
        
        freqs, csd = signal.csd(
            scalar,
            wind, 
            fs = 1/self.hz, # # sample rate,
            window = "hamming",   # apply a Hanning window before taking the DFT
            detrend = "constant", # detrend scalar by subtracting the mean
            scaling = "spectrum" # Selects between computing the power spectral density ('density') where Pxx has units of V**2/Hz and computing the power spectrum ('spectrum') where Pxx has units of V**2, if x is measured in V and fs is measured in Hz.
        )
        csd = csd.real
        # csd = np.abs(csd)
        return freqs, csd

    def plot(self, freqs, density, figsize = (5, 4), title = "", xlabel = "Frequency", ylabel = "Power", savefile = ""):
        """
        plot spectra and cospectra
        Parameters:
        --------
        freq: numpy.ndarray frequencies
        csd(cospectra): numpy.ndarray power spectral density
        Returns:
        --------
        None
        """
        fig, ax = plt.subplots(figsize = figsize)
        ax.semilogx(freqs, density)
        # # equivalent to
        # ax.plot(freqs, density)
        # ax.set_xscale('log')
        ax.set_title(title, fontsize = 14)
        ax.set_xlabel(xlabel, fontsize = 12)
        ax.set_ylabel(ylabel, fontsize = 12)
        ax.tick_params(direction = "in", which = "both", labelsize = 10)
        plt.tight_layout()
        if savefile:
            fig.savefig(savefile, dpi = 300, bbox_inches = "tight")
        plt.close('all')