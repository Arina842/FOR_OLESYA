import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.optimize import curve_fit
from scipy.optimize import fsolve



def form_noise_data(self):
    time_len = len(self._test_data.time) + 8
    self._noise_data.Unload_noise = np.random.uniform(-1, 1, 9)
    self._noise_data.PorePressure_noise = np.random.uniform(0.3, 0.5)
    self._noise_data.CellPress_noise = np.random.uniform(-0.1, 0.1, time_len)
    self._noise_data.VerticalPress_noise = np.random.uniform(-0.1, 0.1, time_len)
    self._noise_data.b_CVI = np.round(np.random.uniform(0.95, 0.98), 2)
    self._noise_data.time_noise = np.random.uniform(0.5, 0.8)


def rock_loading(strain, strain_rad=0, deviator=0, loop_indexes=0, sample_size=0, sigma_3=5):
    """Формирует словарь """


    data = {
        "Time": time,
        "Action": np.full(time.sum(), '0'),
        "Action_Changed": np.full(time.sum(), '0'),
        "MeanVerticalDeformation_mm": np.full(time.sum(), '0'),
        "RadialDeformation_mm": np.full(time.sum(), '0'),
        "CellPress_MPa": np.full(time.sum(), '0'),
        "VerticalForce_kN": np.full(time.sum(), '0'),
        "VerticalStrain": np.full(time.sum(), '0'),
        "RadialStrain": np.full(time.sum(), '0'),
        "Deviator_MPa": np.full(time.sum(), '0'),
        "VerticalDeformationOnDeviatorStage_mm": np.full(time.sum(), '0'),
        "RadialDeformationOnDeviatorStage_mm": np.full(time.sum(), '0'),
        "VerticalStrainOnDeviatorStage": np.full(time.sum(), '0'),
        "RadialStrainOnDeviatorStage": np.full(time.sum(), '0'),
        "VerticalDeformation1_mm": np.full(time.sum(), '0'),
        "VerticalDeformation2_mm": np.full(time.sum(), '0'),
        "Trajectory": trajectory}
    return data
