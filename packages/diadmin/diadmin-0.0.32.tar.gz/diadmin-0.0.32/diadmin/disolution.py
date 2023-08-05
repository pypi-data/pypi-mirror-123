#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
import re
import json

import yaml

from diadmin.vctl_cmds.login import di_login
from diadmin.vctl_cmds.solution import list_solutions, download_solution, upload_solution, import_solution, import_solution_sameuser, import_solution_repo
from diadmin.vctl_cmds.vrep import import_artifact
from datetime import datetime



def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    description =  "Wrapper around <vctl solution>"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c','--config', help = 'Specifies yaml-config file')
    parser.add_argument('-l', '--list', help='Lists solutions',action='store_true')
    parser.add_argument('-d', '--download', help='Downloads solution',action='store_true')
    parser.add_argument('-i', '--importing', help='Import/upload solution',action='store_true')
    parser.add_argument('-u', '--user', help='Filter on user created solutions')
    parser.add_argument('-n', '--name', help='Name of solutions')
    parser.add_argument('-v', '--version', help='Version of solutions')
    parser.add_argument('-f', '--fromdate', help='Date onward filter (YYYY-MM-DD)')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = args.config
        if not re.search('.+\.yaml',config_file) :
            logging.info('Automatically adding extension \'.yaml\'')
            config_file = config_file + '.yaml'
    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    ret = 0
    ret = di_login(params)
    if not ret == 0 :
        return ret

    if args.list :
        from_date =  datetime.strptime(args.date,'%Y-%m-%d') if args.fromdate else None
        user = args.user if args.user else None
        solutions = list_solutions(user=user,from_date = from_date)
        print(json.dumps(solutions,indent=4))

    if args.download :
        if not args.name:
            print('Name of solution required with option \'-n\'')
            return -1
        if not args.version:
            print('Version of solution required with option \'-v\'')
            return -1
        download_solution(args.name,args.version)

    if args.importing:
        if not args.name:
            print('Name of solution required with option \'-n\'')
            return -1
        user = params['USER']
        if  args.user :
            user = args.user
        #import_solution(args.name,user)

if __name__ == '__main__':
    main()