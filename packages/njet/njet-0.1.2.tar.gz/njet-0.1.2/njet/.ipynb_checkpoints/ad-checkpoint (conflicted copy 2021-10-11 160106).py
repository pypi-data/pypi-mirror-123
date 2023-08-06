'''    
    AD-Lib: Automatic Differentiation Library
    Copyright (C) 2021  Malte Titze

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


from .functions import exp, log
from .jet import jet as jet_source
from .poly import polynom


class jet(jet_source):    
    def __pow__(self, other):
        if not isinstance(other, jet):
            other = jet(value=other) # n.b. convert from ad.py would convert to 'jet_source', not jet'.

        if other.order == 0:
            result = jet_source.__pow__(self, other)
        else:
            '''
            General exponentiation, using exp and log functions.
            '''
            result = exp(other*log(self))
            result.graph = [(2, '**'), self.graph, other.graph]
        return result
    
    def __rpow__(self, other):
        if not isinstance(other, jet):
            other = jet(value=other) # n.b. convert from ad.py would convert to 'jet_source', not jet'.
        return other**self
    
    
class der:
    '''
    Class to handle the derivatives of a (jet-)function (i.e. a function consisting of a composition
    of elementary functions).
    '''
    
    def __init__(self, func, order=1, **kwargs):
        self.func = func
        self.order = self.set_order(order)
        
    def set_order(self, order):
        self.order = order
        
    def D(self, z)
        '''
        Compute the derivatives of a (jet-)function up to n-th order.

        Input
        -----
        z: vector at which the function and its derivatives should be evaluated.

        Returns
        -------
        The tensor components Df_k, k = 1, ..., n, each representing the coefficients of a multilinear map.

        This multilinear map corresponds to the k-th derivative of func: Let m be the number of 
        arguments of func. Then
          Df_k(z1, ..., zm) = sum_{j1 + ... + jm = k} Df[j1, ... jm] z1**j1 * ... * zm**jm
        with
          Df[j1, ..., jm] := \partial^j1/\partial_{z1}^j1 ... \partial^jm/\partial_{zm}^jm f .
        '''
        # perform the computation, based on the input vector
        n_args = self.func.__code__.co_argcount # the number of any arguments of func (before *args)
        inp = []
        for k in range(n_args):
            inp.append( jet([z[k], polynom(1, index=k, power=1)], n=order) )
        evaluate = self.func(*inp)
        
        # extract Df from the result
        Df = {}
        for k in range(1, order + 1): # the k-th derivative
            polynomials_k = evaluate.array(k).values
            fac = factorials(order)
            for key, value in polynomials_k.items(): # loop over the individual polynomials of the k-th derivative
                # key corresponds to a specific frozenset
                indices = [0]*n_args
                multiplicity = 1
                for tpl in key:
                    if tpl == (0, 0): # the (0, 0)-entries correspond to the scalar 1 and will be ignored here
                        continue
                    index, power = tpl
                    indices[index] = power
                    multiplicity *= fac[power]
                Df[tuple(indices)] = value/multiplicity
                
        return Df
    