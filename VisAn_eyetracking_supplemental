'''
Code for Supplementary Materials Section of VisAn Eyetracking

Written by Michael S. Vendetti, Ph.D.

Date 6/26/15


This analysis makes the following assumptions:

1. Eyetracking data has been configured into a PANDAS dataframe called, "df_fix"

2. The dataframe contains all subjects used for the analysis and has the following columns:
    a. Subject - containing subject id for each measurement
    b. Trial_order - containing a number corresponding to the order in which the trial occurred 
    c. Fixation_AOI_Letter - containing where the participant was gazing for each measured fixation in the trial
    d. Fixation_duration - containing the duration of the fixation

'''

################################################################


# Initialize variables

# create a series of unique subject ids from the dataframe
subs = pd.Series(df_fix['Subject'].values.ravel()).unique()

#use this variable to collect information about strategies for each participant
strategy_outer = []


for sub_idx, sub in enumerate(subs):
    response_score = 0
    df_new = df_fix_ana_corr[df_fix_ana_corr['Subject']==sub]

    ############################################

    # This will find consecutive repeats in a list

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
    duration_list = list(df_new['Fixation_duration'])

    #initialize output lists
    subj_list = []
    combined_fixation_list = []
    combined_duration_list = []
    combined_trial_order = []
    

    # Set counters to 0 
    counter_result = 0
    counter_source = 0 #use this other counter to track the index for the original duration/fixation 

    while (counter_result < len(result_list)):
        if result_list[counter_result][1]>1:
            combined_fixation_list.append(source_list[counter_source])
            combined_trial_order.append(trial_order[counter_source])
            subj_list.append(subj[counter_source])
            combined_duration_list.append(sum((duration_list[counter_source: counter_source+result_list[counter_result][1]])))
            counter_source = counter_source + result_list[counter_result][1]
            counter_result = counter_result + 1        
        else:
            combined_fixation_list.append(source_list[counter_source])
            combined_trial_order.append(trial_order[counter_source])
            subj_list.append(subj[counter_source])
            combined_duration_list.append(duration_list[counter_source])
            counter_source = counter_source + result_list[counter_result][1]
            counter_result = counter_result + 1

# This creates a new dataframe concatenating adjacent fixations in the same AOI
    new_array = np.column_stack((subj_list, combined_trial_order, combined_trial_id, combined_accuracy, combined_pLure_loc, combined_sLure_loc, combined_uLure_loc, combined_CRESP_loc, combined_Response_Choice, combined_Response_Time, combined_fixation_list, combined_duration_list))
    column_names = ['subject', 'combined_trial_order', 'combined_trial_id', 'combined_accuracy', 'combined_pLure_loc', 'combined_sLure_loc', 'combined_uLure_loc', 'combined_CRESP_loc', 'combined_Response_Choice', 'combined_Response_Time', 'combined_fixation_list', 'combined_duration_list']
    df_newer = pd.DataFrame(new_array, columns=column_names)

    
# This will create a dictionary that creates a list of tuples for each trial, containing 2 values: 
# 1) the AOI, and 2) the fixation durations    
    myDict = {}

    for row, item in df_newer.iterrows():
        if df_newer['combined_trial_order'][row] not in myDict:
            myDict[df_newer['combined_trial_order'][row]]=[]
            myDict[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row],df_newer['combined_duration_list'][row] ))
        elif df_newer['combined_trial_order'][row] in myDict:
            myDict[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row],df_newer['combined_duration_list'][row] ))

    myDict


# This will create two separate list of tuples from the dictionary: 
# 1) fixation locations and 2) durations 

    fix_loc_no_trans = []
    fix_dur_no_trans = []

    for i in range(len(myDict.keys())):
        fix_loc_new, fix_dur_new = zip(*myDict[myDict.keys()[i]]) 
        fix_loc_no_trans.append(fix_loc_new)
        fix_dur_no_trans.append(fix_dur_new)


    

