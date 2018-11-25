import os



def sysSort(file):
    os.system("sort --output="+ file + " -u " + file)
    return


def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    sysSort("prices.txt")
    return

if __name__ == "__main__":
    main()
