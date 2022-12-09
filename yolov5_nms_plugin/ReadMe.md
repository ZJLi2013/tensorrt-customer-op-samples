
## under hood : what's going on ?

step1: yolov5 pytorch 转 yolov5.onnx
step2: yolov5.onnx 通过 onnx_graphsurgeon 修改并添加 batchNMS_TRT 节点， 保存为 yolov5_nms.onnx 文件
step3: yolov5_trt_inference中，通过 trt.onnx_parser(yolov5.onnx) 生成 yolov5_nms.engine

* 那么，step3中的关键问题就是: trt_onnx_parser() 是如何解析包含trt_oss_plugin `op=BatchedNMSDynamic_TRT` onnx模型的 ？

* step3.1: TRT插件实现:
    * 实现一个自定义插件需要写两个类：
        * BatchedNMSPlugin，继承IPluginV2DynamicExt，是插件类，用于写插件具体的实现
        * BatchedNMSPluginCreator，继承BaseCreator，是插件工厂类，用于根据需求创建该插件
    
* step3.2: TRT插件注册：
    * 方式一： 通用`initializePlugin()` 注册

        ```c++
        //  TRT_OSS/plugin/api/InferPlugin.cpp 
        def initLibNvInferPlugins(void* logger, const char* libNamespace):
            initializePlugin<nvinfer1::plugin::BatchedNMSPluginCreator>(logger, libNamespace)
            
        def initializePlugin<nvinfer1::plugin::BatchedNMSPluginCreator>(logger, libNamespace):
            def addPluginCreator():
                getPluginRegistry()->registerCreator(*pluginCreator, libNamespace)
        ```

    * 方式二：在插件实现中通过调用宏注册

        ```c++
        REGISTER_TENSORRT_PLUGIN(BatchedNMSPluginCreator);  // onnx op as BatchedNMSDynamic_TRT
        ```

* step3.3: 插件实现编译
    * 将自定义插件目录放在 TensorRT/plugin 目录下，并在TensorRT/plugin/CMakeLists.txt 中加入对自定义插件的编译。注意添加`LD_LIBRARY_PATH`指向`/trt_plugin/buid/lib`

* step3.4: 在onnx模型解析过程，使用已有trt_oss插件的过程：

    * 在onnx_parser中(内部会)调用 initLibNvInferPlugins()。
        * 调用 initLibNvInferePlugins()之后，在具体解析某个onnx.node(op="BatchedNMSDynamic_TRT")，应该是通过该op.name在runtime查询该op实现并执行（TODO:)

            ```c++
            // tensorrt/parsers/onnx/ModelImporter.cpp
            parse(onnx_model):
                return this->parseWithWeightDescriptors(onnx_model)

            parseWightWeightDescriptors(onnx_model):
                status = deserialize_onnx_model(onnx_model, &model);
                status = this->importModel(model);

            importModel(model):
                #if ENABLE_STD_PLUGIN
                    initLibNvInferPlugins()
                #endif 
            ```

    * 另外，对于用户自定义算子，也可以通过`DEFINE_BUILTIN_OP_IMPORTER` 宏导入：

        ```c++
        // tensorrt/parser/onnx/builtin_op_importers.cpp 
        #define DEFINE_BUILTIN_OP_IMPORTER(op)

        def registerBuiltinOpImporter():
            // 将cus_op 注册到 builtin_op_importers 中
            getBuiltinOpImporterMap().insert({op, importer}).second;
            
        def getBuiltinOpImporterMap():
            return builtin_op_importers

        // tensorrt/parsers/onnx/onn2trt_utils.cpp 
        def unaryHelper(ctx, node, input, op):
            tensorPtr = convertToTensor(input, ctx)
            layer = ctx->network()->adUnary(tensorPtr, op)
            ctx->registryLayer(layer, getNodeName(node))
            tensorPtr = layer->getOutput(0)
            return tensorPtr
        
        DEFINE_BUILTIN_OP_IMPORTER(BatchedNMSDynamic_TRT)
        {
            return unaryHelper(ctx, node, inputs.at(0), nvinfer1::UnaryOperation::kABS);
        }

        ```



## reference 

* [知乎：实现TensorRT自定义插件(plugin)自由](https://zhuanlan.zhihu.com/p/297002406)
* [github: Trt onnx插件](https://github.com/dlunion/tensorRTIntegrate/blob/master/README.onnx.plugin.md)
* [github: tensorRT_Pro](https://github.com/shouxieai/tensorRT_Pro)
