
'''
Abnormal Detection with multivariate gaussian distribution model, a p(x_input) funtion get the data set x_input's epsilon density value,
small density means far away from distribution center.

A training data set with marked abnormal for a best epsilon density value

compare input data set density value p(x) with training data set density value  best_epsilon(x_training),
if p(x_input) < best_epsilon(x_training), means data seems far away from gaussian distribution center , and got the abnormal from input data set

'''

import numpy as np
from matplotlib import pyplot as plt


def display_2d_data(X,marker):
    '''
    display 2D data only
    :param X:
    :param marker:
    :return:
    '''
    fig = plt.figure()
    ax = fig.subplots()

    xs = X[:, 0]
    ys = X[:, 1]

    ax.scatter(xs, ys)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    plt.show()

def display_3d_data(X,marker):
    '''
    display 3D data only
    :param X:
    :param marker:
    :return:
    '''
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    xs = X[:,0]
    ys = X[:,1]
    zs = X[:,2]
    ax.scatter(xs, ys, zs, marker)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def display_abnormal_3d_data(X,abnormal,marker):
    '''
    display abnormal 3D only
    :param X:
    :param abnormal:
    :param marker:
    :return:
    '''
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    xs = X[abnormal,0]
    ys = X[abnormal,1]
    zs = X[abnormal,2]
    ax.scatter(xs, ys, zs, marker)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def estimate_gaussian(X):
    '''
    input collection array as X , calculate mu and sigma2
    :param X:
    :return mu,sigma2:
    '''

    m, n = X.shape
    mu = np.zeros((n, 1))
    sigma2 = np.zeros((n, 1))
    mu = np.mean(X, axis=0)
    sigma2 = np.var(X, axis=0)


    return mu,sigma2

def multivariateGaussian(X,mu,Sigma2):
    '''
    base on mu and sigma2 , input data collection array ,calculate p(x) value ,means density function value
    :param X:
    :param mu:
    :param Sigma2:
    :return p:
    '''
    k = len(mu)
    if (Sigma2.shape[0]>1):
        Sigma2 = np.diag(Sigma2)
    X = X-mu
    argu = (2*np.pi)**(-k/2)*np.linalg.det(Sigma2)**(-0.5)
    p = argu*np.exp(-0.5*np.sum(np.dot(X,np.linalg.inv(Sigma2))*X,axis=1))  # axis表示每行
    return p

def select_best_epsilon(yval,pval):
    '''
    base on p(Xval) ,compare with marked abnormal Yval, steps by steps , choose a best epsilon density for input data collection abnormal comparation
    :param yval:
    :param pval:
    :return:
    '''
    bestEpsilon = 0.
    bestF1 = 0.


    step = (np.max(pval) - np.min(pval)) / 1000

    for epsilon in np.arange(np.min(pval), np.max(pval), step):  #from min to max step 1/1000 , try the best epsilon
        cvPrecision = pval < epsilon # density value to true / false array
        aa = np.sum((cvPrecision == 1) & (yval == 1).ravel()).astype(float) # count abnormal/abnormal(marked)
        an = np.sum((cvPrecision == 1) & (yval == 0).ravel()).astype(float) # count abnormal/normal(marked)
        nn = np.sum((cvPrecision == 0) & (yval == 1).ravel()).astype(float) # count normal/normal(marked)

        if aa + an == 0.:
            precision = float('nan')
        else:
            precision = aa / (aa + an) # should avoid divided by zero ;P
        recision = aa / (aa + nn)


        F1 = (2 * precision * recision) / (precision + recision)  # function score ,find a best boundary between normal and abnormal
        if F1 > bestF1:  # choose the best score
            bestF1 = F1
            bestEpsilon = epsilon
    return bestEpsilon

def main():

    # input data set to get abnormal , to calculate p(X)
    # input data 3D sample , kind of [bandwidth , latency , pps] etc ,multi variable is enable ,  may comes from telemetry data source
    X_list = [[1,2,3],[2,3,4],[3,3,4],[4,5,6],[4,5,5],[2,3,3],[1,3,3],[8,8,8],[1,2,3],[9,7,8],[2,2,3],[3,3,3],[8.1,7.8,9],[1,2,3],[3,3,3],[1,0,1]]

    # marked training data set with marked y value , to calculate p(Xval) and compare with Yval to select best epsilon
    # Yval 0 means normal , 1 means abnormal
    Xval_list = [[1,1,1],[2,2,3],[7,7,7],[1,2,3],[2,3,4],[3,3,4],[4,5,6],[4,5,5],[2,3,3],[6,6,6],[0,0,0]]
    Yval_list = [[1],[0],[1],[0],[0],[0,],[0],[0],[0],[1],[1]]

    # numpy list to array
    X = np.asarray(X_list)
    Xval = np.asarray(Xval_list)
    Yval = np.asarray(Yval_list)

    # display_2d_data(X, 'bx')

    display_3d_data(Xval,'bx')  # display training data set
    display_3d_data(X, 'bx')    # display input data set

    mu,sigma2 = estimate_gaussian(X)
    print("Mean value : %a"%mu) # mean value of each parameter , mean bandwidth , mean latency , mean pps etc
    print("Variance : %a"%sigma2) # variance of each parameter

    p = multivariateGaussian(X,mu,sigma2) # get input data set p(X), density value
    print("Density value %a/"%p)

    pval = multivariateGaussian(Xval,mu,sigma2) # get Xval training data set pval(Xval), density value

    best_epsilon = select_best_epsilon(Yval,pval) # with marked abnormal Yval , compare with pval ,choose the best epsilon density for training data collection
    print("Best Epsilon Density :%a"%best_epsilon)

    abnormal = np.where(p<best_epsilon)
    print("Abnormal Postition : %a"%abnormal)

    display_abnormal_3d_data(X,abnormal,'bx') # display abnormal collection from input data collection



if __name__ == '__main__':
    main()
