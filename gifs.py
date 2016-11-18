'''

    GIF generator library

    Author: Gabriel Lopes de Cicco
    nov/2016

    Disclaimer: this was made as a school project and
    the code here is ridiculously non-optimized
img
    Each function takes one filter (highpass, lowpass, bandpass
    or notch filter) and generate the frames by applying different
    values of one parameter of the filter. 
    The functions will generate one frame for each value in "variation". 
    kwargs will be passed to imageio.mimsave(), which means you can pass 
    the 'fps' argument to control GIF framerate. Default is 'fps=10'

    Gifs will be saved to a directory called 'gifs'.


'''


from img import *
import imageio


# High pass filter, sweeps through cutoff frequency values.
# n = order of the Butterworth 2D filter
def highpass_fsweep(img, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(highpass(img, i, n, show=0))
    imageio.mimsave(path, frames, **kwargs)

# High pass filter, sweeps through the order of the Butterworth
# filter which is applied. freq = cutoff frequency
def highpass_nsweep(img, freq, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(highpass(img, freq, i, show=0))
    imageio.mimsave(path, frames, **kwargs)

# Low pass filter, sweeps through cutoff frequency values.
# n = order of the Butterworth 2D filter
def lowpass_fsweep(img, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(lowpass(img, i, n, show=0))
    imageio.mimsave(path, frames, **kwargs)

# Low pass filter, sweeps through the order of the Butterworth
# filter which is applied. freq = cutoff frequency
def lowpass_nsweep(img, freq, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(lowpass(img, freq, i, show=0))
    imageio.mimsave(path, frames, **kwargs)

# Band pass filter, sweeps through cutin frequency values
def bandpass_insweep(img, cutoff, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(bandpass(img, i, cutoff, n, show=0))
    imageio.mimsave(path, frames, **kwargs)

# Band pass filter, sweeps through cutoff frequency values
def bandpass_offsweep(img, cutin, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(bandpass(img, cutin, i, n, show=0))
    imageio.mimsave(path, frames, **kwargs)

# Notch filter, sweeps through center frequency values
def notch_fsweep(img, band, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(notchfilter(img, i, band, n, show=0))
    imageio.mimsave(path, frames, **kwargs)    

# Notch filter, sweeps through bandwidth values
def notch_bsweep(img, freq, n, path, variation=range(1, 11), **kwargs):
    frames = []
    for i in variation:
        frames.append(notchfilter(img, freq, i, n, show=0))
    imageio.mimsave(path, frames, **kwargs)    
