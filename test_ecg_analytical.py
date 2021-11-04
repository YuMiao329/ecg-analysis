import pytest

import pytest_t1
import pytest_t10
import pytest_t11
import pytest_t2
import pytest_t20
import pytest_t23
import pytest_t28
import pytest_t3
import pytest_t31
import pytest_t32
import pytest_t7
from ecg_analytical import heartpy_exec, create_dictionary


@pytest.mark.parametrize("input, expected", [
    ('test_data1.csv', (pytest_t1.new_time, pytest_t1.new_voltage, pytest_t1.filename)),
    ('test_data2.csv', (pytest_t2.new_time, pytest_t2.new_voltage, pytest_t2.filename)),
    ('test_data3.csv', (pytest_t3.new_time, pytest_t3.new_voltage, pytest_t3.filename))
])
def test_load_data(input, expected):
    from ecg_analytical import load_data
    answer = load_data(input)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected", [
    (pytest_t1.new_time, pytest_t1.new_voltage, False),
    (pytest_t2.new_time, pytest_t2.new_voltage, False),
    (pytest_t11.new_time, pytest_t11.new_voltage, True)
])
def test_bad_data_detection(input1, input2, expected):
    from ecg_analytical import bad_data_detection
    answer = bad_data_detection(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected", [
    (pytest_t1.new_time, pytest_t1.new_voltage, False),
    (pytest_t2.new_time, pytest_t2.new_voltage, False),
    (pytest_t20.new_time, pytest_t20.new_voltage, True),
    (pytest_t28.new_time, pytest_t28.new_voltage, True),
    (pytest_t31.new_time, pytest_t31.new_voltage, True)
])
def test_missing_data_detection(input1, input2, expected):
    from ecg_analytical import missing_data_detection
    answer = missing_data_detection(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected", [
    (pytest_t1.new_voltage, pytest_t1.filename, False),
    (pytest_t2.new_voltage, pytest_t2.filename, False),
    (pytest_t32.new_voltage, pytest_t32.filename, True)
])
def test_voltage_exceeded_detection(input1, input2, expected):
    from ecg_analytical import voltage_exceeded_detection
    answer = voltage_exceeded_detection(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, input3, expected", [
    (pytest_t1.new_time, pytest_t1.new_voltage, pytest_t1.filename, True),
    (pytest_t2.new_time, pytest_t2.new_voltage, pytest_t2.filename, True),
    (pytest_t32.new_time, pytest_t32.new_voltage, pytest_t32.filename, True)
])
def test_heartpy_exec(input1, input2, input3, expected):
    from ecg_analytical import heartpy_exec
    answer = heartpy_exec(input1, input2, input3)[2]
    assert answer == expected


