# Python module to access statistics from QUALITY table

import os
from matplotlib.colors import Normalize

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize

import casacore.tables

mpl.rcParams['image.cmap'] = 'Spectral_r'
mpl.rcParams['image.origin'] = 'lower'
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['axes.grid'] = True


available_stats = ['Mean', 'Std', 'DStd', 'Count', 'DCount', 'Sum', 'DSum', 'DSumP2', 
                   'Variance', 'DVariance', 'SNR', 'RFICount', 'RFIPercentage']

pol_dict = dict(zip(np.arange(4), ['XX', 'XY', 'YX', 'YY']))


def make_ant_matrix(ant1, ant2, m, a_max=None):
    '''Make antenna x antenna matrix from flat array
    
    Args:
        ant1 (array): Antenna 1
        ant2 (array): Antenna 2
        m (array): Flat array
        a_max (int, optional): Max antenna number
    
    Returns:
        array (n_ant, n_ant): antenna x antenna matrix
    '''
    if a_max is None:
        a_max = max(np.max(ant1), np.max(ant2))
    m_map = np.ma.zeros((a_max, a_max)) * np.nan
    for a1, a2, i in zip(ant1, ant2, m):
        if (a1 < a_max) and (a2 < a_max):
            m_map[a1, a2] = i

    return m_map


def set_ylim(ax, log, vmin, vmax):
    if log:
        ax.set_yscale('log')
    ax.set_ylim(vmin, vmax)


def get_norm(log, vmin, vmax):
    if log:
        return LogNorm(vmin=vmin, vmax=vmax)
    return Normalize(vmin=vmin, vmax=vmax)


class BaseAOQuality(object):

    def __init__(self, ms_file, kind=[], value=[], verbose=True):
        if verbose:
            print(f'Opening {ms_file} ...')
        with casacore.tables.table(os.path.join(ms_file, 'QUALITY_KIND_NAME'), ack=False) as q:
            k_name = q.getcol('NAME')
            k_id = q.getcol('KIND')
        self.ms_file = ms_file
        self.k_dict = dict(zip(k_name, k_id))
        self.kind = kind
        self.value = value

    @classmethod
    def from_ms_list(cls, ms_files, verbose=True):
        a = cls(ms_files[0], verbose=verbose)
        for ms_file in ms_files[1:]:
            a.add(cls(ms_file, verbose=True))

        return a

    def add(self, other):
        self.kind = np.concatenate([self.kind, other.kind])
        self.value = np.concatenate([self.value, other.value])

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError()
        if name in self.k_dict:
            return self.value[self.kind == self.k_dict[name]]
        raise AttributeError()

    @property
    def Std(self):
        ''' Standard deviation of the visibilities '''
        return np.sqrt(self.Variance)

    @property
    def Variance(self):
        ''' Variance of the visibilities '''
        with np.errstate(divide='ignore', invalid='ignore'):
            sumMeanSquared = self.Sum ** 2 / self.Count
            return (self.SumP2 - sumMeanSquared) / self.Count

    @property
    def DStd(self):
        ''' Standard deviation of the channels difference visibilities '''
        return np.sqrt(self.DVariance)

    @property
    def DVariance(self):
        ''' Variance of the channels difference visibilities '''
        with np.errstate(divide='ignore', invalid='ignore'):
            sumMeanSquared = self.DSum ** 2 / self.DCount;
            return (self.DSumP2 - sumMeanSquared) / self.DCount

    @property
    def Mean(self):
        ''' Mean of the visibilities '''
        with np.errstate(divide='ignore', invalid='ignore'):
            return self.Sum / self.Count

    @property
    def SNR(self):
        ''' Mean of the visibilities over rms of the channel difference's visibilities '''
        with np.errstate(divide='ignore', invalid='ignore'):
            return abs(self.Mean / self.DStd)

    @property
    def RFIPercentage(self):
        ''' Percentage of RFI flagged data '''
        with np.errstate(divide='ignore', invalid='ignore'):
            return self.RFICount.real / (self.RFICount.real + self.Count.real)

    def get_stat(self, name):
        ''' Return the given statistic.
        
        Args:
            name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
        '''
        return getattr(self, name)


