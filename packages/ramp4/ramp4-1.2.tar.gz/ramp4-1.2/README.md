INTRODUCTION
------------
A simple library to make mp4 movies with matplotlib.pyplot. It use RAM instead of disk storage for the temporary images.

INSTALLATION
------------
```sh
pip install ramp4
```

GET STARTED
-----------
1) Get an instance of ramp4.
2) Add image with matplotlib using the 'add' method.
3) Render the video using the 'render' method.
4) Done

EXAMPLE 1
---------
```python
import numpy as np
import matplotlib.pyplot as plt
from ramp4 import ramp4

X = np.linspace(0, 5, 250)

movie = ramp4()
for i in np.linspace(0, 3.14, 200):
    fig, ax = plt.subplots(1, 1)
    ax.plot(X, np.sin(X+i))
    ax.set_xlim(0, 5)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x+t)")
    movie.add(fig=fig, dpi=200)
    plt.close(fig=fig)

movie.render(outfile="video_example1.mp4", fps=50)
```
EXAMPLE 2
---------

```python
import numpy as np
import matplotlib.pyplot as plt
from ramp4 import ramp4

X = np.linspace(0, 5, 250)

movie = ramp4()
for i in np.linspace(0, 3.14, 200):
    plt.plot(X, np.cos(X+i))
    plt.xlim(0, 5)
    plt.ylim(-1, 1)
    plt.xlabel("x")
    plt.ylabel("cos(x+t)")
    movie.add(dpi=200)
    plt.close()

    movie.render(outfile="video_example_2a.mp4", fps=50, close=False)
    movie.render(outfile="video_example_2b.mp4", fps=100)
```

