![npm](https://img.shields.io/github/followers/YuMiao329?style=flat-square)
![Github Actions Status](https://github.com/BME547-Fall2021/ecg-analysis-YuMiao329/actions/workflows/pytest_runner.yml/badge.svg)
# ECG Analysis Assignment

The `ecg_analytical` will analyze the ecg signal from csv files based on external packages `heartpy`

## Usage

`ecg_analytical` will get the ecg csv file from `test_data` file and you can manually change which
file will be selected simply by changing the `fileopen` variable inside of the function `ecg_analysis`.

Based on the `heartpy` package, we could get file in the form as:

The beats are calculated by 

`heartpy.process(hrdata, sample_rate, windowsize=0.75, report_time=False, calc_freq=False,
freq_method=’welch’, welch_wsize=240, freq_square=False, interp_clipping=False,
clipping_scale=False, interp_threshold=1020, hampel_correct=False, bpmmin=40, bpmmax=180, reject_segmentwise=False, high_precision=False,
high_precision_fs=1000.0, breathing_method=’welch’, clean_rr=False,
clean_rr_method=’quotient-filter’, measures=None, working_data=None)` 

which could directly generate heart beat during the time window and stored in the `measures` parameter. 

The bpm is calculated based on the number of beats in the total time range t and use beats/time * 60 to get bpm.
`    metrics = {'duration': duration,
               'voltage_extremes': voltage_extremes,
               'num_beats': num_beats,
               'mean_hr_bpm': mean_hr_bpm,
               'beats': beats}
`
The metrics will be outputed into the JSON file with specific file loaded.

## Note

Each file will have its own log file which will be outputed in the same directory of ecg_analysis.

That will show whether there is NaN, missing data or excessed voltage data.

They will also be slighly modified to fit into the criteria of the data format.
