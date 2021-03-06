"""Implements polynomials as a list of coefficients, can perform most operations on them"""
import math
def trim_leading_zeroes(ints:list) -> list:
    """Get rid of leading zeroes in a list, returning a list"""
    output = []
    ignore_rest = False
    for item in ints:
        if ignore_rest:
            output.append(item)
            continue
        if item != 0:
            #as soon as it sees a nonzero item, it just appends the rest of the list to output.
            ignore_rest = True
            output.append(item)
    return output

def count_ending_zeroes(ints:list) -> list:
    """Counts the zeroes at the end of a list"""
    count = 0
    for item in reversed(ints):
        if item != 0:
            break
        #stops counting as soon as it hits a nonzero term
        count +=1
    return count

class Polynomial:
    """Implements a polynomial as a series of coefficients"""
    def __init__(self,*args,var="x"):
        """Instantiates a polynomial with a list of coefficients + an optional variable argument."""
        if len(args) == 0:
            raise Exception("Please supply at least one coefficient")

        if not all((type(coeff) in [int,float] for coeff in args)):
            #man, I like list comprehension. Only continues if every item in args is a number
            raise TypeError("Please only enter numerical coefficients")

        self.coefficients = trim_leading_zeroes(args)
        #drop leading zeroes
        #so that degree is calculated right
        #because leading zeroes are useless
        self.var = var
        self.deg = len(self.coefficients)-1

    def __repr__(self) -> str:
        """Converts a polynomial to a string form"""
        output = ""
        if len(self.coefficients) == 1:
            #Covers if it's just a constant
            return f"{self.coefficients[0]}"
        for ind,coeff in enumerate(self.coefficients):
            exp = self.deg - ind
            if coeff == 0:
                continue
                #don't write anything for 0 coefficients
            if coeff > 0 and coeff != 1:
                if ind == 0:
                    output += f"{coeff}"
                else:
                    output += f" + {coeff}"
                #positive coefficients
            elif coeff == 1:
                if ind != 0:
                    output += " + "
                if ind == (len(self.coefficients)-1):
                    output += "1"
                #Only shows 1 if it's a constant
            elif coeff < 0 and not coeff == -1:
                output += f" - {abs(coeff)}"
                #negative coefficients
            elif coeff == -1:
                output += " - "
                #-1
                if ind == (len(self.coefficients)-1):
                    output += "1"
                #-1 for constants
            if exp > 1:
                #Will only write an exponent if it's >1
                output += f"{self.var}^{exp}"
            elif exp == 1:
                output +=f"{self.var}"
        return output

    def __add__(self,other) -> "Polynomial":
        """Allows for addition with a constant or polynomial"""
        output = []
        if type(other) in [int,float]:
            output = self.coefficients
            output[-1] +=other
            return Polynomial(*output,var=self.var)
        #fills out the shorter list so they can line up
        if self.deg > other.deg:
            for i in range(1,(self.deg-other.deg+1)):
                other.coefficients.insert(0,0)
        if self.deg < other.deg:
            for i in range(1,(other.deg-self.deg+1)):
                self.coefficients.insert(0,0)
        for i in range(len(self.coefficients)):
            output.append(self.coefficients[i]+other.coefficients[i])
        return Polynomial(*output,var=self.var)

    def __sub__(self,other) -> "Polynomial":
        """Allows for subtraction"""
        output = []
        if type(other) in [int,float]:
            output = self.coefficients
            output[-1] -=other
            return Polynomial(*output,var=self.var)
        #Pretty much the same as addition with a sign flipped
        if self.deg > other.deg:
            for i in range(1,(self.deg-other.deg+1)):
                other.coefficients.insert(0,0)
        if self.deg < other.deg:
            for i in range(1,(other.deg-self.deg+1)):
                self.coefficients.insert(0,0)
        for i in range(len(self.coefficients)):
            output.append(self.coefficients[i]-other.coefficients[i])
        return Polynomial(*output,var=self.var)

    def __eq__(self,other) -> bool:
        """Allows for equality comparison with other polynomials"""
        #if the coefficients are the same, the polynomials are the same
        return self.coefficients == other.coefficients

    def __mul__(self,other) -> "Polynomial":
        """Allows for multiplication by a constant or another polynomial"""
        if type(other) in [int,float]:
            return Polynomial(*[i*other for i in self.coefficients],var=self.var)
            #mulitplies each coefficient by a constant
        output = [0]*(len(self.coefficients)+len(other.coefficients)-1)
        #distributes each term.
        for ind,coeff in enumerate(self.coefficients):
            for ind2, coeff2 in enumerate(other.coefficients):
                output[ind + ind2] += coeff*coeff2
        return Polynomial(*output,var=self.var)

    def __getitem__(self,index) -> int:
        """Returns the coefficient at a specified index"""
        return self.coefficients[index]

    def __len__(self) -> int:
        """Returns len of list of coefficients"""
        return len(self.coefficients)

    def __contains__(self,other : "Polynomial")  -> bool:
        """Checks if a polynomial is contained in another"""
        #Checks if an entire sequence of coefficients is contained
        return all(coeff in self.coefficients for coeff in other.coefficients)

    def __truediv__(self,other) -> "Polynomial":
        if type(other) in [float,int]:
            return Polynomial(*[i/other for i in self.coefficients],var=self.var)
        raise Exception("Sorry, polynomial division is annoying.\
         You can simplify the whole thing by a constant, though!")

    def __floordiv__(self,other) -> "Polynomial":
        if type(other) in [float,int]:
            return Polynomial(*[i//other for i in self.coefficients],var=self.var)
        raise Exception("Sorry, polynomial division is annoying.\
         You can simplify the whole thing by a constant, though!")

    def compute(self,x_val) -> float:
        """Will compute f(x) for a given x"""
        output = 0.0
        for ind,coeff in enumerate(self.coefficients):
            output += coeff * x_val**(self.deg-ind)
            #iterates through the coefficients and does the powers based on their index
        return output

    def get_roots(self,zero_root:bool=False)  -> str:
        """Will find the *real* roots of a Polynomial or higher degree with <=1 zero root(s)"""
        if zero_root:
            #zero_root is only true if a higher degree polynomial has been simplified
            zero = "and (0.0,0.0)"
        else:
            zero = ""
        if self.deg == 2:
            a_coeff = self.coefficients[0]
            b_coeff = self.coefficients[1]
            c_coeff = self.coefficients[2]
            disc = b_coeff**2 - 4*a_coeff*c_coeff
            #If this is negative, the number will have non real roots
            if disc == 0:
                return f"Root at({(-1*b_coeff)/(2*a_coeff)},0.0) {zero}"
            #ignore the discriminant if it's zero, so only one root
            if disc < 0:
                raise Exception("Sorry, this is too complex for me. No real roots")
                #Don't want to deal with complex numbers
                #Ba-dump-tiss
            return f"Roots at({round((((-1*b_coeff) + math.sqrt(disc))/(2*a_coeff)),3)},0.0) \
            and ({round((((-1*b_coeff) - math.sqrt(disc))/(2*a_coeff)),3)},0.0) {zero}"
              #Just solves the quadratic formula both ways
        if (self.deg-2) == count_ending_zeroes(self.coefficients):
            output =  Polynomial(*self.coefficients[:-(count_ending_zeroes(self.coefficients))])
            return output.get_roots(zero_root = True)
        if self.deg == 1:
            return f"Zero at ({(-1*self.coefficients[-1])/self.coefficients[0]},0.0)"
            #if it can't be simplified to a quadratic and a zero term
        raise Exception("Sorry, degree too high.")
    def get_parabola_vertex(self):
        if self.deg != 2:
            raise ValueError("Only parabolas have a single vertex")
        vertex_x = -self.coefficients[1]/(2*self.coefficients[0])
        return f"Vertex at ({vertex_x},{self.compute(vertex_x)})"
    def get_parabola_vertex(self):
        if self.deg != 2:
            raise ValueError("Only parabolas have a single vertex")
        vertex_x = -self.coefficients[1]/(2*self.coefficients[0])
        return f"Vertex at ({vertex_x},{self.compute(vertex_x)})"





if __name__ == "__main__":
    x = Polynomial(5,3,1)
    print(x.coefficients,x,sep="\n")