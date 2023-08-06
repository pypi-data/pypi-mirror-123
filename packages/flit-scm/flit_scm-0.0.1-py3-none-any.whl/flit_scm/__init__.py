from flit_core import buildapi # Make Flit's build backend available as "flit_scm:buildapi"
from setuptools_scm import get_version
import toml


setuptools_scm_config = toml.load('pyproject.toml')['tool']['setuptools_scm']
get_version(**setuptools_scm_config)
