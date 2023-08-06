/*****************************************************************************
 * Copyright 2020,2021 Reid Swanson
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*****************************************************************************/


#include <algorithm>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Eigen/Core>

#include <Python.h>

#include "gmix2/gmix.hpp"

namespace py = pybind11;

using namespace pybind11::literals;

//-- region Utility Functions ---------------------------------------------------------------------------------------//
template <typename Float>
Eigen::Map<gmix::Array<Float>>
ndarray_to_array(const py::array_t<Float>& array) {
    // Assume it's 1D
    return Eigen::Map<gmix::Array<Float>>(const_cast<Float*>(array.data()), 1, array.shape(0));
}

template <typename Float>
gmix::Array<Float>
list_to_array(const py::list& list) {
    // Assume it's 1D
    const int size = py::len(list);

    gmix::Array<Float> array(size);
    for (int i = 0; i < size; ++i) {
        array(i) = list[i].cast<Float>();
    }
    return array;
}

template <typename Float>
Eigen::Map<gmix::Matrix<Float>>
ndarray_to_matrix(const py::array_t<Float>& array) {
    const int n_rows = array.shape(0), n_cols = array.shape(1);

    return Eigen::Map<gmix::Matrix<Float>>(const_cast<Float*>(array.data()), n_rows, n_cols);
}

template <typename Float>
py::array_t<Float>
matrix_to_array(const gmix::Matrix<Float> &matrix) {
    // Unfortunately, I don't think there's a way around copying the data for the return result;
    const Float * const data = matrix.data();
    // py::array_t<Float> result = py::zeros(py::make_tuple(matrix.rows(), matrix.cols()), py::dtype::get_builtin<double>());
    py::array_t<Float> result({matrix.rows(), matrix.cols()});
    std::copy(data, data + matrix.size(), const_cast<Float*>(result.data()));

    return result;
}

template <typename Float>
py::list
mode_vector_to_list(const gmix::ModeVector<Float>& modes) {
    py::list result;
    for (int i = 0; i < modes.size(); ++i) {
        // For each mixture
        py::list mixture_result;
        for (int j = 0; j < modes[i].size(); ++j) {
            // For each mode in the mixture
            const auto& tuple = modes[i][j];
            mixture_result.append(py::make_tuple(std::get<0>(tuple), std::get<1>(tuple)));
        }
        result.append(std::move(mixture_result));
    }

    return result;
}
//-- endregion Utility Functions ------------------------------------------------------------------------------------//

//-- region Wrapper Functions ---------------------------------------------------------------------------------------//
//-- region Normal Distribution -------------------------------------------------------------------------------------//
py::array_t<double>
normal_pdf(double x, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(normal::pdf<double>(x, m, s));
}
//-- endregion Normal Distribution ----------------------------------------------------------------------------------//

//-- region Mixture Distribution ------------------------------------------------------------------------------------//
/**
 *
 * @param x
 * @param weight
 * @param mean
 * @param std
 * @return
 */
py::array_t<double>
pdf(double x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    //return matrix_to_array(gmix::pdf<double>(x, w, m, s)).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::pdf<double>(x, w, m, s));
    array.resize({array.size()});

    return array;
}

const char *pdf_docstring = "The `probability density function <https://en.wikipedia.org/wiki/Probability_density_function>`_ at x.\n\n"
                            "**x** (float, list of floats or 1d-ndarray): The point or points where the PDF will be evaluated.\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**returns** (1d or 2d-ndarray): For scalar values of ``x`` this returns a 1d array of values containing the PDF of ``x`` for each mixture. "
                            "When ``x`` is a list or array of values then a 2d-array is returned. "
                            "Each row corresponds to a mixture and each column contains the PDF for the corresponding ``x`` value";


py::array_t<double>
pdf_multi_array(const py::array_t<double>& x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& i = ndarray_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::pdf<double>(i, w, m, s));
}

py::array_t<double>
pdf_multi_list(const py::list& x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& i = list_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::pdf<double>(i, w, m, s));
}

/**
 *
 * @param x
 * @param weight
 * @param mean
 * @param std
 * @return
 */
py::array_t<double>
cdf(double x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    // return matrix_to_array(gmix::cdf<double>(x, w, m, s)).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::cdf<double>(x, w, m, s));
    array.resize({array.size()});

    return array;
}

const char *cdf_docstring = "The `cumulative distribution function <https://en.wikipedia.org/wiki/Cumulative_distribution_function>`_ at x.\n\n"
                            "**x** (float, list of floats or 1d-ndarray): The point or points where the CDF will be evaluated.\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**returns** (1 or 2d-ndarray): Returns the CDF value(s) for the input ``x`` in the same way as the :func:`.pdf`";

py::array_t<double>
cdf_multi_array(const py::array_t<double>& x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& i = ndarray_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::cdf<double>(i, w, m, s));
}

