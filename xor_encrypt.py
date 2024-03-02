from itertools import cycle
import argparse

class XorCrypt:
    def __init__(self):
        self.data = None
        self.key = None
        self.binary = None
    def fileReader(self, fPath):
        try:
            readMode = "rb" if self.binary else "r"
            with open(fPath, readMode) as file:
                self.data = file.read()
        except Exception as e:
            print(f"[!] Unable to read contents from file : {fPath}")
            print(e)
            exit(1)
    def fileWriter(self, oPath, content):
        try:
            with open(oPath, "wb") as file:
                file.write(content)
                print("Output saved")
        except Exception as e:
            print(e)
            exit(1)
    def encrypt(self, oPath):
        try:
            if self.binary:
                encryptedMessage = bytes([c^k for c, k in zip(self.data, cycle(self.key.encode()))])
                self.fileWriter(oPath, encryptedMessage)
            else:
                encryptedMessage = "".join([chr(ord(c)^ord(k)) for c, k in zip(self.data, cycle(self.key))])
                encryptedMessage = encryptedMessage.encode().hex()
                return encryptedMessage
        except Exception as e:
            print(e)
            exit(1)
    def decrypt(self, oPath):
        try:
            if self.binary:
                decryptedMessage = bytes([c^k for c, k in zip(self.data, cycle(self.key.encode()))])
                self.fileWriter(oPath, decryptedMessage)
            else:
                unicodeFromHex = bytes.fromhex(self.data).decode("utf-8")
                decryptedMessage = "".join([chr(ord(c)^ord(k)) for c, k in zip(unicodeFromHex, cycle(self.key))])
                return decryptedMessage
        except Exception as e:
            print(e)
            exit(1)
            
            
if __name__ == "__main__":            
    crypt = XorCrypt()
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt Using XOR bitwise operation")
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the supplied message or the file")
    parser.add_argument("-b", "--binary", action="store_true", help="If you want to encrypt or decrypt any files other than text then use binary mode")
    parser.add_argument("-o", "--output", type=str, help= "To store output, need to only use with -b flag as will encrypt or decrypt other binary files which would not be in text format")
    parser.add_argument("-k", "--key", type=str, required=True, help="Key to encrypt or decrypt")
    group.add_argument("-m", "--message", type=str, help="The message to encrypt or decrypt using xor")
    group.add_argument("-f", "--file", type=str, help="File to encrypt or decrypt")
    args = parser.parse_args()
    crypt.key = args.key
    
    if args.binary:
        if not args.output:
            parser.error("When used -b flag need to use -o flag to save output of binary data in a file")
        else:
            if not args.file:
                parser.error("When used -b flag need to use -f flag to use a file as source of data to encrypt or decrypt")
            else:
                crypt.binary = True

    outputFile = args.output if args.output else None
            
    if args.message:
        crypt.data = args.message
    else:
        crypt.fileReader(args.file)
    if args.encrypt:
        outputData = crypt.encrypt(outputFile)
    else:
        outputData = crypt.decrypt(outputFile)
    
    if outputData:
        print(outputData)