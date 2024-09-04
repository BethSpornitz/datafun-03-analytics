'''  ITERATION 5

Module: Synapse Analytics - Reusable Module for My Data Analytics Projects

This module provides a simple, reusable foundation for my analytics projects. 

Process:

In this iteration, I enhance the byline to include calculated statistics. 
This makes the byline more informative and professional, 
ready for use in future projects.
 '''
 
#####################################
# Import Modules at the Top
#####################################

import statistics

 #####################################
# Declare global variables
#####################################

has_international_clients: bool = True
years_in_operation: int = 10
skills_offered: list = ["Data Analysis", "Machine Learning", "Business Intelligence"]
client_satisfaction_scores: list = [4.8, 4.6, 4.9, 5.0, 4.7]
has_spanish_speaking_analysts = True
has_female_analysts = True
number_employees: int = 150
locations:  list = ['Tampa', 'Kansas City', 'New York']
years_of_experience: list = [30, 28, 22, 18, 15]
average_client_satisfaction: float = 4.7
average_years_experience: float = 22.6

#####################################
# Calculate Basic Statistics 
#####################################

# Calculate basic stats using built-in functions min(), max() and statistics module functions mean() and stdev().
min_score: float = min(client_satisfaction_scores)  
max_score: float = max(client_satisfaction_scores)  
mean_score: float = statistics.mean(client_satisfaction_scores)  
stdev_score: float = statistics.stdev(client_satisfaction_scores)

years_of_experience_min_score: float = min(years_of_experience)  
years_of_experience_max_score: float = max(years_of_experience)  
years_of_experience_mean_score: float = statistics.mean(years_of_experience)  
years_of_experience_stdev_score: float = statistics.stdev(years_of_experience)

#####################################
# Declare a global variable named byline. 
# Make it a multiline f-string to show our information.
#####################################

byline: str = f"""
---------------------------------------------------------
Synapse Analytics: Deeper Insights. Clearer Decisions.
---------------------------------------------------------
Has International Clients:  {has_international_clients}
Years in Operation:         {years_in_operation}
Skills Offered:             {skills_offered}
Client Satisfaction Scores: {client_satisfaction_scores}
Minimum Satisfaction Score: {min_score}
Maximum Satisfaction Score: {max_score}
Mean Satisfaction Score:    {mean_score:.2f}
Standard Deviation:         {stdev_score:.2f}
Has Spanish Speaking Analysts:    {has_spanish_speaking_analysts}
Has Female Analysts:    {has_female_analysts}
Number of Employees:    {number_employees}
Locations Served:    {locations}
Years of Experience of our top five analysts:    {years_of_experience}
Mimimum Years of Experience of our top five analysts:    {years_of_experience_min_score}
Maximum Years of Experience of our top five analysts:    {years_of_experience_max_score}
Average Number of Years Experience of our top five analysts:    {years_of_experience_mean_score}    
Standard Deviation Years of Experience of our top five analysts:    {years_of_experience_stdev_score:.2f}  
"""

#####################################
# Define the get_byline() Function
#####################################

def get_byline() -> str:
    '''Return a byline for my analytics projects.'''
    return byline
    
#####################################
# Define a main() function for this module.
#####################################

def main() -> None:
    '''Print results of get_byline() when main() is called.'''
    print(get_byline())

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()
