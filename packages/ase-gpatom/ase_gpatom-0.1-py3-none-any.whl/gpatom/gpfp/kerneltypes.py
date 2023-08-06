import numpy as np


class EuclideanDistance:

    @staticmethod
    def distance(fp1, fp2):
        '''
        Distance function between two fingerprints.
        '''
        return np.linalg.norm(fp1.vector - fp2.vector)

    @staticmethod
    def dD_drm(fp1, fp2):
        '''
        Gradient of distance function:

                      d D(x, x')
                      ----------
                         d xi
        '''

        D = EuclideanDistance.distance(fp1, fp2)

        gradients = fp1.reduce_coord_gradients()

        if D == 0.0:
            return np.zeros((fp1.natoms, 3))

        result = 1 / D * np.einsum('i,hil->hl',
                                   fp1.vector - fp2.vector,
                                   gradients,
                                   optimize=True)

        return result


class BaseKernelType:
    '''
    Base class for all kernel types with common properties,
    attributes and methods.
    '''

    def __init__(self, weight=1.0, scale=1.0, metric=EuclideanDistance):
        # Currently, all the kernel types take weight and scale as parameters

        self.params = {'scale': scale, 'weight': weight}
        self.metric = metric

    @property
    def scale(self):
        return self.params['scale']

    @property
    def weight(self):
        return self.params['weight']

    def update(self, params):
        '''
        Update the kernel function hyperparameters.
        '''
        self.params.update(params)

    def set_fp_params(self, x):
        '''
        Update fingerprint parameters to match with the
        kernel parameters. Recalculate fingerprint if
        the relevant fingerprint parameters change.
        '''

        oldparams = x.params.copy()
        x.params.update(self.params)

        for p in x.param_names:
            if p in self.params:
                if self.params[p] != oldparams[p]:
                    x.recalculate()
                break

    def kernel_gradient(self, fp1, fp2):
        '''
        Calculates the derivative of the kernel between
        fp1 and fp2 w.r.t. all coordinates in fp1.

        Chain rule:

                d k(x, x')    dk      d D(x, x')
                ---------- = ----  X  ----------
                   d xi       dD         d xi
        '''

        return self.dk_dD(fp1, fp2) * self.metric.dD_drm(fp1, fp2)

    def common_hessian_terms(self, fp1, fp2):
        D = self.metric.distance(fp1, fp2)
        kernel = self.kernel(fp1, fp2)

        dD_dr1 = self.metric.dD_drm(fp1, fp2)
        dD_dr2 = self.metric.dD_drm(fp2, fp1)

        g1 = fp1.reduce_coord_gradients()
        g2 = fp2.reduce_coord_gradients()
        tensorprod_gradients = np.einsum('hil,gim->hglm',
                                         g1, g2, optimize=True)
        
        return kernel, D, dD_dr1, dD_dr2, tensorprod_gradients


class SquaredExp(BaseKernelType):
    '''
    Squared Exponential kernel function
    '''

    def kernel(self, fp1, fp2):
        '''
        Kernel function between fingerprints 'fp1' and 'fp2'.
        '''
        return (self.weight**2 *
                np.exp(-self.metric.distance(fp1, fp2)**2 / 2 / self.scale**2))

    def dk_dD(self, fp1, fp2):
        '''
        Derivative of kernel function w.r.t. distance function dk / dD
        '''
        k = self.kernel(fp1, fp2)
        D = self.metric.distance(fp1, fp2)

        result = - D / self.scale**2 * k

        return result

    def kernel_hessian(self, fp1, fp2):
        '''
        Kernel hessian w.r.t. atomic coordinates in both 'fp1' and 'fp2'

                    d^2 k(x, x')
                    ------------
                     dx_i dx'_j
        '''

        kernel, D, dD_dr1, dD_dr2, C1 = self.common_hessian_terms(fp1, fp2)

        prefactor = 1 / self.scale**2 * kernel

        C0 = D**2 / self.scale**2 * np.einsum('ki,lj->klij', dD_dr1, dD_dr2,
                                              optimize=True)

        result = prefactor * (C0 + C1)

        return result


