from flask_restful import Resource
from app.models.users import usersSchema,User
from flask_jwt_extended import jwt_required

class UserResource(Resource):
    @jwt_required()
    def get(self):
        all_users = User.query.all()
        return usersSchema.dump(all_users)
    

