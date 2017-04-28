from LightPipes import *

GridSize = 30*mm
GridDimension = 5
lambda_ = 500*nm #lambda_ is used because lambda is a Python build-in function.

Field = Begin(GridSize, lambda_, GridDimension)

print(Field)
