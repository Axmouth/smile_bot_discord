import json

outputfilename = "data.json"

def load_data():
    try:
        savefile = open('data.json')
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