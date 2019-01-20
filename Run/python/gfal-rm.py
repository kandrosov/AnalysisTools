#!/usr/bin/env python
# Transfer files using gfal tools.
# This file is part of https://github.com/hh-italian-group/AnalysisTools.

import argparse
import sys
import os
import re
import subprocess
import xml.etree.ElementTree

parser = argparse.ArgumentParser(description='Remove remote file or directory.',
                                 formatter_class = lambda prog: argparse.HelpFormatter(prog,width=90))
parser.add_argument('target', nargs=1, type=str,
                    help="target file or directory to remove (format SITE:path, e.g. T2_IT_Pisa:/store/user/foo/bar)")
args = parser.parse_args()

def GetPfnPath(lfn_to_pfn, path, protocol):
    for rule in lfn_to_pfn:
        if rule.get('protocol') != protocol: continue
        path_match = rule.get('path-match')
        if path_match is None or re.match(path_match, path) is None: continue
        result = rule.get('result')
        chained_protocol = rule.get('chain')
        if chained_protocol is not None:
            path = GetPfnPath(lfn_to_pfn, path, chained_protocol)
        fixed_path = re.sub(path_match, '\\1', path)
        return result.replace('$1', fixed_path)
    raise RuntimeError("Protocol {0} not found".format(protocol))

def GetSitePfnPath(site_name, path):
    desc_file = '/cvmfs/cms.cern.ch/SITECONF/{0}/PhEDEx/storage.xml'.format(site_name)
    if not os.path.isfile(desc_file):
        raise RuntimeError("Storage description for {0} not found.".format(site_name))
    storage_desc = xml.etree.ElementTree.parse(desc_file).getroot()
    lfn_to_pfn =storage_desc.findall('lfn-to-pfn')
    return GetPfnPath(lfn_to_pfn, path, 'srmv2')

def Delete(url, display_name):
    p = subprocess.Popen(['gfal-rm -r {0}'.format(url)], shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if len(err) != 0 or p.returncode != 0:
        raise RuntimeError('Unable to delete "{0}".\n{1}'.format(display_name, err))

class TargetDesc:
    def __init__(self, target_str):
        self.target_str = target_str
        split_target = target_str.split(':')
        if len(split_target) != 2:
            raise RuntimeError('Invalid target string {0}'.format(target_str))
        self.site_name = split_target[0]
        self.path = split_target[1]
        self.url = GetSitePfnPath(self.site_name, self.path)

target = TargetDesc(args.target[0])
Delete(target.url, target.target_str)
print('"{0}" successfully deleted.'.format(target.target_str))