# This will create a dictionary that creates a list of tuples for each trial, containing 2 values: 
# 1) the fixation transitions, and 2) the fixation transition durations



    myDict_trans = {}
    
    for row, item in df_newer.iterrows():
        if row == len(df_newer)-1:
            continue
        else:
            if df_newer['combined_trial_order'][row] not in myDict_trans:
                test = row+1
                myDict_trans[df_newer['combined_trial_order'][row]]=[]
                myDict_trans[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row]+df_newer['combined_fixation_list'][test],df_newer['combined_duration_list'][row]+df_newer['combined_duration_list'][test]))
            elif df_newer['combined_trial_order'][row] in myDict_trans:
                test = row+1
                myDict_trans[df_newer['combined_trial_order'][row]].append((df_newer['combined_fixation_list'][row]+df_newer['combined_fixation_list'][test],df_newer['combined_duration_list'][row]+df_newer['combined_duration_list'][test]))

    myDict_trans

    fix_loc = []
    fix_dur = []

    for i in range(len(myDict_trans.keys())):
        fix_loc_new, fix_dur_new = zip(*myDict_trans[myDict_trans.keys()[i]]) 
        fix_loc.append(fix_loc_new)
        fix_dur.append(fix_dur_new)

        ####################################
        
        # THIS WILL CREATE A SCORE FOR EACH FIXATION TRANSITION THAT ACCOUNTS FOR POSITION IN FIXATION SEQUENCE
        
        # Specifically, each duration is multiplied by 1/position in the sequence
        
        ####################################

    fix_score_outer = []
    fix_score_inner = []

    for i in range(len(fix_dur)):
        fix_score_inner = list(np.zeros(len(fix_dur[i])))
        for j in range(len(fix_dur[i])):
            fix_score_inner[j]=(int((fix_dur[i][j]))*(1.0/(j+1)))
        
        fix_score_outer.append(fix_score_inner)

