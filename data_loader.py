import json

outputfilename = "data.json"
userfilename = "userdata.json"


def load_user_data():
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
        json.dump(data, outfile, indent=4, sort_keys=True)


def save_user_data(userdata):
    with open(userfilename, 'w') as outfile:
        json.dump(userdata, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    load_user_data()
    load_data()