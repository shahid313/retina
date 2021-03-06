from kobra.tr_utils import prep_out_path
import pandas as pd
from sklearn.cross_validation import train_test_split
from kobra.train_files import TrainFiles
from skimage.io.collection import ImageCollection
import os
from os import path
from shutil import copy, rmtree
import cv2

def get_sample_csv(sample_size = 0.1):
    X, Y, _, _ = TrainFiles.from_csv(inp_file, test_size = sample_size)
    tf = TrainFiles(train_path)

    tf.dump_to_csv(sample_file, X, Y)

def get_sample_of_class(classs, labels, input_path, num = -1):
    """
    Returns images sampled from files by class
    """
        
    existing_files = pd.DataFrame([path.splitext(f)[0] for f in os.listdir(input_path)], columns =[labels.columns[0]])
    class_labels = pd.DataFrame(labels[labels['level'] == classs]['image'], columns =[labels.columns[0]])
    class_labels = class_labels.merge(existing_files, on=class_labels.columns[0])
    if num == -1:
        num = class_labels.count()

    files = [path.join(raw_train, c + ".jpeg") for c in class_labels[:num][class_labels.columns[0]]]
    return ImageCollection(files, conserve_memory = True)


def sample_files(labels, size, inp_path, out_path):
    if path.exists(out_path):
        rmtree(out_path)
    os.makedirs(out_path)

    files = labels['image']
    levels = labels['level']
    picked_files, _, picked_labels, _ = train_test_split(files, levels, train_size = size)

    inp_files = [path.join(inp_path, f + ".jpeg") for f in picked_files]
    out_files = [path.join(out_path, f + ".jpeg") for f in picked_files]
    for src, dst in zip(inp_files, out_files):
        copy(src, dst)

labels_file = "/Kaggle/Retina/trainLabels.csv"    
inp_path = "/Kaggle/retina/train/thresh5ref6535sc17"
out_path = "/Kaggle/retina/train/labelled_1"

def copy_files_to_label_dirs(inp_path, out_path, labels_file, process = None):
    prep_out_path(out_path)
    
    for i in range(0, 5):
        os.makedirs(path.join(out_path, str(i)))
    
    labels = pd.read_csv(labels_file)
    existing_files = pd.DataFrame([path.splitext(f)[0] for f in os.listdir(inp_path)], columns =[labels.columns[0]])
    existing_files = existing_files.merge(labels, on=existing_files.columns[0])
    
    def processAndCopy(inp_file, out_file):
        im = cv2.imread(inp_file)
        im = process(im)
        cv2.imwrite(out_file, im)

    if process == None:
        cp = copy
    else:
        cp = processAndCopy

    for f, l in zip(existing_files['image'], existing_files['level']):
        file_name = path.join(out_path, str(l), f + ".jpeg")
        inp_file = path.join(inp_path, f + '.jpeg')
        cp(inp_file, file_name)

        print "copied {0} to {1}".format(inp_file, file_name)

def post_proc(im):
    return cv2.medianBlur(im, 13)