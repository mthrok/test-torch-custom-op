#include <torch/extension.h>

#include "custom.h"

PYBIND11_MODULE(_foo, m) {
  m.def("foo", foo, "foo");
}
