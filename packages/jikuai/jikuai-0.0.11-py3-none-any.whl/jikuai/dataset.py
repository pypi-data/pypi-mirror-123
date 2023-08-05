from pathlib import Path
import random
import sys
import numpy as np
IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif',
                  '.tiff', '.webp')

class Dataset(object):
    """A generic data loader where the samples are arranged in this way:

        root/class_a/1.ext
        root/class_a/2.ext
        root/class_a/3.ext

        root/class_b/123.ext
        root/class_b/456.ext
        root/class_b/789.ext"""

    def __init__(self,
                 root,
                 extensions=None,
                 is_valid_file=None):
        self.root = root
        if extensions is None:
            extensions = IMG_EXTENSIONS
        classes, class_to_idx = self._find_classes(self.root)
        # print(classes, class_to_idx )
        # samples = self._find_classes(self.root)
        samples = make_dataset(self.root, class_to_idx, extensions,
                               is_valid_file)
        if len(samples) == 0:
            raise (RuntimeError(
                "Found 0 directories in subfolders of: " + self.root + "\n"
                "Supported extensions are: " + ",".join(extensions)))
        # # print(samples)

        self.samples = samples

    def paddleclastxt(self, eval=None):
        # return self.samples
        trainpath = Path("train.txt")
        evalpath = Path("eval.txt")
        trainlist = None
        evallist = None
        random.shuffle(self.samples)
        # print(self.samples, type(self.samples))
        if eval :
            evalnum = None
            try:
                evalnum = float(eval)
            except:
                pass
            # print(eval,evalnum)
            if eval == "eval" :
                evallist = self.samples
            elif evalnum and 0<evalnum<1 :
                evallistnum = int(len(self.samples) * evalnum)
                trainlist = self.samples[:evallistnum]
                evallist = self.samples[evallistnum:]
            else :
                trainlist = self.samples
        else :
            trainlist = self.samples

        if trainlist:
            with open(trainpath, "w") as f: 
                for i in trainlist:
                    f.writelines(f"{i[0]} {i[1]}\n")    
        if evallist:
            with open(evalpath, "w") as f: 
                for i in evallist:
                    f.writelines(f"{i[0]} {i[1]}\n")
        return "PaddleClas train.txt or eval.txt output OK!"

    def _find_classes(self, dir):
        """
        Finds the class folders in a dataset.

        Args:
            dir (string): Root directory path.

        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), 
                    and class_to_idx is a dictionary.

        """
        classes = [d.name for d in Path(dir).iterdir() if d.is_dir()]
        
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx

def make_dataset(dir, class_to_idx, extensions, is_valid_file=None):
    images = []
    dir = Path(dir)

    if extensions is not None:

        def is_valid_file(x):
            return Path(x).suffix in  extensions

    for target in sorted(class_to_idx.keys()):
        # d = os.path.join(dir, target)
        # if not os.path.isdir(d):
        #     continue
        d = dir/target
        if not d.is_dir:
            continue
        for i in d.iterdir():
            # print(i)
            if i.suffix in extensions:
                item = (str(i), class_to_idx[target])
                images.append(item)
        # for root, _, fnames in sorted(os.walk(d, followlinks=True)):
        #     for fname in sorted(fnames):
        #         path = os.path.join(root, fname)
        #         if is_valid_file(path):
        #             item = (path, class_to_idx[target])
        #             images.append(item)

    return images

def npysplit(data="train.npy", label="train_label.npy", split=0.8):
    # import numpy as np 
    # import random

    dcd = np.load(data) #np 打开npy文件
    dcl = np.load(label)
    print(dcd.shape,dcl.shape )

    dcsplit = split # 分割比例
    dclen = dcd.shape[0] #数据总长度
    dclensplit = int(dclen * dcsplit) #分割点
    dctl = list( range(0, dclen)) #序列坐标
    random.shuffle(dctl) # 打乱序列坐标
    random.shuffle(dctl)
    print("shuffle is OK")

    dcdtmp = np.copy(dcd) # 复制训练集数据
    dcltmp = np.copy(dcl) # 复制训练集合标签

    for i,j in enumerate(dctl):  
        dcd[i] =dcdtmp[j]
        dcl[i] =dcltmp[j]

    np.save("train.npy", dcd[:dclensplit])
    np.save("val.npy", dcd[dclensplit:])
    np.save("train_label.npy", dcl[:dclensplit])
    np.save("val_label.npy", dcl[dclensplit:])
    print("Save files OK")

def get_frame_num(data):
    # print(data.shape)
    C, T, V, M = data.shape
    for i in range(T - 1, -1, -1):
        tmp = np.sum(data[:, i, :, :])
        if tmp > 0:
            T = i + 1
            break
    return T

def datapad(data, window_size=350, reversedata=False):
    C, T, V, M = data.shape
    Tindex = get_frame_num(data)
    if Tindex < window_size:
        # print(Tindex,"^",  end=' ')
        print(".", end="")
        data_pad = np.zeros((C, T, V, M))
        data_pad = data
        if not reversedata :
            data_pad[:, Tindex:Tindex+Tindex, :, :] = data[:, :Tindex:1, :, :]
        else :
            data_pad[:, Tindex:Tindex+Tindex, :, :] = data[:, Tindex:0:-1, :, :]

        return data_pad
    return data

def npsave(loadfile="", savefile="", window_size=350, reversedata =False):
    testdata = np.load(loadfile)
    dchtmp = np.ndarray(testdata.shape)
    dchtmp = testdata
# print(dchtmp.shape)
    for i in range(dchtmp.shape[0]):
        # print(i, end=' ')
        dchtmp[i] = datapad(testdata[i], window_size, reversedata)

    np.save(savefile, dchtmp)
    print("save %s OK!" %savefile)   


if __name__ == "__main__":
    dataset = Dataset(".")
    print(dataset.paddleclastxt(0.8))

    # npysplit("train.npy", "val.npy", 0.8)

    #0.08
   
    loadfile = "/home/aistudio/data/data104924/test_A_data.npy"
    savefile = "vallong.npy"
    npsave(loadfile, savefile)