class Matern(BaseKernelType):
    ''' Matern 5/2 kernel function '''

    def kernel(self, x1, x2):
        '''
        Kernel function between fingerprints 'fp1' and 'fp2'.
        '''
        D = self.metric.distance(x1, x2)
        p = np.sqrt(5) / self.scale

        pre = 1 + (p * D) + (p**2 / 3 * D**2)

        exp = np.exp(-p * D)
        return self.weight**2 * pre * exp

    def dk_dD(self, fp1, fp2):
        '''
        Derivative of kernel function w.r.t. distance function dk / dD
        '''
        kernel = self.kernel(fp1, fp2)
        D = self.metric.distance(fp1, fp2)

        p = np.sqrt(5) / self.scale
        first = - p * kernel / self.weight**2
        second = (p + 2 * D / 3 * p**2) * np.exp(- p * D)
        result = first + second

        return result * self.weight**2

    def kernel_hessian(self, fp1, fp2, metric=EuclideanDistance):
        '''
        Kernel hessian w.r.t. atomic coordinates in both 'fp1' and 'fp2'

                    d^2 k(x, x')
                    ------------
                     dx_i dx'_j
        '''
        kernel, D, dD_dr1, dD_dr2, C1 = self.common_hessian_terms(fp1, fp2)
        
        p = np.sqrt(5) / self.scale
        exp = np.exp(-p * D)
        dk_dD = self.dk_dD(fp1, fp2)
        d_dD_dk_dD = (-2 * p * dk_dD +
                      2 / 3 * p**2 * exp +
                      -p**2 * kernel)

        if D == 0:
            one_over_D_times_dk_dD = - 1 / 3 * p**2 * self.weight**2
        else:
            one_over_D_times_dk_dD = 1 / D * dk_dD

        C0 = ((d_dD_dk_dD - one_over_D_times_dk_dD) *
              np.einsum('ki,lj->klij', dD_dr1, dD_dr2))

        result = C0 - one_over_D_times_dk_dD * C1

        return result


class RationalQuad(BaseKernelType):
    '''
    Rational Quadratic kernel function.
    '''

    def __init__(self, alpha=0.5, **kwargs):
        '''
        alpha: float
            A weight factor for the continuum of length scales
        '''
        BaseKernelType.__init__(self)
        self.params.update({'alpha': alpha})

    @property
    def alpha(self):
        return self.params['alpha']

    def kernel(self, fp1, fp2):
        '''
        Kernel function between fingerprints 'fp1' and 'fp2'.
        '''
        d = self.metric.distance(fp1, fp2)
        k = self.weight**2 * (1 + d**2 / 2 / self.alpha /
                              self.scale**2)**(-self.alpha)
        return k

    def dk_dD(self, fp1, fp2):
        '''
        Derivative of kernel function w.r.t. distance function dk / dD
        '''
        D = self.metric.distance(fp1, fp2)

        p = - 2 * self.alpha / (2 * self.alpha * self.scale**2 + D**2)
        result = p * D * self.kernel(fp1, fp2)

        return result

    def kernel_hessian(self, fp1, fp2):
        '''
        Kernel hessian w.r.t. atomic coordinates in both 'fp1' and 'fp2'

                    d^2 k(x, x')
                    ------------
                     dx_i dx'_j
        '''
        kernel, D, dD_dr1, dD_dr2, C1 = self.common_hessian_terms(fp1, fp2)
        
        p = - 2 * self.alpha / (2 * self.alpha * self.scale**2 + D**2)

        C0 = ((1 + self.alpha**-1) * p**2 * D**2 *
              kernel * np.einsum('ki,lj->klij', dD_dr1, dD_dr2))

        result = C0 - p * kernel * C1

        return result
