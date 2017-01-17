#! 
from datetime import date   
import os     
from os import listdir, path
import shutil

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

#
# path utils
#

def this_folder():

    return os.path.dirname(os.path.abspath(__file__))

def par_folder():

    return path.join(this_folder(), '..')

def make_if_none(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

#
# bootswatch paths
#

root_generator = path.join(this_folder(), 'generator')
root_3rd = path.join(root_generator, '3rd')
root_bootswatch = path.join(root_3rd, 'bootswatch')

root_themes = [(root_bootswatch, '3'),
                (path.join(root_bootswatch, '2'), '2'),
                (path.join(root_bootswatch, '4-alpha'), '4')]

#
# collect theme css to the same folder with script
#

for r, ver in root_themes:
    to = path.join(root_generator, 'bootswatch-themes', ver)
    make_if_none(to)

    for theme_folders in os.listdir(r):
        # logging.info(theme_folders)
        test_file = path.join(r, theme_folders, 'bootstrap.min.css')
        if path.exists(test_file):

            shutil.copy(path.join(r, theme_folders, 'bootstrap.min.css'), path.join(to, theme_folders + '.min.css'))

            # logging.info('done copying {}\n\t{}'.format(test_file, to))
