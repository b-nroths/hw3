#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib
from alignment import Alignment
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'



aclass = Alignment()

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        sequence_1 = self.request.get('sequence_1')
        sequence_2 = self.request.get('sequence_2')
        match = self.request.get('match')
        mismatch = self.request.get('mismatch')
        gap = self.request.get('gap')
        alignment = self.request.get('alignment')
        
        print sequence_1, sequence_2, match, mismatch, gap, alignment

        if 'global' in alignment.lower():
            alignment_type = 'global'
        else:
            alignment_type = 'local'

        a = ''
        b = ''
        error = ''
        # try:
        grid, trace, final_alignment, score = aclass.alignment(sequence_1, 
            sequence_2, 
            alignment_type, 
            int(match), 
            int(mismatch), 
            int(gap))
        grid = grid.tolist()
        trace = trace#.tolist()
        print trace
        a = ""
        for row in grid:
            a+="\t".join([str(int(x)) for x in row])
            a+="\n"
        b = ""
        for row in trace:
            for col in row:
                if 'up' in str(col):
                    b += "^"
                if 'left' in str(col):
                    b += "<"
                if 'diag' in str(col):
                    b += "\\"
                b+="\t"
            b+="\n"
        # except Exception as e:
        #     error = str(e)
        #     print str(e)
        #     pass

        print b
        

        template_values = {
            'sequence_1': sequence_1,
            'sequence_2': sequence_2,
            'match': match,
            'mismatch': mismatch,
            'gap': gap,
            'alignment': alignment_type,
            'grid': a,
            'trace': b,
            'error': error,
            'alignment': "\n".join(final_alignment),
            'score': score
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]



# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
# [END app]
