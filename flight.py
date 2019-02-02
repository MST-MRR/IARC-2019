from flask import Blueprint, Flask

app = Flask(__name__)

commands = Blueprint('commands', __name__, url_prefix='/commands')


@commands.route('/', methods=["GET"])
def list_current_commands():
    return "current", 200


@commands.route('/', methods=["POST"])
def push_command():
    if args.debug:
        # get push data and activate
        return "success", 200
    elif args.routine:
        # get push data and check if start or kill
        # if command == "start":
        #     start routine
        # elif command == "kill":
        #     force into land
        return "routine " + args.routine + " in progress", 200


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=
        'MRRDT flight command line interface. Used to fly the drone.')
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('routine', nargs="?", default="stall", type=str)

    args = parser.parse_args()

    # if args.debug:
    #     debug(args)
    # elif args.routine:
    #     production(args)
    # else:
    #     print("Please try again with routine")
    #     quit()

    app.register_blueprint(commands)

    app.run("127.0.0.1", 8000)
