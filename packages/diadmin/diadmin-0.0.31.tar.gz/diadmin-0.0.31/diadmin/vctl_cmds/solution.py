import logging
from datetime import datetime
import json
import re
from os import path
from subprocess import check_output, run, CalledProcessError

VFLOW_PATHS = {'operators':'/files/vflow/subengines/com/sap/python36/operators/',
               'pipelines':'/files/vflow/graphs/',
               'dockerfiles':'/files/vflow/dockerfiles/'}

def list_solutions(user = False,from_date = None ) :
    logging.info('List solutions')
    solutions = json.loads(check_output(['vctl','solution','list','-o','json']).decode('utf-8'))
    # Filter
    if user :
        solutions = [s for s in solutions if re.match(f".+/{user}",s['CreatedBy'])]
    if from_date :
        solutions = [s for s in solutions if  datetime.strptime(s['CreatedAt'][:26],'%Y-%m-%dT%H:%M:%S.%f') > from_date ]
    return solutions

def download_solution(solution_name,version) :
    file = path.join('solutions',solution_name + '_' + version + '.zip')
    logging.info(f'Download solution: {solution_name} to {file}')
    run(['vctl','solution','download',solution_name,version,'-f',file])

def upload_solution(solution_file,user) :
    logging.info(f'Upload solution: {solution_file} to user: {user}')
    run(['vctl','solution','upload',solution_file,'-u',user])


def import_solution_from_repo(solution_name,version) :
    destination = '/files'
    run(['vctl','vrep','user','import-solution',solution_name,version,destination,])

def export_solution_to_repo(source,solution_name,version) :
    cmd = ['vctl','vrep','user','export-solution',solution_name,version,source]
    logging.info(f'Export vrep  \'{source}\'  to solution: {solution_name}-{version} ( ({" ".join(cmd)}))')
    run(cmd)