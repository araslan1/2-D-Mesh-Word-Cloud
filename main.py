from wordcloud import WordCloud  # ,ImageColorGenerator
import matplotlib.pyplot as plt  # to display our wordcloud
import matplotlib.gridspec as gridspec
# from PIL import Image  # to load our image
import numpy as np  # to get the color of our image


clusters = {}


class Cluster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cancer_names = []
        self.cancer_list = []
        self.size = 0
        self.frequencies = {}


class Cancer:
    def __init__(self, x, y, count, name):
        self.x = int(x)
        self.y = int(y)
        self.count = int(count)
        self.name = name

    def add_one_to_count(self):
        self.count += 1


def create_sample_number_dict(file_name):
    sample_counts = {}
    file = open(file_name, "r")
    for line in file:
        word_found = False
        cancer_name = ""
        total_sample_size = 0
        for word in line.split():
            if not word_found:
                cancer_name = word
                word_found = True
            else:
                total_sample_size = int(word)
        sample_counts[cancer_name] = total_sample_size
    return sample_counts


def read_header(file_name):
    file = open(file_name, 'r')
    file.readline()
    return file


def parse_cluster(file, dictionary_of_sample_counts):
    x_changed = False  # flag for if you enter a new cluster
    y_changed = False  # flag for if you enter a new cluster
    x = -100
    y = -100
    i = 0
    for line in file:
        cancer_name = ""
        y_found = False
        x_found = False
        for word in line.split():
            if x_found and y_found:
                cancer_name = word
            else:
                string = ""
                for char in word:
                    if char.isdigit():
                        string += char
                if not x_found:
                    if int(string) != x:
                        x_changed = True
                    x = int(string)
                    x_found = True
                else:
                    if int(string) != y:
                        y_changed = True
                    y = int(string)
                    y_found = True

        # you will need to tweak this later to check if the clusters aren't in the list as well
        if x_changed or y_changed:
            x_changed = False
            y_changed = False
            if i != 0:
                if (curr_cluster.size < 10):
                    clusters.popitem()
                else:
                    curr_cluster.frequencies = get_cancer_frequency_per_cluster(curr_cluster.cancer_list,
                                                                            dictionary_of_sample_counts)
            clusters[(x, y)] = Cluster(x, y)
            curr_cluster = clusters[(x,y)]
            i += 1
        if cancer_name not in curr_cluster.cancer_names:
            curr_cluster.cancer_names.append(cancer_name)
            curr_cluster.cancer_list.append(Cancer(x, y, 1, cancer_name))
        else:
            for item in curr_cluster.cancer_list:
                if item.name == cancer_name:
                    item.count += 1
        curr_cluster.size += 1
    curr_cluster.frequencies = get_cancer_frequency_per_cluster(curr_cluster.cancer_list,
                                                                dictionary_of_sample_counts)


def print_clusters():
    for cluster in clusters.items():
        print("New Cluster")
        print(cluster[1].x, cluster[1].y)
        print(cluster[1].frequencies)
        print(cluster[1].size)


def get_cancer_frequency_per_cluster(mylist, total_samples):
    cancer_string = {}
    for item in mylist:
        ratio = item.count / total_samples[item.name]
        cancer_string[item.name] = ratio
        # print(item.name, item.x, item.y, item.count, ratio, sample_dict[item.name])
    return cancer_string


def generate_word_cloud(sample_dict):
    max_size = sample_dict["Total"]
     # Calculate the maximum scale factor

    x_coords = set()
    y_coords = set()
    for cluster in clusters.values():
        x_coords.add(cluster.x)
        y_coords.add(cluster.y)

    first_ratio = clusters[(0,0)].size/max_size
    actual_first = first_ratio*(1/first_ratio)
    actual_second = clusters[(0,1)].size/max_size*(1/first_ratio)
    second_ratio = clusters[(1,0)].size/max_size
    actual_third = second_ratio*(1/second_ratio)
    actual_fourth = clusters[(1,1)].size/max_size*(1/second_ratio)

    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    num_rows = y_max - y_min + 1
    num_cols = x_max - x_min + 1
    width_ratios = get_ratios(max_size, num_rows)
    main_fig = plt.figure(constrained_layout=True)
    main_gs = main_fig.add_gridspec(2, 2)
    figs = []
    for i in range(num_rows):
        fig, axs = plt.subplots(1, num_cols, width_ratios=width_ratios[i], figsize=(12, 8))
        for j in range(num_cols):
            if (x_min + j, y_min + i) in clusters:
                cluster = clusters[(x_min + j, y_min + i)]
                words = cluster.cancer_list
                frequencies = cluster.frequencies
                scale_factor = cluster.size/max_size # Normalize the scale factor
                width = 400
                height = 300
                new_width = scale_factor *10
                new_height = scale_factor *10
                wordcloud = WordCloud(collocations=False, background_color='white', width=int(width),
                                      height=int(height),relative_scaling=0.5).generate_from_frequencies(frequencies)

                axs[j].imshow(wordcloud, interpolation='bilinear')
            axs[j].axis('off')
        # fig.tight_layout(pad=0.0)
        figs.append(fig)
    for i, fig in enumerate(figs):
        fig.savefig(f'figure_{i}.png')
        image_data = plt.imread(f'figure_{i}.png')
        ax = main_fig.add_subplot(main_gs[i*2:])
        ax.imshow(image_data)
        ax.axis('off')

        # Read the saved image file and obtain the image data as a NumPy array
        # image_data = plt.imread('figure.png')

        # Display the image using ax.imshow()
        # main_axs[i].axis("off")
        # main_axs[i].imshow(image_data)

    # adjust_size(fig,axs,width_ratios)
    # plt.subplots_adjust(wspace=0.3, hspace=0.3)
    # for i, fig in enumerate(figs):
    #     fig.savefig(f'figure_{i}.png')  # Save each figure individually
    #
    #     # Read the saved image file and obtain the image data as a NumPy array
    #     image_data = plt.imread(f'figure_{i}.png')
    #
    #     # Display the image using main_axs[i].imshow()
    #     main_axs[i].axis('off')
    #     main_axs[i].imshow(image_data)
    #
     # Remove padding or gaps between subplots
    plt.show()


def get_ratios(max_size, num_rows):
    width_ratios = []
    for i in range(num_rows):
        temp_array = []
        for x in range(num_rows):
            temp_array.append(0)
        first_cluster_found = False
        first_ratio = 1
        for cluster in clusters.items():
            if cluster[1].x == i:
                if not first_cluster_found:
                    first_cluster_found = True
                    first_ratio = cluster[1].size/max_size
                val = cluster[1].size/max_size * (1/first_ratio)
                if (val > 1.5):
                    val = 1.5
                temp_array[cluster[1].y] = val
        width_ratios.append(temp_array)

    print(width_ratios)
    return width_ratios


#
# def adjust_size(fig, axs, width_ratios):
#         for i, width_ratio in enumerate(width_ratios):
#             gs = axs[1, 0].get_gridspec()
#             # gs.width_ratios = width_ratio
#             print(gs.get_width_ratios)
#         fig.tight_layout()

def main():
    file = read_header("my.txt")  # read off the header line "Cluster Cancer"
    dictionary_of_sample_counts = create_sample_number_dict("mytotalcount")
    parse_cluster(file, dictionary_of_sample_counts)
    generate_word_cloud(dictionary_of_sample_counts)

    file.close()


main()
