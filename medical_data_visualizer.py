import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
def df():
    df = input('Input file directory: ')
    df_temp = []
    if df != '':
        for each in df:
            if each == '"':
                pass
            elif each == '\\':
                df_temp.append('/')
            else:
                df_temp.append(each)
    df = ''.join(df_temp)
    
    try:
        df = pd.read_csv(df)
        df = pd.DataFrame(df)
    except (ImportError, FileNotFoundError):
        return 'df_err'
    return df
df = df()

# 2
def fix_input(x, target):
    
    if isinstance(x, (str, int, float, np.integer)):
        x = [x]
    elif type(x) == tuple:
        x = list(x)
    elif type(x) == list:
        pass
    else:
        input_error = 'err_5'
        return input_error

    #=== Converts numbered string to numbers collected via input function. ===#
    for x_key, x_value in enumerate(x):
        try:
            x[x_key] = float(x_value)
        except:
            pass

    #=== Begins cap matching process ===#
    for x_key, x_value in enumerate(x):
        for each in target:
            if type(x_value) == str and type(each) == str:
                if x_value.upper() == each.upper():
                    x[x_key] = each
                    input_error = 0
                    break
                else:
                    input_error = 'err_5'
            elif type(x_value) != str and type(each) != str:
                if float(x_value) == float(each):
                    x[x_key] = each
                    input_error = 0
                    break
                else:
                    input_error = 'err_5'
            else:
                input_error = 'err_5'
                pass
                    
    if input_error != 0:
        return input_error

    return x
def bmi():
    #bmi = [ weight (kg)/height (cm)/height (cm) ] x 10,000
    bmi = list()
    cat_list = 'weight', 'height'
    cat_list = fix_input(cat_list, df.columns)
    for each in df.index:
        weight = np.int16(np.round((df.iloc[each][cat_list[0]]), 0))
        height = np.int16(np.round((df.iloc[each][cat_list[1]]), 0))
        bmi.append(np.int16(np.round(((weight/height/height)*10000), 0)))

    for k, v in enumerate(bmi):
        if v > 25:
            bmi[k] = 1
        else:
            bmi[k] = 0

    return bmi
bmi_list = bmi()
df['overweight'] = pd.Series(bmi_list)

# 3
def normalize(x, dataframe):

    if type(dataframe) == pd.core.frame.DataFrame:
        pass
    else:
        return print('Type Error: \"Dataframe\" is the wrong data type.')
    
    target = dataframe.columns
    x = ''.join(fix_input(x, target))
    
    for each in dataframe.index:
        if dataframe.iloc[each][x] <= 1:
            dataframe.loc[each, x] = 0
        else:
            dataframe.loc[each, x] = 1
    
    return dataframe
df = normalize('cholesterol', df)
df = normalize('gluc', df)