@pytest.mark.parametrize("input1, input2, input3, input4, input5, expected", [
    (pytest_t7.new_time, pytest_t7.new_voltage,
     heartpy_exec(pytest_t7.new_time, pytest_t7.new_voltage, pytest_t7.filename)[0],
     heartpy_exec(pytest_t7.new_time, pytest_t7.new_voltage, pytest_t7.filename)[1],
     pytest_t7.filename,
     {'duration': 27.775,
      'voltage_extremes': (-1.05, 2.2),
      'num_beats': 31,
      'mean_hr_bpm': 68.8044170736887,
      'beats': [0.975, 2.014, 3.017, 4.022, 5.083, 6.106, 7.142, 8.108, 8.983,
                9.919, 10.919, 11.894, 12.814, 13.742, 14.597, 15.439, 16.286,
                17.153, 17.978, 18.769, 19.569, 20.378, 21.153, 21.936, 22.731,
                23.542, 24.328, 25.069, 25.756, 26.436, 27.136]}),
    (pytest_t10.new_time, pytest_t10.new_voltage,
     heartpy_exec(pytest_t10.new_time, pytest_t10.new_voltage, pytest_t10.filename)[0],
     heartpy_exec(pytest_t10.new_time, pytest_t10.new_voltage, pytest_t10.filename)[1],
     pytest_t10.filename, {'duration': 27.775,
                           'voltage_extremes': (-1.58, 1.555),
                           'num_beats': 44,
                           'mean_hr_bpm': 94.8238897396631,
                           'beats': [0.297, 0.944, 1.578, 2.236, 2.9,
                                     3.567, 4.219, 4.897, 5.536,
                                     6.153, 6.758, 7.381, 8.0, 8.65, 9.303,
                                     9.95, 10.583, 11.217,
                                     11.842, 12.436, 13.019, 13.631,
                                     14.242, 14.881, 15.525, 16.161,
                                     16.794, 17.389, 18.0, 18.597, 19.214,
                                     19.814, 20.433, 21.064,
                                     21.728, 22.406, 23.031, 23.642,
                                     24.267, 24.917, 25.544, 26.175,
                                     26.831, 27.506]}),
    (pytest_t23.new_time, pytest_t23.new_voltage,
     heartpy_exec(pytest_t23.new_time, pytest_t23.new_voltage, pytest_t23.filename)[0],
     heartpy_exec(pytest_t23.new_time, pytest_t23.new_voltage, pytest_t23.filename)[1],
     pytest_t23.filename, {'duration': 39.996,
                           'voltage_extremes': (-3.34, 3.81),
                           'num_beats': 75,
                           'mean_hr_bpm': 111.9628807746621,
                           'beats': [0.308, 0.976, 1.508, 2.044, 2.476,
                                     2.984, 3.524, 4.076, 4.592,
                                     5.256, 5.788, 6.236, 6.744, 7.276,
                                     7.808, 8.36, 8.892, 9.424,
                                     9.952, 10.476, 11.024, 11.556, 12.096,
                                     12.616, 13.136, 13.676,
                                     14.232, 14.76, 15.408, 15.832, 16.36,
                                     16.896, 17.44, 17.976,
                                     18.612, 19.036, 19.564, 20.116, 20.64,
                                     21.176, 21.716, 22.26,
                                     22.792, 23.324, 23.864, 24.4, 25.028,
                                     25.456, 25.992, 26.524,
                                     27.076, 27.616, 28.148, 28.688, 29.34,
                                     29.88, 30.292, 30.852,
                                     31.368, 31.908, 32.456, 32.992,
                                     33.532, 34.072, 34.624, 35.156,
                                     35.68, 36.24, 36.752, 37.388, 37.92,
                                     38.356, 38.892, 39.424, 39.964]})
])
def test_create_dictionary(input1, input2, input3, input4, input5, expected):
    from ecg_analytical import create_dictionary
    answer = create_dictionary(input1, input2, input3, input4, input5)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected", [
    (pytest_t7.filename, create_dictionary(pytest_t7.new_time, pytest_t7.new_voltage,
                                           heartpy_exec(pytest_t7.new_time, pytest_t7.new_voltage, pytest_t7.filename)[
                                               0],
                                           heartpy_exec(pytest_t7.new_time, pytest_t7.new_voltage, pytest_t7.filename)[
                                               1],
                                           pytest_t7.filename), True),
    (pytest_t10.filename, create_dictionary(pytest_t10.new_time, pytest_t10.new_voltage,
                                            heartpy_exec(pytest_t10.new_time, pytest_t10.new_voltage,
                                                         pytest_t10.filename)[0],
                                            heartpy_exec(pytest_t10.new_time, pytest_t10.new_voltage,
                                                         pytest_t10.filename)[1],
                                            pytest_t10.filename), True),
    (pytest_t23.filename, create_dictionary(pytest_t23.new_time, pytest_t23.new_voltage,
                                            heartpy_exec(pytest_t23.new_time, pytest_t23.new_voltage,
                                                         pytest_t23.filename)[0],
                                            heartpy_exec(pytest_t23.new_time, pytest_t23.new_voltage,
                                                         pytest_t23.filename)[1],
                                            pytest_t23.filename), True)
])
def test_dump_into_json(input1, input2, expected):
    from ecg_analytical import dump_into_json
    answer = dump_into_json(input1, input2)
    assert answer == expected
