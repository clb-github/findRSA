from subprocess import call
import subprocess
import sys
import zipfile
import os


def apkfindRSA():

    file = sys.argv[-1]

    print("\n==================")
    cwd = os.path.dirname(os.path.realpath(__file__))
    print("Current Directory: " + cwd)
    print("Filename(APK): " + file)
    with zipfile.ZipFile(file, 'r') as apk:
        directory = "META-INF"
        apk.extractall(directory)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if ".RSA" in name:
                    print("RSA Key located at: ",end = " ")
                    keydir = os.path.join(root.strip("."), name)
                    print(keydir + "\n")
            for name in dirs:
                if ".RSA" in name:
                    print("RSA Key located at: ", end = " ")
                    keydir = os.path.join(root.strip("."), name)
                    print(keydir + "\n")
        cwd = os.path.dirname(os.path.realpath(__file__))
        fulldir = cwd + keydir
        res = subprocess.check_output(["keytool", "-printcert", "-file", fulldir]).decode().split("\n")
        print(".: RSA Certificate :.")
        call(["keytool", "-printcert", "-file", fulldir])
        call(["rm", "-rf", directory])
        for item in res:
            if "MD5" in item:
                md5 = item[6:].strip()
        return md5


def main():
    if __name__ == '__main__':
        md5 = apkfindRSA()
        print("==================\n")


main()

















