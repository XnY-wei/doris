# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse
import cluster as CLUSTER
import command
import os.path
import sys
import traceback
import utils


def parse_args():
    ap = argparse.ArgumentParser(description="")
    args_parsers = ap.add_subparsers(dest="command")
    for cmd in command.ALL_COMMANDS:
        cmd.add_parser(args_parsers)

    return ap.parse_args(), ap.format_help()


def run(args, disable_log_stdout, help):
    for cmd in command.ALL_COMMANDS:
        if args.command == cmd.name:
            timer = utils.Timer()
            result = cmd.run(args)
            if cmd.print_use_time() and not disable_log_stdout:
                timer.show()
            return result
    print(help)
    return ""


if __name__ == '__main__':
    args, help = parse_args()
    verbose = getattr(args, "verbose", False)
    if verbose:
        utils.set_log_verbose()
    disable_log_stdout = getattr(args, "output_json", False)
    if disable_log_stdout:
        log_file_name = ""
        cluster_name = getattr(args, "NAME", "")
        if cluster_name:
            if type(cluster_name) == type([]):
                cluster_name = cluster_name[0]
            log_file_name = os.path.join(
                CLUSTER.get_cluster_path(cluster_name), "doris-compose.log")
        utils.set_log_to(log_file_name, False)

    code = None
    try:
        data = run(args, disable_log_stdout, help)
        if disable_log_stdout:
            print(utils.pretty_json({"code": 0, "data": data}), flush=True)
        code = 0
    except:
        err = traceback.format_exc()
        if disable_log_stdout:
            print(utils.pretty_json({"code": 1, "err": err}), flush=True)
        else:
            print(err, flush=True)
        code = 1
    sys.exit(code)