###### USE THE KEY FEATURES AND LOOP THROUGH THE TRANSITION LIST TO USE THE SCORE #####


    #Counts of Transitions
    AB_count = 0
    BA_count = 0
    BC_count = 0
    CB_count = 0
    AC_count = 0
    CA_count = 0
    CT_count = 0
    TC_count = 0
    BT_count = 0
    TB_count = 0
    CS_count = 0
    SC_count = 0
    CU_count = 0
    UC_count = 0
    CP_count = 0
    PC_count = 0
    ST_count = 0
    TS_count = 0
    SP_count = 0
    PS_count = 0
    SU_count = 0
    US_count = 0
    PU_count = 0
    UP_count = 0
    PT_count = 0
    TP_count = 0
    UT_count = 0
    TU_count = 0


    strategy_trials=[]
    for i in range(len(fix_score_outer)):
        
        
        

        # Values for transitions to be used when calculating strategies
        first_fix_A = 0
        first_fix_C = 0
        first_fix_B = 0
        first_fix_T = 0
        first_fix_S = 0
        first_fix_P = 0
        first_fix_U = 0
        AB = 0
        BA = 0
        BC = 0
        CB = 0
        CT = 0
        AC = 0
        CA = 0
        CS = 0
        SC = 0
        CP = 0
        PC = 0 
        CU = 0
        UC = 0
        BT = 0
        TB = 0
        TC = 0
        PS = 0
        SP = 0
        PU = 0
        UP = 0
        PT = 0
        TP = 0
        SU = 0
        US = 0
        ST = 0
        TS = 0
        UT = 0
        TU = 0
        

        
        
        for j in range(len(fix_score_outer[i])):
            

            
            ###########################################################
            
            # THIS SECTION CALCULATES THE SCORE            
            # USING THE FIXATION SEQUENCE (I.E., NOT TRANSITION SEQUENCE)
            
            ###########################################################
            
            if first_fix_A == 0:
                if fix_loc_no_trans[i][j]=='A':
                    first_fix_A = first_fix_A + int(fix_dur_no_trans[i][j])
            elif first_fix_C == 0:
                if fix_loc_no_trans[i][j]=='C':
                    first_fix_C = first_fix_C + int(fix_dur_no_trans[i][j])
            elif first_fix_B == 0:
                if fix_loc_no_trans[i][j]=='B':
                    first_fix_B = first_fix_B + int(fix_dur_no_trans[i][j])
            elif first_fix_T == 0:
                if fix_loc_no_trans[i][j]=='T':
                    first_fix_T = first_fix_T + int(fix_dur_no_trans[i][j])
            elif first_fix_S == 0:
                if fix_loc_no_trans[i][j]=='S':
                    first_fix_S = first_fix_S + int(fix_dur_no_trans[i][j])
            elif first_fix_P == 0:
                if fix_loc_no_trans[i][j]=='P':
                    first_fix_P = first_fix_P + int(fix_dur_no_trans[i][j])
            elif first_fix_U == 0:
                if fix_loc_no_trans[i][j]=='U':
                    first_fix_U = first_fix_U + int(fix_dur_no_trans[i][j])
                    
                    
                    
            ###########################################################
            
            # THIS SECTION ASSIGNS THE SCORE            
            # USING THE FIXATION TRANSITIONS 
            
            ###########################################################           
            
            
            
            if fix_loc[i][j]=='AB':
                AB = AB + fix_score_outer[i][j]
                AB_count = AB_count + 1
            elif fix_loc[i][j]=='BA':
                BA = BA + fix_score_outer[i][j]
                BA_count = BA_count + 1
            elif fix_loc[i][j]=='BC':
                BC = BC + fix_score_outer[i][j]
                BC_count = BC_count + 1
            elif fix_loc[i][j]=='CB':
                CB = CB + fix_score_outer[i][j]
                CB_count = CB_count + 1
            elif fix_loc[i][j]=='CT':
                CT = CT + fix_score_outer[i][j]
                CT_count = CT_count + 1
            elif fix_loc[i][j]=='AC':
                AC = AC + fix_score_outer[i][j]
                AC_count = AC_count + 1
            elif fix_loc[i][j]=='CA':
                CA = CA + fix_score_outer[i][j]
                CA_count = CA_count + 1
            elif fix_loc[i][j]=='CS':
                CS = CS + fix_score_outer[i][j]
                CS_count = CS_count + 1
            elif fix_loc[i][j]=='SC':
                SC = SC + fix_score_outer[i][j]
                SC_count = SC_count + 1
            elif fix_loc[i][j]=='CP':
                CP = CP + fix_score_outer[i][j]
                CP_count = CP_count + 1
            elif fix_loc[i][j]=='PC':
                PC = PC + fix_score_outer[i][j]
                PC_count = PC_count + 1
            elif fix_loc[i][j]=='CU':
                CU = CU + fix_score_outer[i][j]
                CU_count = CU_count + 1
            elif fix_loc[i][j]=='UC':
                UC = UC + fix_score_outer[i][j]
                UC_count = UC_count + 1
            elif fix_loc[i][j]=='BT':
                BT = BT + fix_score_outer[i][j]
                BT_count = BT_count + 1
            elif fix_loc[i][j]=='TB':
                TB = TB + fix_score_outer[i][j]
                TB_count = TB_count + 1
            elif fix_loc[i][j]=='TC':
                TC = TC + fix_score_outer[i][j]
                TC_count = TC_count + 1
            elif fix_loc[i][j]=='PS':
                PS = PS + fix_score_outer[i][j]
                PS_count = PS_count + 1
            elif fix_loc[i][j]=='SP':
                SP = SP + fix_score_outer[i][j]
                SP_count = SP_count + 1
            elif fix_loc[i][j]=='PU':
                PU = PU + fix_score_outer[i][j]
                PU_count = PU_count + 1
            elif fix_loc[i][j]=='UP':
                UP = UP + fix_score_outer[i][j]
                UP_count = UP_count + 1
            elif fix_loc[i][j]=='PT':
                PT = PT + fix_score_outer[i][j]
                PT_count = PT_count + 1
            elif fix_loc[i][j]=='TP':
                TP = TP + fix_score_outer[i][j]
                TP_count = TP_count + 1
            elif fix_loc[i][j]=='SU':
                SU = SU + fix_score_outer[i][j]
                SU_count = SU_count + 1
            elif fix_loc[i][j]=='US':
                US = US + fix_score_outer[i][j]
                US_count = US_count + 1
            elif fix_loc[i][j]=='ST':
                ST = ST + fix_score_outer[i][j]
                ST_count = ST_count + 1
            elif fix_loc[i][j]=='TS':
                TS = TS + fix_score_outer[i][j]
                TS_count = TS_count + 1
            elif fix_loc[i][j]=='UT':
                UT = UT + fix_score_outer[i][j]
                UT_count = UT_count + 1
            elif fix_loc[i][j]=='TU':
                TU = TU + fix_score_outer[i][j]
                TU_count = TU_count + 1
        
        ##################################################################
        
        # THIS WILL DEFINE EACH TRIAL AS EITHER PROJECT-FIRST (STRATEGY == 1)
        # STRUCTURE-MAPPING (STRATEGY == 2), SEMANTIC-CONSTRAINT (STRATEGY == 3)
        # IF THE SCORE FOR ONE STRATEGY IS GREATER THAN THE VALUE FOR THE OTHER TWO 
        # STRATEGIES. IT WILL ASSIGN STRATEGY == 0 FOR THAT TRIAL IF THIS IS NOT TRUE
        
        ##################################################################
        
       
        
        if (first_fix_A + first_fix_B + AB + BA + CT) > (first_fix_A + first_fix_C + AC + CA + BT) and (first_fix_A + first_fix_B + AB + BA + CT) > (first_fix_C + first_fix_T + first_fix_S + first_fix_P + first_fix_U + CS + SC + CP + PC + CT + TC):
            strategy = 1
        elif (first_fix_A + first_fix_C + AC + CA + BT) > (first_fix_A + first_fix_B + AB + BA + CT) and (first_fix_A + first_fix_C + AC + CA + BT) > (first_fix_C + first_fix_T + first_fix_S + first_fix_P + first_fix_U + CS + SC + CP + PC + CT + TC): 
            strategy = 2
        elif (first_fix_C + first_fix_T + first_fix_S + first_fix_P + first_fix_U + CS + SC + CP + PC + CT + TC) > (first_fix_A + first_fix_B + AB + BA + CT) and (first_fix_C + first_fix_T + first_fix_S + first_fix_P + first_fix_U + CS + SC + CP + PC + CT + TC) > (first_fix_A + first_fix_C + AC + CA + BT):
            strategy = 3        
        else:
            strategy = 0
        

    
        #####################################################
    
        # THIS CREATES A LIST CONTAINING STRATEGIES VALUES FOR EACH TRIAL
    
        ##################################################### 
    
        strategy_trials.append(strategy)
     
     
    
    #####################################################
    
    # THIS CREATES A LIST CONTAINING STRATEGIES FOR EACH SUBJECT
    
    ##################################################### 
    
    strategy_outer.append(strategy_trials)    




