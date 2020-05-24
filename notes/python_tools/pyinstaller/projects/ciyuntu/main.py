# from matplotlib import MatplotlibDeprecationWarning
from sys import exit as sys_exit
from ciyun.db import update_config
from ciyun.tools import plot_img, spider

# import warnings
# # import matplotlib.cbook
# # warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
# warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)


def main():
    url = 'http://www.people.com.cn/'
    update_config()
    spider(url)
    plot_img()


try:
    main()
except KeyboardInterrupt:
    print('Bye.')
    sys_exit(1)
