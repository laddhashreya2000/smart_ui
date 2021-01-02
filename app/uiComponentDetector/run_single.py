from os.path import join as pjoin
import cv2
import os
from argparse import ArgumentParser

import detect_compo.ip_region_proposal as ip

parser = ArgumentParser()
parser.add_argument("--img", type=str, help="path/to/img")
parser.add_argument("--op_dir", type=str, help="path/to/output/directory")
parser.add_argument("--clf", action='store_true')


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))


if __name__ == '__main__':

    '''
        ele:min-grad: gradient threshold to produce binary map         
        ele:ffl-block: fill-flood threshold
        ele:min-ele-area: minimum area for selected elements 
        ele:merge-contained-ele: if True, merge elements contained in others
        text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
        text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

        Tips:
        1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
        2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
        3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
        4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    '''
    args = parser.parse_args()

    key_params = {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'merge-contained-ele':False,
                  'max-word-inline-gap':4, 'max-line-gap':4}

    # set input image path
    input_path_img = args.img
    output_root = args.op_dir

    resized_height = resize_height_by_longest_edge(input_path_img)

    is_clf = args.clf

    os.makedirs(pjoin(output_root, 'ip'), exist_ok=True)
    
    # switch of the classification func
    classifier = None
    if is_clf:
        classifier = {}
        from cnn.CNN import CNN
        classifier['Elements'] = CNN('Elements')
    ip.compo_detection(input_path_img, output_root, key_params,
                        classifier=classifier, resize_by_height=resized_height, show=False)