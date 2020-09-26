"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from inspect import getmembers
from types import FunctionType
from typing import Callable, List


def get_module_functions(module) -> List[Callable]:
    """
    Get all the functions from a module.

    Returns:
        a list with references to the functions in the module
    """
    members = getmembers(module)

    return [fun[1] for fun in filter(lambda m: isinstance(m[1], FunctionType), members)]


def generate_individual():
    pass
