##### Dataset Link: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams #####

### Libraries/Packages ###
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


### Variables/Parameters ###
PRINT_STUDENTS = 10


### Functions/Methods ###
## Read the file path and return it to a variable ##
def read_dataset(file):
    ## Dataframe - dtype: Declare specific types ##
    df = pd.read_csv(file, dtype={'math score': int, 'reading score': int, 'writing score':int})
    return df


## Calculate the average for every Student ##
def average(data):
    data['average score'] = (data['math score'] + data['reading score'] + data['writing score'])/3
    return data


## Convert strings records to numeric data - mapping ##
def numeric_conversion(data):
    ## Mapping ##
    gender_mapping = {'female': 0, 'male': 1}
    race_mapping = {'group A': 0,'group B': 1,'group C': 2,'group D': 3,'group E': 4}
    parent_education_mapping = {'some high school': 0,'high school': 1,'some college': 2,"associate's degree": 3,"bachelor's degree": 4,"master's degree": 5}
    lunch_mapping = {'free/reduced': 0,'standard': 1}
    preparation_mapping = {'none': 0,'completed': 1}

    ## Replace each string data element with its respective numeric ##
    data['gender'] = data['gender'].replace(gender_mapping)
    data['race/ethnicity'] = data['race/ethnicity'].replace(race_mapping)
    data['parental level of education'] = data['parental level of education'].replace(parent_education_mapping)
    data['lunch'] = data['lunch'].replace(lunch_mapping)
    data['test preparation course'] = data['test preparation course'].replace(preparation_mapping)
    return data


## Ask the user on how many Intervals/Clusters they want the data to be split into ##
def intervals(): 
    while True:
        try:
            num_intervals = int(input("[SYSTEM] How many Intervals do you wish to have? -> "))
            if 1 <= num_intervals <= 100: # Positive.
                return num_intervals # Successful.
            else:
                print("[SYSTEM] The input was out of bounds, please renter your input. -> ")
        except ValueError as e:
            print(f"Input was invalid, enter an integer. Log: {e}")


## Enter the Data for a New Student ##
def add_student():
    student_data = {}
    
    ## Gender ##
    while True:
        gender_in = input('[SYSTEM] Enter gender -> ').lower()
        if gender_in in ['male', 'female']:
            student_data['gender'] = gender_in
            break
        else:
            print("[SYSTEM] Invalid input for the gender attribute, try again.\n")
    
    ## Race ##
    while True:
        race_in = input('[SYSTEM] Enter race/ethnicity (Only the letter) -> ').upper()
        if race_in in ['A', 'B', 'C', 'D', 'E']:
            student_data['race/ethnicity'] = "group " + race_in
            break
        else:
            print("[SYSTEM] Invalid input for the race attribute, try again.\n")

    ## Parental level of Education ##
    while True:
        ple_in = input('[SYSTEM] Enter parental level of education -> ').lower()
        if ple_in in ['some high school', 'high school', 'some college', "associate's degree", "bachelor's degree", "master's degree"]:
            student_data['parental level of education'] = ple_in
            break
        else:
            print("[SYSTEM] Invalid input for the parental level of education attribute, try again.\n")

    ## Lunch ##
    while True:
        lunch_in = input('[SYSTEM] Enter lunch: ').lower()
        if lunch_in in ['free/reduced', 'standard']:
            student_data['lunch'] = lunch_in
            break
        else:
            print("[ERROR] Invalid input for the lunch attribute, try again.\n")
    
    ## Test Preparation ##
    while True:
        test_prep_in = input('[SYSTEM] Enter test preparation course -> ').lower()
        if test_prep_in in ['none', 'completed']:
            student_data['test preparation course'] = test_prep_in
            break
        else:
            print("[ERROR] Invalid input for the test preparation course attribute, try again.\n")

    ## Exam Scores ##
    while True: # Math.
        try:
            math_score_in = int(input('[SYSTEM] Enter math score -> '))
            if 1 <= math_score_in <= 100:
                student_data['math score'] = math_score_in
                break
            else:
                print("[SYSTEM] Invalid input, math score must be an integer and between 1 to 100")
        except ValueError as e:
            print(f"[ERROR] An error came up. Log: {e}\n")

    while True: # Reading.
        try:
            reading_score_in = int(input('[SYSTEM] Enter reading score -> '))
            if 1 <= reading_score_in <= 100:
                student_data['reading score'] = reading_score_in
                break
            else:
                print("[ERROR] Invalid input, reading score must be an integer and between 1 to 100")
        except ValueError as e:
            print(f"[ERROR] An error came up. Log: {e}\n")

    while True: # Writing.
        try:
            writing_score_in = int(input('[SYSTEM] Enter writing score -> '))
            if 1 <= writing_score_in <= 100:
                student_data['writing score'] = writing_score_in
                break
            else:
                print("[ERROR] Invalid input, writing score must be an integer and between 1 to 100")            
        except ValueError as e:
            print(f"[ERROR] An error came up. Log: {e}\n")
            
    return student_data


