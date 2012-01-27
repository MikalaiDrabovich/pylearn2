"""
This script makes a dataset of 32x32 approximately whitened CIFAR-10 images.

"""

from pylearn2.utils import serial
from pylearn2.datasets import preprocessing
from pylearn2.utils import string
import numpy as np
from pylearn2.datsets.cifar10 import CIFAR10

data_dir = string.preprocess('${PYLEARN2_DATA_PATH}/cifar10')

print 'Loading CIFAR-10 train dataset...'
train = CIFAR10(which_set = 'train')

print "Preparing output directory..."
output_dir = data_dir + '/pylearn2_whitened'
serial.mkdir( output_dir )
README = open(output_dir + '/README','w')

README.write("""
The .pkl files in this directory may be opened in python using
cPickle, pickle, or pylearn2.serial.load.

train.pkl, and test.pkl each contain
a pylearn2 Dataset object defining a labeled
dataset of a 32x32 approximately whitened version of the STL-10
dataset. train.pkl contains labeled train examples. test.pkl
contains labeled test examples.

preprocessor.pkl contains a pylearn2 ZCA object that was used
to approximately whiten the images. You may want to use this
object later to preprocess other images.

They were created with the pylearn2 script make_cifar10_whitened.py.

All other files in this directory, including this README, were
created by the same script and are necessary for the other files
to function correctly.
""")

README.close()

print "Learning the preprocessor and preprocessing the unsupervised train data..."
preprocessor = preprocessing.ZCA()
train.apply_preprocessor(preprocessor = preprocessor, can_fit = True)

print 'Saving the unsupervised data'
train.use_design_loc(output_dir+'/train.npy')
serial.save(output_dir + '/train.pkl', train)

print "Loading the test data"
test = CIFAR10(which_set = 'test')

print "Preprocessing the test data"
test.apply_preprocessor(preprocessor = preprocessor, can_fit = False)

print "Saving the test data"
test.use_design_loc(output_dir+'/test.npy')
serial.save(output_dir+'/test.pkl', test)

serial.save(output_dir + '/preprocessor.pkl',preprocessor)
