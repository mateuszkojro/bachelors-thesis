import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def set_style():
    # Create a colormap using the grayscale values
    font = {
            'family' : 'normal',
            'weight' : 'normal',
            'size'   : 20
            }
    matplotlib.rc('font', **font)
    sns.set_style('whitegrid')
    cmap = sns.color_palette("Greys_r", n_colors=5)
    sns.set_palette(cmap, color_codes=True)

def save_plot(name, path="", thight=True):
    if thight:
        plt.tight_layout()
    plt.savefig(name)