class AOQualityBaselineStat(BaseAOQuality):
    '''AO quality baseline statistics
    
    Attributes:
        ant1 (array of int): Antenna 1
        ant2 (array of int): Antenna 2
        ant_name (array of str): Name of the stations
        ant_pos (array): Positions of the stations
        blenght (array): Baseline length in meter
    '''
    
    def __init__(self, ms_file, verbose=True):
        '''AO quality baseline statistics
        
        Args:
            ms_file (str): MS path
        '''
        with casacore.tables.table(os.path.join(ms_file, 'QUALITY_BASELINE_STATISTIC'), ack=False) as q:
            kind = q.getcol('KIND')
            self.ant1 = q.getcol('ANTENNA1')[kind == 1]
            self.ant2 = q.getcol('ANTENNA2')[kind == 1]
            value = q.getcol('VALUE')
            
        with casacore.tables.table(os.path.join(ms_file, 'ANTENNA'), ack=False) as q:
            self.ant_name = q.getcol('NAME')
            self.ant_pos = q.getcol('POSITION')

        self.blenght = np.linalg.norm(self.ant_pos[self.ant1] - self.ant_pos[self.ant2], axis=1)
        BaseAOQuality.__init__(self, ms_file, kind, value, verbose=verbose)

    def add(self, other):
        self.ant1 = np.concatenate([self.ant1, other.ant1])
        self.ant2 = np.concatenate([self.ant2, other.ant2])
        self.blenght = np.concatenate([self.blenght, other.blenght])
        BaseAOQuality.add(self, other)

    def get_combined_stat(self, stat_name, action_fct=np.nanmedian):
        '''Return combined statistics applying action_fct over the frequency axis.
           Useful when gathering statistics from combined QUALITY tables, but safe to use for non combined 
           QUALITY tables as well: it will be a no-op in this case.
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            action_fct (fct, optional): The function to apply over the frequency axis
        
        Returns:
            ant1 (n_baselines), ant2 (n_baselines), blenght (n_baselines), stat (n_baselines, n_pol)
        '''
        b_id = self.ant1 + 1000 * self.ant2
        u_b_id = np.unique(b_id)

        stat = action_fct(self.get_stat(stat_name).reshape(-1, len(u_b_id), 4), axis=0)
        ant1 = self.ant1.reshape(-1, len(u_b_id))[0]
        ant2 = self.ant2.reshape(-1, len(u_b_id))[0]
        blenght = self.blenght.reshape(-1, len(u_b_id))[0]

        return ant1, ant2, blenght, stat
            
    def plot_baseline_stats(self, stat_name, pol=0, flag_autocorr=True, log=False, vmin=None, vmax=None, name=''):
        '''Plot 2D matrix of baselines statistics
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            pol (int, optional): The polarization to plot: 0:XX, 1:XY, 2:YX, 2:YY
        
        Returns:
            Figure: the matplotlib figure
        '''
        ant1, ant2, _, stat = self.get_combined_stat(stat_name)
        ant_matrix = make_ant_matrix(ant1, ant2, stat[:, pol], len(self.ant_name))
        if flag_autocorr:
            ant_matrix[np.diag_indices(ant_matrix.shape[0])] = np.nan
        fig, ax = plt.subplots(figsize=(12, 10))
        i_ant = np.arange(len(self.ant_name))
        im = ax.pcolormesh(i_ant, i_ant, ant_matrix, shading='auto', norm=get_norm(log, vmin, vmax))
        ax.set_xticks(i_ant)
        ax.set_xticklabels(self.ant_name)
        ax.set_yticks(i_ant)
        ax.set_yticklabels(self.ant_name)
        ax.xaxis.set_tick_params(rotation=90)
        plt.colorbar(im, ax=ax)
        ax.set_title(f'{name} | {stat_name} | {pol_dict[pol]}')
        fig.tight_layout()
        
        return fig
    
    def plot_antennae_stats(self, stat_name, pol=0, log=False, vmin=None, vmax=None, name=''):
        '''Plot the statistic for each individual antennae/station
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            pol (int, optional): The polarization to plot: 0:XX, 1:XY, 2:YX, 2:YY
        
        Returns:
            Figure: the matplotlib figure
        '''
        all_snr = [np.nanmedian(self.get_stat(stat_name)[((self.ant1 == i_ant) | (self.ant2 == i_ant)) & (self.ant1 != self.ant2), pol]) for i_ant in range(len(self.ant_name))]
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(self.ant_name, all_snr)
        ax.xaxis.set_tick_params(rotation=90)
        ax.set_ylabel(f'{stat_name} | {pol_dict[pol]}')
        ax.set_title(name)
        set_ylim(ax, log, vmin, vmax)
        fig.tight_layout()

        return fig

    def plot_baseline_length_stats(self, stat_name, pol=0, log=False, vmin=None, vmax=None, name=''):
        '''Plot the statistic for each baselines as function of baseline length
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            pol (int, optional): The polarization to plot: 0:XX, 1:XY, 2:YX, 2:YY
        
        Returns:
            Figure: the matplotlib figure
        '''
        _, _, blenght, stat = self.get_combined_stat(stat_name)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.scatter(blenght, stat[:, pol], c='tab:orange')
        ax.set_xlabel('Baseline lenght [meter]')
        ax.set_ylabel(f'{stat_name} | {pol_dict[pol]}')
        ax.set_title(name)
        set_ylim(ax, log, vmin, vmax)
        fig.tight_layout()

        return fig


