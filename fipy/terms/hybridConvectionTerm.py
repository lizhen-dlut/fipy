#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "hybridConvectionTerm.py"
 #                                    created: 12/5/03 {2:50:05 PM} 
 #                                last update: 1/16/04 {10:59:53 AM} 
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
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 # ###################################################################
 ##

from convectionTerm import ConvectionTerm
from variables.faceVariable import FaceVariable
import Numeric

class HybridConvectionTerm(ConvectionTerm):
    class Alpha(FaceVariable):
	def __init__(self, P):
	    FaceVariable.__init__(self, P.getMesh())
	    self.P = self.requires(P)
	    
	def calcValue(self):
	    eps = 1e-3
	    P  = self.P[:]

	    alpha = Numeric.where(                                 P > 2., (P - 1) / P,    0.)
	    alpha = Numeric.where( Numeric.logical_and(2. >= P, P >= -2.),         0.5, alpha)
	    alpha = Numeric.where(                               -2. >  P,      -1 / P, alpha)

	    self.value = alpha
