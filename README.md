# tensorrt-customer-op-samples


## hello-world 

* [setuptools: building extension module](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html)

* [demo: building python C/C++ extension with setuptools](https://elmjag.github.io/setuptools.html)

* [pybinds](https://realpython.com/python-bindings-overview/)

* [build python extension modules for c++ with pybind11](https://alextereshenkov.github.io/pybind11-python-bindings.html)





```sh
# build libs and put it in source dir 
python setup.py build_ext --inplace  
# build lib and put in normal dir
python setup.py build 

```



## issues



* check [pybind11](https://pybind11.readthedocs.io/en/stable/basics.html)

```sh
$ c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) example.cpp -o example$(python3-config --extension-suffix)
```

* [sample code](https://github.com/pybind/python_example)


```yml
dynamic module does not define module export function(PyInit_add)
```

* [zhihu, 使用pybinding封装c++](https://zhuanlan.zhihu.com/p/80884925)