class AOQualityFrequencyStat(BaseAOQuality):
    '''AO quality frequency statistics
    
    Attributes:
        freqs (array): Frequencies 
    '''
    
    def __init__(self, ms_file, verbose=True):
        '''AO quality frequency statistics
        
        Args:
            ms_file (TYPE): Description
        '''
        with casacore.tables.table(os.path.join(ms_file, 'QUALITY_FREQUENCY_STATISTIC'), ack=False) as q:
            kind = q.getcol('KIND')
            self.freqs = q.getcol('FREQUENCY')[kind == 1]
            value = q.getcol('VALUE')
        BaseAOQuality.__init__(self, ms_file, kind, value, verbose=verbose)

    def add(self, other):
        self.freqs = np.concatenate([self.freqs, other.freqs])
        BaseAOQuality.add(self, other)

    def get_combined_stat(self, stat_name, action_fct=np.nanmedian):
        '''Return combined statistics applying action_fct over the frequency axis.
           Useful when gathering statistics from combined QUALITY tables, but safe to use for non combined
           QUALITY tables as well: it will be a no-op in this case.
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            action_fct (fct, optional): The function to apply over the frequency axis
        
        Returns:
            freqs (n_freqs), ant2 (n_baselines), blenght (n_baselines), stat (n_freqs, n_pol)
        '''
        u_freqs = np.unique(self.freqs)

        stat = action_fct(self.get_stat(stat_name).reshape(-1, len(u_freqs), 4), axis=0)
        freqs = self.freqs.reshape(-1, len(u_freqs))[0]

        return freqs, stat

    def plot_freq_stats(self, stat_name, pol=0, log=False, vmin=None, vmax=None, name=''):
        '''Plot frequency statistics
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            pol (int, optional): The polarization to plot: 0:XX, 1:XY, 2:YX, 2:YY
        
        Returns:
            Figure: the matplotlib figure
        '''
        freqs, stat = self.get_combined_stat(stat_name)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(freqs * 1e-6, stat[:, pol], c='tab:orange')
        ax.set_xlabel('Frequency [MHz]')
        ax.set_ylabel(f'{stat_name} | {pol_dict[pol]}')
        ax.set_title(name)
        set_ylim(ax, log, vmin, vmax)
        fig.tight_layout()

        return fig


class AOQualityTimeStat(BaseAOQuality):

    '''AO quality time statistics
    
    Attributes:
        time (array): Time
    '''
    
    def __init__(self, ms_file, verbose=True):
        '''AO quality time statistics
        
        Args:
            ms_file (str): MS path
        '''
        with casacore.tables.table(os.path.join(ms_file, 'QUALITY_TIME_STATISTIC'), ack=False) as q:
            kind = q.getcol('KIND')
            self.time = q.getcol('TIME')[kind == 1]
            self.freqs = q.getcol('FREQUENCY')[kind == 1]
            value = q.getcol('VALUE')
        BaseAOQuality.__init__(self, ms_file, kind, value, verbose=verbose)

    def add(self, other):
        self.freqs = np.concatenate([self.freqs, other.freqs])
        self.time = np.concatenate([self.time, other.time])
        BaseAOQuality.add(self, other)

    def get_combined_stat(self, stat_name):
        '''Return combined statistics.
           Useful when gathering statistics from combined QUALITY tables
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
        
        Returns:
            time (n_time), freqs (n_freqs), stat (n_freqs, n_time, n_pol)
        '''
        u_time = np.unique(self.time)

        stat = self.get_stat(stat_name).reshape(-1, len(u_time), 4)
        time = self.time.reshape(-1, len(u_time))[0]
        freqs = self.freqs.reshape(-1, len(u_time))[:, 0]

        return time, freqs, stat

    def plot_time_stats(self, stat_name, pol=0, log=False, vmin=None, vmax=None, name=''):
        '''Plot time statistics
        
        Args:
            stat_name (str): The statistic to retrieve. See aoquality.available_stats for a list of available statistics
            pol (int, optional): The polarization to plot: 0:XX, 1:XY, 2:YX, 2:YY
        
        Returns:
            Figure: the matplotlib figure
        '''

        time, freqs, stat = self.get_combined_stat(stat_name)

        if stat.shape[0] == 1:
            fig, ax = plt.subplots(figsize=(12, 5))
            stat = stat[0, :, pol]
            ax.plot(time - time[0], stat, c='tab:orange')
            ax.set_xlabel('Time [second since start]')
            ax.set_ylabel(f'{stat_name} | {pol_dict[pol]}')
            ax.set_title(name)
            set_ylim(ax, log, vmin, vmax)
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            extent = [0, time.max() - time[0], freqs.min() * 1e-6, freqs.max() * 1e-6]
            im = ax.imshow(stat[:, :, pol].real, aspect='auto', cmap='magma', extent=extent, norm=get_norm(log, vmin, vmax))
            plt.colorbar(im, ax=ax)
            ax.set_xlabel('Time [second since start]')
            ax.set_ylabel('Frequency [MHz]')
            ax.set_title(f'{name} | {stat_name} | {pol_dict[pol]}')
        fig.tight_layout()
        return fig