py::array_t<double>
cdf_multi_list(const py::list& x, const py::array_t<double>& weight, const py::array_t<double>& mean, const py::array_t<double>& std) {
    const auto& i = list_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::cdf<double>(i, w, m, s));
}

/**
 *
 * @param p
 * @param weight
 * @param mean
 * @param std
 * @param lower_bound
 * @param upper_bound
 * @param tol
 * @param max_itr
 * @return
 */
py::array_t<double>
ppf(
    double p,
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

//    return matrix_to_array(
//        gmix::ppf<double>(p, w, m, s, lower_bound, upper_bound, tol, max_itr)
//    ).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::ppf<double>(p, w, m, s, lower_bound, upper_bound, tol, max_itr));
    array.resize({array.size()});

    return array;
}

const char *ppf_docstring = "The `percent point function <https://en.wikipedia.org/wiki/Quantile_function>`_ (aka quantile or inverse cumulative distribution function)_ for probability p. "
                            "This returns the value ``x`` such that its probability is less than or equal to ``p``. "
                            "There is no analytic solution to finding the ``ppf`` of a Gaussian mixture so a heuristic search is performed following the recipe in this `Stack Exchange solution <https://stats.stackexchange.com/a/14484>`_.\n\n"
                            "**p** (float, list of floats or 1d-ndarray): The desired probability of the resulting x value(s).\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**lower_bound** (float): The lower bound of the search.\n\n"
                            "**upper_bound** (float): The upper bound of the search.\n\n"
                            "**tol** (float): The accepted tolerance.\n\n"
                            "**max_itr** (int): The maximum number of iterations before giving up.\n\n"
                            "**returns** (1 or 2d-ndarray): Returns the PPF value(s) for the input ``p`` in the same way as the :func:`.pdf`";

py::array_t<double>
ppf_multi_array(
    const py::array_t<double>& p,
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& i = ndarray_to_array<double>(p);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::ppf<double>(i, w, m, s, lower_bound, upper_bound, tol, max_itr));
}

py::array_t<double>
ppf_multi_list(
    const py::list& p,
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& i = list_to_array<double>(p);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::ppf<double>(i, w, m, s, lower_bound, upper_bound, tol, max_itr));
}

py::array_t<double>
mean(const py::array_t<double>& weight, const py::array_t<double>& mean) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);

    // return matrix_to_array(gmix::mean<double>(w, m)).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::mean<double>(w, m));
    array.resize({array.size()});

    return array;
}

const char *mean_docstring = "The mean <https://en.wikipedia.org/wiki/Mean>`_ value of the distribution(s).\n\n"
                             "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                             "Each row is a separate distribution. Each column is a weight for that distribution. "
                             "The weights in a row should sum to 1.0.\n\n"
                             "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                             "**returns** (1d-ndarray): The mean value for each mixture";


py::array_t<double>
median(
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const double lower_bound = 1e-4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

//    return matrix_to_array(
//        gmix::median<double>(w, m, s, lower_bound, upper_bound, tol, max_itr)
//    ).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::median<double>(w, m, s, lower_bound, upper_bound, tol, max_itr));
    array.resize({array.size()});

    return array;
}

const char *median_docstring = "The `median <https://en.wikipedia.org/wiki/Median>`_ value of the distribution. "
                               "This is simply a shortcut for calling :func:`ppf` with a ``p=1.0``.\n\n"
                               "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                               "Each row is a separate distribution. Each column is a weight for that distribution. "
                               "The weights in a row should sum to 1.0.\n\n"
                               "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                               "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                               "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                               "**returns** (1d-ndarray): The median value for each mixture";



py::list
mode(
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const int max_itr = 1000,
    const double min_diff = 1e-4,
    const double min_grad = 1e-9
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return mode_vector_to_list(gmix::mode<double>(w, m, s, max_itr, min_diff, min_grad));
}

const char *mode_docstring = "The `mode(s) <https://en.wikipedia.org/wiki/Mode_(statistics)>`_ of the distribution. "
                             "This method uses a slightly simplified version of the approach described in `this paper <http://faculty.ucmerced.edu/mcarreira-perpinan/papers/cs-99-03.pdf>`_.\n\n"
                             "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                             "Each row is a separate distribution. Each column is a weight for that distribution. "
                             "The weights in a row should sum to 1.0.\n\n"
                             "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                             "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                             "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                             "**max_itr** (int): The maximum number of iterations before terminating regardless of convergence.\n\n"
                             "**min_diff** (float): Only keep modes whose values are at least ``min_diff`` apart.\n\n"
                             "**min_grad** (float): Stop iterating when the magnitude of the gradient falls below this value.\n\n"
                             "**returns** (a 2d list of tuples): For each mixture this returns a list of tuples. "
                             "The first value of each tuple is the ``x`` value of the mode and the second value is its density.";

py::array_t<double>
variance(
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    //return matrix_to_array(gmix::variance<double>(w, m, s)).reshape(py::make_tuple(-1));
    auto array = matrix_to_array(gmix::variance<double>(w, m, s));
    array.resize({array.size()});

    return array;
}

