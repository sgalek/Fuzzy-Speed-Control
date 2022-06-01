# Szymon Gałek 
# Nr. albumu : 20843
# Fuzzy Speed Control


# Założenia :
#   2 rozmyte wejścia:
#       - różnica prędkości (speed_dif)
#       - przyśpieszenie (acc)
#   1 rozmyte wyjście:
#       - kontrola przepustnicy (control)
#   Przestrzeń zdarzeń:
#       - x[0:240]

#   Przedziały:
#       ujemna wysoka - UW:     OpenLeft (a = 30, b = 60)
#       ujemna średnia - US:    Triangular(a = 30, b = 60, c = 90)
#       ujemna niska - UN:      Triangular(a = 60, b = 90, c = 120)
#       zero - ZERO:            Triangular(a = 90, b = 120, c = 150)
#       dodatnia niska - DN:    Triangular(a = 120, b = 150, c = 180)
#       dodatnia średnia - DS:  Triangular(a = 150, b = 180, c = 210)
#       dodatnia wysoka - DW:   OpenRight (a = 180, b = 210)

#   Reguły:
#       R1: if speed_dif is UW and acc is ZERO then control is DN
#       R2: if speed_dif is ZERO and acc is UW then control is DN
#       R3: if speed_dif is US and acc is ZERO then control is DS
#       R4: if speed_dif is UN and acc is DW then control is DW
#       R5: if speed_dif is DN and acc is UN then control is UN
#       R6: if speed_dif is DW and acc is ZERO then control is UW
#       R7: if speed_dif is ZERO and acc is UN then control is DW
#       R8: if speed_dif is ZERO and acc is US then control is DS


import FCS_lib

Speed = int(input("Podaj prędkość wejściową... : "))
Acceleration = int(input("Podaj wartość wejściową przyśpieszenia... : "))
print("\n")
print("\n")
print("\n")
print("Prędkość wejściowa: ", Speed)
print("Wartość wejściowa przyśpieszenia: ", Acceleration)
print("\n")


# Getting fuzzy values for all the inputs for all the fuzzy sets
UWSD,USSD,UMSD,ZEROSD,DMSD,DSSD,DWSD = FCS_lib.partition(Speed)
UWAC,USAC,UMAC,ZEROAC,DMAC,DSAC,DWAC = FCS_lib.partition(Acceleration)

# Display the fuzzy values for all fuzzy sets
outPut = [[UWSD,USSD,UMSD,ZEROSD,DMSD,DSSD,DWSD],
          [UWAC,USAC,UMAC,ZEROAC,DMAC,DSAC,DWAC]]
print("Rozmyte wartości wejść")
print(["UW","US","UM","ZERO","DM","DS","DWSD"])
print(FCS_lib.np.round(outPut,2))



DWcontrol, DScontrol, DMcontrol, UMcontrol, UWcontrol = FCS_lib.rule(UWSD,USSD,UMSD,ZEROSD,DMSD,DSSD,DWSD,UWAC,USAC,UMAC,ZEROAC,DMAC,DSAC,DWAC)

print("\n")
# Display the fuzzy values for all rules
outPutRules = [[DWcontrol, DScontrol, DMcontrol, UMcontrol, UWcontrol ]]
print("Wyjścia rozmyte: ")
print(["DWcontrol", "DScontrol", "DMcontrol", "UMcontrol", "UWcontrol"])
print(FCS_lib.np.round(outPutRules,2))



crispOutputFinal = FCS_lib.defuzzyfication(DWcontrol, DScontrol, DMcontrol, UMcontrol, UWcontrol)

if crispOutputFinal !=0:
    print("\nThe crisp TC value is: ", crispOutputFinal)
