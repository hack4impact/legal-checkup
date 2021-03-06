from .. import db

class ApiParameterLink(db.Model):
    __tablename__ = 'api_parameter_link'
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'), primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), primary_key=True)
    parameter_description = db.Column(db.String(128))
    api = db.relationship('Api', backref='parameter_associations')
    parameter = db.relationship('Parameter', backref='api_associations')

    def __init__(self, api, param, description):
        self.api = api
        self.parameter = param
        self.parameter_description = description
        param.incr_count

    def __repr__(self):
        return '<ApiParameterLink \'%s %s %s\'>' % (self.api.name, self.parameter.name,
            self.parameter_description)

class Api(db.Model):
    __tablename__ = 'apis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(128), unique=True)
    region = db.Column(db.String(64))
    description = db.Column(db.String(128))
    parameters = db.relationship('Parameter', secondary='api_parameter_link')

    def add_param(self, param, description):
        self.parameter_associations.append(ApiParameterLink(api=self,
            param=param, description=description))

    def get_params(self):
        param_links = ApiParameterLink.query.filter_by(api_id=self.id).all()
        params = []
        for link in param_links:
            params.append(link.parameter)
        return params

    def __init__(self, name, url, region, description):
        self.name = name
        self.url = url
        self.region = region
        self.description = description

    def __repr__(self):
        return '<Api \'%s %s %s %s\'>' % (self.name, self.url, self.region, self.description)

class Parameter(db.Model):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    param_format = db.Column(db.String(64))
    count = db.Column(db.Integer)
    apis = db.relationship('Api', secondary='api_parameter_link')

    def get_apis(self):
        return ApiParameterLink.query.filter_by(parameter_id=self.id).all()

    def incr_count(self):
        self.count += 1

    def __init__(self, name, param_format, count):
        self.name = name
        self.param_format = param_format
        self.count = count

    def __repr__(self):
        return '<Parameter \'%s %s %s\'>' % (self.name, self.param_format,
            self.count)
