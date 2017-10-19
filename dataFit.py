import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time

import scipy.optimize as op
import scipy.fftpack as ft
import scipy.signal as sg
import scipy.ndimage.filters as flt

def date2epoch(date):
    pattern = "%Y-%m-%d"
    return time.mktime(time.strptime(str(date)[2:-1], pattern))

def missing2nan(string):
    try:
        return float(string)
    except:
        return float('nan')

def sine(x, a, b):
    return a*np.sin(x+b) 

def line(x, a, b): return a*x+b

def fitCurve(func, xdata, ydata):
    popt, pcov = op.curve_fit(func, xdata, ydata)
    model = func(xdata, *popt)
    res = ydata - model
    return model, res

def fitSine(func, xdata, ydata):
    sampRate = 1/(xdata[1]-xdata[0])
    spect, freqs = mlab.psd(ydata, Fs=sampRate, detrend='linear', NFFT=16, noverlap=8)
#    spect = ft.dct(ydata)
#    idx = np.argmax( np.abs(spect[1:]) ) + 1
#    freq = 1/(xdata[1] - xdata[0]) * 2 * (idx)/len(ydata)
    maxFreq = freqs[np.argmax(spect)]
#    maxFreq = freqs[np.argmax(spect[1:]) + 1]
    return fitCurve(func, xdata * maxFreq, ydata)

def interpolateMissing(data, r=1):
    data = np.pad(data, r, mode='reflect')
    mask = np.isnan(data)
    buf = np.zeros_like(data[mask])
    newMask = np.array(mask)
    for i in range(r):
        temp = np.roll(data,i+1)[mask] * (r-i) / (r+1)
        temp = temp + np.roll(data,-r+i)[mask] * (i+1) / (r+1)
        buf = buf + np.nan_to_num(temp)
        newMask = newMask & np.roll(newMask, 1)
    data[mask] = buf
    data = data[r:-r]
    if newMask[r:-r].any():
        for i in range(r):
            newMask = newMask | np.roll(newMask, -1)
        data[newMask[r:-r]] = float('nan')
        data = interpolateMissing(data, r+1)
    return data

def stripOutliers(data):
#    median = sg.medfilt(data, 5)
    median = flt.median_filter(data, size=5, mode='mirror')
    diff = abs(data - median)
#    mad = sg.medfilt(diff, 5)
    mad = flt.median_filter(diff, size=5, mode='mirror')
    mask = diff > (4 * mad)
    data[mask] = float('nan')
    return interpolateMissing(data)

def loadData(ticker):
    dict = {0: date2epoch, 1: missing2nan, 2: missing2nan, 3: missing2nan, 4: missing2nan, 5: missing2nan, 6: missing2nan}
    blob = np.loadtxt(ticker + '.txt', skiprows=1, delimiter=',', converters=dict, unpack=True)
    for idx, col in enumerate(blob):
        if not idx: continue
        data = np.array(col)
        if np.isnan(data).any():
            data = interpolateMissing(data)
        blob[idx] = stripOutliers(data)
    return blob


def fitData(xdata, ydata, line, sine):
    wave = np.zeros_like(xdata)
    linear = np.zeros_like(xdata)
    for i in np.arange(0,1):
        linear, resLine = fitCurve(line, xdata, ydata - wave)
        wave, resSine = fitSine(sine, xdata, resLine)
    return linear, wave

def plotData(ticker, xdata, ydata, linear, wave, path):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(ticker)
    ax.plot(xdata, ydata)
    ax.plot(xdata, wave + linear, color='red')
    ax.plot(xdata, linear, color='darkgreen')
    fig.savefig(path + '/' + ticker + '.svg')
    plt.close(fig)
