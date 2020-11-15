import os
import csv
import random
import numpy as np
from shutil import copyfile

FILEDIR = './raw/'
TXTNAME = 'm.TXT'
CSVNAME = 'results.csv'
SAVEDIR = './processed/'
LABELS = {0: 'Negative', 'Negative': 0,
          1: 'A_Kappa', 'A_Kappa': 1,
          2: 'A_Lambda', 'A_Lambda': 2,
          3: 'G_Kappa', 'G_Kappa': 3,
          4: 'G_Lambda', 'G_Lambda': 4,
          5: 'M_Kappa', 'M_Kappa': 5,
          6: 'M_Lambda', 'M_Lambda': 6,
          7: 'Kappa', 'Kappa': 7,
          8: 'Lambda', 'Lambda': 8,
          9: 'Others', 'Others': 9}

labels_set = {
    'Negative': [],
    'A_Kappa': [],
    'A_Lambda': [],
    'G_Kappa': [],
    'G_Lambda': [],
    'M_Kappa': [],
    'M_Lambda': [],
    'Kappa': [],
    'Lambda': [],
}
LABELS_INDEX = {
    'A_Kappa': 3,
    'A_Lambda': 4,
    'G_Kappa': 5,
    'G_Lambda': 6,
    'M_Kappa': 7,
    'M_Lambda': 8,
    'Kappa': 9,
    'Lambda': 10,
}


def make_dataset(filedir, filename):
    filelist = []
    with open(filedir + filename, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            filelist.append(line)
    return filelist


def find_labels(filedir, filename):
    filelist = []
    with open(filedir + filename, encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            tmp = np.array(row)
            filelist.append(tmp[1] + '.gif')
            # negative
            if np.sum(tmp == '阴性(-)') == 9:
                labels_set["Negative"].append(row[1] + '.gif')
            elif np.sum(tmp == '阴性(-)') == 8:
                for key, value in LABELS_INDEX.items():
                    if tmp[value] == '弱阳性' or tmp[value] == '阳性(+)' or tmp[value] == '强阳性(++)':
                        labels_set[key].append(row[1] + '.gif')
                        break


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


if __name__ == '__main__':
    filelist = make_dataset(filedir=FILEDIR, filename=TXTNAME)
    find_labels(filedir=FILEDIR, filename=CSVNAME)
    for path, files in labels_set.items():
        mkdir("test/" + path)
        mkdir("train/" + path)
        for file in files:
            if random.random() < 0.75:
                copyfile("./raw/" + file, "./dataset/train/" + path + "/" + file.replace("gif", "png"))
            else:
                copyfile("./raw/" + file, "./dataset/test/" + path + "/" + file.replace("gif", "png"))
