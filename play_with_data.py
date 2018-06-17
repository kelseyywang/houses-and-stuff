import sys, json, numpy as np

def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])
    
def main():
    #get our data as an array from read_in()
    lines = read_in()
    retval = ""
    for key in lines.keys():
        #TODO: change this test. currently only prints all address keys
        retval += key
    print(retval)
    # print(json.dumps(lines))

if __name__ == '__main__':
    main()