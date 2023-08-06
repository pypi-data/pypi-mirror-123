find_package(Eigen3 3 REQUIRED NO_MODULE)
find_package(Python 3 COMPONENTS Interpreter Development)

set(GMIX_INCLUDE "${PROJECT_SOURCE_DIR}/include")
set(PYBIND11_INCLUDE "${PROJECT_SOURCE_DIR}/extern/pybind11/include")

message("Python found: ${Python_FOUND}")
message("GMIX_INCLUDE: ${GMIX_INCLUDE}")
message("PYBIND11_INCLUDE: ${PYBIND11_INCLUDE}")
message("PYTHON_INCLUDE: ${Python_INCLUDE_DIRS}")

# include directories
include_directories("$GMIX_INCLUDE")
include_directories("${Python_INCLUDE_DIRS}")
include_directories("${PYBIND11_INCLUDE}")

add_library(cgmix2 SHARED pygmix2.cpp)

target_include_directories(cgmix2 PUBLIC ${GMIX_INCLUDE} ${PYBIND11_INCLUDE})
target_compile_features(cgmix2 PUBLIC cxx_std_17)

set_target_properties(
        cgmix2
        PROPERTIES
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS OFF
        PREFIX ""
        OUTPUT_NAME "cgmix2"
        LINKER_LANGUAGE CXX
)

target_link_libraries(cgmix2 PRIVATE Eigen3::Eigen)

#add_custom_command(
#    TARGET cgmix2 POST_BUILD
#    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:cgmix2> ../../../python-package/
#)
