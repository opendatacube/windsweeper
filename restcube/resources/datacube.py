# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask_cognito import cognito_auth_required
import datacube
import re

class Datacube(Resource):

    @cognito_auth_required
    def get(self):
        """Get the name of the database that the datacube is using and returns a dict"""
        with datacube.Datacube() as dc:
            connstr = str(dc)
            print(connstr)
            matches = re.search("postgresql.+/(.+)\\)>>>", connstr)
            return {"name": matches.group(1)}, 200
