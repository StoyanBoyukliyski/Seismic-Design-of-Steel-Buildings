# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:50:20 2020

@author: srb119
"""



import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


#_______________________DESIGN SPECTRUM FOR ELASTIC ANALSIS______________________

#Gtype = [A, B, C, D, E]
#Stype = [1, 2]
#agR = 0.25
#imp = 1 (Default)
#damping = 5% (default)


class DesignResponseSpectrum():
    def __init__(self, Gtype, Stype, agR, q, W1, W2, W3, h1, h2, h3, IM = "II", damping= 5, beta = 0.2):
        self.beta = beta
        self.Gtype = Gtype
        self.Stype = Stype
        self.q = q
        self.W1 = W1
        self.W2 = W2 
        self.W3 = W3
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.path = "H:\Desktop\StoyanBoyukliysiMSc\SeismicDesign"
        if IM == "I":
            self.imp = 0.8
            self.v = 0.5
        elif IM == "II":
            self.imp = 1.0
            self.v = 0.5
        elif IM == "III":
            self.imp = 1.2
            self.v= 0.4
        elif IM == "IV":
            self.imp = 1.4
            self.v = 0.4
        else:
            pass
        self.ag= agR*self.imp
        
        if Stype == 1:
            if Gtype == "A":
                self.S = 1.0
                self.Tb = 0.15
                self.Tc = 0.4
                self.Td = 2
            elif Gtype == "B":
                self.S = 1.2
                self.Tb = 0.15
                self.Tc = 0.4
                self.Td = 2.0
            elif Gtype == "C":
                self.S = 1.15
                self.Tb = 0.2
                self.Tc = 0.6
                self.Td = 2.0
            elif Gtype == "D":
                self.S = 1.35
                self.Tb = 0.2
                self.Tc = 0.8
                self.Td = 2.0
            elif Gtype == "E":
                self.S = 1.4
                self.Tb = 0.15
                self.Tc = 0.5
                self.Td = 2.0
            else:
                pass
        elif Stype == 2:
            if Gtype == "A":
                self.S = 1.0
                self.Tb = 0.05
                self.Tc = 0.25
                self.Td = 1.2
            elif Gtype == "B":
                self.S = 1.35
                self.Tb = 0.05
                self.Tc = 0.25
                self.Td = 1.2
            elif Gtype == "C":
                self.S = 1.5
                self.Tb = 0.1
                self.Tc = 0.25
                self.Td = 1.2
            elif Gtype == "D":
                self.S = 1.8
                self.Tb = 0.1
                self.Tc = 0.3
                self.Td = 1.2
            elif Gtype == "E":
                self.S = 1.6
                self.Tb = 0.05
                self.Tc = 0.25
                self.Td = 1.2
            else:
                pass
        else:
            pass
            
        self.n = np.sqrt(10/(5+damping))
        if self.n >= 0.55:
            self.n = 0.55
        else:
            pass
        
    
    #Period Estimations of Steel and Concrete Structures EC8
    
    '''
    This function takes in the height and type of the building and returns
    the natural period defined by Eurocode 8
    
    MFS for Moment Frame Steel Structure
    MFC for Moment Frame Concrete Structure
    ECBFS for Eccentrically Braced Frame Steel Structure
    '''


    def PeriodEstimation(self,strtype):
        if strtype == "MFS":
            Ct = 0.085
        elif strtype == "MFC":
            Ct = 0.075
        elif strtype == "ECBFS":
            Ct = 0.075
        else:
            Ct = 0.050
        self.natperiod= Ct*(self.h1 + self.h2 + self.h3)**(3/4)


    '''
    This function takes as parameter the lateral displacement of a structure
    with applied gravity loading (1.0*g) in the lateral direction and outputs
    the natural period (in s)
    '''


    def PeriodEstimate2(self,d):
        self.natperiod = 2*np.sqrt(d)
        
    '''
    Develop the plastic response spectrum given specific factors describing the site, 
    structural type and importance. Once the curve is created the natural period
    is taken as input and the peak ground acceleration is taken as output.
    '''
        
    def PlotSpectrum(self, NPeriod = None):
        if NPeriod != None:
            self.natperiod = NPeriod
        else:
            pass
        self.ResponseSpectrum = []
        self.Period = []            
        for j in np.arange(0.0, 4.0, 0.001):
            if j> 0 and j <=self.Tb:
                Sd = self.ag*self.S*(2/3+(j/self.Tb)*(2.5/self.q-2/3))
                self.ResponseSpectrum.append(Sd)
                self.Period.append(j)
            elif j> self.Tb and j <= self.Tc:
                Sd = self.ag*self.S*2.5/self.q
                self.ResponseSpectrum.append(Sd)
                self.Period.append(j)
            elif j>self.Tc and j<=self.Td:
                Sd = self.ag*self.S*2.5/self.q*(self.Tc/j)
                if Sd < self.beta*self.ag:
                    Sd = self.beta*self.ag
                else:
                    pass
                self.ResponseSpectrum.append(Sd)
                self.Period.append(j)
            elif j>self.Td:
                Sd = self.ag*self.S*2.5/self.q*(self.Tc*self.Td/j**2)
                if Sd<self.beta*self.ag:
                    Sd = self.beta*self.ag
                else:
                    pass
                self.ResponseSpectrum.append(Sd)
                self.Period.append(j)
            else:
                pass
        
        self.RESPONSE = pd.DataFrame({"Period (s)": self.Period,
                                 "PGA (m/s**2)": self.ResponseSpectrum})
        self.RESPONSE.to_csv(self.path + "/PlasticReponseSpectrum" + "S" + str(self.Stype) + "G" + str(self.Gtype) + "a" + str(self.ag) + "q" + str(self.q) + "h" + str(self.h1) + "im" + str(self.imp) + ".csv")
        plt.plot(self.Period, self.ResponseSpectrum, label = "Curve No " + "S" + str(self.Stype) + "G" + str(self.Gtype) + "a" + str(self.ag) + "q" + str(self.q) + "h" + str(self.h1) + "im" + str(self.imp))
        plt.legend()
        plt.xlabel("Period (s)")
        plt.ylabel("PGA (m/s^2)")
        #plt.show()
    
    def CalculatePGA(self):
        self.T = self.natperiod
        if self.T> 0 and self.T <=self.Tb:
            self.Sd = self.ag*self.S*(2/3+(self.T/self.Tb)*(2.5/self.q-2/3))
        elif self.T> self.Tb and self.T <= self.Tc:
            self.Sd = self.ag*self.S*2.5/self.q
            
        elif self.T>self.Tc and self.T<=self.Td:
            self.Sd = self.ag*self.S*2.5/self.q*(self.Tc/self.T)
            if self.Sd < self.beta*self.ag:
                self.Sd = self.beta*self.ag
            else:
                pass
        elif self.T>self.Td:
            self.Sd = self.ag*self.S*2.5/self.q*(self.Tc*self.Td/self.T**2)
            if self.Sd<self.beta*self.ag:
                self.Sd = self.beta*self.ag
            else:
                pass
        else:
            pass
        
        plt.plot([self.T for x in np.arange(0, self.Sd, 0.001)], np.arange(0,self.Sd, 0.001), "g--")
        plt.plot(np.arange(0,self.T, 0.001), [self.Sd for x in np.arange(0,self.T, 0.001)], "g--")
        plt.plot(self.T, self.Sd, "r*")
        #plt.show()
        plt.savefig(self.path + "/Plot" + "S" + str(self.Stype) + "G" + str(self.Gtype) + "a" + str(self.ag) + "q" + str(self.q) + "h" + str(self.h1) + "im" + str(self.imp) + ".png")
        plt.close()
        
    def BaseShear(self):
        self.Fb = (self.W1 + self.W2 + self.W3)*self.Sd
        Whtotal = self.W1*self.h1 + self.W2*(self.h1+self.h2) +self.W3*(self.h1+self.h2+self.h3)
        self.F1 = self.Fb*(self.W1*self.h1)/(Whtotal)
        self.F2 = self.Fb*self.W2*(self.h1+self.h2)/(Whtotal)
        self.F3 = self.Fb*self.W3*(self.h1+self.h2+self.h3)/(Whtotal)
    
    def PostProcessChecks(self, Medf, Nedf, Vedf, Medr, Nedr, Vedr):
        self.Vplf = 406*10**3
        self.Mplf = 213*10**3
        self.Nplf = 1575*10**3
        self.Vplr = 249*10**3
        self.Mplr = 108*10**3
        self.Nplr = 1091*10**3
        self.Nedf = Nedf
        self.Medf = Medf
        self.Vedf = Vedf
        self.Vedr = Vedr
        self.Medr = Medr
        self.Nedr = Nedr
        self.Nffactor = self.Nedf/self.Nplf
        self.Mffactor = self.Medf/self.Mplf
        self.Vffactor = self.Vedf/self.Vplf
        self.Mrfactor = self.Vedr/self.Vplr
        self.Vrfactor = self.Medr/self.Mplr
        self.Nrfactor = self.Nedr/self.Nplr
        self.f = open(self.path + "/CriteriaChecks" + "S" + str(self.Stype) + "G" + str(self.Gtype) + "a" + str(self.ag) + "q" + str(self.q) + "h" + str(self.h1) + "im" + str(self.imp) +  ".txt", "w")
        print("____________FACTOR OF SAFETY - STRENGTH RELATED CRITERIA_________\n")
        self.f.write("____________FACTOR OF SAFETY - STRENGTH RELATED CRITERIA_________\n")
        
        if self.Nffactor < 0.15:
            print("Compression Factor of Safety: " + str(self.Nffactor) + " : SATISFIED\n")
            self.f.write("Compression Factor of Safety: " + str(self.Nffactor) + " : SATISFIED\n")
        elif self.Nffactor >= 0.15:
            print("Compression Factor of Safety: " + str(self.Nffactor) + " : FAILURE\n")
            self.f.write("Compression Factor of Safety: " + str(self.Nffactor) + " : FAILURE\n")
        else:
            raise ValueError()
        
        
        if self.Vffactor < 0.5:
            print("Shear Factor of Safety: " + str(self.Vffactor) + " : SATISFIED\n")
            self.f.write("Shear Factor of Safety: " + str(self.Vffactor) + " : SATISFIED\n")
        elif self.Vffactor >= 0.5:
            print("Shear Factor of Safety: " + str(self.Vffactor) + " : FAILURE\n")
            self.f.write("Shear Factor of Safety: " + str(self.Vffactor) + " : FAILURE\n")
        else:
            raise ValueError()
            
        if self.Mffactor < 1:
            print("Moment Factor of Safety: " + str(self.Mffactor) + " : SATISFIED\n")
            self.f.write("Moment Factor of Safety: " + str(self.Mffactor) + " : SATISFIED\n")
        elif self.Mffactor >= 1:
            print("Moment Factor of Safety: " + str(self.Mffactor) + " : FAILURE\n")
            self.f.write("Moment Factor of Safety: " + str(self.Mffactor) + " : FAILURE\n")
        else:
            raise ValueError()
            
        if self.Mffactor < 1 and self.Vffactor < 0.5 and self.Nffactor < 0.15:
            print("All Floor Beams have satisfied Strength Criteria\n")
            self.f.write("All Floor Beams have satisfied Strength Criteria\n")
        else:
            print("Not all Floor Beams have satisfied Strength Criteria\n")
            self.f.write("Not all Floor Beams have satisfied Strength Criteria\n")
        if self.Nrfactor < 0.15:
            print("Compression Factor of Safety: " + str(self.Nrfactor) + " : SATISFIED\n")
            self.f.write("Compression Factor of Safety: " + str(self.Nrfactor) + " : SATISFIED\n")
        elif self.Nrfactor >= 0.15:
            print("Compression Factor of Safety: " + str(self.Nrfactor) + " : SATISFIED\n")
            self.f.write("Compression Factor of Safety: " + str(self.Nrfactor) + " : SATISFIED\n\n")
        else:
            raise ValueError()
        
        if self.Vrfactor < 0.5:
            print("Shear Factor of Safety: " +  str(self.Vrfactor) + " : SATISFIED\n")
            self.f.write("Shear Factor of Safety: " +  str(self.Vrfactor) + " : SATISFIED\n")
        elif self.Vrfactor >= 1:
            print("Shear Factor of Safety: " + str(self.Vrfactor) + " : FAILURE\n")
            self.f.write("Shear Factor of Safety: " + str(self.Vrfactor) + " : FAILURE\n\n")
        else:
            raise ValueError()
            
        if self.Mrfactor < 1:
            print("Moment Factor of Safety: " + str(self.Mrfactor) + " : SATISFIED\n")
            self.f.write("Moment Factor of Safety: " + str(self.Mrfactor) + " : SATISFIED\n")
        elif self.Mffactor >= 1:
            print("Moment Factor of Safety: " + str(self.Mrfactor) + " : FAILURE\n")
            self.f.write("Moment Factor of Safety: " + str(self.Mrfactor) + " : FAILURE\n\n")
        else:
            raise ValueError()
            
        if self.Mrfactor < 1 and self.Vrfactor < 0.5 and self.Nrfactor < 0.15:
            print("All Roof Beams have satisfied Strength Criteria\n")
            self.f.write("All Roof Beams have satisfied Strength Criteria\n\n")
        else:
            print("Not all Roof Beams have satisfied Strength Criteria\n")
            self.f.write("Not all Roof Beams have satisfied Strength Criteria\n\n")
            
        self.Overstrength = min(self.Mplf/self.Medf, self.Mplr/self.Medr)
        self.f.close()
    
            
    def ServicibilityChecks(self, ds1, ds2, ds3, state = "Brittle"):
        self.dr1 = ds1*self.q
        self.dr2 = ds2*self.q
        self.dr3 = ds3*self.q
        self.f = open(self.path + "/CriteriaChecks" + "S" + str(self.Stype) + "G" + str(self.Gtype) + "a" + str(self.ag) + "q" + str(self.q) + "h" + str(self.h1) + "im" + str(self.imp) +  ".txt", "a")
        if state == "Brittle":
            self.maxr1 = 0.005*self.h1*10**3/self.v
            self.maxr2 = 0.005*self.h2*10**3/self.v
            self.maxr3 = 0.005*self.h3*10**3/self.v
        elif state == "Ductile":
            self.maxr1 = 0.0075*self.h1*10**3/self.v
            self.maxr2 = 0.0075*self.h2*10**3/self.v
            self.maxr3 = 0.0075*self.h3*10**3/self.v
        elif state == "Detatched":
            self.maxr1 = 0.01*self.h1*10**3/self.v
            self.maxr2 = 0.01*self.h2*10**3/self.v
            self.maxr3 = 0.01*self.h3*10**3/self.v
        else: 
            pass
        print("____________FLOOR DRIFTS - SERVICABILITY RELATED CRITERIA_________\n\n")
        self.f.write("____________FLOOR DRIFTS - SERVICABILITY RELATED CRITERIA_________\n")
        
        if self.maxr1 > self.dr1:
            print("First floor drift: ", str(self.dr1), "\n", "Criteria SATISFIED!\n")
            self.f.write("First floor drift: "+ str(self.dr1)+ "\n"+ "Criteria SATISFIED!\n")
        else:
            print("First floor drift: ", str(self.dr1), "\n", "Criteria NOT SATISFIED!\n")
            self.f.write("First floor drift: "+ str(self.dr1)+ "\n"+ "Criteria NOT SATISFIED!\n")
        if self.maxr2 > self.dr2:
            print("Second floor drift: ", str(self.dr2), "\n", "Criteria SATISFIED!\n")
            self.f.write("Second floor drift: "+ str(self.dr2)+ "\n"+ "Criteria SATISFIED!\n")
        else:
            print("Second floor drift: ", str(self.dr2), "\n", "Criteria NOT SATISFIED!\n")
            self.f.write("Second floor drift: "+ str(self.dr2)+ "\n"+ "Criteria NOT SATISFIED!\n")
        
        if self.maxr3 > self.dr3:
            print("Third floor drift: ", str(self.dr3), "\n", "Criteria SATISFIED!\n")
            self.f.write("Third floor drift: "+ str(self.dr3)+ "\n"+ "Criteria SATISFIED!\n")
        else:
            print("Third floor drift: ", str(self.dr3), "\n", "Criteria NOT SATISFIED!\n")
            self.f.write("Third floor drift: "+str(self.dr3)+ "\n"+ "Criteria NOT SATISFIED!\n")
            
        if self.maxr1 > self.dr1 and self.maxr2 > self.dr2 and self.maxr3 > self.dr3:
            print("All floor drifts are in check. The SLS criteria is SATISFIED!\n")
            self.f.write("All floor drifts are in check. The SLS criteria is SATISFIED!\n\n")
        else:
            print("The SLS criteria has not been satisfied!\n")
            self.f.write("The SLS criteria has not been satisfied!\n\n")
            
        self.fita1= ((self.W1 + self.W2 + self.W3)*self.dr1)/((self.F1 + self.F2 + self.F3)*self.h1*10**3)
        self.fita2= ((self.W2 + self.W3)*self.dr2)/((self.F2 + self.F3)*self.h2*10**3)
        self.fita3= ((self.W3)*self.dr3)/((self.F3)*self.h3*10**3)
        
        print("____________2ND ORDER EFFECTS_________\n\n")
        self.f.write("____________2ND ORDER EFFECTS_________\n")
        
        if self.fita1 < 0.1:
            print("No 2nd order effects take place!\n" + str(self.fita1) + " < " + str(0.1) + "\n")
            self.f.write("No 2nd order effects take place!\n" + str(self.fita1) + " < " + str(0.1) + "\n")
        elif self.fita1 >= 0.1 and self.fita1 < 0.2:
            self.F1 = self.F1*(1/1-self.fita1)
            print("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita1) + " > " + str(0.1) + "\n")
            self.f.write("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita1) + " > " + str(0.1) + "\n")
        elif self.fita1 >= 0.2:
            print("Analyize taking into accound 2nd order effects!\n" + str(0.2) + " > " + str(self.fita1) + "\n")
            self.f.write("Analyize taking into accound 2nd order effects!\n"+ str(0.2) + " > " + str(self.fita1) + "\n")
        else:
            pass
        
        if self.fita2 < 0.1:
            print("No 2nd order effects take place!\n"+ str(self.fita2) +" < " + str(0.1) + "\n")
            self.f.write("No 2nd order effects take place!\n"+ str(self.fita2) +" < " + str(0.1) + "\n")
        elif self.fita2 >= 0.1 and self.fita2 < 0.2:
            self.F2 = self.F2*(1/1-self.fita2)
            print("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita2) + " > " + str(0.1) + "\n")
            self.f.write("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita2) + " > " + str(0.1) + "\n")
        elif self.fita2 >= 0.2:
            print("Analyize taking into accound 2nd order effects!\n"+ str(0.2) + " > " + str(self.fita2) + " > " + str(0.1) + "\n")
            self.f.write("Analyize taking into accound 2nd order effects!\n"+ str(0.2) + " > " + str(self.fita2) + " > " + str(0.1) + "\n")
        else:
            pass
        
        if self.fita3 < 0.1:
            print("No 2nd order effects take place!\n" + str(self.fita3) + " < " + str(0.1) + "\n")
            self.f.write("No 2nd order effects take place!\n"  + str(self.fita3) + " < " + str(0.1) + "\n")
        elif self.fita3 >= 0.1 and self.fita3 < 0.2:
            self.F3 = self.F3*(1/1-self.fita3)
            print("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita3) + " > " + str(0.1) + "\n")
            self.f.write("Take into account additional lateral force due to 2nd order effect!\n" + str(0.2) + " > " + str(self.fita3) + " > " + str(0.1) + "\n")
        elif self.fita3 >= 0.2:
            print("Analyize taking into accound 2nd order effects!\n"+ str(0.2) + " > " + str(self.fita3) + " > " + str(0.1) + "\n")
            self.f.write("Analyize taking into accound 2nd order effects!\n"+ str(0.2) + " > " + str(self.fita3) + " > " + str(0.1) + "\n")
        else:
            pass
        
        self.f.close()
    
    
        
    