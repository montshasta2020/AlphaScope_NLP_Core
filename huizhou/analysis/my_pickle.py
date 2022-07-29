import cPickle as pickle

def my_pickle_dump(fname, data):
    with open(fname, 'w') as f:
        pickle.dump(data, f)

def my_pickle_load(fname):
    with open(fname) as f:
        return pickle.load(f)

#if __name__=='__main__':