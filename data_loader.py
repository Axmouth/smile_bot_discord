import json

outputfilename = "data.json"
userfilename = "user.json"


def load_user():
    try:
        savefile = open(userfilename)
        user = json.load(savefile)
    except:
        with open(userfilename, 'w') as userfile:
            json.dump("", userfile)
            return ""
    return user


def load_data():
    try:
        savefile = open(outputfilename)
        data = json.load(savefile)
    except:
        with open(outputfilename, 'w') as outfile:
            json.dump({}, outfile)
            return {}
    return data

def save_data(data):
    with open(outputfilename, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    load_data()