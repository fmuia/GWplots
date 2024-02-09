import numpy as np
####Definition of analytic function for spectrum of sound waves from 1st-order PT
#Function of nucleation temperature T* in GeV and dimless parameters alpha, betaoverH, vw, gstar
# f in Hz
# Taken from Ref. 1910.13125: Detecting gravitational waves from cosmological phase transitions with LISA: an update

def hPT(Tstar, alpha, betaoverH, vw, gstar, f):
    Fgw0 =3.57e-5*(100./gstar)**(1./3.)
    TildeOmegagw = 1.e-2
    HstarRstar = (8.*np.pi)**(1/3.)/(betaoverH)
    fp0 = 26.e-6*(1./HstarRstar)*(Tstar/100.)*(gstar/100.)**(1/6.)
    s = f/fp0
    C = s**3.*(7./(4.+3.*s**2))**(7./2.)
    kappaA = vw**(6/5)*6.9*alpha/(1.36-0.037*np.sqrt(alpha)+alpha)
    kappaB = alpha**(2/5.)/(0.017+(.997+alpha)**(2/5))
    cs = 1/np.sqrt(3.)
    kappa = cs**(11./5)*kappaA*kappaB/((cs**(11./5)-vw**(11./5))*kappaB+vw*cs**(6/5)*kappaA)
    K = kappa*alpha/(1+alpha)
    h=.674 #Hubble/100
    return((1.26e-18/f)*np.sqrt(h**2*0.687*Fgw0*K**(3/2)*(HstarRstar/np.sqrt(cs))**2*TildeOmegagw*C))



    
