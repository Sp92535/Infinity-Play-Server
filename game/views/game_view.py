from . import get_bucket,Game,jsonify,DoesNotExist,ObjectId,Response,hashlib,secure_filename,requests,os,get_jwt_identity,Unauthorized,ValidationError

class GameView:

    def __init__(self):
        self.__buck = get_bucket()

    @staticmethod
    def get_game_by_name(game_name):
        try:
            game = Game.objects(gameName=game_name).first()

            if not game:
                raise DoesNotExist("Game Not Found")

            return jsonify({"success": True, "data": game.to_dict()}), 200

        except DoesNotExist as d:
            print(d)
            return jsonify({"success": False, "error": str(d)}), 404

        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": 'Internal Server Error'}), 500


    def get_game_file_by_id(self,file_id):
        try:
            file_id = ObjectId(file_id)
            download_stream = self.__buck.open_download_stream(file_id)

            # Create a generator to yield data from the download stream
            def generate():
                try:
                    while True:
                        chunk = download_stream.read(4096)  # Read in chunks
                        if not chunk:
                            break
                        yield chunk
                finally:
                    download_stream.close()  # Ensure the stream is closed after usage
            return Response(generate(),content_type='application/octet-stream')

        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": 'Internal Server Error.'}), 500


    def upload_game(self,request):
        game_file = request.files.get('gameFile')
        image_file = request.files.get('image')

        if not game_file or not image_file:
            return jsonify({"success": False, "error": "Game File or Image is missing."}), 400

        game_buffer = game_file.read()
        image_buffer = image_file.read()

        game_hash = hashlib.sha256(game_buffer).hexdigest()
        existing_game = Game.objects(fileHash=game_hash)

        if existing_game:
            return jsonify({"success": False, "error": "Duplicate game file upload detected"}), 409

        image_file_name = secure_filename(image_file.filename)
        image_upload_stream = self.__buck.open_upload_stream(image_file_name)

        try:
            image_upload_stream.write(image_buffer)
            image_upload_stream.close()
        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": "Image upload failed"}), 500

        game_filename = secure_filename(game_file.filename)  # Safe filename

        game_type = 'html5'
        if game_filename.endswith('.swf'):
            game_type = 'flash'

        game_upload_stream = self.__buck.open_upload_stream(game_filename)

        try:
            game_upload_stream.write(game_buffer)
            game_upload_stream.close()
        except Exception as e:
            self.__buck.delete(image_upload_stream._id)
            print(str(e))
            return jsonify({"success": False, "error": "Game file upload failed"}), 500

        released_by = get_jwt_identity()
        game = Game(
            gameName=request.form.get('gameName'),
            gameDescription=request.form.get('gameDescription'),
            gameCategory=request.form.getlist('gameCategory'),
            gameKeywords=request.form.getlist('gameKeywords'),
            fileHash=game_hash,
            releasedBy=released_by,
            gamePath=game_upload_stream._id,
            gameType=game_type,
            image=image_upload_stream._id
        )
        game.gameKeywords.append(released_by)

        try:
            game.save()
        except ValidationError as v:
            print(v)
            return jsonify({"success": False, "error": str(v)}), 400
        except Exception as e:
            self.__buck.delete(image_upload_stream._id)
            self.__buck.delete(game_upload_stream._id)
            print(str(e))
            return jsonify({"success": False, "error": "Game save failed"}), 500

        return jsonify({"success": True, "message": "Game uploaded successfully", "gameId": str(game.id)}), 201


    @staticmethod
    def vote_game(game_name,like):
        try:
            game = Game.objects(gameName=game_name).first()
            game.noOfVotes += 1
            game.noOfLikes += 1 if like==1 else 0
            game.save()
            return jsonify({"success": True,"message": "Voted..","noOfVotes": game.noOfVotes}),200

        except Exception as e:
            print(e)
            return jsonify({"success":False,"message":"Internal Server Error"}),500


    def delete_game_by_name(self,game_name):
        try:
            if get_jwt_identity() != os.getenv('SUPER_USERNAME') + "NEGRO":
                raise Unauthorized("Authorization failed")

            game = Game.objects(gameName=game_name).first()

            if not game:
                raise DoesNotExist("Game not found")

            image_path = game.image
            file_path = game.gamePath

            self.__buck.delete(image_path)
            self.__buck.delete(file_path)
            game.delete()

            return jsonify({"success": True,"message": f"Game '{game_name}' deleted successfully."}), 200

        except Unauthorized as u:
            print(u)
            return jsonify({"success": False,"error": str(u)}), 401

        except DoesNotExist as d:
            print(d)
            return jsonify({"success": False, "error": str(d)}), 404

        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Internal Server Error"}), 500


    @staticmethod
    def submit_report(request):
        try:
            # Get the report data from the request body
            report_data = request.get_json()
            game_name = report_data.get('game_name')
            message = report_data.get('message')

            # Prepare the payload for Web3Forms
            web3forms_data = {
                'access_key': os.getenv('MAIL_API_KEY'),  # Replace with your actual access key
                'subject': f'Report for {game_name}',
                'email': 'infinityplay@gmail.com',
                'message': message
            }

            # Send the POST request to Web3Forms
            response = requests.post('https://api.web3forms.com/submit', data=web3forms_data)

            # Check if the request was successful
            if response.status_code == 200:
                return jsonify({"success":True,"message": "Report sent successfully!"}), 200
            else:
                return jsonify({"success":False,"error": "Failed to send report."}), 500

        except Exception as e:
            return jsonify({"success":False, "error": str(e)}), 500
