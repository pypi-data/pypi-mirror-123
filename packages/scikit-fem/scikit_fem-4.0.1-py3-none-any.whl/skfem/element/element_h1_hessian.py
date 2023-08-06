import numpy as np

from .element import Element
from .discrete_field import DiscreteField


class ElementH1Hessian(Element):
    """Variant of :class:`skfem.element.ElementH1` with second derivatives."""

    def gbasis(self, mapping, X, i, tind=None):
        """Identity transformation."""
        phi, dphi, ddphi = self.lbasis(X, i)
        invDF = mapping.invDF(X, tind)
        if len(X.shape) == 2:
            return (DiscreteField(
                value=np.broadcast_to(phi, (invDF.shape[2], invDF.shape[3])),
                grad=np.einsum('ijkl,il->jkl', invDF, dphi),
                hess=np.einsum('kilm,jilm,kjm->ijlm', invDF, invDF, ddphi),
            ),)
        elif len(X.shape) == 3:
            return (DiscreteField(
                value=np.broadcast_to(phi, (invDF.shape[2], invDF.shape[3])),
                grad=np.einsum('ijkl,ikl->jkl', invDF, dphi),
                hess=np.einsum('kilm,jilm,kljm->ijlm', invDF, invDF, ddphi),
            ),)

    def lbasis(self, X, i):
        raise Exception("ElementH1.lbasis method not found.")
