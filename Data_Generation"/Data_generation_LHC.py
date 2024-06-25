import os
import csv
from pyDOE import lhs
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

        # Concentration ranges for Latin Hypercube Sampling
        ph_range = (6, 8)
        mg_bound_range = (0.001, 0.01)
        ca_bound_range = (2e-10, 1e-8)
        c4_bound_range = (2e-10, 1e-4)
        cl_bound_range = (1e-2, 1e-3)
        mg_ini_range = (2e-7, 1e-8)
        ca_ini_range = (2e-7, 1e-6)
        c4_ini_range = (2e-7, 1e-2)
        cl_ini_range = (1e-7, 1e-1)
        cal_ini_mol = 1.22e-1
        dol_ini_mol = 1.22e-1

        # Perform Latin Hypercube Sampling
        num_simulations = 10000
        num_params = 10
        lhd = lhs(num_params, samples=num_simulations)

        results = []

        for i in range(num_simulations):
            # Extract values from Latin Hypercube Samples
            ph = lhd[i][0] * (ph_range[1] - ph_range[0]) + ph_range[0]
            mg_bound = lhd[i][1] * (mg_bound_range[1] - mg_bound_range[0]) + mg_bound_range[0]
            ca_bound = lhd[i][2] * (ca_bound_range[1] - ca_bound_range[0]) + ca_bound_range[0]
            c4_bound = lhd[i][3] * (c4_bound_range[1] - c4_bound_range[0]) + c4_bound_range[0]
            cl_bound = lhd[i][4] * (cl_bound_range[1] - cl_bound_range[0]) + cl_bound_range[0]
            mg_ini = lhd[i][5] * (mg_ini_range[1] - mg_ini_range[0]) + mg_ini_range[0]
            ca_ini = lhd[i][6] * (ca_ini_range[1] - ca_ini_range[0]) + ca_ini_range[0]
            c4_ini = lhd[i][7] * (c4_ini_range[1] - c4_ini_range[0]) + c4_ini_range[0]
            cl_ini = lhd[i][8] * (cl_ini_range[1] - cl_ini_range[0]) + cl_ini_range[0]

            # Generate input script
            script_mod = self.input_string(temp, ph, mg_bound, ca_bound, c4_bound, cl_bound,
                                           mg_ini, ca_ini, c4_ini, cl_ini, cal_ini_mol, dol_ini_mol)

            # Run PhreeQC simulation
            values = {'phreeqcpath': p['phreeqcpath'], 'DBpath': p['DBpath']}
            phreeqc_result = self.selected_array(p['DBpath'], values, script_mod)

            # Process and save results
            results.append((ph, mg_bound, mg_ini, ca_bound, ca_ini, c4_bound, c4_ini, cl_bound, cl_ini, cal_ini_mol, dol_ini_mol, *phreeqc_result[-1]))

        # Save results to CSV file
        output_file = os.path.join(p['out_compar'], 'output_LHS.csv')
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
    params['phreeqcpath'] = "Lib/site-packages/phreeqpy/iphreeqc/phreeqc3/IPhreeqc-3.7.3.dll"
    params['DBpath'] = '/iphreeqc-3.7.3-15968/database/phreeqc.dat'
    params['folderresults'] = 'Testproblem6/'
    params['out_compar'] = params['folderresults'] + '/Comparisson/'
    return params

if __name__ == "__main__":
    p = addInputParameters({})
    q1 = runSimulation(p)
    print('Finished')
