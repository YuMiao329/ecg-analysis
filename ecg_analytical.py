import json
import math
import logging
import heartpy as hp
import pandas as pd
import warnings


def load_data(fileopen):
    """Load the data from csv files

    Load csv data from test_data files and will be transformed from
    pandas form into python general list of variables

    :param fileopen: string of file name in test_data file
    :returns:
        - new_time - time array of data
        - new_voltage - voltage array of data
        - filename - string of file name
    """
    # fileopen = 'test_data1.csv'
    filepath = 'test_data/' + fileopen
    filename = fileopen.split('.')[0]
    diagnose_name = filename + '_diagnose'
    logging.basicConfig(filename=diagnose_name + '.log', level=logging.INFO)
    df = pd.read_csv(filepath, header=None)
    voltage = df.iloc[:, 1]
    time = df.iloc[:, 0]
    new_voltage = []
    new_time = []
    for i in voltage:
        new_voltage.append(i)
    for i in time:
        new_time.append(i)

    return new_time, new_voltage, filename


def bad_data_detection(new_time, new_voltage):
    """Detect if there is string type data inside of the list

    It will first test if there is any string type of data
    and will then change it to float type and throw exception.
    If it can not be changed, then test if is a "bad data".
    if yes for time, then increment a time step for it,
    if yes for voltage, then repeat voltage from last voltage.
    Lastly, cast string of number into float type.

    :param new_time: list of time of data
    :param new_voltage: list of voltage of data
    :returns:
        - bad_detected - test if the data has bad data
    """
    bad_detected = False
    for j in range(len(new_time)):

        try:
            new_time[j] = float(new_time[j])
        except ValueError:
            print("Non-numerical value of time detected"
                  ", and has been cleaned")
            bad_detected = True

        try:
            new_voltage[j] = float(new_voltage[j])
        except ValueError:
            print("Non-numerical value of voltage detected"
                  ", and has been cleaned")
            bad_detected = True

        if new_time[j] == "bad data":
            new_time[j] = new_time[j - 1] + new_time[1]
            logging.error('Bad data detected at line {} of time'.format(j + 1))
        new_time[j] = float(new_time[j])

        if new_voltage[j] == "bad data":
            new_voltage[j] = new_voltage[j - 1]
            logging.error('Bad data detected at line {} of voltage'
                          .format(j + 1))
        new_voltage[j] = float(new_voltage[j])
    return bad_detected


def missing_data_detection(new_time, new_voltage):
    """Detect if there is missing data inside of the list

    If there is missing data in time or voltage, it will
    repeat data from the last data point.

    :param new_time: list of time of data
    :param new_voltage: list of voltage of data
    :returns:
        - miss_detected - test if the data has missing data
    """
    miss_detected = False
    for j in range(len(new_time)):
        if math.isnan(new_time[j]):
            new_time[j] = new_time[j - 1]
            logging.error('Miss data detected at line {} of time'
                          .format(j + 1))
            miss_detected = True
        new_time[j] = float(new_time[j])

        if math.isnan(new_voltage[j]):
            new_voltage[j] = new_voltage[j - 1]
            logging.error('Miss data detected at line {} of voltage'
                          .format(j + 1))
            miss_detected = True
        new_voltage[j] = float(new_voltage[j])
    return miss_detected


def voltage_exceeded_detection(new_voltage, fileopen):
    """Detect if there is a voltage >300mV or <-300mV

    If there is a/several voltage data point(s) >300mV or <-300mV,
    it will generate only one warning message in the log file.

    :param new_voltage: list of voltage of data
    :param fileopen: name of the file being read
    :returns:
        - exceed_boo - test if the data has exceeding voltage
    """
    vol_high_where = 0
    exceed_boo = False
    for j in range(len(new_voltage)):
        if new_voltage[j] >= 300 or new_voltage[j] <= -300:
            vol_high_where, exceed_boo = j, True
            break
    if exceed_boo:
        logging.warning(
            'Voltage is exceeding normal range at line {}, in the file {}'
            .format((vol_high_where + 1), fileopen))
    return exceed_boo


