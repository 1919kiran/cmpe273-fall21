from flask import Flask, request, jsonify

app = Flask(__name__)

users = dict()
index_add_counter = 100


# 1. POST /users (Create new user) - done
# 2. PATCH /users/{user_id}/followers/{follower_id} (Create new follower) - done
# 3. POST /users/{user_id}/tweets - done
# 4. GET /users/{user_id} - done
# 5. GET /users/{user_id}/timeline - done

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# {
#     "name": "John Smith",
#     "email": "john.smith@gmail.com"
# }
@app.route('/users', methods=['POST'])
def create_users():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    global index_add_counter
    index_add_counter = index_add_counter + 1
    users[index_add_counter] = {'id': index_add_counter, 'name': name, 'email': email, 'tweets': [], 'followers': []}

    return jsonify(users[index_add_counter])


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # print(users.get(int(user_id)))
    return jsonify(users.get(int(user_id)))


@app.route('/users/<user_id>/followers/<follower_id>', methods=['PATCH'])
def create_followers(user_id, follower_id):
    user_id = int(user_id)
    user = dict(users.get(user_id))
    if user['followers'] is None or len(user['followers']) == 0:
        user['followers'] = [str(follower_id)]
    else:
        user['followers'].append(str(follower_id))
        print(user['followers'])
    users[user_id] = user
    print(users)
    return jsonify(user)


# {
#     "tweet": "Fan art is the best"
# }
@app.route('/users/<user_id>/tweets', methods=['POST'])
def create_tweet(user_id):
    user_id = int(user_id)
    data = request.get_json()
    tweet = data.get('tweet')
    user = users.get(user_id)
    if user['tweets'] is None or len(user['tweets']) == 0:
        user['tweets'] = [tweet]
    else:
        user['tweets'].append(tweet)

    users[user_id] = user
    user_tweets = user['tweets']
    print(user_tweets)
    response = []
    for i in range(len(user_tweets)):
        tweet_dict = {"tweet_id": str(i+1), "tweet": user_tweets[i]}
        response.append(tweet_dict)

    return jsonify(response)


@app.route('/users/<user_id>/timeline', methods=['GET'])
def get_timeline(user_id):
    user_id = int(user_id)
    user = users.get(user_id)
    user_tweets = user['tweets']

    timeline = []
    for i in range(len(user_tweets)):
        timeline.append({"user_id": str(user_id), "tweet_id": str(i+1), "tweet":user_tweets[i]})

    response = {}
    response['timeline'] = timeline
    return response


if __name__ == '__main__':
    user_id_counter = 100
    app.run()
