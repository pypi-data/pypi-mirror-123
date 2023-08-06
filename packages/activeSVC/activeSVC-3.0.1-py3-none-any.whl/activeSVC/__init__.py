import numpy as np
import random
import math
import os
import time
import multiprocessing as mp
from sklearn import svm
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import normalize 
from sklearn.metrics.pairwise import cosine_similarity


class TimerError(Exception):
     """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        

        

def text_create(path, name, msg):
    full_path = path + "/" + name + '.txt'
    file = open(full_path, 'w')
    file.write(str(msg))



def SVM(X, y, penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    model = svm.LinearSVC(penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,  
                          random_state=random_state, max_iter=max_iter)
    model.fit(X, y)
    return model


def get_error(model, X, y):
    y_pred = model.predict(X)
    return mean_squared_error(y_pred, y)


def get_sv_classes(c,y,sv):
    sv_classes = list(set(list(np.where(y == c)[0])) & set(sv))
    return sv_classes
def select_samples_mincomplexity(X, y, num_samples,balance=False,penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    model = SVM(X, y,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight, 
                          random_state=random_state, max_iter=max_iter)
    y_pred = model.predict(X)
    sv = [i for i in range(len(y)) if y[i] != y_pred[i]]
    if balance:
        indices=[]
        classes=np.unique(y)
        
        pool = mp.Pool(mp.cpu_count())
        sv_classes=pool.starmap(get_sv_classes,[(c,y,sv) for c in classes])
        pool.close()
        
        sv_classes.sort(key=len)
        for i in range(len(classes)):
            sv_class=sv_classes[i]
            at_least=int((num_samples-len(indices))/(len(classes)-i))
            if len(sv_class)<=at_least:
                indices+=sv_class
            else:
                indices += random.sample(sv_class, at_least)
    else:
        if len(sv)<num_samples:
            indices =sv
        else:
            indices = random.sample(sv, num_samples)
    return indices, model


def select_samples_minacquisition(X, y, num_samples, sample_selected,penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    model = SVM(X, y,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight, 
                          random_state=random_state, max_iter=max_iter)
    y_pred = model.predict(X)
    sv = [i for i in range(len(y)) if y[i] != y_pred[i]]
    reused = list(set(sample_selected) & set(sv))
    num_select=num_samples-len(reused)
    if num_select<=0:
        return [],model
    else:
        indices = reused
        sv = list(set(sv) - set(indices))
        if len(sv)<=num_select:
            indices +=sv
        else:
            indices += random.sample(sv, num_select)
    return indices, model




def get_angles(i, X, y, feature_list,w_padded,penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    X_local = X[:, feature_list + [i]]
    w_new = SVM(X_local, y,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter).coef_
    cos=cosine_similarity(w_padded, w_new)
    angle = 0
    for j in range(w_padded.shape[0]):
        tmp=cos[j,j]
        if tmp>1:
            tmp=1
        elif tmp<-1:
            tmp=-1
        angle = angle + math.acos(tmp)            
    return angle
def select_feature(X, y, feature_list,penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    coef_ = SVM(X[:, feature_list], y,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter).coef_
    w_padded = np.hstack((coef_, np.zeros((coef_.shape[0], 1))))
    
    pool = mp.Pool(mp.cpu_count())
    angles=pool.starmap(get_angles, [(i, X, y,feature_list,w_padded,penalty,loss,dual, tol, C, fit_intercept,
                                      intercept_scaling, class_weight,
                                      random_state, max_iter) for i in range(X.shape[1])])
    pool.close()

    indices = sorted(range(X.shape[1]), key=lambda i: angles[i], reverse=True)
    return [i for i in indices if i not in feature_list][0]



def get_scores(i, X_global, y_global,penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    model=SVM(X_global[:,i].reshape(-1, 1),y_global,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)
    return model.score(X_global[:,i].reshape(-1, 1),y_global) 
def min_complexity(X_train, y_train, X_test, y_test, num_features, num_samples,init_samples=None, balance=False,
                   penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    feature_selected = []
    num_samples_list = []
    train_errors = []
    test_errors = []
    train_scores = []
    test_scores = []
    if init_samples is None:
        init_samples=num_samples
    
    if balance:
        samples=[]
        classes=np.unique(y_train)
        sample_classes=[]
        for c in classes:
            sample_class = list(np.where(y_train == c)[0])
            sample_classes.append(sample_class)
        sample_classes.sort(key=len)
        for i in range(len(classes)):
            sample_class=sample_classes[i]
            at_least=int((init_samples-len(samples))/(len(classes)-i))
            if len(sample_class)<=at_least:
                samples+=sample_class
            else:
                samples += random.sample(sample_class, at_least)
    else:
        shuffle = np.arange(X_train.shape[0])
        np.random.shuffle(shuffle)
        samples = shuffle[:init_samples]
            
    X_global = X_train[samples, :]
    y_global = y_train[samples]
    samples_global=samples
    num_samples_list.append(len(samples_global))

    pool = mp.Pool(mp.cpu_count())
    scores=pool.starmap(get_scores, [(i,X_global, y_global,penalty,loss,dual, tol, C, fit_intercept,
                                      intercept_scaling, class_weight,
                                      random_state, max_iter) for i in range(X_global.shape[1])])
    pool.close() 
    
    new_feature = sorted(range(X_global.shape[1]), key=lambda i: scores[i], reverse=True)[0]
    feature_selected.append(new_feature)

    for i in range(num_features - 1):
        t=Timer()
        t.start()

        X_measured_train = X_train[:,feature_selected]
        X_measured_test = X_test[:,feature_selected]

        samples, model = select_samples_mincomplexity(X_measured_train, y_train, num_samples,balance=balance,
                                                     penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                                                      intercept_scaling=intercept_scaling, class_weight=class_weight,
                                                      random_state=random_state, max_iter=max_iter)

        train_error = get_error(model, X_measured_train, y_train)
        test_error = get_error(model, X_measured_test, y_test)
        train_score = model.score(X_measured_train, y_train)
        test_score = model.score(X_measured_test, y_test)
        train_errors.append(train_error)
        test_errors.append(test_error)
        train_scores.append(train_score)
        test_scores.append(test_score)
        print("feature " + str(i) + ' : gene ' + str(new_feature)+'  '+str(len(samples_global)) + ' samples')
        print('training error=' + str(train_error) + ' test error=' + str(test_error))
        print('training accuracy=' + str(train_score) + ' test accuracy=' + str(test_score))
        samples_global = list(set().union(samples_global, samples))
        num_samples_list.append(len(samples_global))
        
        new_feature=select_feature(X_train[samples], y_train[samples],feature_selected,
                                   penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)
        feature_selected.append(new_feature)
        t.stop()

    X_measured_train = X_train[:,feature_selected]
    X_measured_test = X_test[:,feature_selected]
    model=SVM(X_measured_train,y_train,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)
    train_error = get_error(model, X_measured_train, y_train)
    test_error = get_error(model, X_measured_test, y_test)
    train_score = model.score(X_measured_train, y_train)
    test_score = model.score(X_measured_test, y_test)
    train_errors.append(train_error)
    test_errors.append(test_error)
    train_scores.append(train_score)
    test_scores.append(test_score)
    print("feature " + str(i+1) + ' : gene ' + str(new_feature)+'  '+str(len(samples_global)) + ' samples')
    print('training error=' + str(train_error) + ' test error=' + str(test_error))
    print('training accuracy=' + str(train_score) + ' test accuracy=' + str(test_score))

    return feature_selected, num_samples_list, train_errors, test_errors, train_scores, test_scores




def min_acquisition(X_train, y_train, X_test, y_test, num_features, num_samples,init_samples=None,
                    penalty='l2',loss='squared_hinge',dual=True, tol=1e-4, C=1.0, fit_intercept=True,
                          intercept_scaling=1, class_weight=None, random_state=None, max_iter=1000):
    feature_selected = []
    num_samples_list = []
    samples_global=[]
    train_errors = []
    test_errors = []
    train_scores = []
    test_scores = []
    if init_samples is None:
        init_samples=num_samples
        
    shuffle = np.arange(X_train.shape[0])
    np.random.shuffle(shuffle)
    samples = shuffle[:init_samples]
    X_global = X_train[samples, :]
    y_global = y_train[samples]
    samples_global=samples
    num_samples_list.append(len(samples_global))

    pool = mp.Pool(mp.cpu_count())
    scores=pool.starmap(get_scores, [(i,X_global, y_global,penalty,loss,dual, tol, C, fit_intercept,
                                      intercept_scaling, class_weight,
                                      random_state, max_iter) for i in range(X_global.shape[1])])
    pool.close() 

    new_feature = sorted(range(X_global.shape[1]), key=lambda i: scores[i], reverse=True)[0]
    feature_selected.append(new_feature)

    for i in range(num_features - 1):
        t=Timer()
        t.start()

        X_measured_train = X_train[:,feature_selected]
        X_measured_test = X_test[:,feature_selected]

        samples, model = select_samples_minacquisition(X_measured_train, y_train, num_samples,samples_global,
                                                       penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)

        train_error = get_error(model, X_measured_train, y_train)
        test_error = get_error(model, X_measured_test, y_test)
        train_score = model.score(X_measured_train, y_train)
        test_score = model.score(X_measured_test, y_test)
        train_errors.append(train_error)
        test_errors.append(test_error)
        train_scores.append(train_score)
        test_scores.append(test_score)
        print("feature " + str(i) + ' : gene ' + str(new_feature)+'  '+str(len(samples_global)) + ' samples')
        print('training error=' + str(train_error) + ' test error=' + str(test_error))
        print('training accuracy=' + str(train_score) + ' test accuracy=' + str(test_score))
        samples_global = list(set().union(samples_global, samples))
        num_samples_list.append(len(samples_global))
        
        new_feature=select_feature(X_train[samples_global], y_train[samples_global],feature_selected,
                                   penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)
        feature_selected.append(new_feature)
        t.stop()

    X_measured_train = X_train[:,feature_selected]
    X_measured_test = X_test[:,feature_selected]
    model=SVM(X_measured_train,y_train,penalty=penalty,loss=loss,dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                          intercept_scaling=intercept_scaling, class_weight=class_weight,
                          random_state=random_state, max_iter=max_iter)
    train_error = get_error(model, X_measured_train, y_train)
    test_error = get_error(model, X_measured_test, y_test)
    train_score = model.score(X_measured_train, y_train)
    test_score = model.score(X_measured_test, y_test)
    train_errors.append(train_error)
    test_errors.append(test_error)
    train_scores.append(train_score)
    test_scores.append(test_score)
    print("feature " + str(i+1) + ' : gene ' + str(new_feature)+'  '+str(len(samples_global)) + ' samples')
    print('training error=' + str(train_error) + ' test error=' + str(test_error))
    print('training accuracy=' + str(train_score) + ' test accuracy=' + str(test_score))

    return feature_selected, num_samples_list, samples_global, train_errors, test_errors, train_scores, test_scores