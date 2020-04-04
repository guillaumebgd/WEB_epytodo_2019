from app import app

@app.route('/', methods =['GET'])
@app.route('/register', methods=['POST'])
@app.route('/signip', methods=['POST'])
@app.route('/signout', methods=['POST'])
@app.route('/user', methods=['GET'])
@app.route('/user/task', methods=['GET'])
@app.route('/user/task/id', methods=['GET'])
@app.route('/user/task/id', methods=['POST'])
@app.route('/user/task/add', methods=['POST'])
@app.route('/user/task/del/id', methods=['POST'])


@app.route('/index', methods=['GET'])

def route_home() :
    return "Hello world !\n"


@app.route('/user/<username>', methods=['POST'])

def route_add_user(username) :
    return "User added !\n"