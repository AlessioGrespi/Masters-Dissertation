import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import numpy as np

# Your formatted data points
data = [
    [2, 2, 207.8078431, 182.8627451],
    [4, 2, 310.7960784, 230.3137255],
    [6, 2, 312.3686275, 253.9647059],
    [8, 2, 294.5215686, 273.6509804],
    [10, 2, 293.8078431, 295.2705882],
    [12, 2, 283.5176471, 285.9019608],
    [14, 2, 232.9176471, 291.0470588],
    [16, 2, 209.8941176, 290.1294118],
    [2, 4, 208.8078431, 191.572549],
    [4, 4, 277.4039216, 223.6901961],
    [6, 4, 313.8862745, 263.4352941],
    [8, 4, 325.8431373, 294.1254902],
    [10, 4, 329.1882353, 284.454902],
    [12, 4, 325.4509804, 289.5686275],
    [14, 4, 309.2431373, 288.6627451],
    [16, 4, 302.4784314, 276.6941176],
    [2, 6, 208.8078431, 204.0235294],
    [4, 6, 247.0745098, 250.1176471],
    [6, 6, 303.7882353, 283.6627451],
    [8, 6, 320.745098, 290.5137255],
    [10, 6, 327.6313725, 278.3372549],
    [12, 6, 330.2588235, 245.3098039],
    [14, 6, 328.2352941, 238.8392157],
    [16, 6, 330.1607843, 233.3254902],
    [2, 8, 208.8078431, 180.9254902],
    [4, 8, 217.8823529, 249.2588235],
    [6, 8, 272.0588235, 240.7137255],
    [8, 8, 311.2196078, 227.8392157],
    [10, 8, 320.0392157, 222.345098],
    [12, 8, 323.5607843, 220.4901961],
    [14, 8, 330.0392157, 213.9686275],
    [16, 8, 331.3215686, 208.9294118]
]

# Separate data into lists for each column
distance, score, heading_90, heading_230 = zip(*data)

# Reshape data for scatter plotting
distance = np.array(distance)
score = np.array(score)
heading_90 = np.array(heading_90)
heading_230 = np.array(heading_230)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot scatter for Heading 90
ax.scatter(distance, score, heading_90, c='blue', marker='o', label='Heading 90')

# Plot scatter for Heading 230
ax.scatter(distance, score, heading_230, c='red', marker='^', label='Heading 230')

# Add a vertical line at distance 9 with score 6
ax.axvline(x=9, color='green', linestyle='--', label='Vertical Line at (9, 6)')

# Set axis labels
ax.set_xlabel('Distance Gain')
ax.set_ylabel('Score Gain')
ax.set_zlabel('Cost Saving')

# Create custom legend entries for scatter
legend_elements_90 = [Line2D([0], [0], marker='o', color='w', label='Heading 90', markerfacecolor='r', markersize=10)]
legend_elements_230 = [Line2D([0], [0], marker='^', color='w', label='Heading 230', markerfacecolor='b', markersize=10)]

# Add legends to the plot
ax.legend(handles=legend_elements_90 + legend_elements_230, loc='upper right')

# Show the plot
plt.show()
