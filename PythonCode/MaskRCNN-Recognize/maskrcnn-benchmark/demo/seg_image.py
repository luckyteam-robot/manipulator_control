import argparse
import cv2

from maskrcnn_benchmark.config import cfg
from mypredictor import COCODemo

import time

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def load(url):
    """
    Given an url of an image, downloads the image and
    returns a PIL image
    """
    pil_image = Image.open(url)
    # convert to BGR format
    image = np.array(pil_image)[:, :, [2, 1, 0]]
    return image

def main():
    parser = argparse.ArgumentParser(description="PyTorch Object Segmentation Image Demo")
    parser.add_argument(
        "--config-file",
        default="configs/my_test_e2e_mask_rcnn_R_50_FPN_1x.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.7,
        help="Minimum score for the prediction to be shown",
    )
    parser.add_argument(
        "--min-image-size",
        type=int,
        default=224,
        help="Smallest size of the image to feed to the model. "
            "Model was trained with 800, which gives best results",
    )
    parser.add_argument(
        "--show-mask-heatmaps",
        dest="show_mask_heatmaps",
        help="Show a heatmap probability for the top masks-per-dim masks",
        action="store_true",
    )
    parser.add_argument(
        "--masks-per-dim",
        type=int,
        default=2,
        help="Number of heatmaps per dimension to show",
    )
    parser.add_argument(
        "opts",
        help="Modify model config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    parser.add_argument(
        "--input-file",
        default="test/1.jpg",
        metavar="FILE",
        help="path to input file",
    )
    parser.add_argument(
        "--output-file",
        default="test/1predictions.jpg",
        metavar="FILE",
        help="path to output file",
    )

    args = parser.parse_args()

    # load config from file and command-line arguments
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    # prepare object that handles inference plus adds predictions on top of image
    coco_demo = COCODemo(
        cfg,
        confidence_threshold=args.confidence_threshold,
        show_mask_heatmaps=args.show_mask_heatmaps,
        masks_per_dim=args.masks_per_dim,
        min_image_size=args.min_image_size,
    )

    image = load(args.input_file)
    predictions = coco_demo.run_on_opencv_image(image)
    cv2.imwrite(args.output_file,predictions)

if __name__ == "__main__":
    main()