#####################################################
    
# THIS CREATES A CSV FILE CLASSIFYING THE COUNTS AND PERCENTAGES OF TRIALS FOR EACH PARTICIPANT AS EITHER PROJECT FIRST, STRUCTURE MAPPING, OR SEMANTIC-CONSTRAINT
    
#####################################################  

Project_First = []
Structure_Mapping = []
Semantic_Constraint = []
Project_First_count = []
Structure_Mapping_count = []
Semantic_Constraint_count = []

for idx, i in enumerate(subs):
    Project_First.append((strategy_outer[idx].count(1))/float(len(strategy_outer[idx])))
    Structure_Mapping.append((strategy_outer[idx].count(2))/float(len(strategy_outer[idx])))
    Semantic_Constraint.append((strategy_outer[idx].count(3))/float(len(strategy_outer[idx])))
    Project_First_count.append((strategy_outer[idx].count(1)))
    Structure_Mapping_count.append((strategy_outer[idx].count(2)))
    Semantic_Constraint_count.append((strategy_outer[idx].count(3)))
    
PF_array = np.array(Project_First)
SM_array = np.array(Structure_Mapping)
SC_array = np.array(Semantic_Constraint)
PF_array_count = np.array(Project_First_count)
SM_array_count = np.array(Structure_Mapping_count)
SC_array_count = np.array(Semantic_Constraint_count)

strategy_df = pd.DataFrame([PF_array, SM_array, SC_array, PF_array_count, SM_array_count, SC_array_count, subs])
strategy_df = strategy_df.transpose()
strategy_df.columns = ['Project-First', 'Structure-Mapping', 'Semantic_Constraint', 'Project-First_count', 'Structure-Mapping_count', 'Semantic_Constraint_count', 'Subject']

#SAVE THE OUTPUT TO A CSV FILE TO BE USED FOR FURTHER ANALYSIS
strategy_df.to_csv('strategy_classification_6-24-15_fix_3_strategies.csv')
