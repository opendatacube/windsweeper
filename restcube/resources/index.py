# -*- coding: utf-8 -*-

from flask_restful import Api, reqparse, abort, Resource, request
from flask import current_app, jsonify
from flask_cognito import cognito_auth_required
from restcube.tasks.indexing import index_from_s3
from restcube.resources.tasks import Task
import os
import json

postargparser = reqparse.RequestParser()
postargparser.add_argument('pattern', type=str, required=True, help="S3 Pattern to search")
postargparser.add_argument('dc_product', type=str, required=False, help="DC Product to match against")

sqs_url = os.getenv("SQS_QUEUE_URL", "")

class Index(Resource):
    """
    The Index resource refers to a 'virtual' resource around indexing data into the datacube
    """
    @cognito_auth_required
    def post(self):
        """
        Creates a task to index data into the datacube
        """
        #args = postargparser.parse_args()
        #s3_pattern = args['pattern']
        #dc_product = args['dc_product']
        json_data = request.get_json(force=True)
        s3_pattern = json_data['s3_pattern']
        dc_product = json_data['dc_product']
        if s3_pattern is None:
            abort(400, message="no s3 pattern defined")
        index_task = index_from_s3.apply_async(args=[s3_pattern, dc_product])
        api = Api
        return jsonify({"task_id": index_task.id})
