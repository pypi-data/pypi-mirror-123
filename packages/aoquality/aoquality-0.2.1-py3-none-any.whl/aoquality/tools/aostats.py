#!/usr/bin/env python3

import os
import sys

import click

import aoquality
from aoquality import __version__

from matplotlib.backends import backend_pdf

t_dir = click.Path(exists=True, file_okay=False)


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command('plot')
@click.argument('ms_files', type=t_dir, nargs=-1, required=True)
@click.argument('stat_name', type=click.Choice(aoquality.available_stats, case_sensitive=False))
@click.option('--out_prefix', '-o', help='Prefix to the output filename', default='stat', show_default=True, type=str)
@click.option('--pol', '-p', help='Polarization index: 0->XX, 1->XY, 2->YX, 3->YY ', default=0, 
              show_default=True, type=click.IntRange(0, 3))
@click.option('--log', help='Plot in log scale', is_flag=True)
@click.option('--vmin', help='Minimum value', default=None, type=float)
@click.option('--vmax', help='Maximum value', default=None, type=float)
@click.option('--name', help='Title of the plot', default=None, type=str)
def plot(ms_files, stat_name, out_prefix, pol, log, vmin, vmax, name):
    ''' Plot Statistics from AO Quality Tables 

    MS_FILES: Input MS files
    STAT_NAME: Statistic Name
    '''
    pdf = backend_pdf.PdfPages(f'{out_prefix}_{stat_name.lower()}_{aoquality.pol_dict[pol]}.pdf')

    if name is None:
        name = os.path.basename(ms_files[0])

    print('Plotting Baseline statistic ...')
    aoq = aoquality.AOQualityBaselineStat.from_ms_list(ms_files)
    fig = aoq.plot_baseline_stats(stat_name, pol, log=log, vmin=vmin, vmax=vmax, name=name)
    pdf.savefig(fig)
    fig = aoq.plot_antennae_stats(stat_name, pol, log=log, vmin=vmin, vmax=vmax, name=name)
    pdf.savefig(fig)
    fig = aoq.plot_baseline_length_stats(stat_name, pol, log=log, vmin=vmin, vmax=vmax, name=name)
    pdf.savefig(fig)

    print('Plotting Time statistics ...')
    aoq = aoquality.AOQualityTimeStat.from_ms_list(ms_files)
    fig = aoq.plot_time_stats(stat_name, pol, log=log, vmin=vmin, vmax=vmax, name=name)
    pdf.savefig(fig)

    print('Plotting Frequency statistics ...')
    aoq = aoquality.AOQualityFrequencyStat.from_ms_list(ms_files)
    fig = aoq.plot_freq_stats(stat_name, pol, log=log, vmin=vmin, vmax=vmax, name=name)
    pdf.savefig(fig)

    pdf.close()

    print('All done')

if __name__ == '__main__':
    main()
