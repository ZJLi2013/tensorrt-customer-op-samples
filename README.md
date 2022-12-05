# tensorrt-customer-op-samples



## setuptool_demo 

* there are two things in mind:
    * setuptool module is only responsible for compiling C++ functions/class
    * pybinding module is actually used to mapping the functions in C++ to Python

* both `setuptool` and `pybind11` moduels need first be installed.  

* build & test 

```sh
# for local test, run the following command
python3 setup.py build 
# for container test, can directly isntall
python3 setup.py build install
# test 
python3 test.py
```

* reference 
    * [setuptools: building extension module](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html)
    * [pybind11](https://pybind11.readthedocs.io/en/stable/basics.html)
        * [Pybinding::Extension sample code](https://github.com/pybind/python_example)
    * [zhihu, 使用pybinding封装c++](https://zhuanlan.zhihu.com/p/80884925)



## yolov5_nms_plugin

this sample is derived from [NV-AI-IOT/yolov5_gpu_optimization](https://github.com/NVIDIA-AI-IOT/yolov5_gpu_optimization)

* step1:
	* using `Dockerfile_onnx` to generate `yolov5.onnx`, which is derived from [ultra/yolov5](https://github.com/ultralytics/yolov5), but need modify the outputs of model from original `concated_xy_wh_conf` layout to `bbox, score` layout

* step2:
	* run `python3 onnx_nms_insert.py` to insert nms plugin to `yolov5.onnx` 

* step3:
	* run inference with script from `yolov5_gpu_optimization` as:
	```sh
	python yolov5_trt_inference.py --input_images_folder=</path/to/coco/images/val2017/> --output_images_folder=./coco_output --onnx=</path/to/yolov5s.onnx>
	```


