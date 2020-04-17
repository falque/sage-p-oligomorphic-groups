
####################################################

from sage.structure.parent import Parent
from sage.rings.infinity import Infinity
from sage.libs.gap.element import GapElement as LibGapElement
import sage

class PoligomorphicGroup(Parent):
    
    def cardinality(self):
        return Infinity

    def order(self):
        return Infinity

    def degree(self):
        return Infinity

    def is_finite(self):
        return False

    def is_highly_homogeneous(self):
        # default
        return False
        
    def profile_series(self, variable='z'):
        # return the generating series of the orbital profile
        pass

    @cached_method
    def _series(self):
        # used to compute values of the profile without recomputing
        var('v')
        return self.profile_series(v)

    def profile_first_values(self, n):
        # for visual appreciation of the first values
        return (self._series().series(v, n+1)).coefficients(v, sparse=False)
    
    def profile(self, n):
        # return series coefficient
        return (self.profile_series(v).series(v, n+1)).coefficients(v, sparse=False)[n]

    def nice_factorization_series(self, variable='z', print_facto=False):
        # Return a "combinatorial" factorization of the profile series
        bound_on_degree = self.diagonal_action().degree()
        # bound_on_degree : higher bound for the degree of generators in the
        #                   orbit algebra (will be the degree of the finite
        #                   diagonal action)
        from sage.rings.integer_ring import ZZ
        if isinstance(variable, str):
            R = PolynomialRing(ZZ, Integer(1), order = 'neglex', names=(variable,))
            (variable,) = R._first_ngens(1)
            # in theory equivalent to R.<z> = PolynomialRing(ZZ, 1, order = 'neglex')
            # but preparsed so it is accepted in a function
            # (something like z = PolynomialRing(ZZ, order='neglex') just won't work
            # in the sense that the printing of the series will not follow the specified order)
        z = variable
        series = self.profile_series(z)
        return nice_factorization(series, bound_on_degree, print_facto)
        
    def kernel(self):
        pass
    
    @abstract_method
    def orbit_representatives(self, n):
        pass
    
    @abstract_method
    def orbit_orbitalgebra(self):
        pass
    
    #def lattice_of_potential_finite_synchronizations(self):

    def add_to_kernel_indep(self, finite_group):
        return DirectProductOfPoligomorphicGroups([self, finite_group])

    def add_wreath_on_finite_blocks(self, finite_group):
        new_wreath = WreathProductFiniteBlocks(finite_group)
        return DirectProductOfPoligomorphicGroups([self, new_wreath])

    def add_wreath_on_infinite_blocks(self, highly_homogeneous_group, action_on_blocks):
        new_wreath = WreathProductInfiniteBlocks(highly_homogeneous_group, action_on_blocks)
        return DirectProductOfPoligomorphicGroups([self, new_wreath])

        
class HighlyHomogeneousGroup(PoligomorphicGroup):
    def profile_series(self, variable='z'):
        from sage.rings.integer_ring import ZZ

        if isinstance(variable, str):   # creation or recuperation of the variable
            variable = ZZ[variable].gen()
        z = variable
        return 1 / (1-z)
    
    def profile(self, n):
        return 1

    def is_highly_homogeneous(self):
        return True

    def restriction_to_finite_block(self):
        return PermutationGroup_generic([], domain = [1])

    def kernel(self):
        return []

    def retriction_to_kernel(self):
        return PermutationGroup([])
    
    
class AutQQ(HighlyHomogeneousGroup, UniqueRepresentation):  # 2 instances will be considered equal
    def _repr_(self):
        return "The group of automorphisms of the rational chain Aut(QQ)"
    
    def _latex_(self):
        return r"\DeclareMathOperator{\Aut}{Aut} \Aut(\mathbb{Q})"

class RevQQ(HighlyHomogeneousGroup, UniqueRepresentation):
    def _repr_(self):
        return r"The group Rev(QQ) generated by the automorphisms of the rational chain and one reflection"
    
    def _latex_(self):
        return r"\DeclareMathOperator{\Rev}{Rev} \Rev(\mathbb{Q})"
    
class AutQQCircle(HighlyHomogeneousGroup, UniqueRepresentation):
    def _repr_(self):
        return r"The group of automorphisms of the rational circle Aut(QQ/ZZ)"
    
    def _latex_(self):
        return r"\DeclareMathOperator{\Aut}{Aut} \Aut(\mathbb{Q}/\mathbb{Z})"
    
class RevQQCircle(HighlyHomogeneousGroup, UniqueRepresentation):
    def _repr_(self):
        return r"The group Rev(QQ/ZZ) generated by the automorphisms of the rational circle and one reflection"

    def _latex_(self):
        return r"\DeclareMathOperator{\Rev}{Rev} \Rev(\mathbb{Q}/\mathbb{Z})"

class SymInfinity(HighlyHomogeneousGroup, UniqueRepresentation):
    def _repr_(self):
        return "The closed infinite symmetric group S_infinity"
    
    def _latex_(self):
        return r"\mathfrak{S}_\infty"

