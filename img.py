import copy
import imageio
import scipy.misc
import scipy.fftpack
import numpy as np
import matplotlib.image
import matplotlib.pyplot as plt
from skimage import exposure

# Loads image file
def load(path):
    img = matplotlib.image.imread(path)
    if isinstance(img, np.ndarray) and img.dtype == 'float32':
        img = (img*255).astype('uint8')
    return img


# Saves image file
def save(img, name, usepyplot=False, grayscale=True):
    if usepyplot:
        plt.figure(1)
        plt.clf()
        if grayscale:
            plt.imshow(img, cmap="Greys_r")
        else:
            plt.imshow(img) 
        plt.savefig(name)
    else:
         scipy.misc.imsave(name, img)
    
# Displays image
def display(img, grayscale=True):
    plt.figure(1)
    plt.clf()
    # Grayscale here only makes some difference to single-channel
    # images as they would otherwise be shown with the heatmap-like
    # default colorscheme.
    # For colored images this is ignored.
    if grayscale:
        plt.imshow(img, cmap="Greys_r")
    else:
        plt.imshow(img) 
    plt.show()

# Isolate RGB channels of the image 
# Currently ignores alpha channel of transparent images
def isolate_channels(img):
    channels = {
        'red': copy.copy(img),
        'green': copy.copy(img),
        'blue': copy.copy(img) 
    }

    images = {
        'red': copy.copy(img),
        'green': copy.copy(img),
        'blue': copy.copy(img) 
    }

    for i in range(len(img)):
        for j in range(len(img[i])):
            images['red'][i][j] = [img[i][j][0], 0, 0] 
            images['green'][i][j] = [0, img[i][j][1], 0]
            images['blue'][i][j] = [0, 0, img[i][j][2]] 
            channels['blue'][i][j] = img[i][j][0]
            channels['green'][i][j] = img[i][j][1] 
            channels['red'][i][j] = img[i][j][2] 
    
    for channel in channels:
        channels[channel] = img2channel(channels[channel])

    return channels, images

# Join channels into a colored image
def join_channels(red_channel, green_channel, blue_channel):
    img = []
    for channel in [red_channel, green_channel, blue_channel]:
        if not isinstance(channel, np.ndarray) and not isinstance(channel, np.array):
            print("Error: channel must be of type \"numpy array\", but it is:")
            print(type(channel))
            return False
    for i in range(len(red_channel)):
        img.append([])
        for j in range(len(red_channel[i])):
            img[i].append([blue_channel[i][j], green_channel[i][j], red_channel[i][j]])
    return np.array(img)



# Transforms grayscale img (MxNx3 matrix in which all channels have
# the same values) into a separate 'channel' (MxN matrix)
def img2channel(img):
    return img[:,:,0]

# Transforms 'channel' (MxN matrix) into a grayscale img (MxNx3 matrix)
def channel2img(channel):
    img = []
    for i in range(len(channel)):
        img.append([])
        for j in range(len(channel[i])):
            img[i].append([channel[i][j], channel[i][j], channel[i][j]])
    return np.array(img)

# Generates grayscale img from a colored one
def grayscale(img):
    channels = isolate_channels(img)[0]
    gray = (0.2989*channels['red'] + 0.5870*channels['green'] + 0.1140*channels['blue'])/255
    return channel2img(gray)


# Calculates FFT2
def calc_fft2(img):
    fft = scipy.fftpack.fft2(img)
    fft = scipy.fftpack.fftshift(fft)
    fft_amplitude = np.abs(fft)
    return fft

# Calculates inverse FFT2
def calc_ifft2(fft):
    ifft = scipy.fftpack.ifftshift(fft)
    ifft = np.abs(scipy.fftpack.ifft2(ifft))
    # Here we take the absolute values to avoid floating point errors.
    # ifft should be all real but sometimes fftpack return small imaginary
    # values which we need to get rid off
    return ifft

# Applies a 2D n-th order Butterworth lowpass filter to an img
# where f is the cutoff frequency
# 'Show' level (0-4) means what will be plotted
# 'eq' flag means histogram equalization, this is a kind of normalization
def lowpass(img, f, n, show=2, eq=True):
    channels = isolate_channels(img)[0]    
    rows, columns = img.shape[0:2]
    x = np.linspace(-0.5, 0.5, columns)  * columns
    y = np.linspace(-0.5, 0.5, rows)  * rows
    radius = np.sqrt((x**2)[np.newaxis] + (y**2)[:, np.newaxis])
    filt = 1 / (1.0 + (radius / f)**(2*n))
    if show > 0:
        display(filt, grayscale=True) 
    for channel in channels:
        fft = calc_fft2(channels[channel])
        if show > 2:
            display(np.abs(fft))
        nfft = filt * fft
        if show > 3:
            display(np.abs(nfft))
        channels[channel] = calc_ifft2(nfft)
    nimg = join_channels(channels['red'], channels['green'], channels['blue'])
    if eq:
        nimg = exposure.equalize_hist(nimg)
    if show > 1:
        display(nimg)
    return nimg

# Applies a 2D n-th order Butterworth highpass filter to an img
# where f is the cutoff frequency
def highpass(img, f, n, show=2, eq=True):
    showfilter = 0 
    if show > 0: 
        showfilter = 1
    low = lowpass(img, f, n, show=showfilter, eq=False)
    nimg = img - low
    if eq:
        nimg = exposure.equalize_hist(nimg)
    if show > 1:
        display(nimg)
    return nimg



# Applies a 2D n-th order Butterworth bandpass filter to an img
def bandpass(img, cutin, cutoff, n, show=2, eq=True):
    showfilter = 0 
    if show > 0: 
        showfilter = 1
    below = lowpass(img, cutin, n, show=showfilter, eq=False)
    above = highpass(img, cutoff, n, show=showfilter, eq=False)
    nimg = img - (below + above)
    if eq:
        nimg = exposure.equalize_hist(nimg)
    if show > 1:
        display(nimg)
    return nimg


# Applies a 2D n-th order Butterworth notch filter to an img
def notchfilter(img, f, band, n, show=2, eq=True):
    showfilter = 0 
    if show > 0: 
        showfilter = 1
    below = lowpass(img, f-(band/2), n, show=showfilter, eq=False)
    above = highpass(img, f+(band/2), n, show=showfilter, eq=False)
    nimg = below + above
    if eq:
        nimg = exposure.equalize_hist(nimg)
    if show > 1:
        display(nimg)
    return nimg

