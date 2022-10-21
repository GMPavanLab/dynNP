#%%
from figureSupportModule import (
    colorBarExporter,
    topDownColorMap,
    bottomUpColorMap,
    topDownFullColorMap,
)

#%%
colorBarExporter(topDownColorMap[::-1], "topDownCMAP.png")
#%%
colorBarExporter(bottomUpColorMap[::-1], "bottomUpCMAP.png")
#%%
colorBarExporter(topDownFullColorMap[::-1], "topDownFullCMAP.png")

# %%
