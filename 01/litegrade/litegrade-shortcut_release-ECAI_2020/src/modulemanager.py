#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

# modulemanager.py 
#   This script manages all needed modules for litegrade.py, to increase 
#   organization and reduce import overhead

from importlib import reload
import commondriver
import questiondriver
import apidriver
commondriver = reload(commondriver)
questiondriver = reload(questiondriver)
apidriver = reload(apidriver)
from commondriver import print_err, safe_fopen
from questiondriver import hello_from_qdriver, get_nested_value
from apidriver import hand_in_assignment
