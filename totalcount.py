from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt  # to display our wordcloud
from PIL import Image  # to load our image
import numpy as np  # to get the color of our image


cancer_names = []
cancer_list = []


class Cancer:
    def __init__(self, x, y, count, name):
        self.x = int(x)
        self.y = int(y)
        self.count = int(count)
        self.name = name




def parse_file(file_name):
    file = open(file_name, 'r')
    file.readline()
    for line in file:
        cancer_name = ""
        start_reading_cancer_name = False
        x = 0
        y = 0
        x_found = False
        for char in line:
            if char.isdigit() and x_found:
                y = int(char)
            elif char.isdigit():
                x = int(char)
            elif char == '\t':
                start_reading_cancer_name = True
            elif char == "\n":
                pass
            elif start_reading_cancer_name:
                cancer_name += char
        # you will need to tweak this later to check if the clusters aren't in the list as well
        if cancer_name not in cancer_names:
            cancer_names.append(cancer_name)
            cancer_list.append(Cancer(x, y, 1, cancer_name))
        else:
            for item in cancer_list:
                if item.name == cancer_name:
                    item.count += 1


def create_cancer_file(mylist):
    count_file = open("total_count", "w")
    total = 0
    for item in mylist:
        total += item.count
        count_file.write(str(item.name) + " " + str(item.count) + "\n")
    count_file.write("Total " + str(total) + "\n")
    count_file.close()





def main():
    parse_file("cancertypes.txt")
    create_cancer_file(cancer_list)

    # generate_word_cloud(my_string)


main()
