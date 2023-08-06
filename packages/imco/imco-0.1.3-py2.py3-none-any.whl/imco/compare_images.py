import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


def compareImages(
        images, image_names=None, compute_metrics=True, crop_size=None,
        crop_coordinates=None, font_size=1, font_stoke=3, first_text_line_y=40,
        text_spacing=40, text_x_coordinate=10, white_box_height=140):
    """Compare list of images to one image

    Concatenate images into single image with added similarity metrics printed
    below each comparison image.

    Arguments
    ---------
    images : list of numpy arrays
        List including images which are compared to the reference image
    image_names : list of strings
        List of names for each comparison image and reference image
    compute_metrics : bool
        If True, all images are compared to the last image. If False, no
        comparison or metrics computed.
    crop_size : int
        If defined, all images will be center cropped with this size
    crop_coordinates : tuple or None
        (x, y) coordinates of top left coordinate. If None, crop from center.
    font_size : int
        Text font size
    font_stoke : int
        Text width
    first_text_line_y : int
        Text y-coordinate in the first line
    text_spacing : int
        Text row height
    text_x_coordinate : int
        Text x-coordinate in each row
    white_box_height : int
        Height in pixels of each white box added below the images

    Return
    ------
    Numpy array of concatenated comparison image with similarity metrics
    """
    def centerCrop(image):
        center = np.divide(list(image.shape), 2)
        x = center[1] - crop_size / 2
        y = center[0] - crop_size / 2
        return image[int(y):int(y + crop_size), int(x):int(x + crop_size)]
    def crop(image):
        (x, y) = crop_coordinates
        return image[int(y):int(y + crop_size), int(x):int(x + crop_size)]
    def addText(image, text, position):
        return cv2.putText(
            image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size,
            (0, 0, 0, 255), font_stoke)
    def getWhiteBox(image):
        shape = tuple([white_box_height] + list(image.shape[1:]))
        return np.ones(shape) * 255

    # Add unknown names
    image_names += ["" for i in range(len(images) - len(image_names))]

    # Crop images
    if type(images) == np.array:
        images = [images]
    if crop_size:
        if crop_coordinates is not None:
            images = [crop(image) for image in images]
        else:
            images = [centerCrop(image) for image in images]

    # Define texts
    texts = []
    if image_names:
        texts.append(image_names)
    if compute_metrics:
        texts += [
            [
                "PSNR: {0:.2f}dB".format(
                    psnr(images[i], images[-1]))
                    for i in range(len(images) - 1)
            ],
            [
                "SSIM: {0:.2f}".format(
                    ssim(images[i], images[-1], multichannel=True))
                    for i in range(len(images) - 1)
            ],
        ]

    # Add text to images
    for i, image in enumerate(images):
        white_area = getWhiteBox(image)
        for j, text_list in enumerate(texts):
            if i >= len(text_list):
                break
            position = (text_x_coordinate, first_text_line_y + j*text_spacing)
            white_area = addText(white_area, text_list[i], position)
        images[i] = np.concatenate([image, white_area], axis=0)
    return np.concatenate(images, axis=1)


if __name__ == "__main__":
    # Paths
    image_paths = [
        "../input/REDS/train_blur/001/00000000.png",
        "../input/REDS/train_sharp/001/00000000.png",
        "../input/REDS/train_sharp/001/00000000.png",
    ]

    # Images and names
    images = [cv2.imread(image_path) for image_path in image_paths]
    images[2] = (images[2]**0.5 * 4).astype(np.uint8)
    names = ["Input", "Prediction 1", "Ground Truth"]

    # Create comparison image
    comparison_image = compareImages(images, names, True, 256, (10, 30))
    cv2.imwrite("comparison_image.png", comparison_image)