def calculations(df, operation, columns, criteria = None, rounded = None, table_criteria = None):
        
        '''
        #     = !! READ-ME Comments !! = 
        ### -1- operation:
                --- What type of calculation to perform, only one per-function. Listed are as follows, total, average, compare, minimum, maximum.
                >> terms:
                --- 'tabl' : table, returns the table for all entries within the specified column. 
                --- 'ttl'/'ttl_l' : total, returns the total amount and percentage of the specified entry/entires from 'table_criteria'. For unspecified ones, use 'ttl_l'. 
                --- 'avrg' : average, returns the average amount within the specified column, numerical only.
                --- 'com' : compare, returns the comparison between the occurance of both specified entries.
                --- 'max'/'most' : maximum, 'max' returns the highest entry in terms of amount within the specified column (numerical only). While 'most', returns the most entry that occurs within the specified column.
                --- 'min'/'least' : minimum, 'min' returns the lowest entry in terms of amount within the specified column (numerical only). While 'least', returns the least entry that occurs within the specified column.
        ### -2- columns:
                --- Enter single or multiple input(s), separated by commas. Column names must follow the names used as per csv table. Is not case sensitive.
        ### -3- criteria:
                --- Enter single or multiple input(s), separated by commas. Also write in order of the criteria needed to calculate corresponding to the column. Is not case sensitive.
                >> terms:
                --- Where x is a number, '_MT_x' is more than ('_MTE_x' with equal), '_LT_x' is less than ('_LTE_x' with equal) and '_RG_x' is range.
                --- Eg: The average income of men (in the 'gender' column) wearing blue shirts (in the 'shirts' column) that makes ranging between 50k until 75k (in the 'salary' column), thus the list would be ['Men', 'Blue', '_RG_50000, 75000']
        ### -4- rounded:
                --- Rounds up the number is specified. Entering 0 returns whole numbers.
        ### -5- table_criteria:
                --- When going for the ttl,total or ttl_l function, use a variable to specify multiple entries or a single entry. A single entry could also be specified while running use the function (an input function will be executed).
                >> total() types:
                --- ttl, returns the value for each stated criteria. ttl_l, returns the ones that were not stated (leftovers).
        '''

        #= Set up =#
        def load_dataset(df):
            #=== Loading the data ===#
            # 1) getting every name of each column
            dfcolumns = np.array(df.columns)

            # 2) getting every value of every column
            dfrows = []
            for k, v in enumerate(dfcolumns):
                dfrows.append(df[v])
            row_length = len(dfrows[0])

            # 3a) combining both dfcolumns & dfvalues into a single py dictionary
            np_table = {} # 
            for k, v in enumerate(dfcolumns):
                np_table.setdefault(v,[]).append(dfrows[k])
            # 3b) creates variables 'cN' (where N is a number) that functions as keys when indexing np_table's columns
            for k, v in enumerate(dfcolumns):
                exec(f"c{k} = '{v}'")
                # now the dictionary could be accessed as such as well, np_table[c0]
            c_vars = [v for k, v in locals().items() if k.startswith('c')] # to call all the 'cN' variables

            return dfcolumns, dfrows, np_table, c_vars, row_length
        dfcolumns, dfrows, np_table, c_vars, row_length = load_dataset(df)
        v_df = df
        points = rounded
        #===##===#
        def round_up(number, points = None):
            if points == None:
                return number
            elif points == 0:
                return int(round(number, points))
            else:
                return round(number, points)
        #===##===#
        def fix_input(x, target):
            
            #=== Converts numbered string to numbers collected via input function. ===#
            for x_key, x_value in enumerate(x):
                try:
                    x[x_key] = float(x_value)
                except:
                    pass

            #=== Begins cap matching process ===#
            for x_key, x_value in enumerate(x):
                for each in target:
                    if type(x_value) == str and type(each) == str:
                        if x_value.upper() == each.upper():
                            x[x_key] = each
                            input_error = 0
                            break
                        else:
                            input_error = 'err_5'
                    elif type(x_value) != str and type(each) != str:
                        if float(x_value) == float(each):
                            x[x_key] = each
                            input_error = 0
                            break
                        else:
                            input_error = 'err_5'
                    else:
                        input_error = 'err_5'
                        pass
                        
            if input_error != 0:
                return input_error

            return x
        #===##===#
        def error_types(input_error):
            if input_error == 'err_1': # Inside: cal_setup.
                return 'Type Error: Parameter(s) was a wrong data type. Please read the READ-ME comments for additional info.'
            elif input_error == 'err_2': # Inside: cal_setup.
                return 'Type Error: Criteria or column is neither a str or list type. Please read the READ-ME comments for additional info.'
            elif input_error == 'err_3': # Inside: cal_setup.
                return 'Count Error: Number of criteria exceeds or equals to number of columns. Please read the READ-ME comments for additional info.'
            elif input_error == 'err_4': # Inside: cal_setup.
                return 'Key Error: Mismatch \"column\" entry or \"column\" not found.'
            elif input_error == 'err_5': # Inside: cal_setup.
                return 'Input Error: Listed \"criteria\"(s) was a mismatch or not found.'
            elif input_error == 'err_6': # Inside: total.
                return 'Type Error: Elements are neither a str/int/float data type. Please check input or the data set.'
            elif input_error == 'err_7': # Inside: cal_setup, total.
                return 'Range Error: Request out of range.'
            elif input_error == 'err_8': # Inside: avrg, max & min.
                return f'Type Error: The data entry for \"{columns[-1]}\" is not a number type. Please select a column with only numeric entries.'
            elif input_error == 'err_9': # Inside: avrg.
                return f'Name Error: Column \'{columns[-1].upper()}\' not found. Please read description for additional info.'
            elif input_error == 'err_10': # Inside: avrg.
                return 'Type Error: Last column must consists of number values only.'
            elif input_error == 'err_11': # Inside: avrg.
                return 'Input Error: No criteria/entry was defined for the table to evaluate.'
            else:
                if input_error[0] == 'err_list_1': # Inside: cal_setup.
                    input_error = input_error[1]
                    return f'Input Error: Invalid input for \"{input_error}\", Please read the READ-ME comments for additional info.'
                elif input_error[0] == 'err_list_2': # Inside: compare.
                    return f'Input Error: No matching entry for either {input_error[1]} or {input_error[2]}.'
                elif input_error[0] == 'err_list_3': # Inside: compare.
                    return f'Input Error: The \"{input_error[1]}\" was not defined.'
                elif input_error[0] == 'err_list_4': # Inside: compare.
                    return 'Input Error: Neither comparison entries were defined.'
        #===##===#
        def cal_setup(v_df = v_df, columns = columns, criteria = criteria):

            #=== Captures any input error. ===#
            # 1) for columns
            if isinstance(columns, (str, int, float, tuple)):
                pass
            else:
                input_error = 'err_1'
                return input_error
            # 2) for criteria
            if criteria != None:
                if isinstance(criteria, (str, int, float, tuple)):
                    pass
                else:
                    input_error = 'err_2'
                    return input_error
                    
            #=== Converts both inputs into a list. ===#
            # 1) for columns
            if type(columns) == tuple:
                columns = list(columns)
            else:
                columns = [columns]
            # 2) for criteria   
            if type(criteria) == tuple:
                criteria = list(criteria)
            elif criteria == None:
                pass
            else:
                criteria = [criteria]

            #=== Checks if number of 'criteria' doesn't exceed or equal to the number of 'columns'. ===#
            if criteria != None:
                if len(criteria) == len(columns)-1:
                    pass
                else:
                    input_error = 'err_3'
                    return input_error
            else:
                pass

            #=== Converting all criterias listed to string to avoid TypeErrors. ===#
            if type(criteria) == list:
                for k, v in enumerate(criteria):
                    if type[v] != str:
                        criteria[k] = str(v)
                    else:
                        pass

            #=== Converting the column list names into the correct terms used in df. ===#
            for a_key, a_val in enumerate(columns):
                columns[a_key] = a_val.upper()
                for b_key, b_val in enumerate(dfcolumns):
                    dfcolumns[b_key] = b_val.upper()
                    if columns[a_key] == dfcolumns[b_key]:
                        columns[a_key] = c_vars[b_key]
                        input_error = 0 # False
                        break
                    else:
                        input_error = 'err_4'

            #=== Converting the criterias to match the terms used in each of the df columns respectively. ===#
            if criteria != None and input_error == 0:
                for k, v in enumerate(criteria):
                    if ('_MT_' in v or '_MTE_' in v or '_LT_' in v or '_LTE_' in v or '_RG_' in v):
                        pass
                    else:
                        for each in np.unique(v_df[columns[k]]):
                            try: # If string
                                if criteria[k].upper() == each.upper():
                                    criteria[k] = each
                                    input_error = 0 # Error = False
                                    break
                                else:
                                    input_error = 'err_5'
                            except: # If numeric
                                criteria[k] = float(criteria[k])
                                if criteria[k] == each:
                                    criteria[k] = each
                                    input_error = 0 # Error = False
                                    break
                                else:
                                    input_error = 'err_5'
            
            if input_error != 0:
                return input_error
            
            #=== Going through the criteria if multiple/set input (list), trimming the dataset begins here. ===#
            if type(criteria) == list:
                for k, v in enumerate(criteria):
                    if type(v) == str:
                        if '_MT_' in v:
                            try:
                                num = float(v[4:]) ##___##; pass
                                v_df = v_df[v_df[columns[k]] > num] ##___##; print('_MT_ === ',len(v_df))
                            except:
                                input_error = ('err_list_1', v)
                                return input_error
                        elif '_MTE_' in v:
                            try:
                                num = float(v[5:]) ##___##; pass
                                v_df = v_df[v_df[columns[k]] >= num] ##___##; print('_MTE_ === ',len(v_df))
                            except:
                                input_error = ('err_list_1', v)
                                return input_error
                        elif '_LT_' in v:
                            try:
                                num = float(v[4:]) ##___##; pass
                                v_df = v_df[v_df[columns[k]] < num] ##___##; print('_LT_ === ',len(v_df))
                            except:
                                input_error = ('err_list_1', v)
                                return input_error
                        elif '_LTE_' in v:
                            try:
                                num = float(v[5:]) ##___##; pass
                                v_df = v_df[v_df[columns[k]] <= num] ##___##; print('_LTE_ === ',len(v_df))
                            except:
                                input_error = ('err_list_1', v)
                                return input_error
                        elif '_RG_' in v:
                            # going through for all 'range' in the criteria set (if any) #
                            x='' ; num_1 = '' ; num_2 = '' ; next = 0   # counters used for this loop of range only
                            for key, val in enumerate(v):
                                if val == ',':
                                    x=''
                                    next = 1
                                if val in '1234567890':
                                    if next == 1:
                                        num_2 = num_2+val
                                    else:
                                        num_1 = num_1+val
                                    pass
                            try:
                                num_1, num_2 = map(float,(num_1, num_2)) #; print(num_1, num_2)
                                v_df = v_df[v_df[columns[k]] >= num_1] ; v_df = v_df[v_df[columns[k]] <= num_2]
                                x='' ; num_1 = '' ; num_2 = '' ; next = 0  # resets all of the counters for range only
                                ##___## print('_RG_ === ',len(v_df))
                                if v_df.empty:
                                    input_error = 'err_7'
                                    return input_error
                            except:
                                input_error = ('err_list_1', v)
                                return input_error
                    else:
                        v_df = v_df[v_df[columns[k]] == v]

            return v_df, columns, criteria
        try:
            v_df, columns, criteria = cal_setup()
        except:
            input_error = cal_setup()
            return error_types(input_error)
        
        #= Calculations =#
        def table(keyword = ''):
            
            if keyword == 'COMP_slf_TRIGGER':
                keyword = ''
            else:
                #keyword = input('Enter a keyword, shifts the arrangement of entries containing the keyword to the bottom of the list, ie: moving all \'other\' entires to the bottom. Default (no input) will result in the default alphabetical order')
                pass

            #=== Identify the data type listed within the column. ===#
            for each in np.unique(v_df[columns[-1]]):
                if isinstance(each, (int, float, np.integer)):
                    values = 'Number'
                else:
                    values = 'String'

            #=== Change the 'keyword' data type to a float, if necessary. ===#
            try:
                keyword = float(keyword)
            except:
                pass
            
            #=== Cleaning up the np.array to a clean dict. ===#
            # 1) creating the first column/key with it's value. Also, if specified in the def's parameter, shifts all specified entries containing the word within the keyword, to the bottom of the list
            #    --- Eg: moving all 'other' entires to the bottom
            new_array = {}
            counter = 0
            later_input = {}
            
            for key, listings in enumerate(np.unique(v_df[columns[-1]], return_counts = 1)):
                if counter < len(listings):
                    for each in listings:
                        if values == 'String' and type(keyword) == str:
                            match_key = each.upper()
                            if keyword.upper() in match_key.split():
                                later_input.setdefault(keyword,[]).append(each)
                                later_input.setdefault('value',[]).append(counter)
                                pass
                            else:
                                new_array.setdefault(f'{columns[-1]}',[]).append(each)
                        elif values == 'Number' and type(keyword) == float or values == 'Number' and keyword == '':
                            if keyword == each:
                                later_input.setdefault(keyword,[]).append(each)
                                later_input.setdefault('value',[]).append(counter)
                                pass
                            else:
                                new_array.setdefault(f'{columns[-1]}',[]).append(each)
                        else:
                            input_error = 'err_6'
                            input_error = error_types(input_error)
                            return input_error
                        counter = counter + 1
                elif len(later_input)>0:
                    for each in later_input.get(keyword):
                        new_array.setdefault(f'{columns[-1]}',[]).append(each)

            # 2) creating the second column/key with it's value. Also shifts the values correctly to match the first column entry, if specified in the def's parameter.
            counter = 0
            for key, value in enumerate(listings):
                if len(later_input)>0:
                    try:
                        key == later_input.get('value')[counter]
                        counter = counter + 1
                        pass
                    except:
                        new_array.setdefault('Occurance',[]).append(value)
                        new_array.setdefault('Percentage',[]).append( round_up((value/len(v_df)*100), points) )
                else:
                    new_array.setdefault('Occurance',[]).append(value)
                    new_array.setdefault('Percentage',[]).append( round_up((value/len(v_df)*100), points) )
            if len(later_input)>0:
                for each in later_input.get('value'):
                    new_array.setdefault('Occurance',[]).append(listings[each])
                    new_array.setdefault('Percentage',[]).append( round_up((value/len(v_df)*100), points) )

            try:
                entire_table = pd.DataFrame(new_array, index=[''] * len(new_array.get(f'{columns[-1]}')))
                entire_table = entire_table.rename(columns = {columns[-1]:columns[-1].capitalize()}) ; columns[-1] = columns[-1].capitalize()
            except:
                input_error = 'err_7'
                input_error = error_types(input_error)
                return input_error

            return entire_table
        #===##===#
        def total(table_criteria = table_criteria):
            
            entire_table = table('COMP_slf_TRIGGER')
            
            #=== Reads the 'table_criteria' if any, throws an error if mismatch or none given. ===#
            if table_criteria == None:
                table_criteria = input('Input entry to return it\'s values. To input multiple entries, please use a varible instead.')
                if table_criteria == '':
                    input_error = 'err_11'
                    input_error = error_types(input_error)
                    return input_error
            
            #=== Converts it to a list. ===#
            if type(table_criteria) == tuple:
                table_criteria = list(table_criteria)
            elif isinstance(table_criteria, (float, int, str, np.integer)):
                table_criteria = [table_criteria]
            elif type(table_criteria) == list:
                pass
            else:
                input_error = 'err_1'
                input_error = error_types(input_error)
                return input_error
            
            #=== Converts the input criteria and fix any capitalization mismatch. ===#
            table_criteria = fix_input(table_criteria, entire_table[columns[-1]])
            # If it returns an error, mismatch criteria. #
            if table_criteria == 'err_5':
                input_error = table_criteria
                input_error = error_types(input_error)
                return input_error

            #=== Getting the index number on the requested entry for the iloc function. ===#
            n = 0
            leftover_criteria = []
            t_table = entire_table[columns[-1]]
            for a_key, a_val in enumerate(table_criteria):
                for b_key, b_val in enumerate(t_table):
                    if n < len(t_table):
                        leftover_criteria.append(b_key)
                        n = n + 1
                    if a_val == b_val:
                        table_criteria[a_key] = b_key
                        leftover_criteria.remove(table_criteria[a_key])
            
            #=== Getting the values. ===#
            n = 0
            data_list = {}
            ttl_values = list()
            if operation == 'ttl':
                while n < len(table_criteria):
                    get_data = entire_table.iloc[int(table_criteria[n])].values
                    ttl_values.append(float(get_data[1]))
                    data_list[get_data[0]] = float(get_data[1])
                    n = n + 1
            else:
                while n < len(leftover_criteria):
                    get_data = entire_table.iloc[int(leftover_criteria[n])].values
                    ttl_values.append(float(get_data[1]))
                    data_list[get_data[0]] = float(get_data[1])
                    n = n + 1

            
            #=== Finally, calculates the percentage. ===#
            total = 0
            for every in ttl_values:
                total = every + total

            data_list['Total %'] = round_up(float((total/len(v_df))*100), points)
            
            return data_list
        #===##===#
        def average():

            #=== Checks the input column, if entries are non numeric, returns an error message. ===#
            test = v_df[columns[-1]][0]
            try:
                float(test)
            except:
                input_error = 'err_8'
                input_error = error_types(input_error)
                return input_error
            
            #=== Calculation starts. ===#
            if type(criteria) == list: # calculate the average if 'criteria' was a list
                try:
                    average = np.average(np.array(v_df[columns[-1]]))
                    average = round_up(float(average), points)
                except (KeyError, TypeError) as err:
                    k_err = 'err_9'
                    t_err = 'err_10'
                    input_error = {
                        KeyError: k_err,
                        TypeError: t_err
                    }
                    input_error = input_error[type(err)]
                    input_error = error_types(input_error)
                    return input_error
            else:
                average = np.average(np.array(v_df[columns])) # calculate the average if 'criteria' was none
                average = round_up(float(average), points)

            statement = f'The average {columns[-1]} for {criteria[-1]} is: {average}'
            return average, statement
        #===##===#
        def compare():
            
            entire_table = table('COMP_slf_TRIGGER')
            first_element = input('Enter 1st element to compare to')
            second_element = input('Enter 2nd element to compare with')
            
            #=== Checks if inputs matches the columns. ===#
            for each in entire_table.iloc:
                if type(each) == str:
                    if each[columns[-1]].upper() == first_element.upper():
                        fe_val = each['Occurance']
                        break
                    else:
                        fe_val = False
                else:
                    if each[columns[-1]] == first_element:
                        fe_val = each['Occurance']
                        break
                    else:
                        fe_val = False

            for each in entire_table.iloc:
                if type(each) == str:
                    if each[columns[-1]].upper() == second_element.upper():
                        se_val = each['Occurance']
                        break
                    else:
                        se_val = False
                else:
                    if each[columns[-1]] == second_element:
                        se_val = each['Occurance']
                        break
                    else:
                        se_val = False

            if fe_val == False or se_val == False:
                if first_element == '':
                    first_element = '-NONE_DEFINE-'
                if second_element == '':
                    second_element = '-NONE_DEFINE-'
                if first_element == '-NONE_DEFINE-' and second_element == '-NONE_DEFINE-':
                    input_error = ('err_list_4', first_element, second_element)
                    input_error = error_types(input_error)
                    return input_error
                if first_element == '-NONE_DEFINE-' or second_element == '-NONE_DEFINE-':
                    if first_element == '-NONE_DEFINE-':
                        first_element = 'First Element'
                        missing_element = first_element
                    elif second_element == '-NONE_DEFINE-':
                        second_element = 'Second Element'
                        missing_element = second_element
                    input_error = ('err_list_3', missing_element)
                    input_error = error_types(input_error)
                    return input_error
                else:
                    input_error = ('err_list_2', first_element, second_element)
                    input_error = error_types(input_error)
                    return input_error
                
            #=== Calculation begins. ===#       
            if fe_val > se_val:
                com_data = {first_element: fe_val, second_element: se_val, 'difference': fe_val - se_val, 'percentage': round_up(((fe_val - se_val)/fe_val*100),points)}
                compare = f'\'{first_element}\' is greater than \'{second_element}\', by {fe_val - se_val} ({round_up(((fe_val - se_val)/fe_val*100),points)}%)'
            elif se_val > fe_val:
                com_data = {first_element: fe_val, second_element: se_val, 'difference': se_val - fe_val, 'percentage': round_up(((se_val - fe_val)/se_val*100),points)}
                compare = f'\'{second_element}\' is greater than \'{first_element}\', by {se_val - fe_val} ({round_up(((se_val - fe_val)/se_val*100),points)}%)'
            else:
                com_data = {first_element: fe_val, second_element: se_val}
                compare = f'\'{first_element}\' is equal to \'{second_element}\''
            
            return compare, com_data
        #===##===#
        def maximum():

            if operation == 'most':
                entire_table = table('COMP_slf_TRIGGER')
                max_occurance = entire_table['Occurance'].max()
                most_data = entire_table[entire_table['Occurance'] == max_occurance]
                most_data = most_data.iloc[0].values

                return most_data

            #=== Checks the input column, if entries are non numeric, returns an error message. ===#
            test = v_df[columns[-1]][0]
            try: 
                float(test)
            except:
                input_error = 'err_8'
                input_error = error_types(input_error)
                return input_error
            
            entire_table = input('Enter \'Y\' and hit Enter to return the entire table, otherwise press \'Enter\' to continue.')
            
            max_data = v_df[columns[-1]].max()
            maximum = f'The maximum {columns[-1]} is {v_df[columns[-1]].max()}.'
            max_v_df = None
            
            if entire_table == 'Y' or entire_table == 'y':
                max_v_df = v_df[v_df[columns[-1]] == max_data]
                return maximum, max_data, max_v_df
            else:
                return maximum, max_data, max_v_df
        #===##===#
        def minimum():

            if operation == 'least':
                entire_table = table('COMP_slf_TRIGGER')
                min_occurance = entire_table['Occurance'].min()
                least_data = entire_table[entire_table['Occurance'] == min_occurance]
                least_data = least_data.iloc[0].values

                return least_data

            #=== Checks the input column, if entries are non numeric, returns an error message. ===#
            test = v_df[columns[-1]][0]
            try:
                float(test)
            except:
                input_error = 'err_8'
                input_error = error_types(input_error)
                return input_error
                
            entire_table = input('Enter \'Y\' and hit Enter to return the entire table, otherwise press \'Enter\' to continue.')
            
            min_data = v_df[columns[-1]].min()
            minimum = f'The minimum \"{columns[-1]}\" is, {min_data}.'
            min_v_df = None
            
            if entire_table == 'Y' or entire_table == 'y':
                min_v_df = v_df[v_df[columns[-1]] == min_data]
                return minimum, min_data, min_v_df
            else:
                return minimum, min_data, min_v_df

        #= Returns =#
        if operation == 'tabl':
            entire_table = table()
            return entire_table 
        #===##===#
        if operation == 'ttl' or operation == 'ttl_l':
            total_value = total()
            return total_value 
        #===##===#
        elif operation == 'avrg':
            average_value, statement = average()
            return average_value, v_df
        #===##===#
        elif operation == 'com':
            compare_value = compare()
            return compare_value
        #===##===#
        elif operation == 'max' or operation == 'most':
            maximum_value, max_data, max_v_df = maximum()
            return maximum_value, max_data, max_v_df
        #===##===#
        elif operation == 'min' or operation == 'least':
            minimum_value, min_data, min_v_df = minimum()
            return minimum_value, min_data, min_v_df
        
        #= END =#
