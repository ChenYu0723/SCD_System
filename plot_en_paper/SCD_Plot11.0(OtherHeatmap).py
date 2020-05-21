import numpy as np
import matplotlib.pyplot as plt
from Practice.heatmap.image_annotated_heatmap import heatmap, annotate_heatmap

label = ['Home-to-Other','Work-to-Other','Other-to-Home','Other-to-Work']
# label = ['Other-to-Other']

station = [1056,930,1159,1621,252,253,255]
# station = [(753,251),  (235,236),   (251,417),   (417,251),  (235,1627),  (250,417),   (417,941),   (633,417)]

trans_ls = [[0.,         0.,         0.,         0.,         0.,         0.,
  0.        ],
 [0.07692308, 0.,         0.07692308, 0.,         0.84615385, 0.,
  0.        ],
 [0.07692308, 0.,         0.07692308, 0.53846154, 0.30769231, 0.,
  0.        ],
 [1.,         0.,         0.,         0.,         0.,         0.,
  0.        ]]

# trans_ls = [[0.16666667, 0.,         0.33333333, 0.16666667, 0.,         0.,
#   0.16666667, 0.16666667]]

trans_MX = np.array(trans_ls)
# print(trans_MX)


fig, ax = plt.subplots(figsize = (8,6))
im, cbar = heatmap(trans_MX, label, station, title="Commuter's Evening", cmap = 'Reds', cbarlabel="Transition Probability of Other Station")
texts = annotate_heatmap(im)

plt.tick_params(labelsize=18)
fig.tight_layout()
plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\OtherChooseProbability.eps', dpi=150)
# plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\OtherChooseProbability2.eps', dpi=150)
plt.show()