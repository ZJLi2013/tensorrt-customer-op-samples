# https://github.com/ultralytics/yolov5/blob/master/export.py

import onnx 
import onnx_graphsurgeon as onnx_gs 
import numpy as np 
import sys 

def insert_nms_plugin(model_onnx):
    yolo_graph = onnx_gs.import_onnx(model_onnx)
    box_data = yolo_graph.outputs[0]
    cls_data = yolo_graph.outputs[1]
    # https://github.com/NVIDIA/TensorRT/tree/main/plugin/batchedNMSPlugin
    # The boxes and scores input generates the following four outputs:
        # num_detections #shape [batch_size] #int32 tensor with number of valid detections
        # nmsed_boxes #shape [batch_size, keepTopK, 4] #fp32 tensor with coordinate of nms boxes
        # nmsed_scores #shape[batch_size, keepTopK], #fp32 tensor with scores of boxes
        # nmsed_classes #shape[batch_size, keepTopK], #fp32 tensor with classes of boxes
    nms_out_0 = onnx_gs.Variable(
        "BatchedNMS",
        dtype=np.int32
    )
    nms_out_1 = onnx_gs.Variable(
        "BatchedNMS_1",
        dtype=np.float32
    )
    nms_out_2 = onnx_gs.Variable(
        "BatchedNMS_2",
        dtype=np.float32
    )    
    nms_out_3 = onnx_gs.Variable(
        "BatchedNMS_3",
        dtype=np.float32
    )

    nms_attrs = dict()
    nms_attrs["shareLocation"] = 1 
    nms_attrs["backgroundLabelId"]=-1
    nms_attrs["scoreThreshold"] = 0.001
    nms_attrs["iouThreshold"] = 0.65 
    nms_attrs["topK"] = 2*300 
    nms_attrs["keepTopK"] = 300
    nms_attrs["numClasses"]=80
    nms_attrs["clipBoxes"]=0
    nms_attrs["isNormalized"]=0
    nms_attrs['scoreBits']=16

    nms_plugin = onnx_gs.Node(
        op="BatchedNMSDynamic_TRT",
        name="BatchedNMS_N",
        inputs=[box_data, cls_data],
        outputs=[nms_out_0, nms_out_1, nms_out_2, nms_out_3],
        attrs=nms_attrs
    )

    yolo_graph.nodes.append(nms_plugin)
    yolo_graph.outputs = nms_plugin.outputs 
    yolo_graph.cleanup().toposort()
    model_onnx = onnx_gs.export_onnx(yolo_graph)
 #   #Metadata 
 #   d = {'stride': int(max(model.stride)), 'names': model.names}
 #   for k, v in d.items():
 #       meta = model_onnx.metadata_props.add()
 #       meta.key, meta.value = k, str(v)
    f = "yolov5s_nms.onnx" 
    onnx.save(model_onnx, f)
    print(f'onnx_nms export success')
    return f 


if __name__ == "__main__":
    assert (len(sys.argv)==2)
    onnx_model = onnx.load(sys.argv[1])
    insert_nms_plugin(onnx_model)
    print("successfully inserted nms plugin to yolov5 onnx model\n")





