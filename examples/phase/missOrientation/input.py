#!/usr/bin/env python

## 
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/10/03 {3:23:47 PM}
 #                                last update: 1/16/04 {10:55:13 AM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

from __future__ import nested_scopes

from meshes.grid2D import Grid2D
from examples.phase.phase.type1PhaseEquation import Type1PhaseEquation
from solvers.linearPCGSolver import LinearPCGSolver
from boundaryConditions.fixedValue import FixedValue
from boundaryConditions.fixedFlux import FixedFlux
from iterators.iterator import Iterator
from examples.phase.theta.modularVariable import ModularVariable
from variables.cellVariable import CellVariable
from viewers.grid2DGistViewer import Grid2DGistViewer

class PhaseSystem:
   def __init__(self):
      self.steps = 100
      timeStepDuration = 0.02
   
      phaseParameters={
         'tau' :        0.1,
         'time step duration' : timeStepDuration,
         'epsilon' :    0.008,
         's' :          0.01,
         'alpha' :      0.015,
         'c2':          0.0,
         'anisotropy':  0.,
         'symmetry':    4.
         }
      
      valueLeft=1.
      valueRight=1.
      
      dx = self.L / self.nx
      dy = self.L / self.ny
      
      mesh = Grid2D(dx, dy, self.nx, self.ny)
      
      self.var = CellVariable(
         name = 'PhaseField',
         mesh = mesh,
         value = 1.
         )
      
      theta = ModularVariable(
         name = 'Theta',
         mesh = mesh,
         value = self.thetaValue,
         hasOld = 0
         )
      
      rightCells = mesh.getCells(self.func)

      theta.setValue(self.thetaFuncValue,rightCells)
      
      fields = {
         'temperature' : 1.,
         'theta' : theta
         }            
      
      eq = Type1PhaseEquation(
         self.var,
         solver = LinearPCGSolver(
         tolerance = 1.e-15, 
         steps = 1000
         ),
         boundaryConditions=(),
         fields = fields,
         parameters = phaseParameters
         )

      self.it = Iterator((eq,))

      self.parameters = {
         'steps'  : self.steps,
         'var'    : self.var,
         'it'     : self.it
         }
        
   def getParameters(self):
      return self.parameters
      
   def run(self):
      self.it.timestep(self.steps)      
      viewer = Grid2DGistViewer(self.var)      
      viewer.plot()
      raw_input()
   

