import numpy as np
import utils.core, utils.image

floorsLevelsImgs = [
    utils.image.loadAsArray('radar/images/floor-levels/0.png'),
    utils.image.loadAsArray('radar/images/floor-levels/1.png'),
    utils.image.loadAsArray('radar/images/floor-levels/2.png'),
    utils.image.loadAsArray('radar/images/floor-levels/3.png'),
    utils.image.loadAsArray('radar/images/floor-levels/4.png'),
    utils.image.loadAsArray('radar/images/floor-levels/5.png'),
    utils.image.loadAsArray('radar/images/floor-levels/6.png'),
    utils.image.loadAsArray('radar/images/floor-levels/7.png'),
    utils.image.loadAsArray('radar/images/floor-levels/8.png'),
    utils.image.loadAsArray('radar/images/floor-levels/9.png'),
    utils.image.loadAsArray('radar/images/floor-levels/10.png'),
    utils.image.loadAsArray('radar/images/floor-levels/11.png'),
    utils.image.loadAsArray('radar/images/floor-levels/12.png'),
    utils.image.loadAsArray('radar/images/floor-levels/13.png'),
    utils.image.loadAsArray('radar/images/floor-levels/14.png'),
    utils.image.loadAsArray('radar/images/floor-levels/15.png'),
]

np.save('radar/npys/floorsLevelsImgs.npy', floorsLevelsImgs)