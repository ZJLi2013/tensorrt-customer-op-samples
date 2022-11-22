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


## hello_world