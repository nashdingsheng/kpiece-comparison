import sys
sys.path.append('../src/')
from openravepy import Environment, RaveCreateCollisionChecker
from MyKPIECE1 import *
import numpy as np
import time
import random


NDOF = int(raw_input('Please enter ndof: '))
THRESHOLD = 0.05
PROJECTION_CHOICE = 3
CELLSIZE = 0.1
DISTANCE_WEIGHT = 0.5 # this value is for q
PROPAGATION_STEPSIZE = 0.5
GOAL_BIAS = 0.1
RP_DIM = 3 # dimension of the random projecting space

description = {0: 'NDOF', 1: 'THRESHOLD', 2: 'PROJECTION_CHOICE', 
               3: 'CELLSIZE', 4: 'PROPAGATION_STEPSIZE', 5: 'GOAL_BIAS', 
               6: 'RANDOM_PROJ_DIM', 7: 'running time', 8: 'success rate', 
               9: 'MAX_RUNNING_TIME', 10: 'N_RUNS'}


env = Environment()
env.SetViewer('qtcoin')
env.Load('../../robots/denso_base.xml')
robot = env.GetRobots()[0]

startvect = np.zeros(2 * NDOF)
goalvect = np.hstack((np.ones(NDOF), np.zeros(NDOF)))

N_RUNS = 30
max_running_time = 300.
T = []
for i in range(N_RUNS):
    print "Iteration {0}".format(i + 1)
    ss = Plan(robot, startvect, goalvect, max_running_time, 
              threshold = THRESHOLD, 
              projection_choice = PROJECTION_CHOICE, 
              cellsize = CELLSIZE,
              distance_weight = DISTANCE_WEIGHT,
              propagation_stepsize = PROPAGATION_STEPSIZE, 
              goal_bias = GOAL_BIAS,
              rp_dim = RP_DIM, 
              N = NDOF)

    if ss.haveExactSolutionPath():
        T.append(ss.getLastPlanComputationTime())

good = len(T)/float(N_RUNS) # success rate

T.sort()
# Remove the best and the worst
T.pop(0)
T.pop(len(T) - 1)
avgtime = sum(T)/float(len(T))


print "==================== INFO ===================="
print "ndof                 = {0}".format(NDOF)
print "THRESHOLD            = {0}".format(THRESHOLD)
print "PROJECTION_CHOICE    = {0}".format(PROJECTION_CHOICE)
print "CELLSIZE             = {0}".format(CELLSIZE)
print "PROPAGATION_STEPSIZE = {0}".format(PROPAGATION_STEPSIZE)
print "GOAL_BIAS            = {0}".format(GOAL_BIAS)
print "=============================================="

print "Success rate = {0}%".format(100.*good)
print "Average running time = {0} s.".format(avgtime)

data = np.array([NDOF, 
                 THRESHOLD, 
                 PROJECTION_CHOICE, 
                 CELLSIZE, 
                 PROPAGATION_STEPSIZE, 
                 GOAL_BIAS, 
                 RP_DIM, 
                 avgtime, 
                 good, 
                 max_running_time, 
                 N_RUNS])

import os.path
import pickle
FILENAME = 'KPIECE1.data'
raw_input('Press any key to write the data to KPIECE1.data')
if not os.path.isfile(FILENAME):
    with open(FILENAME, 'w') as f:
        pickle.dump([description, data], f, pickle.HIGHEST_PROTOCOL)
else:
    with open(FILENAME, 'r') as f:
        [des, dat] = pickle.load(f)
    dat = np.vstack((dat, data))
    with open(FILENAME, 'w') as f:
        pickle.dump([des, dat], f, pickle.HIGHEST_PROTOCOL)


"""
sol = ss.getSolutionPath()
sol.interpolate()
M = sol.printAsMatrix()
M = M.strip().split('\n')
raw_input('Press any key to visualize the solution')
for i in range(len(M)):
    w = M[i]
    w1 = [float(s) for s in w.split()]
    if NDOF < 6:
        robot.SetDOFValues(np.hstack((w1[0:NDOF], np.zeros(6 - NDOF))))
    else:
        robot.SetDOFValues(w1[0:6])
    time.sleep(0.1)

si = ss.getSpaceInformation()
g = ss.getGoal().getState()
f = sol.getStates()[-1]
print "Running time: {0} s.".format(ss.getLastPlanComputationTime())
print "Threshold = {0}".format(THRESHOLD)
print "Distance to goal = {0}".format(si.distance(f, g))

"""
