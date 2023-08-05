//
// Created by jorge on 12/25/20.
//

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN  // in only one cpp file

#define BOOST_TEST_MODULE ftdc_basic_suite

#include <boost/test/unit_test.hpp>
#include <boost/format.hpp>

#include <fstream>
#include <FTDCParser.h>
#include <Chunk.h>
#include <iostream>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/thread.hpp>

#include <filesystem>

static const char *DATA_TEST_FILE_NAME = "../../../tests_cpp_tests/metrics.data";
static const char *CSV__TEST_FILE_NAME = "../../../tests_cpp_tests/first.csv";


static const char *DATA_TEST_FILE_NAME2 = "../../../tests/diagnostic.data_40/metrics.2021-07-17T22-36-31Z-00000";
static const char *DATA_TEST_DIR = "../../../tests/diagnostic.data_40/";


int ParserTaskConsumerThread(ParserTasksList *parserTasks, Dataset *dataSet);

std::vector<ChunkMetric *>
readMetricsFromCSV() {

    std::vector<ChunkMetric *> metrics;
    metrics.reserve(1500);

    //
    std::ifstream f;
    f.open(CSV__TEST_FILE_NAME, std::ios::in);
    std::string line;
    while (getline(f, line)) { //read data from file object and put it into string.

        std::stringstream ss(line);
        std::string token;
        ChunkMetric *pM = nullptr;
        int field = 0;
        do {
            std::getline(ss, token, ':');

            if (!pM) {
                pM = new ChunkMetric(token, BSON_TYPE_INT64, 0);
            } else {
                pM->values[field++] = atol(token.c_str());
            }

        } while (field < 300);
        metrics.emplace_back(pM);
    }
    f.close();

    return metrics;
}


