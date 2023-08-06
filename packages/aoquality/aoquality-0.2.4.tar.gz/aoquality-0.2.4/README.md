# pyaoquality

Python module to access Measurement Sets' quality statistics produced by aoflagger, aoquality or DPPP.

## Installation

pyaoquality can be installed via pip:

    $ pip install aoquality

and requires Python 3.6.0 or higher.

# Usage

Example to retrieve baseline statistics:


```python
aoq = aoquality.AOQualityBaselineStat(ms_file)

# plot SNR as function of baseline length:
plt.plot(aoq.blenght, aoq.SNR)

# plot SNR as function of first antenna:
plt.plot(aoq.ant1, aoq.SNR)

```

To retrieve time statistics:


```python
aot = aoquality.AOQualityTimeStat(ms_file)

# plot RFI percentage as function of time:
plt.plot(aot.time, aot.RFIPercentage)

```

To retrieve frequency statistics:


```python
aof = aoquality.AOQualityFrequencyStat(ms_file)

# plot Std as function of frequencies:
plt.plot(aof.freqs, aof.Std)

```

# Command line tool

There is also a command line tool, aostats, which usage is as follow:

    Usage: aostats plot [OPTIONS] MS_FILES... [Mean|Std|DStd|Count|DCount|Sum|DSum
                        |DSumP2|Variance|DVariance|SNR|RFICount|RFIPercentage]

      Plot Statistics from AO Quality Tables

      MS_FILES: Input MS files STAT_NAME: Statistic Name

    Options:
      -o, --out_prefix TEXT    Prefix to the output filename  [default: stat]
      -p, --pol INTEGER RANGE  Polarization index: 0->XX, 1->XY, 2->YX, 3->YY
                               [default: 0]

      --log                    Plot in log scale
      --vmin FLOAT             Minimum value
      --vmax FLOAT             Maximum value
      --name TEXT              Title of the plot
      --help                   Show this message and exit.


