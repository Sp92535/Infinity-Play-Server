from datetime import timedelta

from . import get_jwt_identity,os,jsonify,Admin,Q,DoesNotExist,create_access_token,bcrypt,Unauthorized,ValidationError

class AdminView:

    @staticmethod
    def create_user(request):
        try:
            if get_jwt_identity() != os.getenv('SUPER_USERNAME') + "NEGRO":
                raise Unauthorized("Authorization failed")

            req_data = request.get_json()
            username = req_data.get('username')
            password = req_data.get('password')

            if username==os.getenv('SUPER_USERNAME'):
                raise ValidationError("Username already exists")

            admin = Admin(username=username)
            admin.password = password   # setter for private field
            admin.save()  # Save the new admin to the database

            return jsonify({"success": True, "message": "Created Admin."}), 201

        except Unauthorized as u:
            print(u)
            return jsonify({"success": False,"error": str(u)}), 401

        except ValidationError as v:
            print(v)
            return jsonify({"success": False, "error": str(v)}), 400

        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Internal Server Error"}), 500


    @staticmethod
    def find_admin(username):
        try:
            if get_jwt_identity() != os.getenv('SUPER_USERNAME') + "NEGRO":
                raise Unauthorized("Authorization failed")

            admins = Admin.objects(Q(username__icontains=username))
            admin_usernames = [_.username for _ in admins]

            return jsonify({"success": True, "admins": admin_usernames}), 200

        except Unauthorized as u:
            print(u)
            return jsonify({"success": False, "error": str(u)}), 401

        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Internal Server Error"}), 500


    @staticmethod
    def delete_admin(username):
        try:
            if get_jwt_identity() != os.getenv('SUPER_USERNAME') + "NEGRO":
                raise Unauthorized("Authorization failed")

            admin = Admin.objects(username=username).first()

            if not admin:
                raise DoesNotExist("Admin not found")

            admin.delete()
            return jsonify({"success": True, "message": "Admin deleted successfully."}), 200

        except Unauthorized as u:
            print(u)
            return jsonify({"success": False, "error": str(u)}), 401

        except DoesNotExist as d:
            print(d)
            return jsonify({"success": False, "error": str(d)}), 404

        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Internal Server Error"}), 500

    @staticmethod
    def __get_jwt_expiration():
        exp = os.getenv('JWT_EXPIRATION')
        num = int(exp[:-1])
        unit = exp[-1]

        if unit=='m':
            return timedelta(minutes=num)
        elif unit == 'h':
            return timedelta(hours=num)
        elif unit == 's':
            return timedelta(seconds=num)
        elif unit == 'd':
            return timedelta(days=num)
        else:
            raise ValueError("Invalid time unit. Use 'm' for minutes, 'h' for hours, or 's' for seconds.")

    def login(self,request):
        try:
            req_data = request.get_json()
            username = req_data.get('username')
            password = req_data.get('password')

            if username==os.getenv('SUPER_USERNAME') and password==os.getenv('SUPER_PASSWORD'):
                access_token = create_access_token(identity=username+"NEGRO",expires_delta=self.__get_jwt_expiration())
                return jsonify({"success": True, "access_token": access_token, "super_access":True}), 200

            admin = Admin.objects(username=username).first()

            if not admin:
                raise DoesNotExist("Admin not found")

            if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
                raise Unauthorized("Wrong Username or Password")

            access_token = create_access_token(identity=username,expires_delta=self.__get_jwt_expiration())

            return jsonify({"success": True, "access_token": access_token}), 200

        except Unauthorized as u:
            print(u)
            return jsonify({"success": False, "error": str(u)}), 401

        except DoesNotExist as d:
            print(d)
            return jsonify({"success": False, "error": str(d)}), 404

        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Internal Server Error"}), 500