# Quick ref: 'tabl':table, 'ttl'/'ttl_l':total, 'avrg':average, 'com':compare, 'max'/'most': maximum, 'min'/'least': minimum

# 4
def draw_cat_plot():
    
    # 5
    id_vars = 'id', 'age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo', 'cardio'
    melt_df = df.melt(id_vars) # 'melt'ed dataframe (THIS WILL BE df_cat)
    df_cat = melt_df
    
    
    # 6
    # creating the value table to insert back to all the tables accordingly 
    keys_list = ['Cardio', 'Value']
    values_list = [0, 1]

    ## For cardio = 0 ##
    # 1) calculate every entries where value = 1, (cardio = 0)
    columns = 'cardio', 'value', 'variable' ; criteria = 0, 0
    df_cat_c0v0 = calculations(df_cat, 'tabl', columns, criteria, rounded = 0)
    # 2) calculate every entries but value = 2, (cardio = 0)
    columns = 'cardio', 'value', 'variable' ; criteria = 0, 1
    df_cat_c0v1 = calculations(df_cat, 'tabl', columns, criteria, rounded = 0)
    # 3) adds in the 'value' column to their respective tables & values
    df_cat_c0v0[keys_list] = [values_list[0], values_list[0]]
    df_cat_c0v1[keys_list] = [values_list[0], values_list[1]]
    # 4) concatenates the two tables
    df_cat_cardio_0 = pd.concat([df_cat_c0v0, df_cat_c0v1])
    # 5) renames the 'Occurance' column to 'Total'
    df_cat_cardio_0.rename(columns = {df_cat_cardio_0.columns[1] : 'Total'}, inplace = 1)

    ## For cardio = 1 ##
    # 1) step 1, as above
    columns = 'cardio', 'value', 'variable' ; criteria = 1, 0
    df_cat_c1v0 = calculations(df_cat, 'tabl', columns, criteria, rounded = 0)
    # 2) step 2, as above
    columns = 'cardio', 'value', 'variable' ; criteria = 1, 1
    df_cat_c1v1 = calculations(df_cat, 'tabl', columns, criteria, rounded = 0)
    # 3) step 3, as above
    df_cat_c1v0[keys_list] = [values_list[1], values_list[0]]
    df_cat_c1v1[keys_list] = [values_list[1], values_list[1]]
    # 4) step 4, as above
    df_cat_cardio_1 = pd.concat([df_cat_c1v0, df_cat_c1v1])
    # 5) step 5, as above
    df_cat_cardio_1.rename(columns = {df_cat_cardio_1.columns[1] : 'Total'}, inplace = 1)
    
    
    # 7
    df_cat_all = pd.concat([df_cat_cardio_0, df_cat_cardio_1])
    df_cat = df_cat_all
    
    
    # 8
    df_catplot = sns.catplot(
        df_cat,
        x = 'Variable',
        y = 'Total',
        hue = 'Value',
        order = ('active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'),
        kind = 'bar',
        col = 'Cardio', # This splits the chart according to 'cardio' & prints the chart side-by-side (col = column)
        legend_out = 1,
    )
    fig = df_catplot
    
    
    # 9
    fig.savefig('catplot.png')
    return fig
    

