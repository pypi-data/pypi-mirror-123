import numpy as np
from ase.parallel import world
from gpatom.gpfp.kerneltypes import SquaredExp, Matern, RationalQuad


class FPKernel():

    def __init__(self, kerneltype='sqexp', params=None):
        '''
        params: dict
            Hyperparameters for the kernel type
        '''
        kerneltypes = {'sqexp': SquaredExp,
                       'matern': Matern,
                       'rq': RationalQuad}

        if params is None:
            params = {}

        kerneltype = kerneltypes.get(kerneltype)
        self.kerneltype = kerneltype(**params)

        self.ndof = 3  # degrees of freedom per atom

    def kernel_function_gradient(self, x1, x2):
        '''
        Gradient of kernel_function w.r.t. coordinates in 'x1'.
        x1: fingerprint object
        x2: fingerprint object
        '''
        gradients = self.kerneltype.kernel_gradient(x1, x2)
        return gradients.reshape(-1)

    def kernel_function_hessian(self, x1, x2):
        '''
        Full Hessian matrix of the kernel function w.r.t.
        coordinates in both 'x1' and 'x2'.
        '''
        hessian = self.kerneltype.kernel_hessian(x1, x2)

        # Reshape to 2D matrix:
        size = self.get_size(x1) - 1
        hessian = hessian.swapaxes(1, 2).reshape(size, size)
        return hessian

    def kernel(self, x1, x2):
        '''
        Return a full kernel matrix between two
        fingerprints, 'x1' and 'x2'.
        '''

        size = self.get_size(x1)

        K = np.empty((size, size), dtype=float)

        K[0, 0] = self.kerneltype.kernel(x1, x2)
        K[1:, 0] = self.kernel_function_gradient(x1, x2)
        K[0, 1:] = self.kernel_function_gradient(x2, x1)
        K[1:, 1:] = self.kernel_function_hessian(x1, x2)

        return K

    def kernel_matrix(self, X):
        '''
        Calculates C(X,X) i.e. full kernel matrix for training data.
        '''

        Ntrain = len(X)
        size = self.get_size(X[0])

        # allocate memory
        K = np.empty((Ntrain * size,
                      Ntrain * size), dtype=float)

        for x in X:
            self.kerneltype.set_fp_params(x)

        for i in range(0, Ntrain):
            for j in range(i + 1, Ntrain):
                k = self.kernel(X[i], X[j])
                K[i * size:(i + 1) * size, j *
                  size:(j + 1) * size] = k
                K[j * size:(j + 1) * size, i *
                  size:(i + 1) * size] = k.T

            K[i * size:(i + 1) * size,
              i * size:(i + 1) * size] = self.kernel(X[i], X[i])

        world.broadcast(K, 0)

        return K

    def kernel_vector(self, x, X):
        '''
        Calculates K(x,X) ie. the kernel matrix between fingerprint
        'x' and the training data fingerprints in X.
        '''
        self.kerneltype.set_fp_params(x)
        for x2 in X:
            self.kerneltype.set_fp_params(x2)

        return np.hstack([self.kernel(x, x2) for x2 in X])

    def get_size(self, x):
        '''
        Return the correct size of a kernel matrix when gradients are
        trained.
        '''
        return len(x.atoms) * self.ndof + 1

    def set_params(self, params):
        '''
        Set new (hyper)parameters for the kernel function.
        '''
        self.kerneltype.update(params)


class FPKernelNoforces(FPKernel):

    def kernel(self, x1, x2):
        return np.atleast_1d(self.kerneltype.kernel(x1, x2))

    def get_size(self, x):
        '''
        Return the correct size of a kernel matrix when gradients are
        NOT trained.
        '''
        return 1


