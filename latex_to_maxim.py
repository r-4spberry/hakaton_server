from sympy.parsing.latex import parse_latex
from sympy import symbols, Add, Mul, Pow, Integral, log
from sympy import E, Pow


def sympy_to_custom(expr):
    """
    Recursively converts a SymPy expression into your custom grammar format.
    """
    if expr.is_Number:
        return f"num({expr})"
    elif expr.is_Symbol:
        return f"var({expr})"
    elif expr == E:  # Handle Euler's number
        return "num(E)"
    elif isinstance(expr, Add):
        args = ", ".join(sympy_to_custom(arg) for arg in expr.args)
        return f"sum({args})"
    elif isinstance(expr, Mul):
        # Handle fractions like a * b**-1
        numerators = []
        denominators = []
        for arg in expr.args:
            if (
                isinstance(arg, Pow) and arg.exp == -1
            ):  # Negative exponent -> denominator
                denominators.append(sympy_to_custom(arg.base))
            else:  # Otherwise, it's a numerator
                numerators.append(sympy_to_custom(arg))
        if denominators:  # If there are denominators, it's a fraction
            numer = (
                "mul(" + ", ".join(numerators) + ")"
                if len(numerators) > 1
                else numerators[0]
            )
            denom = (
                "mul(" + ", ".join(denominators) + ")"
                if len(denominators) > 1
                else denominators[0]
            )
            return f"fraq({numer}, {denom})"
        else:  # Otherwise, it's just a product
            args = ", ".join(sympy_to_custom(arg) for arg in expr.args)
            return f"mul({args})"
    elif isinstance(expr, Pow):
        base, exp = expr.args
        if exp == -1:
            return f"fraq(num(1), {sympy_to_custom(base)})"
        return f"pow({sympy_to_custom(base)}, {sympy_to_custom(exp)})"
    elif isinstance(expr, Integral):
        integrand, *bounds = expr.args
        if len(bounds) == 2:  # Definite integral
            return f"integral({sympy_to_custom(integrand)}, {sympy_to_custom(bounds[0])}, {sympy_to_custom(bounds[1])})"
        else:  # Indefinite integral
            return f"integral({sympy_to_custom(integrand)}, var(x), var(x))"  # Adjust for indefinite
    elif isinstance(expr, log):
        arg, base = expr.args
        print(arg, base)
        return f"log({sympy_to_custom(arg)}, {sympy_to_custom(base)})"
    elif expr.is_Rational:  # Handle simple fractions
        return f"fraq(num({expr.p}), num({expr.q}))"
    else:
        raise ValueError(f"Unsupported SymPy expression: {expr}")


# Example usage
if __name__ == "__main__":
    latex_input = r"\lim_{x\to\infty} f(x)"  # Replace with your LaTeX input
    sympy_expr = parse_latex(latex_input)
    grammar_expr = sympy_to_custom(sympy_expr)

    print("SymPy Expression:", sympy_expr)
    print("Custom Grammar Format:", grammar_expr)
