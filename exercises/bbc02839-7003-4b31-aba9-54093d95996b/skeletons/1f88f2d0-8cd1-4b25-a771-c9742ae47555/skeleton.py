import os
import numpy as np
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/.tmp"
import matplotlib.pyplot as plt

def main():
    build_plot()
    path = save_boxplot()
    print(path)
    
def build_plot():
    # Sample data with fixed values
    data = [
        [1, 2, 2, 3, 3, 3, 4, 4, 5],  # Group A
        [2, 3, 3, 4, 4, 4, 5, 5, 6],  # Group B  
        [3, 4, 4, 5, 5, 5, 6, 6, 7],  # Group C
        [4, 5, 5, 6, 6, 6, 7, 7, 8]   # Group D
    ]

    # Create boxplot
    plt.boxplot(data, labels=['A', 'B', 'C', 'D'])
    plt.title('Boxplot Example')
    plt.ylabel('Values')
    
def save_boxplot():
    # Save plot
    file_path = 'boxplot_' + str(np.random.randint(1000)) + '.png'
    plt.savefig(file_path)
    plt.close()  # Close the figure to free memory

    return os.path.abspath(file_path)

if __name__ == '__main__':
    main()
    