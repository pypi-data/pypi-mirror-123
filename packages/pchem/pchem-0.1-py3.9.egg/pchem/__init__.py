import sympy as sm

def solve(equation, variable, subs=None, unwrap=True):
    """Solve equation for the given variable; if given, a dictionary of subs
    (substitutions) can be given. This is useful if you want to solve numerically
    rather than symbolically. 
    
    Parameters:
    equation : the sympy equation to solve
    variable : the sympy variable to solve for
    subs : the dictionary of substitutions
    unwrap : if there is only one solution, return it directly rather than returning a list.
    
    Returns:
    The solution (if one solution and unwrap=True), or a list of all possible solutions.
    
    Examples: 
    >>> solve(a*x**2 + b*x + c, x)
        [(-b + sqrt(-4*a*c + b**2))/(2*a), -(b + sqrt(-4*a*c + b**2))/(2*a)]
        
    """
    if subs is not None:
        subs = copy(subs)
        subs.pop(variable.name, None)
        out = sm.solve(equation.subs(subs), variable)
    else:
        out = sm.solve(equation, variable)
    if unwrap and len(out) == 1:
        out = out[0]
    return out