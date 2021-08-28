cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(foo)

string(FIND "${CMAKE_CXX_FLAGS}" "-std=c++" env_cxx_standard)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if (APPLE)
  set(CMAKE_MACOSX_RPATH ON)
  set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
endif()

find_package(Torch REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall ${TORCH_CXX_FLAGS}")

add_library(
  foo
  SHARED
  src/custom.cpp
  )

add_library(
  _foo
  SHARED
  src/pybind.cpp
  )
set_target_properties(_foo PROPERTIES PREFIX "")

if (APPLE)
  set_target_properties(foo PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
  set_target_properties(_foo PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
endif()

target_include_directories(
  foo
  PRIVATE
  ${PROJECT_SOURCE_DIR}/src
  )

target_link_libraries(
  foo
  ${TORCH_LIBRARIES}
  )

target_include_directories(
  _foo
  PRIVATE
  ${PROJECT_SOURCE_DIR}/src
  ${Python_INCLUDE_DIR}
  )

target_link_libraries(
  _foo
  ${TORCH_LIBRARIES}
  )

install(
  TARGETS foo
  LIBRARY DESTINATION .
  RUNTIME DESTINATION .
  )

install(
  TARGETS _foo
  LIBRARY DESTINATION .
  RUNTIME DESTINATION .
  )
