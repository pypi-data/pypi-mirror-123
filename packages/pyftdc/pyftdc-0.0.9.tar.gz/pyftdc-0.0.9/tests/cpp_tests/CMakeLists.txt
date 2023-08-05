project(Boost_Tests_run)

find_package (Boost REQUIRED COMPONENTS unit_test_framework)

add_executable (${PROJECT_NAME}
        basic_tests.cpp
        ${CMAKE_SOURCE_DIR}/src/CSVWriter.cpp
        ${CMAKE_SOURCE_DIR}/src/Dataset.cpp
        ${CMAKE_SOURCE_DIR}/src/ParserTask.cpp
        ${CMAKE_SOURCE_DIR}/src/Chunk.cpp
        ${CMAKE_SOURCE_DIR}/src/FTDCParser.cpp
        ${CMAKE_SOURCE_DIR}/src/ParserTasksList.cpp
        ${CMAKE_SOURCE_DIR}/src/ConstDataRangeCursor.cpp
        ${CMAKE_SOURCE_DIR}/src/ChunkMetric.cpp
        ../../src/parser/Configuration.cpp
        ../../src/parser/Configuration.h ../../src/MergerTask.cpp ../../src/include/MergerTask.h ../../src/MergerTasksList.cpp ../../src/include/MergerTasksList.h)

target_include_directories (${PROJECT_NAME}  PUBLIC
        ${Boost_INCLUDE_DIRS}
        "/usr/local/include/libbson-1.0"
        "/opt/homebrew/include/libbson-1.0"
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src/include
        )

target_link_libraries (${PROJECT_NAME}
        ${Boost_LIBRARIES}
        Boost::log
         )