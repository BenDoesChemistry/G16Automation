######################################################################################################################
# log_file
# This class is meant to be used to parse and hold the values of a gaussian 16 log file. This can also be used to 
# return the values as a dictionary so that those dictionaries can be fed in to a pandas dataframe.
######################################################################################################################

class log_file:

######################################################################################################################
# Clean_BTW_Energy
# This is a method which takes the slices of the lines in a log file which contain the Bottom of the well(BTW) energy
# and returns the BTW energy as a floating point number.
######################################################################################################################

    def Clean_BTW_Energy(self, Val_List):
        temp_str = ""
        for i in Val_List:
            temp_str=temp_str+str(i)
        temp_list = temp_str.split('\\')
        for i in temp_list:
            if "HF="in i:
                final = i.replace(" ","")
                return float(final[3:]) 
            
######################################################################################################################
# Clean_Thermal_Corrections
# This takes a list of lines from a log file that contain the thermal corrections and stores them in the thermal
# corrections dictionary. It is called in the __init__ Method
######################################################################################################################
    def Clean_Thermal_Corrections(self,Corrections_List):
        for i in Corrections_List:
            i = i.split("=")
            if "Hartree" in i[1]:
                self.Thermal_Corrections[i[0][1:]] = float(i[1][:-18])
            else:
                self.Thermal_Corrections[i[0][1:]] = float(i[1])
                
######################################################################################################################
# Clean_Frequencies
# This function take a line from gaussian which contains Frequencies and adds them to the class frequency variable.
######################################################################################################################
    def Clean_Frequencies(self,List):
        List = List.split()
        for i in range(2,len(List)):
            if float(List[i]) < 0 :
                self.Num_Imaginary_Frequencies = self.Num_Imaginary_Frequencies + 1
            self.Frequencies.append(float(List[i]))

######################################################################################################################
# Final_Checks
# Ben_Payton
# 2024-03-07
# This function take a line from gaussian which contains Frequencies and adds them to the class frequency variable.
######################################################################################################################

    def Final_Checks(self):
#       checks to see if the bottom of the well energies were found in the file. if it hasn't then it calculates it from the freq calculation thermo
        if self.BTW_Energy == 0 and self.Thermal_Corrections["Sum of electronic and zero-point Energies"] != 0:
            self.BTW_Energy = self.Thermal_Corrections["Sum of electronic and zero-point Energies"] - self.Thermal_Corrections["Zero-point correction"]


######################################################################################################################
# __init__
# This function is called when the class is implemented it is meant to assign all of the self. values. This is the 
# implementation of parsing and cleaning functions above.
######################################################################################################################
        
    def __init__(self,File_Name):
        
        self.File_Name = File_Name
        self.Functional = ""
        self.Basis_Set = ""
        self.Geometry_Opt = False
        self.Frequency_Opt = False
        self.Transiton_Opt = False
        self.Hindered_Rotor = False
        self.Num_Imaginary_Frequencies = 0
        self.Frequencies = []
        self.BTW_Energy = 0
        self.Num_Statp = 0
        self.Thermal_Corrections = {"Zero-point correction":0,
                                    "Thermal correction to Energy":0,
                                    "Thermal correction to Enthalpy":0,
                                    "Thermal correction to Gibbs Free Energy":0,
                                    "Sum of electronic and zero-point Energies":0,
                                    "Sum of electronic and thermal Energies":0,
                                    "Sum of electronic and thermal Enthalpies":0,
                                    "Sum of electronic and thermal Free Energies":0}
        
        with open(self.File_Name) as file:
            lines = file.read().splitlines()
            for i in range(len(lines)):
# implementation of finding the BTW Energies               
                if "\HF=" in lines[i]:
                    self.BTW_Energy = self.Clean_BTW_Energy(lines[i] + lines[i+1])
# Counting the Number of Stationary points            
                if "Stationary point found" in lines[i]:
                    self.Num_Statp += 1
# This gets the Thermal Corrections            
                if "Zero-point correction" in lines[i]:
                    self.Clean_Thermal_Corrections(lines[i:i+8])
# This collects the Frequencues and counts the imaginary frequencies                
                if "Frequencies --" in lines[i]:
                    self.Clean_Frequencies(lines[i])
                if "Warning -- explicit consideration of" in lines[i]:
                    self.Hindered_Rotor =True

        self.Final_Checks

######################################################################################################################
# Output_Dict
# This method returns all values scraped from the log file in the form of a dictionary. 
######################################################################################################################
    def Output_Dict(self):
        Out_Dict = {"File_Name":self.File_Name, 
                    "Functional":self.Functional, 
                    "Basis_Set":self.Basis_Set,
                    "Geometry_Optimization":self.Geometry_Opt,
                    "Frequency_Optimization": self.Frequency_Opt,
                    "Transition_Optimization": self.Transiton_Opt,
                    "Hindered_Rotor": self.Hindered_Rotor,
                    "Number_of_Imaginary_Frequencies":self.Num_Imaginary_Frequencies,
                    "Frequencies": self.Frequencies,
                    "BTW_Energy": self.BTW_Energy,
                    "Number_of_Stationary_Points": self.Num_Statp,
                    "Zero-point correction":self.Thermal_Corrections["Zero-point correction"],
                    "Thermal correction to Energy":self.Thermal_Corrections["Thermal correction to Energy"],
                    "Thermal correction to Enthalpy":self.Thermal_Corrections["Thermal correction to Enthalpy"],
                    "Thermal correction to Gibbs Free Energy":self.Thermal_Corrections["Thermal correction to Gibbs Free Energy"],
                    "Sum of electronic and zero-point Energies":self.Thermal_Corrections["Sum of electronic and zero-point Energies"],
                    "Sum of electronic and thermal Energies":self.Thermal_Corrections["Sum of electronic and thermal Energies"],
                    "Sum of electronic and thermal Enthalpies":self.Thermal_Corrections["Sum of electronic and thermal Enthalpies"],
                    "Sum of electronic and thermal Free Energies":self.Thermal_Corrections["Sum of electronic and thermal Free Energies"]}
        return Out_Dict