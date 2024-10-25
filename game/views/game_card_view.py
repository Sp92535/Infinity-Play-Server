from . import get_bucket,base64,Game,Q,jsonify

class GameCardView:

    def __init__(self):
        self.__buck = get_bucket()
        self.__filters = {
            'new':'-releasedOn',
            'trending':'-avgRating',
            'popular':'-noOfVotes'
        }

    def __get_image_url(self,image_id):
        if not image_id:
            return ""
        with self.__buck.open_download_stream(image_id) as image_stream:
            image_buffer = image_stream.read()
        image_base64 =  base64.b64encode(image_buffer).decode('utf-8')
        return f'data:image/jpeg;base64,{image_base64}'

    def __get_images_with_name(self,games):
        games_with_images = []
        for game in games:
            image_url = self.__get_image_url(game.image)
            games_with_images.append({"name": game.gameName,"img": image_url})
        return games_with_images

    def __get_games(self, sort_by='-releasedOn', category=None):
        try:
            if category:
                games = Game.objects(Q(gameCategory__in=[category])).order_by(sort_by).limit(10).only('gameName', 'image')
            else:
                games = Game.objects.order_by(sort_by).limit(10).only('gameName', 'image')

            games_with_images = self.__get_images_with_name(games)

            return jsonify({"success": True, "games": games_with_images}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": 'Internal Server Error'}), 500

    def get_games_by_category(self,filter_type):
        if filter_type in self.__filters:
            return self.__get_games(sort_by=self.__filters[filter_type])
        return self.__get_games(category=filter_type)

    def __get_all_games(self, sort_by='-releasedOn', category=None, page_no=1):
        try:
            if category:
                games = Game.objects(Q(gameCategory__in=[category])).order_by(sort_by).only('gameName', 'image')
            else:
                games = Game.objects.order_by(sort_by).only('gameName', 'image')

            page_limit = 30
            offset = (page_no - 1) * page_limit
            total = games.count()
            games = games.skip(offset).limit(page_limit)

            games_with_images = self.__get_images_with_name(games)

            return jsonify({"success": True, "games": games_with_images, "total": total}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": 'Internal Server Error'}), 500

    def get_all_games_by_category(self,filter_type,page_no):
        if filter_type in self.__filters:
            return self.__get_all_games(sort_by = self.__filters[filter_type], page_no = page_no)
        return self.__get_all_games(category = filter_type, page_no = page_no)

    def get_games_by_query(self, query, page_no):
        try:
            page_limit = 20
            offset = (page_no - 1) * page_limit

            games = Game.objects(
                Q(gameName__icontains=query) | Q(gameKeywords__icontains=query)
            ).only('gameName', 'image')

            total = games.count()
            games = games.skip(offset).limit(page_limit)
            games_with_images = self.__get_images_with_name(games)

            return jsonify({"success": True, "games": games_with_images, "total": total}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "error": 'Internal Server Error'}), 500