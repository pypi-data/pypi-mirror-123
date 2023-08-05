//
// Created by jorge on 12/16/20.
//
#include "include/Dataset.h"
#include "MergerTask.h"
#include "MergerTasksList.h"
#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/thread.hpp>

namespace logging = boost::log;

size_t
Dataset::getMetricNames(std::vector<std::string> & metrics) {
    if (chunkVector.size() > 0) {
        chunkVector[0]->getMetricNames(metrics);
        return metrics.size();
    }
    else {
        metrics = metricNames;
        return metricNames.size();
    }
}

void
Dataset::addChunk(Chunk *pChunk) {

    // Critical section
    mu.lock();
    this->chunkVector.emplace_back(pChunk);

    // total size of samplesInDataset
    samplesInDataset += pChunk->getSamplesCount();

    // Append metrics here.
    mu.unlock();
}


void
Dataset::addMergedMetric(std::string   metricName,  Dataset::MetricsPtr data) {

    // Critical section
    mu.lock();
    hashMapMetrics.emplace( metricName, data);
    // Append metrics here.
    mu.unlock();
}

void
Dataset::sortChunks() {
    struct {
        bool operator()(Chunk *a, Chunk *b) const { return a->getId() < b->getId(); }
    } compare;
    std::sort(chunkVector.begin(), chunkVector.end(), compare);
}

Dataset::MetricsPtr
Dataset::getMetric(std::string   metricName)
{
    auto v = hashMapMetrics[metricName];

    if (!v) {
        uint64_t *data;
        if (chunkVector.size() > 0) {
            data = new uint64_t [samplesInDataset];

            // fill them now
            uint64_t *p = data;
            for (auto &m: chunkVector) {
                m->getMetric(metricName, p);
                p += m->getSamplesCount();
            }
            v = new Dataset::Metrics ();
            v->insert(v->begin(), data, data+samplesInDataset);
            addMergedMetric( metricName, v);
            delete [] data;
        }
    }
    return v;
}


void Dataset::FileParsed() {

    int metricsNameLen = 0;
    for (auto chunk : chunkVector) {

        auto currMetricLen = chunk->getMetricsCount();
        if (metricsNameLen != 0  && metricsNameLen!=currMetricLen) {
            BOOST_LOG_TRIVIAL(debug) << "Number of metrics differ from chunk to chunk:" << metricsNameLen << "!= " << currMetricLen;
        }

        if (metricsNameLen!=currMetricLen) {
            metricNames.clear();
            chunk->getMetricNames(metricNames);
            metricsNameLen = currMetricLen;
        }
    }
}

