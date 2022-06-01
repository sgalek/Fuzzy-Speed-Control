import numpy as np

#Funkcje fuzzyfikacji lewo i prawo stronnej  
def openLeft(x,alpha, beta):
    if x<alpha:
        return 1
    if alpha<x and x<=beta:
        return (beta - x)/(beta - alpha)
    else:
        return 0
    
def openRight(x,alpha, beta):
    if x<alpha:
        return 0
    if alpha<x and x<=beta:
        return (x-alpha)/(beta - alpha)
    else:
        return 0

#Funkcje fuzzyfikacji trójkątnej 
def triangular(x,a,b,c):
    return max(min((x-a)/(b-a), (c-x)/(c-b)),0)

#Przedziały rozmyte 
def partition(x):
    UW = 0;  US = 0; UM = 0; ZERO = 0; DM = 0; DS = 0; DW = 0
    
    if x> 0 and x<60:
        UW = openLeft(x,30,60)
    if x> 30 and x<90:
        US = triangular(x,30,60,90)
    if x> 60 and x<120:
        UM = triangular(x,60,90,120)
    if x> 90 and x<150:
        ZERO = triangular(x,90,120,150)
    if x> 120 and x<180:
        DM = triangular(x,120,150,180)
    if x> 150 and x<210:
        DS = triangular(x,120,150,180)
    if x> 180 and x<240:
        DW = openRight(x,180,210)
 
    return UW,US,UM,ZERO,DM,DS,DW


#Implementacja reguł
def compare(control1, control2):
    control = 0
    if control1>control2 and control1 !=0 and control2 !=0:
        control = control2
    else:
        control = control1
    
    if control1 == 0 and control2 !=0:
        control = control2
        
    if control2 == 0 and control1 !=0:
        control = control1
        
    return control


def rule(UWSD,USSD,UMSD,ZEROSD,DMSD,DSSD,DWSD,UWAC,USAC,UMAC,ZEROAC,DMAC,DSAC,DWAC):
    DWcontrol1 = min(UWSD,ZEROAC) 
    DWcontrol2 = min(ZEROSD,UWAC)
    DWcontrol = compare(DWcontrol1, DWcontrol2)
    
    DScontrol1 = min(USSD,ZEROAC)
    DScontrol2 = min(ZEROSD,USAC)
    DScontrol = compare(DScontrol1, DScontrol2)
    
    DMcontrol1 = min(UMSD,DMAC)
    DMcontrol2 = min(ZEROSD,UMAC)
    DMcontrol = compare(DMcontrol1, DMcontrol2)
    UMcontrol = min(DMSD,UMAC)
    UWcontrol = min(DWSD,ZEROAC)
    
    return DWcontrol, DScontrol, DMcontrol, UMcontrol, UWcontrol

#Defuzzyfikacja
def areaTR(mu, a,b,c):
    x1 = mu*(b-a) + a
    x2 = c - mu*(c-b)
    d1 = (c-a); d2 = x2-x1
    a = (1/2)*mu*(d1 + d2)
    return a 

def areaOL(mu, alpha, beta):
    xOL = beta -mu*(beta - alpha)
    return 1/2*mu*(beta+ xOL), beta/2

def areaOR(mu, alpha, beta):
    xOR = (beta - alpha)*mu + alpha
    aOR = (1/2)*mu*((240 - alpha) + (240 -xOR))
    return aOR, (240 - alpha)/2 + alpha

def defuzzyfication(DWcontrol, DScontrol, DMcontrol, UMcontrol, UWcontrol):
    areaDW = 0; areaDS = 0; areaDM = 0; areaUM = 0; areaUW = 0
    cDW = 0; cDS = 0; cDM = 0; cUM = 0; cUW = 0

    if DWcontrol != 0:
        areaDW, cDW = areaOR(DWcontrol, 180, 210)
                
    if DScontrol != 0:
        areaDS = areaTR(DScontrol, 150, 180, 210)
        cDS = 180
    
    if DMcontrol != 0:
        areaDM = areaTR(DMcontrol, 120, 150, 180)
        cDM = 150
          
    if UMcontrol != 0:
        areaUM = areaTR(UMcontrol, 60, 90, 120)
        cUM = 90
        
    if UWcontrol !=0:
        areaUW, cUW = areaOL(UWcontrol, 30, 60)
        
    numerator = areaDW*cDW + areaDS*cDS + areaDM*cDM + areaUM*cUM + areaUW*cUW
    denominator = areaDW + areaDS + areaDM + areaUM + areaUW
    if denominator == 0:
        print("Brak reguł dających wynik")
        return 0
    else:
        crispOutput = numerator/denominator
        return crispOutput