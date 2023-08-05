#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <FTDCParser.h>
#include <vector>
#include <filesystem>
#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>

namespace py = pybind11;

typedef std::vector<uint64_t>* Metrics;
typedef std::vector<std::string> MetricNames;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

// helper function to avoid making a copy when returning a py::array_t
// author: https://github.com/YannickJadoul
// source: https://github.com/pybind/pybind11/issues/1042#issuecomment-642215028
template <typename Sequence>


inline py::array_t<typename Sequence::value_type>
as_pyarray(Sequence &&seq) {
    auto size = seq.size();
    auto data = seq.data();
    std::unique_ptr<Sequence> seq_ptr = std::make_unique<Sequence>(std::move(seq));
    auto capsule = py::capsule(seq_ptr.get(), [](void *p) { std::unique_ptr<Sequence>(reinterpret_cast<Sequence*>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}

inline py::array_t<uint64_t >
as_pyarray(Metrics m) {
    auto size = m->size();
    auto data = m->data();
    std::unique_ptr<Metrics> seq_ptr = std::make_unique<Metrics>(std::move(m));
    auto capsule = py::capsule(seq_ptr.get(),
                               [](void *p) { std::unique_ptr<Metrics>(reinterpret_cast<Metrics *>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}


struct ParserClass {
    FTDCParser *pParser;
    std::vector<std::string> metadata;
    std::vector<std::string> fileList;
    MetricNames metric_names;
    Metrics timestamps;
    uint64_t sample_count;


    explicit ParserClass() {
        pParser = new FTDCParser();
    };

    int parseFile(std::string file) {

        fileList.emplace_back(file);
        int n = pParser->parseFiles(&fileList, false, false);

        if (n == 0) {
            // Timestamps, metric names, and metadata as fields in python
            metric_names = pParser->getMetricsNames();
            metadata = pParser->getMetadata();
            timestamps = pParser->getMetric( "start");
            sample_count = pParser->getMetricLength();
        }
        return n;
    }
    int parseDir(std::string dir) {

        // if it exists an it is a directory, pop and push contents
        if (std::filesystem::exists(dir) && std::filesystem::is_directory(dir)) {

            for (auto&& fileInPath : std::filesystem::directory_iterator(dir))
                fileList.push_back(fileInPath.path().string());

            // Not really necessary.
            std::sort(fileList.begin(), fileList.end());
            int n = pParser->parseFiles(&fileList, false, false);

            if (n == 0) {
                // metric names and metadata as fields in python
                metric_names = pParser->getMetricsNames();
                metadata = pParser->getMetadata();
                timestamps = pParser->getMetric( "start");

                sample_count = pParser->getMetricLength();
            }
            return n;

        }
        return -1;
    }
    Metrics  get_timestamps() {
        return pParser->getMetric((std::string &) "start");
    }
    Metrics  getMetric(std::string metricName) {
        return pParser->getMetric(metricName);
    }
    uint64_t getMetricSampleCount() {
        return pParser->getMetricLength();
    }
    py::array_t<unsigned long>  getMetricAsNumpyArray(std::string metricName) {
        auto m = pParser->getMetric(metricName);
        return as_pyarray(m);
    }
    std::vector<py::array_t<unsigned long>> getMetricListAsNumpyArray(std::vector<std::string> metricNames) {
        std::vector<py::array_t<unsigned long>> metricList;

        for(auto name : metricNames) {
            auto element = as_pyarray( pParser->getMetric(name));
            metricList.emplace_back(element);
        }
        return metricList;
    }

    py::array_t<uint64_t>  getMetricListAsNumpyMatrix(std::vector<std::string> metricNames, bool transposed=Py_False) {

        if (transposed) {
            py::array_t<uint64_t, py::array::f_style> a;
            a.resize({(int) metricNames.size(), (int) pParser->getMetricLength()});
            auto r = a.mutable_unchecked();
            for (py::ssize_t i = 0; i < r.shape(0); i++) {
                auto element = pParser->getMetric(metricNames[i]);
                for (py::ssize_t j = 0; j < r.shape(1); j++)
                    r(i, j) = element->at(j);
            }
            return a;
        }
        else {
            py::array_t<uint64_t, py::array::c_style> a;

            a.resize({(int) metricNames.size(), (int) pParser->getMetricLength()});
            auto r = a.mutable_unchecked();
            for (py::ssize_t i = 0; i < r.shape(0); i++) {
                auto element = pParser->getMetric(metricNames[i]);
                for (py::ssize_t j = 0; j < r.shape(1); j++)
                    r(i, j) = element->at(j);
            }
            return a;
        }

    }

    py::array_t<uint64_t> miau(std::vector<std::string> metricNames) {
        py::array_t<uint64_t , py::array::c_style> a;
        a.resize({(int)metricNames.size(), (int)pParser->getMetricLength()});

        auto  dims = a.ndim();
        printf("Dimensions %ld\n", dims);

        auto r = a.mutable_unchecked();
        printf("Shapes %ld, %ld\n", r.shape(0), r.shape(1));
        for (py::ssize_t i=0; i<r.shape(0); i++) {
            auto element = pParser->getMetric(metricNames[i]);
            for (py::ssize_t j=0; j<r.shape(1); j++) {
                r(i,j) = element->at(j);
            }
        }
        return a;
    }
};



PYBIND11_MODULE(_core, m) {
    //try { py::module_::import("numpy"); }
    //catch (...) { return; }

    m.doc() = R"pbdoc(
        MongoDB FTDC files parser library.
        -----------------------

        .. currentmodule:: pyftdc

        .. autosummary::
           :toctree: _generate

           parse_dir
           parse_file
           get_metric
           get_timestamps
           get_metric_sample_count
           get_metric_names
           timestamps
           metadata
           get_metric_numpy
           get_metrics_list_numpy
           get_metrics_list_numpy_matrix
    )pbdoc";


  py::class_<ParserClass>(m, "FTDCParser")
        .def(py::init<>())
        //.def("__repr__",   [](const ParserClass &p) {return "<Parser class object>." ;})
        .def("parse_dir", &ParserClass::parseDir)
        .def("parse_file", &ParserClass::parseFile)
        .def("get_metric", &ParserClass::getMetric)
        .def("get_timestamps", &ParserClass::get_timestamps)
        .def("get_metric_sample_count", &ParserClass::getMetricSampleCount)
        .def_readonly("metric_names", &ParserClass::metric_names)
        .def_readonly("metadata", &ParserClass::metadata)
        .def_readonly("timestamps", &ParserClass::timestamps)
        .def_readonly("sample_count", &ParserClass::sample_count)
        .def("get_metric_numpy", &ParserClass::getMetricAsNumpyArray)
        .def("get_metrics_list_numpy", &ParserClass::getMetricListAsNumpyArray)
        .def("get_metrics_list_numpy_matrix", &ParserClass::getMetricListAsNumpyMatrix)
        ;



#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
} // PYBIND11_MODULE
