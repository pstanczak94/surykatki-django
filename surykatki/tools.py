import numpy as np
import tensorflow as tf
import scipy.misc

from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

if tf.VERSION != '1.4.0':
    raise ImportError('Please upgrade your tensorflow installation to v1.4.0!')


class ErrorHelper(object):
    def __init__(self):
        self.success = True
        self.msg = ''
    def setError(self, msg):
        self.success = False
        self.msg = msg
    def clearError(self):
        self.success = True
        self.msg = ''


def load_image_into_numpy_array(image):
    max_wide = 800
    
    image.thumbnail((max_wide, max_wide), Image.ANTIALIAS)
    
    (im_width, im_height) = image.size
    
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def object_detection(imageFile, filenameBefore, filenameAfter):

    MODEL_NAME = 'training'
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    PATH_TO_LABELS = MODEL_NAME + '/object-detection.pbtxt'
    NUM_CLASSES = 1

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name = '')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes = NUM_CLASSES, use_display_name = True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph = detection_graph) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            image = Image.open(imageFile)
            image_np = load_image_into_numpy_array(image)
            image_np_expanded = np.expand_dims(image_np, axis = 0)

            scipy.misc.imsave(filenameBefore, image_np)
            
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict = {image_tensor: image_np_expanded}
            )

            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates = True,
                line_thickness = 4
            )

            scipy.misc.imsave(filenameAfter, image_np)

