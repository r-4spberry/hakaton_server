import pytest
from sympy.parsing.latex import parse_latex
from latex_to_maxim import (
    sympy_to_custom,
)  # Replace with the actual module name where the function is defined


@pytest.mark.parametrize(
    "latex_input, expected_output",
    [
        # Basic Fractions
        (r"\frac{1}{2}", "fraq(num(1), num(2))"),
        (r"\frac{a}{b}", "fraq(var(a), var(b))"),
        (r"\frac{a \cdot c}{b}", "fraq(mul(var(a), var(c)), var(b))"),
        (r"\frac{\left(a + b\right)}{c}", "fraq(sum(var(a), var(b)), var(c))"),
        # MultiplicationsЗ
        (r"a \cdot b", "mul(var(a), var(b))"),
        (r"a \times b", "mul(var(a), var(b))"),
        (
            r"\frac{a \cdot b}{c \cdot d}",
            "fraq(mul(var(a), var(b)), mul(var(c), var(d)))",
        ),
        # Summations
        (r"a + b + c", "sum(sum(var(a), var(b)), var(c))"),
        (r"\left(a + b\right)", "sum(var(a), var(b))"),  # Wrapped in parentheses
        # Powers
        (r"a^b", "pow(var(a), var(b))"),
        (r"\left(a + b\right)^c", "pow(sum(var(a), var(b)), var(c))"),
        (r"a^{b + c}", "pow(var(a), sum(var(b), var(c)))"),
        # Nested Operations
        (r"\frac{a + b}{c + d}", "fraq(sum(var(a), var(b)), sum(var(c), var(d)))"),
        (r"a \cdot b + c", "sum(mul(var(a), var(b)), var(c))"),
        (
            r"\left(\frac{a}{b}\right) + \frac{c}{d}",
            "sum(fraq(var(a), var(b)), fraq(var(c), var(d)))",
        ),
        # Constants and Functions
        (r"\log{x}", "log(var(x), num(E))"),
        (r"\frac{\log{x}}{z}", "fraq(log(var(x), num(E)), var(z))"),
        (r"e^x", "pow(var(e), var(x))"),
        # Stress Tests
        (
            r"\frac{\left(a^b + c\right) \cdot d}{e \cdot f + g}",
            "fraq(mul(sum(pow(var(a), var(b)), var(c)), var(d)), sum(mul(var(e), var(f)), var(g)))",
        ),
        (
            r"\frac{\frac{a}{b}}{\frac{c}{d}}",
            "fraq(fraq(var(a), var(b)), fraq(var(c), var(d)))",
        ),
    ],
)
def test_sympy_to_custom(latex_input, expected_output):
    """
    Test conversion of LaTeX to custom grammar format.
    """
    sympy_expr = parse_latex(latex_input)
    result = sympy_to_custom(sympy_expr)
    assert result == expected_output, f"Failed for input: {latex_input}"
