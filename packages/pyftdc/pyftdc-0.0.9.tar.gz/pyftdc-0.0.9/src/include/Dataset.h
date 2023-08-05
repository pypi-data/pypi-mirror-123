//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <boost/thread/mutex.hpp>
#include "Chunk.h"
#include "MergerTasksList.h"

class Dataset {

public:
    typedef std::vector<uint64_t> Metrics;
    typedef std::vector<uint64_t>* MetricsPtr;

    Dataset() : samplesInDataset(0),  metricNames(0) {};

    void addChunk(Chunk *pChunk);
    size_t getChunkCount() { return chunkVector.size(); }
    Chunk *getChunk(size_t n) { return (n < chunkVector.size()) ? chunkVector[n] : nullptr; }
    std::vector<Chunk *> getChunkVector() { return chunkVector; }
    size_t getMetricNames(std::vector< std::string> & metricNames);
    [[nodiscard]] size_t getMetricLength() const { return samplesInDataset; }

    MetricsPtr getMetric(std::string   metricName);

    std::map<std::string, MetricsPtr> getHashMetrics() { return hashMapMetrics; }
    size_t getMetricNamesCount() { return metricNames.size(); }
    void sortChunks();
    void FileParsed();
    void   addMergedMetric(std::string   metricName, MetricsPtr data );


private:
    void releaseChunks();

private:
    std::vector<Chunk*> chunkVector;
    size_t samplesInDataset;
    boost::mutex mu;
    std::vector<std::string> metricNames;
    std::map<std::string,  MetricsPtr>  hashMapMetrics;
};


#endif //FTDCPARSER_DATASET_H