const char *variance_docstring = "The `variance <https://en.wikipedia.org/wiki/Variance>`_ of the distribution. "
                                 "`This StackExchange answer <https://stats.stackexchange.com/a/16609>` gives a concise derivation of the variance for a Gaussian mixture.\n\n"
                                 "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                                 "Each row is a separate distribution. Each column is a weight for that distribution. "
                                 "The weights in a row should sum to 1.0.\n\n"
                                 "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                                 "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                                 "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                                 "**returns** (1d-ndarray): The variance for each mixture.";

// Boost Python does not like the name random for some reason and will fail to build
// if the function has that name.
py::array_t<double>
gmix_random(
    size_t n,
    const py::array_t<double>& weight,
    const py::array_t<double>& mean,
    const py::array_t<double>& std,
    const int seed = -1
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::random<double>(n, w, m, s, seed));
}

const char *random_docstring = "Generate `random <https://en.wikipedia.org/wiki/Inverse_transform_sampling>`_ values from the distribution using inverse transform sampling.\n\n"
                               "**n** (int): The number of random values to generate for each mixture.\n\n"
                               "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                               "Each row is a separate distribution. Each column is a weight for that distribution. "
                               "The weights in a row should sum to 1.0.\n\n"
                               "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                               "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                               "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                               "**seed** (int): The seed to use if you would like reproducible random values.\n\n"
                               "**returns** (2d-ndarray): For each mixture (the rows) this returns ``n`` random values (the columns) drawn from that mixture.";
//-- endregion Mixture Distribution ---------------------------------------------------------------------------------//
//-- endregion Wrapper Functions ------------------------------------------------------------------------------------//

//BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_overloads, ppf, 4, 8)
//BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_array_overloads, ppf_multi_array, 4, 8)
//BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_list_overloads, ppf_multi_list, 4, 8)
//BOOST_PYTHON_FUNCTION_OVERLOADS(median_overloads, median, 3, 7)
//BOOST_PYTHON_FUNCTION_OVERLOADS(mode_overloads, mode, 3, 6)
//BOOST_PYTHON_FUNCTION_OVERLOADS(rand_overloads, gmix_random, 4, 5)

PYBIND11_MODULE(cgmix2, m) {
    // NOTE: It is imperative that all numpy arrays created in gmix2
    // are in the default storage order ('C' / Row Major)
    Py_Initialize();
//    py::initialize();

    // py::docstring_options doc_options(true, true, false);
    m.doc() = "All the functions listed and documented below in the ``cgmix2`` module are actually made available "
              "in python by importing the ``gmix2`` module. I apologize for this confusion which is probably "
              "arising due to a misunderstanding of how to structure and name C++ extensions";

    m.def("normal_pdf", normal_pdf);
    m.def("pdf", &pdf, pdf_docstring, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def("pdf", &pdf_multi_array, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def("pdf", &pdf_multi_list, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def("cdf", &cdf, cdf_docstring, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def("cdf", &cdf_multi_array, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def("cdf", &cdf_multi_list, "x"_a, "weights"_a, "means"_a, "stddevs"_a);
    m.def(
        "ppf",
        &ppf,
        ppf_docstring,
        "p"_a,
        "weight"_a,
        "mean"_a,
        "std"_a,
        "lower_bound"_a = -1e4,
        "upper_bound"_a = 1e4,
        "tol"_a = 1e-12,
        "max_itr"_a = 100
        );
    m.def(
        "ppf",
        &ppf_multi_array,
        "p"_a,
        "weight"_a,
        "mean"_a,
        "std"_a,
        "lower_bound"_a = -1e4,
        "upper_bound"_a = 1e4,
        "tol"_a = 1e-12,
        "max_itr"_a = 100
    );
    m.def(
        "ppf",
        &ppf_multi_list,
        "p"_a,
        "weight"_a,
        "mean"_a,
        "std"_a,
        "lower_bound"_a = -1e4,
        "upper_bound"_a = 1e4,
        "tol"_a = 1e-12,
        "max_itr"_a = 100
    );
    m.def("mean", &mean, mean_docstring, "weights"_a, "means"_a);
    m.def(
        "median",
        &median,
        median_docstring,
        "weights"_a,
        "means"_a,
        "std"_a,
        "lower_bound"_a = -1e4,
        "upper_bound"_a = 1e4,
        "tol"_a = 1e-12,
        "max_itr"_a = 100
    );
    m.def(
        "mode",
        &mode,
        mode_docstring,
        "weight"_a,
        "mean"_a,
        "std"_a,
        "max_itr"_a = 1000,
        "min_diff"_a = 1e-4,
        "min_grad"_a = 1e-9
    );
    m.def("variance", &variance, variance_docstring, "weights"_a, "means"_a, "stddevs"_a);
    m.def("random", &gmix_random, random_docstring, "n"_a, "weight"_a, "mean"_a, "std"_a, "seed"_a = 1);
}