class FPKernelParallel(FPKernel):

    def kernel_matrix(self, X):
        '''
        Calculates C(X,X) i.e. full kernel matrix for training data.
        '''

        Ntrain = len(X)
        size = self.get_size(X[0])

        # allocate memory
        K = np.empty((Ntrain * size,
                      Ntrain * size), dtype=float)

        for x in X:
            self.kerneltype.set_fp_params(x)

        # CALCULATE:
        for i in range(0, Ntrain):
            for j in range(i + 1, Ntrain):

                ij_rank = (i * Ntrain + j) % world.size
                if world.rank == ij_rank:

                    k = self.kernel(X[i], X[j])
                    K[i * size:(i + 1) * size, j *
                      size:(j + 1) * size] = k
                    K[j * size:(j + 1) * size, i *
                      size:(i + 1) * size] = k.T

            ii_rank = (i * Ntrain + i) % world.size
            if world.rank == ii_rank:
                k = self.kernel(X[i], X[i])
                K[i * size:(i + 1) * size,
                  i * size:(i + 1) * size] = k

        # DISTRIBUTE:
        for i in range(0, Ntrain):
            for j in range(i + 1, Ntrain):

                k = K[i * size:(i + 1) * size,
                      j * size:(j + 1) * size]

                # prepare for broadcast:
                k = k.flatten()

                ij_rank = (i * Ntrain + j) % world.size
                world.broadcast(k, ij_rank)

                # reshape back:
                k = k.reshape((size, size))

                K[i * size:(i + 1) * size,
                  j * size:(j + 1) * size] = k
                K[j * size:(j + 1) * size,
                  i * size:(i + 1) * size] = k.T

            k = K[i * size:(i + 1) * size,
                  i * size:(i + 1) * size]
            k = k.flatten()

            ii_rank = (i * Ntrain + i) % world.size
            world.broadcast(k, ii_rank)

            k = k.reshape((size, size))
            K[i * size:(i + 1) * size,
              i * size:(i + 1) * size] = k

        world.broadcast(K, 0)

        return K


class CCKernel(FPKernel):
    '''
    Kernel with Cartesian coordinates.
    '''

    # ---------Derivatives--------
    def squared_distance(self, x1, x2):
        return self.kerneltype.metric.distance(x1, x2)**2

    def dK_dweight(self, X):
        '''
        Return the derivative of K(X,X) respect to the weight
        '''
        return self.K(X, X) * 2 / self.kerneltype.weight

    # ----Derivatives of the kernel function respect to the scale ---
    def dK_dl_k(self, x1, x2):
        '''
        Returns the derivative of the kernel function respect to l
        '''
        return self.squared_distance(x1, x2) / self.kerneltype.scale

    def dK_dl_j(self, x1, x2):
        '''
        Returns the derivative of the gradient of the kernel function
        respect to l
        '''
        prefactor = (-2 * (1 - 0.5 * self.squared_distance(x1, x2)) /
                     self.kerneltype.scale)
        return self.kernel_function_gradient(x1, x2) * prefactor

    def dK_dl_h(self, x1, x2):
        '''
        Returns the derivative of the hessian of the kernel function respect
        to l
        '''
        I = np.identity(self.get_size(x1) - 1)
        P = (np.outer(x1.vector - x2.vector, x1.vector - x2.vector) /
             self.kerneltype.scale**2)
        prefactor = 1 - 0.5 * self.squared_distance(x1, x2)
        return -2 * (prefactor * (I - P) - P) / self.kerneltype.scale**3

    def dK_dl_matrix(self, x1, x2):
        k = np.asarray(self.dK_dl_k(x1, x2)).reshape((1, 1))
        j2 = self.dK_dl_j(x1, x2).reshape(1, -1)
        j1 = self.dK_dl_j(x2, x1).reshape(-1, 1)
        h = self.dK_dl_h(x1, x2)
        return np.block([[k, j2], [j1, h]]) * self.kernel(x1, x2)

    def dK_dl(self, X):
        '''
        Return the derivative of K(X,X) respect of l
        '''
        return np.block([[self.dK_dl_matrix(x1, x2) for x2 in X] for x1 in X])

    def gradient(self, X):
        '''
        Computes the gradient of matrix K given the data respect to the
        hyperparameters. Note matrix K here is self.K(X,X).
        Returns a 2-entry list of n(D+1) x n(D+1) matrices
        '''
        return [self.dK_dweight(X), self.dK_dl(X)]

    def K(self, X1, X2):
        '''
        Compute the kernel matrix
        '''
        self.D = len(X1[0].atoms) * 3
        return np.block([[self.kernel(x1, x2) for x2 in X2] for x1 in X1])
