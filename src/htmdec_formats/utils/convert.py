import logging
import numpy as np
from unyt import unyt_quantity


def _replace_nan(worksheet, row, col, value, format=None):
    if np.isnan(value):
        return worksheet.write_blank(row, col, None, format)
    else:
        return None  # let xlsxwriter do its thing


def export_inputs_to_xlsx(dataset, workbook, name):
    cols = {
        "Pre-Test Inputs": {
            "TargetLoad": {"unit": "mN"},
            "TargetDepth": {"unit": "nm"},
            "PoissonsRatioOfSample": {"unit": "None"},
            "TargetIndentationStrainRate": {"unit": "1/s"},
            "TargetIndentationStrainRate2": {"unit": "1/s"},
            "TargetIndentationStrainRate3": {"unit": "1/s"},
            "TargetIndentationStrainRate4": {"unit": "1/s"},
            "TargetIndentationStrainRate5": {"unit": "1/s"},
            "TargetFrequency": {"unit": "Hz"},
            "SurfaceApproachVelocity": {"unit": "nm/s"},
            "TargetDynamicDisplacement": {"unit": "nm"},
            "HoldMaximumLoadTime": {"unit": "s"},
            "SurfaceApproachDistance": {"unit": "nm"},
            "MeasureDriftRateQ": {"unit": "None"},
            "DataAcquisitionRate": {"unit": "Hz"},
            "TargetDepthJump": {"unit": "nm"},
            "TargetDepthJump2": {"unit": "nm"},
            "TargetDepthJump3": {"unit": "nm"},
            "TargetDepthJump4": {"unit": "nm"},
        },
        "Post-Test Inputs": {
            "DepthOrForce": {"unit": "Integer"},
            "DepthToEndAverages": {"unit": "nm"},
            "DepthToStartAverages": {"unit": "nm"},
            "DriftCorrectionFlag": {"unit": "Integer"},
            "LoadToEndAverages": {"unit": "mN"},
            "LoadToStartAverages": {"unit": "mN"},
            "MinimumDepthForResults": {"unit": "nm"},
            "PoissonsRatioOfSample": {"unit": "None"},
            "TestIsValid": {"unit": "Integer"},
        },
    }

    worksheet = workbook.add_worksheet(name)
    worksheet.add_write_handler(float, _replace_nan)
    ntests = len(dataset.tests)

    worksheet.write(0, 0, "Test")
    for i in range(1, ntests + 1):
        worksheet.write(i + 1, 0, i)

    correction = 0
    for i, (key, value) in enumerate(cols[name].items()):
        unit = value["unit"]
        if unit not in ("None", "°C", "Integer"):
            unit = unyt_quantity(1, unit).in_base().d
        else:
            unit = 1.0

        col = i + 1 - correction
        try:
            worksheet.write(0, col, dataset.result_vars[key].displayname)
        except KeyError:
            logging.warning(f"Key {key} not found in dataset")
            correction += 1
            continue
        worksheet.write(1, col, value["unit"])
        data = dataset.result_vars[key].accumulator / unit
        for j in range(ntests):
            worksheet.write(j + 2, col, data[j])


def export_results_to_xlsx(dataset, workbook):
    cols = {
        "TestXPosition": {"unit": "µm"},
        "TestYPosition": {"unit": "µm"},
        "MaximumLoadInTest": {"unit": "mN"},
        "MaximumDepthInTest": {"unit": "nm"},
        "ReportingDepth": {"unit": "nm"},
        "VHN": {"unit": "None"},
        "AverageHARDNESS": {"unit": "GPa"},
        "AverageMODULUS": {"unit": "GPa"},
        "DriftRate": {"unit": "nm/s"},
        "TestTemperature": {"unit": "°C"},
        "SurfaceApproachVelocity": {"unit": "nm/s"},
        "TargetLoad": {"unit": "mN"},
        "TargetDepth": {"unit": "nm"},
        "TargetIndentationStrainRate": {"unit": "1/s"},
        "TargetFrequency": {"unit": "Hz"},
        "TargetDynamicDisplacement": {"unit": "nm"},
        "MeasureDriftRateQ": {"unit": "None"},
    }
    worksheet = workbook.add_worksheet("Results")
    worksheet.add_write_handler(float, _replace_nan)
    worksheet.add_write_handler(np.float64, _replace_nan)
    ntests = len(dataset.tests)
    # Add first column with test number
    worksheet.write(0, 0, "Test")
    for i in range(1, ntests + 1):
        worksheet.write(i + 1, 0, i)
    worksheet.write(ntests + 2, 0, "Average")
    worksheet.write(ntests + 3, 0, "Standard Deviation")
    worksheet.write(ntests + 4, 0, "Coefficient of Variation")

    correction = 0
    for i, (key, value) in enumerate(cols.items()):
        unit = value["unit"]
        if unit not in ("None", "°C", "Integer"):
            unit = unyt_quantity(1, unit).in_base().d
        else:
            unit = 1.0

        col = i + 1 - correction
        try:
            worksheet.write(0, col, dataset.result_vars[key].displayname)
        except KeyError:
            logging.warning(f"Key {key} not found in dataset")
            continue
        worksheet.write(1, col, value["unit"])

        data = dataset.result_vars[key].accumulator / unit
        stats = dataset.result_vars[key].statistics

        for j in range(ntests):
            worksheet.write(j + 2, col, data[j])

        worksheet.write(ntests + 2, col, stats[0] / unit)
        worksheet.write(ntests + 3, col, stats[1] / unit)
        worksheet.write(ntests + 4, col, stats[-1])


