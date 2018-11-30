import os
import sys
import json
import easyvvuq.utils.json as json_utils
import tempfile
from string import Template
from easyvvuq.encoders import BaseEncoder

__copyright__ = """

    Copyright 2018 Robin A. Richardson, David W. Wright 

    This file is part of EasyVVUQ 

    EasyVVUQ is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EasyVVUQ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__license__ = "LGPL"

class GaussEncoder(BaseEncoder, encoder_name = "gauss"):

    def __init__(self, app_info, *args, **kwargs):

        # Handles creation of `self.app_info` attribute (dicts)
        super().__init__(app_info, *args, **kwargs)
        app_info = self.app_info

    def encode(self, params={}, target_dir=''):
        print("Using custom gauss encoder")
        out_file = params['out_file']
        num_steps = params['num_steps']
        mu = params['mu']
        sigma = params['sigma']
        output_str = '{"outfile": "' + out_file + '", "num_steps": "' + str(num_steps) + '", "mu": "' + str(mu) + '", "sigma": "' + str(sigma) + '"}\n'

        encoder_outfname = os.path.join(target_dir, "gauss_input.json")
        with open(encoder_outfname, "w") as outfile:
            outfile.write(output_str)

        runscript_fname = os.path.join(target_dir, "run_cmd.sh")
        run_cmd = 'tests/gauss/gauss_json.py gauss_input.json\n'
        local_run_cmd = os.path.realpath(os.path.expanduser(run_cmd))
        with open(runscript_fname, "w") as outfile:
            outfile.write(local_run_cmd)

