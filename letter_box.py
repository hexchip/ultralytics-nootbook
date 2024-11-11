import cv2

class LetterBox:
    """Resize image and padding for detection, instance segmentation, pose."""

    def __init__(self, new_shape=(640, 640), scale_fill=False, scaleup=True, center=True):
        """Initialize LetterBox object with specific parameters."""
        self.new_shape = new_shape
        self.scale_fill = scale_fill
        self.scaleup = scaleup
        self.center = center  # Put the image in the middle or top-left

    def __call__(self, image):
        """Return image with added border."""
        shape = image.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape
        
        ratio = None
        new_unpad = None
        dw = None
        dh = None
 
        # Compute scale ratio and padding
        if self.scale_fill:  # stretch
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios
            new_unpad = new_shape[1], new_shape[0]
            dw, dh = 0, 0
        else:
            # Scale ratio (new / old)
            r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
            if not self.scaleup:  # only scale down, do not scale up (for better val mAP)
                r = min(r, 1.0)
            ratio = r, r
            new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
            dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if self.center:
            dw /= 2  # divide padding into 2 sides
            dh /= 2

        if shape[::-1] != new_unpad:  # resize
            image = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)
        
        top, bottom = int(round(dh - 0.1)) if self.center else 0, int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)) if self.center else 0, int(round(dw + 0.1))
        image = cv2.copyMakeBorder(
            image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114)
        )  # add border
        
        return image