BOOST_AUTO_TEST_SUITE(ftdc_basic_suite)


    BOOST_AUTO_TEST_CASE(OpenFile) {

        // Create parser
        auto *parser = new FTDCParser();

        auto file_path = std::filesystem::current_path();
        file_path.append(DATA_TEST_FILE_NAME);
        BOOST_TEST_MESSAGE(file_path);

        auto reader = parser->open(file_path);
        BOOST_CHECK_NE(reader, nullptr);

        bson_reader_destroy(reader);

        delete parser;
    }

    BOOST_AUTO_TEST_CASE(ReadInfoChunk) {

        // Create parser
        auto *parser = new FTDCParser();

        auto file_path = std::filesystem::current_path();
        file_path.append(DATA_TEST_FILE_NAME);
        BOOST_TEST_MESSAGE(file_path);
        auto reader = parser->open(file_path);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        bson_reader_destroy(reader);
        delete parser;
        BOOST_CHECK_EQUAL(1, 1);
    }

    BOOST_AUTO_TEST_CASE(ReadDataChunk) {

        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break; // <-- only one!

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);
        BOOST_CHECK(pChunk);

        bson_reader_destroy(reader);

        delete parser;
        BOOST_CHECK_EQUAL(1, 1);
    }

    BOOST_AUTO_TEST_CASE(checkMetricNames) {

        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        // - - - - - - - - - -
        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break;

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);

        BOOST_CHECK(pChunk);

        auto decomp_result = pChunk->Decompress();
        auto data = pChunk->getUncompressedData();
        BOOST_CHECK(data);
        auto dataSize = pChunk->getUncompressedSize();
        BOOST_CHECK(dataSize);

        // We construct the metrics. This are name and first value only since deltas have not been read.
        int metrics = pChunk->ConstructMetrics(data);
        BOOST_CHECK_EQUAL(metrics, pChunk->getMetricsCount());

        // Get names
        std::vector<std::string> metricsNames;
        pChunk->getMetricNames(metricsNames);

        // Compare first 1000 names
        for (int m = 0; m < 1000; ++m) {

            auto pMetric = pChunk->getMetric(m);
            BOOST_CHECK(pMetric);

            BOOST_CHECK_EQUAL(pMetric->name, metricsNames[m]);
        }

        //
        bson_reader_destroy(reader);

        delete parser;
    }


    BOOST_AUTO_TEST_CASE(compareMetrics_1) {
        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);


        parser->parseInfoChunk(pBsonChunk);

        // - - - - - - - - - -
        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break;

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);
        BOOST_CHECK(pChunk);

        auto data = pChunk->getUncompressedData();
        BOOST_CHECK(data);
        auto dataSize = pChunk->getUncompressedSize();
        BOOST_CHECK(dataSize);

        // We construct the metrics. This are name and first value only since deltas have not been read.
        int metrics = pChunk->ConstructMetrics(data);
        BOOST_CHECK_EQUAL(metrics, pChunk->getMetricsCount());

        auto readMetrics = readMetricsFromCSV();
        // Get names
        pChunk->ReadVariableSizedInts();

        int brokenMetrics = 0;
        for (int i = 0; i < readMetrics.size(); ++i) {
            auto pMetric = pChunk->getMetric(i);
            auto pMetricsFromCSV = readMetrics[i];

            // compare
            BOOST_TEST_MESSAGE(pMetric->name);

            for (int j = 0; j < 300; ++j) {

                if (pMetric->values[j] != pMetricsFromCSV->values[j]) {

                    uint64_t diff = pMetric->values[j] - pMetricsFromCSV->values[j];

                    auto errs = str(
                            boost::format("ChunkMetric %1% %2% diverges index %3%  abs(%4%)  Is %5%  should be %6%")
                            % pMetric->name.c_str() % i % j % std::abs((long) (diff)) % pMetric->values[j] %
                            pMetricsFromCSV->values[j]);

                    ++brokenMetrics;
                    BOOST_TEST_MESSAGE(errs);
                    break;
                }
            }
        }

        BOOST_CHECK_EQUAL(brokenMetrics, 0);
        //
        bson_reader_destroy(reader);
    }


    BOOST_AUTO_TEST_CASE(timestamp_dataset_monotony) {     // Are timestamps sequential?
        // Create parser
        auto parser = new FTDCParser();

        parser->keepChunkStructures(true);  // Do not release Chunks after parsing is done.

        std::vector<std::string> files;

        files.emplace_back(DATA_TEST_FILE_NAME);
        namespace logging = boost::log;

        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        auto status = parser->parseFiles(&files, false, false);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        BOOST_CHECK_EQUAL(status, 0);
        auto chunkVector = parser->getChunks();

        BOOST_CHECK_GT(chunkVector.size(), 1);

        for (int i = 1; i < chunkVector.size(); ++i) {
            auto prevChunkFinalTimestamp = chunkVector[i - 1]->getEnd() / 1000;
            auto thisChunkInitialTimestamp = chunkVector[i]->getStart() / 1000;

            if (prevChunkFinalTimestamp + 1 != thisChunkInitialTimestamp)
                BOOST_CHECK_EQUAL(prevChunkFinalTimestamp + 1, thisChunkInitialTimestamp);
        }
    }


    BOOST_AUTO_TEST_CASE(timestamp_dataset_dir_monotony) {     // Are timestamps sequential?
        // Create parser
        auto parser = new FTDCParser();


        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        namespace logging = boost::log;

        parser->keepChunkStructures(true);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
        auto status = parser->parseFiles(&fileList, false, false);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        BOOST_CHECK_EQUAL(status, 0);

        auto chunkVector = parser->getChunks();

        BOOST_CHECK_GT(chunkVector.size(), 1);

        for (int i = 1; i < chunkVector.size(); ++i) {
            auto prevChunkFinalTimestamp = chunkVector[i - 1]->getEnd() / 1000;
            auto thisChunkInitialTimestamp = chunkVector[i]->getStart() / 1000;

            if (prevChunkFinalTimestamp + 1 != thisChunkInitialTimestamp)
                BOOST_CHECK_EQUAL(prevChunkFinalTimestamp + 1, thisChunkInitialTimestamp);
        }
    }


    BOOST_AUTO_TEST_CASE(dataSetMonotony) {
        // Create parser
        auto parser = new FTDCParser();

        namespace logging = boost::log;

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
        auto status = parser->parseFiles(&fileList, false, false);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        BOOST_CHECK_EQUAL(status, 0);

        auto ts = parser->getMetric("start");
        auto end = parser->getMetric( "end");
        uint64_t prevTimestamp = (*ts)[0] / 1000;
        uint64_t thisTimestamp, endTimeStamp;
        for (int i = 1; i < ts->size(); ++i) {

            thisTimestamp = (*ts)[i] / 1000;
            endTimeStamp = ts->at(i);
            if (prevTimestamp + 1 != thisTimestamp)
                BOOST_CHECK_EQUAL(prevTimestamp + 1, thisTimestamp);

            prevTimestamp = thisTimestamp;
        }
        BOOST_CHECK_EQUAL(1, 1);


    }

    BOOST_AUTO_TEST_CASE(metrics) {     // Are there metrics here?
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> files;

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        namespace logging = boost::log;
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
        auto status = parser->parseFiles(&fileList, false, false);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        for (auto mn: metricNames) {
            BOOST_TEST_MESSAGE(mn);
        }
        BOOST_TEST_MESSAGE(msg);
    }

    BOOST_AUTO_TEST_CASE(matrix) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        namespace logging = boost::log;
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
        auto status = parser->parseFiles(&fileList, false, false);
        logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        auto ts = parser->getMetric("start");
        auto m1 = parser->getMetric(metricNames[1]);
        auto m2 = parser->getMetric(metricNames[3]);
        auto m3 = parser->getMetric(metricNames[5]);
        auto m4 = parser->getMetric(metricNames[7]);

        msg = str( boost::format("Timestamp has %1% elements\n%2%:%3%\n%4%:%5%\n%6%:%7%\n%8%:%9%\n") % ts->size() %
                metricNames[1] % m1->size() %
                metricNames[3] % m2->size() %
                metricNames[5] % m3->size() %
                metricNames[7] % m4->size() );
        BOOST_TEST_MESSAGE(msg);
    }


BOOST_AUTO_TEST_SUITE_END()

