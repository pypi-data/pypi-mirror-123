#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

from os import path,makedirs,getcwd, walk
import logging
import argparse
import tarfile
import re

import yaml

from diadmin.vctl_cmds.login import di_login
from diadmin.vctl_cmds.vrep import import_artifact
from diadmin.vctl_cmds.solution import export_solution_to_repo

VFLOW_PATHS = {'operators':'/files/vflow/subengines/com/sap/python36/operators/',
               'pipelines':'/files/vflow/graphs/',
               'dockerfiles':'/files/vflow/dockerfiles/'}


def make_tarfile(source_dir) :
    tar_filename = path.join(path.dirname(source_dir),path.basename(source_dir) + '.tgz')
    with tarfile.open(tar_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=path.basename(source_dir))
    return tar_filename

def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    achoices = ['operators','pipelines','dockerfiles','bundle']
    description =  "Uploads operators, pipelines, dockerfiles and bundle to SAP Data Intelligence.\nPre-requiste: vctl."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c','--config', help = 'Specifies yaml-config file',default='config_demo.yaml')
    parser.add_argument('-r','--conflict', help = 'Conflict handling flag of \'vctl vrep import\'')
    parser.add_argument('artifact_type', help='Type of artifacts',choices=achoices)
    parser.add_argument('artifact', help='Artifact file(tgz) or directory')
    parser.add_argument('-s', '--solution', help='Solution name if upload should be exported to repository')
    parser.add_argument('-v', '--version', help='Version of solution. Necessary if exported to repository',default='0.0.1')
    parser.add_argument('-u', '--user', help='SAP Data Intelligence user (not for \'solutions\')')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = args.config
    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    ret = 0
    ret = di_login(params)
    if not ret == 0 :
        return ret

    user = params['USER']
    if  args.user :
        user = args.user

    conflict = None
    if args.conflict :
        conflict = args.conflict

    if (re.match('.+\.tgz$',args.artifact) or re.match('.+\.tar.gz$',args.artifact)):
        import_artifact(args.artifact_type,args.artifact,user,conflict)
    else :
        tf = make_tarfile(args.artifact)
        import_artifact(args.artifact_type,tf,user,conflict)

    if args.solution:

        if re.match('.+\.tgz$',args.artifact):
            basename =  re.match('(.+)\.tgz$',args.artifact).group(0)
        elif re.match('.+\.tar.gz$',args.artifact) :
            basename = re.match('(.+)\.tar.gz$',args.artifact).group(0)
        else :
            basename = args.artifact
        basename = path.basename(basename)
        source = path.join(VFLOW_PATHS[args.artifact_type],basename)
        export_solution_to_repo(source,args.solution,args.version)

if __name__ == '__main__':
    main()