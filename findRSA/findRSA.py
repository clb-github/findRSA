from subprocess import call
import subprocess
import zipfile
import csv
import sys
import os
import re


W = '\033[0m'  # default
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


def findRSA():


    file = sys.argv[1]
    print(R+"\n=================="+W)
    cwd = os.path.dirname(os.path.realpath(__file__))
    print(P+"\nCurrent Directory: " + W + cwd)
    print(P+"Path to APK: " + W + file)

    try:
        with zipfile.ZipFile(file, 'r') as apk:
            directory = "META-INF"
            apk.extractall(directory)
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    if ".RSA" in name or ".DSA" in name:
                        print(P+"RSA Key located at: ", end=" "+W)
                        key = os.path.join(root, name)
                        print(O+key + "\n"+W)
                for name in dirs:
                    if ".RSA" in name or ".DSA" in name:
                        print(P+"RSA Key located at: ", end=" "+W)
                        key = os.path.join(root, name)
                        print(O+key + "\n"+W)

            cwd = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(cwd, key)
            res = subprocess.check_output(["keytool", "-printcert", "-file", path]).decode().split("\n")
            print(R+".: RSA Certificate :."+W)
            print(R+"---------------------"+W)
            call(["keytool", "-printcert", "-file", path])
            call(["rm", "-rf", directory])
            for i in range(0, len(res)):
                if "MD5" in res[i]:
                    extract = re.findall('[0-9:a-f:A-F]{47}', res[i])
                    md5 = " ".join(extract)
                    return md5
    except IOError:
        print("ERROR: No Valid APK Package Found.")


def plRSA(md5):

    try:
        with open(sys.argv[2], encoding='cp1252') as f:
            reader = csv.reader(f, delimiter=",")
            for line in reader:
                for i in range(0, len(line)):
                    if str(md5) in line[i]:
                        length = len("\n .: Matching hash found for :" + line[0] + ":.")
                        print(R+"\n.: Matching hash found for : " + O + line[0] + " :. "+W)
                        for j in range(0, length):
                            print(R+"-", end=""+W)
                        print("\n" + line[i] + "\n")
    except IOError:
        print("ERROR: Invalid CSV File")


def main():

    if __name__ == '__main__':
        if len(sys.argv) != 3:
            print("Usage: python3 findRSA.py <path/to/apk> <path/to/client_csv>")
            sys.exit()
        md5 = findRSA()
        plRSA(md5)
        print(R+"=================="+W)

main()

















