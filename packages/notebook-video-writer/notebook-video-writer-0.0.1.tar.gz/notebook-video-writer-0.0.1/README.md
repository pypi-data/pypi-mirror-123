# notebook-video-writer
Create videos from numpy arrays in a jupyter notebook  

[Original source](https://colab.research.google.com/github/znah/notebooks/blob/master/external_colab_snippets.ipynb  
) from [Alexander Mordvintsev](https://github.com/znah)

### Install    
  
`pip install notebook-video-writer`  

### Dependencies  
  - Must have ffmpeg installed  

### Usage  
```python

import numpy as np
# optionally wrap with tqdm for progress bar
from tqdm import tqdm
from notebook_video_writer import VideoWriter

with VideoWriter(fps=40) as vw:
    for i in tqdm(range(100)):
        frame = np.random.rand(256,256,3)
        vw.add(render)

```
