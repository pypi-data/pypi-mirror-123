import time
from scipy.optimize import minimize
import numpy as np
from ase.parallel import paropen


class HyperparameterFitter:

    @classmethod
    def fit(cls, model, params_to_fit, fit_weight=True, pd=None,
            bounds=None, tol=1e-2, txt='mll.txt'):
        '''
        Fit hyperparameters that are allowed to fit
        based on maximum log likelihood of the data in gp.
        '''
        gp = model.gp

        txt = paropen(txt, 'a')
        txt.write('\n{:s}\n'.format(20 * '-'))
        txt.write('{}\n'.format(time.asctime()))
        txt.write('Number of training points: {}\n'.format(len(gp.X)))

        arguments = (model, params_to_fit, fit_weight, pd, txt)

        params = []

        # In practice, we optimize the logarithms of the parameters:
        for string in params_to_fit:
            params.append(np.log10(gp.hp[string]))

        t0 = time.time()

        result = minimize(cls.neg_log_likelihood,
                          params,
                          args=arguments,
                          method='Nelder-Mead',
                          options={'fatol': tol})

        txt.write("Time spent minimizing neg log likelihood: "
                  "{:.02f} sec\n".format(time.time() - t0))

        converged = result.success

        # collect results:
        optimalparams = {}
        powered_results = np.power(10, result.x)
        for p, pstring in zip(powered_results, params_to_fit):
            optimalparams[pstring] = p

        gp.set_hyperparams(optimalparams)
        gp.train(gp.X, gp.Y)

        txt.write('{} success: {}\n'.format(str(gp.hp), converged))
        txt.close()

        return model

    @staticmethod
    def neg_log_likelihood(params, *args, fit_weight=True):

        model, params_to_fit, fit_weight, prior_distr, txt = args
        gp = model.gp

        params_here = np.power(10, params)

        txt1 = ""
        paramdict = {}
        for p, pstring in zip(params_here, params_to_fit):
            paramdict[pstring] = p
            txt1 += "{:18.06f}".format(p)

        gp.set_hyperparams(paramdict)
        gp.train(gp.X, gp.Y)

        if fit_weight:
            GPPrefactorFitter.fit(model)

        # Compute log likelihood
        logP = gp.logP()

        # Prior distribution:
        if prior_distr is not None:
            logP += prior_distr.get(gp=gp)

        # Don't let ratio fall too small, resulting in numerical
        # difficulties:
        if 'ratio' in params_to_fit:
            ratio = params_here[params_to_fit.index('ratio')]
            if ratio < 1e-6:
                logP -= (1e-6 - ratio) * 1e6

        txt.write('Parameters: {:s}       -logP: {:12.02f}\n'
                  .format(txt1, -logP))
        txt.flush()

        return -logP


class GPPrefactorFitter:

    @staticmethod
    def fit(model):
        
        gp = model.gp

        oldvalue = gp.hp['weight']

        y = np.array(gp.Y).flatten()
        factor = np.sqrt(np.dot(y - gp.prior_array, gp.model_vector) / len(y))

        newvalue = factor * oldvalue
        gp.set_hyperparams({'weight': newvalue})

        # Rescale accordingly ("re-train"):
        gp.model_vector /= factor**2
        gp.L *= factor  # lower triangle of Cholesky factor matrix
        gp.K *= factor**2

        return model
