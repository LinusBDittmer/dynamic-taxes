import os

filename = 'geo2.out'                       # Hier muss das mit Linus Teil verknüpft werden.

def read_file():
    content = []
    with open('geo2.out', 'r') as file: 
        cont = ''.join(file.read())
        content.append(cont)
    return content

file_cont = read_file()



def find_multiplicity():
    multiplicity = []
    for inhalt in file_cont:
        multiplicity_start = inhalt.find('\n0 1\n')+3
        multiplicity_content = inhalt[multiplicity_start:multiplicity_start+1]
        multiplicity.append(multiplicity_content)
    return multiplicity

file_multi = find_multiplicity()    
print(file_multi)



def find_excitationenergies():
    for inhalt2 in file_cont:
        ex = []
        ex_start = inhalt2.find('Excited state')+2
        while True:
            ex_start1 = inhalt2.find('Excited state', ex_start)
            if ex_start1 == -1:
                break    
            else:
                ex_end = inhalt2.find('Total energy for state', ex_start1)-2
                ex_start2 = inhalt2.find('Excited state   ', ex_end)
                ex_content = inhalt2[ex_start1:ex_end]
                ex.append(ex_content)
                ex_start = ex_end
    return ex

file_energies = find_excitationenergies()



def find_firstexcitation():
    for content in file_cont:
        first_exc_start = content.find('Excited state   1:')+47
        first_exc_end = first_exc_start+6
        first_exc = content[first_exc_start:first_exc_end]
    return first_exc

file_first_exc = find_firstexcitation()




def find_transitionmoments():                                   
    for inhalt3 in file_cont:
        tm = []
        tm_start = inhalt3.find('Transition Moments Between')
        tm_end = inhalt3.find('\n    1  20', tm_start)+3
        while True:
            tm_start1 = inhalt3.find('\n    1', tm_start)+3
            if tm_start1 == tm_end:
                #tm_end1 = inhalt3.find('\n    2', tm_start1)-1
                #tm_raw_yield = inhalt3[tm_start1:tm_end1]
                #tm_almost_done = tm_raw_yield.split()
                #tm.append(tm_almost_done[5])
                break # keine Ahnung, warum das funktioniert
            else:
                tm_end1 = inhalt3.find('\n    1', tm_start1)-1
                tm_raw_yield = inhalt3[tm_start1:tm_end1]
                tm_almost_done = tm_raw_yield.split()
                tm.append(tm_almost_done[5])
                tm_start = tm_end1            
    return tm

file_tm = find_transitionmoments()
print(file_tm)



def calc_energies():
    exc_energies = []
    for inhalt4 in file_energies:
            while True:
                state_begin = inhalt4.find('Excited state')+15
                if state_begin == -1:
                    print(v3_closetofinal_final)
                else:
                    state_end = state_begin+2
                    state_content = inhalt4[state_begin:state_end]
                    energy_begin = inhalt4.find('excitation energy (eV) =')+28
                    energy_end = energy_begin+6
                    energy_content = inhalt4[energy_begin:energy_end]
                    exc_energy = float(energy_content) - float(file_first_exc)       
                    excitation_energy = 'exc_energy: 1->' + str(state_content) + ' = ' + str(exc_energy) + ' eV.'
                    #print(excitation_energy)
                    exc_energies.append(exc_energy)
                    break
    return exc_energies

file_energies = calc_energies()
print(file_energies)



def find_state_labels():
    state_labels = []
    for inhalt5 in file_cont:
        state_begin = inhalt5.find('Excited state')+2
        forced_end = inhalt5.find('Excited state  20')
        while True:
            state_begin1 = inhalt5.find('Excited state', state_begin)
            if state_begin1 == forced_end:
                state_end = inhalt5.find(': excitation energy (eV)', state_begin1)
                state_raw_yield = inhalt5[state_begin1:state_end]
                state_almost_done = state_raw_yield.split()
                state_labels.append(state_almost_done[2])
                break
            else:
                state_end = inhalt5.find(': excitation energy (eV)', state_begin1)
                state_raw_yield = inhalt5[state_begin1:state_end]
                state_almost_done = state_raw_yield.split()
                state_labels.append(state_almost_done[2])
                state_begin = state_end
    return state_labels

state_labels = find_state_labels()
print(state_labels)



def find_filenames():
    return [filename]

filenames = find_filenames()



def convert_geo_to_time():
    for inhalt6 in filenames:
        geonumber_start = inhalt6.find('geo')+3                                 # HIER GGF. AUCH MIT LINUS TEIL VERKNÜPFEN
        geonumber_end = inhalt6.find('.out')
        geonumber = inhalt6[geonumber_start:geonumber_end]
        time = str(float(geonumber) * 0.05) + ' fs'
    return time
timestamp = convert_geo_to_time()
print(timestamp)



def rename_geofile():
    new_name = timestamp + '.out'
    os.rename(filename, new_name)
    return new_name
#new_names = rename_geofile()
