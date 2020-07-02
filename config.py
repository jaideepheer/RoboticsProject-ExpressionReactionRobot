resources = {}

# FACE DETECT
resources['facedetect_haarcascade_frontalface'] = "./resources/facedetect_haarcascade_frontalface_default.xml"
resources['facedetect_dnnmodel_weights'] = "./resources/facedetect_dnn_res10_300x300_ssd_iter_140000_fp16.caffemodel"
resources['facedetect_dnnmodel_structure'] = "./resources/facedetect_dnn_deploy.prototxt"

# EMOTION DETECT - SARENGIL
resources['emotiondetect_sarengil_weights'] = "./resources/emotiondetect/sarengil/facial_expression_model_weights.h5"
resources['emotiondetect_sarengil_structure'] = "./resources/emotiondetect/sarengil/facial_expression_model_structure.json"

# EMOTION DETECT - OARRIAGA
resources['emotiondetect_oarriaga_102'] = "./resources/emotiondetect/oarriaaga/fer2013_mini_XCEPTION.102-0.66.hdf5"
resources['emotiondetect_oarriaga_107'] = "./resources/emotiondetect/oarriaaga/fer2013_mini_XCEPTION.107-0.66.hdf5"
resources['emotiondetect_oarriaga_110'] = "./resources/emotiondetect/oarriaaga/fer2013_mini_XCEPTION.110-0.65.hdf5"
resources['emotiondetect_oarriaga_KDEF'] = "./resources/emotiondetect/oarriaaga/mini_XCEPTION_KDEF.hdf5"