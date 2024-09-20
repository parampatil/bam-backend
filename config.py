class Config:
    SECRET_KEY = '91d40a4e6a1b4e9dbfbb60c04dc123457869ed1d576e3f4c8e6e68d3bcadcbf8'
    # DATABASE = 'bam.db'
    DATABASE = '/home/buildingamind/bam-backend/bam.db'
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')