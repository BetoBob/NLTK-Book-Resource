#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

# simulate_notebook.py 
#   This script is meant to simulate the Jupyter Notebook environment
#   on Google Colab, the environment for which litegrade is imported

from importlib import reload
import litegrade
litegrade = reload(litegrade)
from litegrade import begin, ask, handin
#from litegrade import hello_from_litegrade

#hello_from_litegrade()

student = begin("assignment A")

ask(student, "apples_question")
#ask(student, "cleverness_question")
ask(student, "Vertex Representation")

handin("assignment A", student)


