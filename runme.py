'''
    This is a sample of how to use the 'gifs' library.
'''

import gifs

images = {
    'muse': 'src/muse.jpg'
}

for prefix, file in images.items():
    
    img = gifs.load(file)
    
    gifs.highpass_fsweep(img, 2, prefix+'_high_fsweep.gif', variation=range(50))
    gifs.highpass_nsweep(img, 20, prefix+'_high_nsweep.gif', variation=range(20), fps=5)

    gifs.lowpass_fsweep(img, 2, prefix+'_low_fsweep.gif', variation=range(50, -1, -1))
    gifs.lowpass_nsweep(img, 10, prefix+'_low_nsweep.gif', variation=range(20), fps=3)

    gifs.bandpass_insweep(img, 60, 2, prefix+'_banda_insweep.gif', variation=range(50))
    gifs.bandpass_offsweep(img, 10, 2, prefix+'_banda_offsweep.gif', variation=range(100,10,-5))
    
    gifs.notch_fsweep(img, 3, 100, prefix+'_notch_fsweep.gif', variation=range(50,-1,-1))
    gifs.notch_bsweep(img, 50, 5, prefix+'_notch_bsweep.gif', variation=range(10, 100, 2))