def heartpy_exec(new_time, new_voltage, filename):
    """Use external package heartpy to analyze the ECG data

    It will load heartpy package and auto examine the file
    and divide the file into parts into parameters working_data
    and measures.

    :param new_time: list of time of data
    :param new_voltage: list of voltage of data
    :param filename: name of the file being read

    :returns:
        - working_data - basic information of raw data before processing
        - measures - a dictionary of information of processed data
        - heartpy_pass - test if heartpy package is working or not
    """

    heartpy_pass = False
    try:
        logging.info("Start analyzing of ECG trace of file {}"
                     .format(filename))
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        fs = round(hp.get_samplerate_mstimer(new_time) / 1000)
        working_data, measures = hp.process(new_voltage, fs)
        heartpy_pass = True
        return working_data, measures, heartpy_pass
    except ValueError:
        print("Heartpy does not work for this data")


def create_dictionary(new_time, new_voltage, working_data, measures,
                      filename):
    """Create a fully analyzed dictionary of the ECG data

    It will load the processed data from measures and raw data from
    working_data and generate a dictionary listed as
    metrics = {'duration': duration,
               'voltage_extremes': voltage_extremes,
               'num_beats': num_beats,
               'mean_hr_bpm': mean_hr_bpm,
               'beats': beats}.

    :param new_time: list of time of data
    :param new_voltage: list of voltage of data
    :param working_data: basic information of raw data before processing
    :param measures: a dictionary of information of processed data
    :param filename: name of the file being read

    :returns:
        - metrics - a dictionary containing duration,
                    voltage extremes, number of beats, beats per minute,
                    and the time where beats occur
    """
    logging.info("Start calculation/assigning duration of"
                 " ECG trace of file {}".format(filename))
    duration = new_time[len(new_time) - 1]

    logging.info("Start calculation/assigning voltage_extremes of"
                 " ECG trace of file {}".format(filename))
    voltage_extremes = (min(new_voltage), max(new_voltage))

    logging.info("Start calculation/assigning num_beats of"
                 " ECG trace of file {}".format(filename))

    peak_len = len(working_data['peaklist'])
    rm_peak_len = len(working_data['removed_beats'])
    num_beats = peak_len - rm_peak_len

    logging.info("Start calculation/assigning mean_hr_bpm of"
                 " ECG trace of file {}".format(filename))
    mean_hr_bpm = measures['bpm']

    logging.info("Start calculation/assigning where the beats"
                 " of ECG trace of file {}".format(filename))
    beats = [new_time[i] for i in [x for x in working_data['peaklist']
                                   if x not in working_data['removed_beats']]]

    metrics = {'duration': duration,
               'voltage_extremes': voltage_extremes,
               'num_beats': num_beats,
               'mean_hr_bpm': mean_hr_bpm,
               'beats': beats}
    return metrics


def dump_into_json(filename, metrics):
    """Dump the metrics dictionary into a JSON file

    It will automatically dump the dictionary:
    metrics = {'duration': duration,
               'voltage_extremes': voltage_extremes,
               'num_beats': num_beats,
               'mean_hr_bpm': mean_hr_bpm,
               'beats': beats}.
    in to a JSON file with the file name as the data file name.

    :param filename: name of the file being read
    :param metrics: a dictionary containing duration,
                    voltage extremes, number of beats, beats per minute,
                    and the time where beats occur
    :returns:
        - successful_JSON - test if it has successfully create JSON
    """
    successful_JSON = False
    try:
        output_file = open(filename + '.json', 'w')
        json.dump(metrics, output_file)
        output_file.close()
        successful_JSON = True
    except TypeError:
        print("Unsuccessfully output JSON file")
    return successful_JSON


def ecg_analysis():
    """Main file of ECG analysis tools

    The function will first load the file from the test_data path,
    and then it will process data by first checking if there is any
    string inside of the list of data and clean it if there is any.
    Then it will check the missing data and modify it without losing
    the generality of the data (not changing the length). Then it will
    use Heartpy external packages to analyze data and divide data into
    readable matrics and return to JSON files.

    :returns:
        - finish_work - test if the ecg_analysis has successfully executed
    """
    fileopen = 'test_data32.csv'

    new_time, new_voltage, filename = load_data(fileopen)

    bad_data_detection(new_time, new_voltage)

    missing_data_detection(new_time, new_voltage)

    voltage_exceeded_detection(new_voltage, fileopen)

    working_data, measures, _ = heartpy_exec(new_time, new_voltage, filename)

    metrics = create_dictionary(new_time, new_voltage,
                                working_data, measures, filename)

    dump_into_json(filename, metrics)


if __name__ == '__main__':
    ecg_analysis()