# 10
def draw_heat_map():
    # Getting data for both weight and height respectively in terms of occurances
    height_data = calculations(df, 'tabl', 'height', rounded = 4)
    weight_data = calculations(df, 'tabl', 'weight', rounded = 4)

    fig, axes = plt.subplots(1, 2, figsize=(6,50), gridspec_kw = {'wspace':0.45})
    height_map = sns.heatmap(
        height_data.pivot_table(
            index = 'Height',
            values = 'Occurance',
            aggfunc = 'sum'
            ),
        annot = True,
        cbar = False,
        cmap = 'YlGnBu',
        ax = axes[0]
        )
    weight_map = sns.heatmap(
        weight_data.pivot_table(
            index = 'Weight',
            values = 'Occurance',
            aggfunc = 'sum'
            ),
        annot = True,
        cmap = 'YlGnBu',
        ax = axes[1]
        )
    df_heat = df
    
    
    # 11
    # Getting the incorrect data for the 'ap's, when 'ap_lo' > 'ap_hi'
    Ap_id = np.where((df_heat['ap_lo'] > df_heat['ap_hi']), df_heat['id'], '') #; np.set_printoptions(threshold = np.inf)
    Ap_id = np.delete(Ap_id, np.where(Ap_id == ''))
    Ap_id = Ap_id.astype(np.int64) # the indices in a list
    
    # Calculating the percentile from the previously acquired (occurances) data
    Hp2_5 = np.percentile(height_data['Height'], 2.5)
    Hp2_5 = list(i for i in height_data['Height'] if i < Hp2_5) #; print(f'Hp2_5 = {Hp2_5}')

    Hp97_5 = np.percentile(height_data['Height'], 97.5)
    Hp97_5 = list(i for i in height_data['Height'] if i > Hp97_5) #; print(f'Hp97_5 = {Hp97_5}')

    Wp2_5 = np.percentile(weight_data['Weight'], 2.5)
    Wp2_5 = list(i for i in weight_data['Weight'] if i < Wp2_5) #; print(f'Wp2_5 = {Wp2_5}')

    Wp97_5 = np.percentile(weight_data['Weight'], 97.5)
    Wp97_5 = list(i for i in weight_data['Weight'] if i > Wp97_5) #; print(f'Wp97_5 = {Wp97_5}')
    #print(f'Hp2_5 = {Hp2_5} ----- Hp97_5 = {Hp97_5} ----- Wp2_5 = {Wp2_5} ----- Wp97_5 = {Wp97_5}')
    
    # Dropping the listed indices
    def drop_multiple_rows(df, values, details = False):
        
        def fix_input(x, target):
                
                if type(x) == list:
                    pass
                else:
                    x = [x]
                
                #=== Converts numbered string to numbers collected via input function. ===#
                for x_key, x_value in enumerate(x):
                    try:
                        x[x_key] = float(x_value)
                    except:
                        pass
                
                #=== Begins cap matching process ===#
                for x_key, x_value in enumerate(x):
                    for each in target:
                        if type(x_value) == str and type(each) == str:
                            if x_value.upper() == each.upper():
                                x[x_key] = each
                                input_error = False
                                break
                            else:
                                input_error = True
                        elif type(x_value) != str and type(each) != str:
                            if float(x_value) == float(each):
                                x[x_key] = each
                                input_error = False
                                break
                            else:
                                input_error = True
                        else:
                            input_error = True
                            pass
                            
                if input_error == True:
                    return input_error

                return x
        
        if type(values) == dict:
            pass
        else:
            return print('Type Error: Values must be a dictionary.')
        
        column = list(values.keys())    
        column_ret = fix_input(column, df)
        if column_ret == True:
            return print(f'Name Error: Column \'{column.upper()}\' was not found.')
        else:
            column = column_ret
            
        table = pd.DataFrame(columns = ['Column','Value','Index'])
        index = 1
        for k, v in enumerate(column):
            values_list = values[v]
            value_check = any(isinstance(sub, (list, tuple)) for sub in values_list)
            if value_check == True:
                new_list = values_list[0]
                n = 1
                while n < len(values_list):
                    new_list.extend(values_list[n])
                    n = n + 1
                values_list = new_list
            for each in values_list:
                to_drop = df[df[column[k]] == each].index
                #print(each, type(to_drop[0]))
                try:
                    if details == True:
                        table.loc[index, ['Column','Value','Index']] = [column[k], each, to_drop[0]]
                    df = df.drop(to_drop)
                except:
                    pass
                index = index + 1

        if details == True:
            return df, table
        else:
            return df
    df_heat = drop_multiple_rows(df_heat, {'height':[Hp2_5, Hp97_5], 'weight':[Wp2_5, Wp97_5], 'id':Ap_id})
    
    
    # 12
    corr = df_heat
    corr = corr.corr()
    

    # 13
    mask = np.triu(np.ones_like(corr))
    
    
    # 14
    fig, axs = plt.subplots(figsize = (10,8))
    

    # 15
    sns.heatmap(
        corr, 
        mask = mask, 
        annot = True, 
        fmt = '.1f', 
        ax = axs, 
        cmap = "icefire", 
        center = 0,
        vmin = -.16,
        vmax = .32,
        cbar_kws = {'shrink':.7}
        )
    
    
    # 16
    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()
draw_heat_map()