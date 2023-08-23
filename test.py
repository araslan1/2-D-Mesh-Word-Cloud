def main():
    file = open("my.txt", "r")
    header = file.readlines()
    print(header)


main()