def export_summary_to_xlsx(dataset, workbook):
    cols = {
        "PdotOverP": {"display": "(dP/dt) / P", "unit": "1/s"},
        "TipTemperature": {"display": "Cabinet  Temp.", "unit": "°C"},
        "DisplacementDerivativeOfForce": {"display": "d(Force)/d(Disp)", "unit": "N/m"},
        "ShowDepth": {"display": "DEPTH", "unit": "nm"},
        "Displacement": {"display": "Displacement", "unit": "nm"},
        "DynamicDisplacement": {"display": "Dyn. Disp.", "unit": "nm"},
        "DynamicForce": {"display": "Dyn. Force", "unit": "µN"},
        "DynamicFrequency": {"display": "Dyn. Freq.", "unit": "Hz"},
        "DynamicPhase": {"display": "Dyn. Phase", "unit": "degree"},
        "DynamicStiffnessSquaredOverLoad": {
            "display": "Dyn. Stiff.^2/Load",
            "unit": "GPa",
        },
        "Extension": {"display": "Extension", "unit": "mm"},
        "Force": {"display": "Force", "unit": "mN"},
        "HARDNESS": {"display": "HARDNESS", "unit": "GPa"},
        "Index": {"display": "Index", "unit": "Integer"},
        "ShowLoad": {"display": "LOAD", "unit": "mN"},
        "MODULUS": {"display": "MODULUS", "unit": "GPa"},
        "SpringStiffness": {"display": "Spring Stiffness", "unit": "N/m"},
        "ShowStiffness": {"display": "STIFFNESS", "unit": "N/m"},
        "Time": {"display": "Time", "unit": "s"},
        "TimeOnSample": {"display": "TIME", "unit": "s"},
        "XAxis": {"display": "X Axis Position", "unit": "µm"},
        "YAxis": {"display": "Y Axis Position", "unit": "µm"},
    }
    worksheet = workbook.add_worksheet("Sample Summary")
    worksheet.add_write_handler(float, _replace_nan)
    for i, (key, value) in enumerate(cols.items()):
        data = dataset.sample_summary.channels[key].bins
        nrows, _ = data.shape
        unit = value["unit"]
        if unit not in ("None", "°C", "Integer"):
            unit = unyt_quantity(1, unit).in_base().d
        else:
            unit = 1.0

        for j, op in enumerate([("Mean", 0), ("StdDev", 2), ("Median", 1)]):
            col = i * 3 + j
            worksheet.write(0, col, f"{value['display']} {op[0]}")
            worksheet.write(1, col, value["unit"])
            for k in range(nrows):
                try:
                    worksheet.write(k + 2, col, data[k, op[1]] / unit)
                except TypeError:
                    worksheet.write(k + 2, col, "")


def export_test_to_xlsx(test, test_index, workbook):
    cols = {
        "ShowDepth": {"unit": "nm"},
        "ShowLoad": {"unit": "mN"},
        "TimeOnSample": {"unit": "s"},
        "HARDNESS": {"unit": "GPa"},
        "MODULUS": {"unit": "GPa"},
    }
    worksheet = workbook.add_worksheet(f"Test {test_index + 1}")
    worksheet.add_write_handler(float, _replace_nan)
    surface_index = test.calculations["SurfaceIndex"]
    start_report_index = test.calculations["StartAverageDynamics"]
    end_report_index = test.calculations["EndAverageDynamics"]
    end_of_load_index = test.inputs["EndOfLoadingIndex"]

    markers = np.zeros_like(test.arrays["ShowDepth"], dtype="<U32")
    markers[int(surface_index.doublevalue)] = surface_index.displayname
    markers[int(start_report_index.doublevalue)] = start_report_index.displayname
    markers[int(end_report_index.doublevalue)] = end_report_index.displayname
    markers[int(end_of_load_index.doublevalue)] = end_of_load_index.displayname

    col = ["Markers", ""] + markers[int(surface_index.doublevalue) : -1].tolist()
    worksheet.write_column(0, 0, col)
    i = 1
    for key, value in cols.items():
        data = test.arrays[key][int(surface_index.doublevalue) : -1]
        worksheet.write_column(0, i, [key, value["unit"]])
        unit = value["unit"]
        if unit not in ("None", "°C", "Integer"):
            unit = unyt_quantity(1, unit).in_base().d
        else:
            unit = 1.0
        data = data / unit
        worksheet.write_column(2, i, data.tolist())
        i += 1
