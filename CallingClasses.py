# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:33:16 2020

@author: srb119
"""

import SeismicityProgramv200 as SP
import numpy as np

'''
DesignResponseSpectrum(Ground Type = [A,B,C,D or E depending on the soil conditions v30 waves], 
                       Curve Type = [1 or 2 depending on size of earthquake expected], 
                       agR = [maximum expected ground acceleration measured at site], 
                       q = [non-linear q factor, to be derived based on EC8 recommendations], 
                       W1 = [Weight of floor 1 (lower)], 
                       W2 = [Weight of floor 2 (middle)], 
                       W3 = [Weight of floor 3 (top)],
                       h1 = [Height of lower floor], 
                       h2 = [Height of middle floor],
                       h3 = [Height of top floor], 
                       IM = [This is a passed argument, default III, structure's functional importance], 
                       damping= [Default damping is 5% (specify in %)], 
                       beta = [Default value is 0.2])

PlotSpectrum([No arguments required just building the Spectrum])

~~~~ONE OF THOSE TWO FUNCTIONS SHOULD BE USED IN ORDER TO ESTIMATE THE NATURAL PERIOD OF THE STRUCTURE~~~~

PeriodEstimation([MFS = Moment Frame Steel Structure, 
                  MFC = for Moment Frame Concrete Structure
                  ECBFS = for Eccentrically Braced Frame Steel Structure])

PeriodEstimate2(d = parameter the lateral displacement of a structure
                 with applied gravity loading (1.0*g) in the lateral direction and outputs
                 the natural period (in s))
 
PlotSpectrum(NPeriod = Default value is equal to None, in such a case the Period Estimate is taken from above,
             in other cases where the NPeriod is taken from somewhere else (like Eigenvalue Analysis) assign the value in (sec))

BaseShear([No arguments required, all of the arguments are specified in the __init__ function])

PostProcessChecks(Medf = Maximum Applied Moment for any floor beam
                  Nedf = Maximum Applied Axial force for any floor beam
                  Vedf = Maximum Applied Shear force for any floor beam
                  Medr = Maximum Applied Moment force for any roof beam
                  Nedr = Maximum Applied Axial force for any roof beam 
                  Vedr = Maximum Applied Shear force for any roof beam):
 
ServicibilityChecks(ds1 = Interstorey drift for floor 1
                    ds2 = Interstorey drift for floor 2
                    ds3 = Interstorey drift for floor 3
                    state = "Brittle"):

'''


C2 = SP.DesignResponseSpectrum("B", 1, 0.25*9.81, 1.0,320*10**3, 320*10**3, 268.8*10**3, 4.5, 3, 3, IM = "II")
C2.PlotSpectrum()
C2.PeriodEstimation("ECBFS")
C2.CalculatePGA()
C2.BaseShear()
C2.PostProcessChecks(146500.0, 273600.0, 309900.0, 54810.0, 109700.0, 82890.0)
C2.ServicibilityChecks(5.48, 2.56, 1.81)


'''
for j in ["A", "B", "C", "D", "E"]:
    for i in [1,2]:
        for k in np.arange(0.1*9.81, 1.0*9.81, 0.4*9.81):
            for m in [1,2,3,4,5]:
                for q in [1, 2, 3, 4, 5, 6]:
                    C1 = SP.DesignResponseSpectrum(j, i, k, q,441*10**3, 441*10**3, 333*10**3, m, m, m, IM = "III")
                    C1.PlotSpectrum()
                    C1.PeriodEstimation("MFS")
                    C1.CalculatePGA()
                    C1.BaseShear()
                    C1.PostProcessChecks(71.7*10**3, 7.28*10**3, 142*10**3, 39.4*10**3, 11.5*10**3, 61*10**3)
                    C1.ServicibilityChecks(4.5, 5.2, 4.0)
                    
'''


C3 = SP.DesignResponseSpectrum("B", 1, 0.25*9.81, 6, 320*10**3, 320*10**3, 268.8*10**3, 4.5, 3, 3, IM = "II")
C3.PlotSpectrum()
C3.PeriodEstimation("ECBFS")
C3.CalculatePGA()
C3.BaseShear()
C3.PostProcessChecks(146500.0, 273600.0, 309900.0, 54810.0, 109700.0, 82890.0)
C3.ServicibilityChecks(5.48, 2.56, 1.81)

