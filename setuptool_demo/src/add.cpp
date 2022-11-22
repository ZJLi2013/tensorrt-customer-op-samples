#include <pybind11/pybind11.h>

int add(int a, int b){
	return a+b;
}

PYBIND11_MODULE(cppextension, m){
	m.def("add", &add, "add func");
}

