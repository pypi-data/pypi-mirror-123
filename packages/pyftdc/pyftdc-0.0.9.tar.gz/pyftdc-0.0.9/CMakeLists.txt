cmake_minimum_required(VERSION 3.15...3.19)

project(pyftdc VERSION "0.0.1")


if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path automatically,
  # so we need to add it _or_ the pybind11 specific directory here.
  execute_process(
    COMMAND
      "${PYTHON_EXECUTABLE}" -c
      "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()

# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

set(CMAKE_CXX_STANDARD 17)

find_package(Boost COMPONENTS log program_options filesystem REQUIRED)
find_package(Threads REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package (bson-1.0  REQUIRED)

include_directories(
        ${Boost_INCLUDE_DIRS}
        "/usr/local/include/libbson-1.0"
	    "/opt/homebrew/include/libbson-1.0"
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src/parser
        ${CMAKE_SOURCE_DIR}/src/include
)

link_directories(
        "/usr/local/opt/icu4c/lib"
        "/usr/local/lib"
        )

# Link libraries to the targets
link_libraries(
        Threads::Threads
        ${Boost_LIBRARIES}
        bson-static-1.0
        z
        yaml-cpp
        ${CMAKE_DL_LIBS}
        )

pybind11_add_module(_core MODULE
        src/main.cpp
        src/CSVWriter.cpp
        src/Dataset.cpp
        src/ParserTask.cpp
        src/Chunk.cpp
        src/FTDCParser.cpp
        src/ParserTasksList.cpp
        src/ConstDataRangeCursor.cpp
        src/ChunkMetric.cpp
        src/MergerTasksList.cpp
        src/MergerTask.cpp
)

target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _core DESTINATION .)

add_subdirectory(tests/cpp_tests)
add_subdirectory(src/parser)
