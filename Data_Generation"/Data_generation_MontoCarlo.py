#Running 
import os
import csv
import random
import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod

class Phreeqc_info(object):
    def __init__(self, wa):
        self.wa = wa

    def input_string(self, temp, ph, mg_bound, ca_bound, c4_bound, cl_bound,
                     mg_ini, ca_ini, c4_ini, cl_ini, cal_ini_mol, dol_ini_mol):
        """
        Generates a PhreeQC input script based on provided values.
        """
        input_string0 = f"""
        SOLUTION 0 Mgcl2 
            temp  {temp} 
            pH    {ph} charge
            pe    4 
            units mol/kgw 
            Cl   {cl_bound}
            Mg   {mg_bound}
            Ca   {ca_bound} 
            C(4)  {c4_bound} 
        
        SOLUTION 1 Calcite 
            temp  {temp} 
            pH    {ph} charge
            pe    4
            units mol/kgw
            Cl   {cl_ini}
            Mg   {mg_ini}
            Ca   {ca_ini} 
            C(4)  {c4_ini} 
        

        EQUILIBRIUM_PHASES 1
            Calcite  0 {cal_ini_mol} 
            Dolomite 0 {dol_ini_mol} 
        
        PRINT 
            -reset true 
            -selected_output true
        
        SELECTED_OUTPUT 
            -file phout_sel-PQC.dat
            -high_precision 
            -reset false
        
        USER_PUNCH 
            -headings C(4) Ca Mg cl pH Calcite Dolomite 
            -start
            20 PUNCH TOT("C(4)"), TOT("Ca"), TOT("Mg"), TOT("Cl") 
            30 PUNCH -LA("H+") 
            70 PUNCH EQUI("Calcite") 
            80 PUNCH EQUI("Dolomite")
            -end
        
        END"""
        return input_string0

    def selected_array(self, db_path, values, script_mod):
        """
        Runs the PhreeQC script, retrieves the selected output, and returns it as a NumPy array.
        """
        lib_path = values['phreeqcpath']
        phreeqc = phreeqc_mod.IPhreeqc(lib_path)
        phreeqc.load_database(db_path)
        phreeqc.run_string(script_mod)

        return phreeqc.get_selected_output_array()

    def Phreeqc_module(self, p):
        """
        Sets up the simulation parameters, generates the script, runs PhreeQC, and returns the simulation results.
        """
        # Define simulation parameters (example ranges)
        temp = 25

        # Concentration ranges for Monte Carlo (adjust as needed)
        ph_range = (6, 8)
        mg_bound_range = (0.001, 0.01)
        ca_bound_range = (2e-10, 1e-8)
        c4_bound_range = (1e-7, 1e-1)
        cl_bound_range = (1e-2, 1e-3)
        mg_ini_range = (2e-7, 1e-8)
        ca_ini_range = (2e-7, 1e-6)
        c4_ini_range = (1e-7, 1e-2)
        cl_ini_range = (1e-7, 1e-1)
        cal_ini_mol = 1.22e-1
        dol_ini_mol = 1.22e-1





        # Perform Monte Carlo simulation (replace with your desired number of runs)
        num_simulations = 10000

        results = []

        for _ in range(num_simulations):
            # Randomly select values within the defined ranges
            ph = random.uniform(*ph_range)
            mg_bound = random.uniform(*mg_bound_range)
            ca_bound = random.uniform(*ca_bound_range)
            c4_bound = random.uniform(*c4_bound_range)
            cl_bound = random.uniform(*cl_bound_range)
            mg_ini = random.uniform(*mg_ini_range)
            ca_ini = random.uniform(*ca_ini_range)
            c4_ini = random.uniform(*c4_ini_range)
            cl_ini = random.uniform(*cl_ini_range)

            # Generate input script
            script_mod = self.input_string(temp, ph, mg_bound, ca_bound, c4_bound, cl_bound,
                                           mg_ini, ca_ini, c4_ini, cl_ini, cal_ini_mol, dol_ini_mol)

            # Run PhreeQC simulation
            values = {'phreeqcpath': p['phreeqcpath'], 'DBpath': p['DBpath']}
            phreeqc_result = self.selected_array(p['DBpath'], values, script_mod)

            # Process and save results
            results.append((ph, mg_bound, mg_ini, ca_bound, ca_ini, c4_bound, c4_ini, cl_bound, cl_ini, cal_ini_mol, dol_ini_mol, *phreeqc_result[-1]))

        # Save results to CSV file
        output_file = os.path.join(p['out_compar'], 'output_10.csv')
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['pH', 'Mg Bound (Initial)', 'Mg Initial', 'Ca Bound (Initial)', 'Ca Initial',
                             'C(4) Bound (Initial)', 'C(4) Initial', 'Cl Bound (Initial)', 'Cl Initial', 'cal_ini_mol', 'dol_ini_mol',  
                             'C(4) Final', 'Ca Final', 'Mg Final', 'Cl Final',  'pH_out',
                             'Calcite', 'Dolomite'])
            writer.writerows(results)

        return results
def runSimulation(p):
    phreeqc = Phreeqc_info(0)
    return phreeqc.Phreeqc_module(p)

def addInputParameters(params):
    params['phreeqcpath'] = "C:/Users/21294596/OneDrive - Curtin/Coding/Phree_t1/.conda/Lib/site-packages/phreeqpy/iphreeqc/phreeqc3/IPhreeqc-3.7.3.dll"
    params['DBpath'] = 'C:/Users/21294596/OneDrive - Curtin/Coding/Phree_t1/iphreeqc-3.7.3-15968/database/phreeqc.dat'
    params['folderresults'] = 'Testproblem6/'
    params['out_compar'] = params['folderresults'] + '/Comparisson/'
    return params

if __name__ == "__main__":
    p = addInputParameters({})
    q1 = runSimulation(p)
    print('Finished')
