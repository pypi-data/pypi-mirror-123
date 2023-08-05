cmake_minimum_required(VERSION 3.16)
project(ftdcparser)

add_executable(${PROJECT_NAME}
        ExtractMetrics.cpp
        Configuration.cpp
        ../CSVWriter.cpp
        ../Dataset.cpp
        ../ParserTask.cpp
        ../Chunk.cpp
        ../FTDCParser.cpp
        ../ParserTasksList.cpp
        ../ConstDataRangeCursor.cpp
        ../ChunkMetric.cpp
        ../MergerTasksList.cpp
        ../MergerTask.cpp
        )

target_include_directories(${PROJECT_NAME}  PUBLIC
        ${Boost_INCLUDE_DIRS}
        "/usr/local/include/libbson-1.0"
        "${CMAKE_SOURCE_DIR}/src/parser"
        )

# Link libraries to the targets
target_link_libraries(${PROJECT_NAME} PUBLIC
        Threads::Threads
        Boost::program_options
        Boost::log
        mongo::bson_shared
        z
        yaml-cpp
        ${CMAKE_DL_LIBS})
