from datetime import datetime

from flask import Flask
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
API_URI = "http://localhost:5000/"
GITHUB_API_URI = "https://api.github.com/"


class RequestLogModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requests_body = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"RequestLog(requests_body = {requests_body}, timestamp = {timestamp}, status_code={status_code})"


# db.create_all()

# Logging
def logging(request_uri, status_code):
    req_log = RequestLogModel(requests_body=request_uri, timestamp=datetime.now(), status_code=status_code)
    db.session.add(req_log)
    db.session.commit()


# 1.	Get repo details.
class Repo(Resource):
    def get(self, repo_owner, repo_name):
        request_uri = GITHUB_API_URI + 'repos/' + repo_owner + '/' + repo_name
        response = requests.get(request_uri)
        # Logging
        logging(request_uri, response.status_code)
        # If status isn't equal 200, then stop
        if response.status_code != 200:
            abort(response.status_code, message="Status: " + str(response.status_code) + " " + response.reason)
        # Otherwise, display repo information
        return response.json()


# 2.	Get a list of all pull requests.
class Pulls(Resource):
    def get(self, repo_owner, repo_name):
        request_uri = GITHUB_API_URI + 'repos/' + repo_owner + '/' + repo_name + '/pulls'
        response = requests.get(request_uri)
        # Logging
        logging(request_uri, response.status_code)
        # If status isn't equal 200, then stop
        if response.status_code != 200:
            abort(response.status_code, message="Status: " + str(response.status_code) + " " + response.reason)
        # Otherwise, display repo information
        return response.json()


# 3.	Get a list of all pull requests which have not been merged for two weeks or more.
class OldPulls(Resource):
    def get(self, repo_owner, repo_name):
        # Get a list of all pull requests from this Repo
        data = Pulls.get(self, repo_owner, repo_name)
        # Search for an unmerged pull-requests with creation date more the 2 weeks ago
        old_pulls = []
        for i in range(len(data)):
            created = data[i]['created_at']
            created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
            diff = (datetime.now() - created)
            # if difference between now and creation date is more than 14 days then pass
            if diff.days >= 14 and not data[i]['merged_at']:
                old_pulls.append(data[i])
        print(len(old_pulls))
        return old_pulls


# 4.	Get a list of all issues.
class Issues(Resource):
    def get(self, repo_owner, repo_name):
        request_uri = GITHUB_API_URI + 'repos/' + repo_owner + '/' + repo_name + '/issues'
        response = requests.get(request_uri)
        # Logging
        logging(request_uri, response.status_code)
        # If status isn't equal 200, then stop
        if response.status_code != 200:
            abort(response.status_code, message="Status: " + str(response.status_code) + " " + response.reason)
        # Otherwise, display repo information
        return response.json()


#     5.	Get a list of all forks.
class Forks(Resource):
    def get(self, repo_owner, repo_name):
        request_uri = GITHUB_API_URI + 'repos/' + repo_owner + '/' + repo_name + '/forks'
        response = requests.get(request_uri)
        # Logging
        logging(request_uri, response.status_code)
        # If status isn't equal 200, then stop
        if response.status_code != 200:
            abort(response.status_code, message="Status: " + str(response.status_code) + " " + response.reason)
        # Otherwise, display repo information
        return response.json()


api.add_resource(Repo, "/<string:repo_owner>/<string:repo_name>")
api.add_resource(Pulls, "/<string:repo_owner>/<string:repo_name>/pulls")
api.add_resource(OldPulls, "/<string:repo_owner>/<string:repo_name>/oldpulls")
api.add_resource(Issues, "/<string:repo_owner>/<string:repo_name>/issues")
api.add_resource(Forks, "/<string:repo_owner>/<string:repo_name>/forks")

if __name__ == "__main__":
    app.run(debug=True)