## Find the closest Students to each new addded one ##
def close_students(new_data, data):
    ## Filter Students for the new data - make a copy of the original DataFrame ##
    same_cluster = data[data['cluster'] == new_data['cluster'].values[0]].copy()
    same_cluster_cp = same_cluster[['math score', 'reading score','writing score']].copy()
    
    ## Calculate the Distance between the recorded students ##
    original_scores = same_cluster_cp[['math score', 'reading score', 'writing score']]
    new_student_scores = new_data[['math score', 'reading score', 'writing score']]
    distances = ((original_scores - new_student_scores)**2).sum(axis=1)
    ## Save it - pandas accessor ##
    same_cluster_cp['distances'] = distances
    
    ## Sort and get the closest students related to the new one ##
    closest_students = same_cluster_cp.sort_values(by='distances').head(PRINT_STUDENTS)
    return closest_students


### Core ###
def main():
    ## Pass the .csv name and read it to a variable ##
    csv_file = 'StudentsPerformance.csv'
    student_data = read_dataset(csv_file)
    student_data = average(student_data)
    student_data = numeric_conversion(student_data)
    
    ## Clustering ##
    total_intervals = intervals()
    
    ## Call and create the intervals ##
    data_scaler = StandardScaler() # standardize the data.
    scaled_data = data_scaler.fit_transform()
    
    ## Use KMeans for the Clustering ##
    data_kmeans = KMeans(n_clusters=total_intervals, n_init=10)
    student_data['cluster'] = data_kmeans.fit_predict(scaled_data)
    
    ## Display Data Statistics ##
    plt.scatter(student_data['average score'], student_data['cluster'] + 1, c=student_data['cluster'], cmap='viridis') # x, y, color, variant of colors.
    plt.title('Clustering of Students')
    plt.xlabel("Student's average scores")
    plt.ylabel('Cluster')
    plt.show()

    ## Ask the user is they wish to input a New Student ##
    while True: 
        try:
            answer= input("\nDo you wish to add another student? yes/no -> ").strip().lower()
            if answer== 'yes':
                new_student = add_student()
                
                ## Redo the process ##
                new_student = pd.DataFrame([new_student]) # Dataframe.
                new_student_avg = average(new_student) # Average.
                new_student_final = numeric_conversion(new_student_avg) # Convert strings to Numbers.
                new_student_scaled = data_scaler.transform(new_student_final) # Standardize.
                new_student_final['cluster'] = data_kmeans.predict(new_student_scaled) # Clusterize.
                
                ## Results ##
                print(f"\n[SYSTEM] Cluster in which the Student belongs: {new_student_final['cluster'].values[0] + 1}")
                
                ## Closest Students ##
                closest_students = close_students(new_student_final, student_data)
                print(f"\n[SYSTEM] Here are the closest students: {closest_students}")
            elif answer== 'no':
                break
            else:
                print("[SYSTEM] answermust be either 'yes' or 'no'.")
        except ValueError as e:
            print(f"[ERROR] Invalid input. Log: {e}")


### Execute the program ###
if __name__ == '__main__':
    main()
