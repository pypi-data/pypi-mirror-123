"""
    Title: stop_all
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 27-09-2021
    Date Modified: 27-09-2021
    Description:
        ###############################################################
        ##      Remove all repo details from centralized file        ## 
        ###############################################################
"""


import click
from click.decorators import command
from buildpan import find_path

@click.command()
def status():
    '''
     For restart CI-CD operation
    \f
    
   
    '''
    find_path.find_path()
    file_path = find_path.find_path.file_path

    try:
        with open(file_path + "/info.txt") as file:
            info = file.readlines()
            print("Buildpan process is running and following process are configured\n")
            for row in info:
                data = eval(row)
                project_id = data["project_id"]
                repo_name = data["repo_name"]
                path = data["path"]

                print("project_id = " + project_id + "\trepo_name = " + repo_name + "\tpath = " + path)
    
    except:
        print("No CI-CD operation is found.\nRun:- buildpan init to initiate CI-CD operation")