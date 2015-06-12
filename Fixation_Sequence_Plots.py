#####################################################

# THIS WILL CREATE A PLOT FOR EACH PARTICIPANT SHOWING SCANPATH SEQUENCES


#####################################################

import pandas as pd
import numpy as np

#This will create a plot for each participant for each trial showing each duration of each fixation in order

#This is a vector containing unique subject ids
subs = pd.Series(df_fix['Subject'].values.ravel()).unique()


for sub in subs:  

    #The original script sliced a larger dataframe containing all subjects to only include one subject per plot
    #This could be replaced such that df_new = pd.read_csv('insert filename of input file here')
    df_new = df_fix_ana_corr[df_fix_ana_corr['Subject']==sub]


    ############################################

    # This will find consecutive repeats in a list

    #Note: You will need to replace the names of columns with the headers used in your dataframe corresponding to
    # Fixation name, Fixation duration, Trial Order, Trial ID, and Accuracy
    
    ############################################
    

    source_list = list(df_new['Fixation_AOI_Letter']) #convert the fixation letter sequence to a list 
    result_list = []
    current = source_list[0]
    count = 0
    for row,value in enumerate(source_list):
        if value == current:
            count += 1
        else:
            result_list.append((current, count))
            current = value
            count = 1

            
    result_list.append((current, count))


    ######################################################

    # THIS WILL CONCATENATE ADJACENT REPEATING FIXATIONS INTO ONE FIXATION

    ######################################################

    #Initialize lists from dataframe columns -- probably not the most efficient way to do this
    subj = list(df_new['Subject'])
    trial_order = list(df_new['Trial_Order'])
    trial_id = list(df_new['Trial_ID'])
    Accuracy = list(df_new['Accuracy'])
    duration_list = list(df_new['Fixation_duration'])

    #initialize output lists
    subj_list = []
    combined_fixation_list = []
    combined_duration_list = []
    combined_trial_order = []
    combined_trial_id = []
    combined_accuracy = []
    

    # Set counters to 0 
    counter_result = 0
    counter_source = 0 #use this other counter to track the index for the original duration/fixation 

    while (counter_result < len(result_list)):
        if result_list[counter_result][1]>1:
            combined_fixation_list.append(source_list[counter_source])
            combined_trial_order.append(trial_order[counter_source])
            combined_trial_id.append(trial_id[counter_source])
            combined_accuracy.append(Accuracy[counter_source])
            subj_list.append(subj[counter_source])
            combined_duration_list.append(sum((duration_list[counter_source: counter_source+result_list[counter_result][1]])))
            counter_source = counter_source + result_list[counter_result][1]
            counter_result = counter_result + 1        
        else:
            combined_fixation_list.append(source_list[counter_source])
            combined_trial_order.append(trial_order[counter_source])
            combined_trial_id.append(trial_id[counter_source])
            combined_accuracy.append(Accuracy[counter_source])
            subj_list.append(subj[counter_source])
            combined_duration_list.append(duration_list[counter_source])
            counter_source = counter_source + result_list[counter_result][1]
            counter_result = counter_result + 1


    new_array = np.column_stack((subj_list, combined_trial_order, combined_trial_id, combined_accuracy, combined_fixation_list, combined_duration_list))
    column_names = ['subject', 'combined_trial_order', 'combined_trial_id', 'combined_accuracy', 'combined_fixation_list', 'combined_duration_list']



    df_newer = pd.DataFrame(new_array, columns=column_names)
    
    
        
    #With Andrew (Belen's Husband)'s help 4-14-15:
    #Create a dictionary with trial number as the key and fixation location and duration as tuple values in the list for each trial


    myDict = {}

    for row, item in df_newer.iterrows():
        if df_newer['combined_trial_order'][row] not in myDict:
            myDict[df_newer['combined_trial_order'][row]]=[]
            myDict[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row],df_newer['combined_duration_list'][row] ))
        elif df_newer['combined_trial_order'][row] in myDict:
            myDict[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row],df_newer['combined_duration_list'][row] ))
    
    
    
    '''
    # THIS COMMENTED SECTION WOULD BE USED TO NOT INCLUDE THE FIXATION SEQUENCES COMBINING ADJACENT IDENTICAL FIXATIONS
    #With Andrew (Belen's Husband)'s help 4-14-15:
    #Create a dictionary with trial number as the key and fixation location and duration as tuple values in the list for each trial


    myDict = {}

    for row, item in df_new.iterrows():
        if df_new['Trial_Order'][row] not in myDict:
            myDict[df_new['Trial_Order'][row]]=[]
            myDict[df_new['Trial_Order'][row]].append((df_new['Fixation_AOI_Lure'][row],df_new['Fixation_duration'][row] ))
        elif df_new['Trial_Order'][row] in myDict:
            myDict[df_new['Trial_Order'][row]].append((df_new['Fixation_AOI_Lure'][row],df_new['Fixation_duration'][row] ))
    

    # This calculates the duration for each trial in terms of fixation duration
    trials = pd.Series(df_new['Trial_Order'].values.ravel()).unique()
    sum_durations = []

    for index,trial in enumerate(trials):
        duration = []
        for row,item in enumerate(myDict[trial]):
            duration.append(myDict[trial][row][1])
        sum_durations.append(sum(duration))

    sum_durations = array(sum_durations) #convert the sum of trial durations into an array so that we could use the max function
#    trials = pd.Series(df_new['Trial_Order'].values.ravel()).unique()
    
    #This creates a broken bar plot where each of the rows is a trial and each length of color is fixation duration
    fig, ax = plt.subplots()

    for index,trial in enumerate(trials):
        point = 0
        for row,item in enumerate(myDict[trial]):
            if myDict[trial][row][0] == '2A':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'blue')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == '2B':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'red')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == '2C':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'yellow')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == 'CRESP':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'green')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == 'sLure_loc':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'cyan')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == 'pLure_loc':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'magenta')
                point += myDict[trial][row][1]
            elif myDict[trial][row][0] == 'uLure_loc':
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'grey')
                point += myDict[trial][row][1]
            else:
                ax.broken_barh([(point, myDict[trial][row][1])], ((index+1)*10,9), facecolors = 'black')
                point += myDict[trial][row][1]
                
    '''
    # This calculates the duration for each trial in terms of fixation duration
    trials = pd.Series(df_newer['combined_trial_order'].values.ravel()).unique()
    sum_durations = []

    for index,trial in enumerate(trials):
        duration = []
        for row,item in enumerate(myDict[trial]):
            duration.append(int(myDict[trial][row][1]))
        sum_durations.append(sum(duration))

    sum_durations = np.array(sum_durations) #convert the sum of trial durations into an array so that we could use the max function
