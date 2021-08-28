#include <iostream>
#include <torch/script.h>
#include "custom.h"

void foo() {
  std::cout << "foo" << std::endl;
}

TORCH_LIBRARY_FRAGMENT(foo, m) {
  m.def("foo::foo", &foo);
}