#    trials = pd.Series(df_new['Trial_Order'].values.ravel()).unique()

#    max_trial = np.zeros(len(trials))

    #This For loop sums up the fixation duration for each particular trial and stores it in the appropriate index for the max_trial variable
#    for index, trial in enumerate(trials):
#        max_trial[index] = (df_new['Fixation_duration'][0:len(df_new[df_new['Trial_Order'].isin([trial])])].sum())


#This creates a broken bar plot where each of the rows is a trial and each length of color is fixation duration
    fig, ax = plt.subplots()
    
    
    #PLEASE NOTE: I HARD CODED AOI LOCATIONS (E.G., A, B, C, T, ETC.) YOU WILL NEED TO CHANGE THESE TO REFLECT NAMES OF AOIS

    for index,trial in enumerate(trials):
        point = 0
        for row,item in enumerate(myDict[trial]):
            if myDict[trial][row][0] == 'A':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'blue')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'B':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'red')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'C':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'yellow')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'T':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'green')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'S':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'cyan')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'P':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'magenta')
                point += int(myDict[trial][row][1])
            elif myDict[trial][row][0] == 'U':
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'grey')
                point += int(myDict[trial][row][1])
            else:
                ax.broken_barh([(point, int(myDict[trial][row][1]))], ((index+1)*10,9), facecolors = 'black')
                point += int(myDict[trial][row][1])

    ticks=[]    
#This will format the plot
    index=0
    for x in range(0,len(trials)+1):
        tick=(index+1) * 10 + 5
        ticks.append(tick)
        index+=1
    ax.set_ylim(5,len(trials))
    ax.set_xlim(0,sum_durations.max()+500)
    ax.set_xlabel('Fixation Duration (ms)')
    ax.set_yticks(ticks)
    ax.set_yticklabels([])
    ax.grid(False)
    
    #SAME THING HERE FOR RENAMING AOI NAMES IN FIGURE LEGEND
    
    A_loc = mpatches.Patch(color='blue', label='A')
    B_loc = mpatches.Patch(color='red', label='B')
    C_loc = mpatches.Patch(color='yellow', label='C')
    D_loc = mpatches.Patch(color='black', label='D')
    Target_loc = mpatches.Patch(color='green', label='T')
    sLure_loc = mpatches.Patch(color='cyan', label='S')
    pLure_loc = mpatches.Patch(color='magenta', label='P')
    uLure_loc = mpatches.Patch(color='grey', label='U')

    lgd = plt.legend(handles=[A_loc, B_loc, C_loc, D_loc, Target_loc, sLure_loc, pLure_loc, uLure_loc],bbox_to_anchor=(1, 1), loc=2,
           ncol=1, borderaxespad=0.)

    subject = df_new['Subject'].iloc[1]
    pylab.savefig(str(subject) + '_fix_dur.png', bbox_extra_artists=(lgd,), bbox_inches='tight') #This resizes the figure within the figure box to make the legend fit neatly
    plt.close()
