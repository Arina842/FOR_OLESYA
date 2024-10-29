import numpy as np
import os
import pandas as pd
import datetime
import statistics

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

start = datetime.datetime.now()


def form_noise_data(self):
    time_len = len(self._test_data.time) + 8
    self._noise_data.Unload_noise = np.random.uniform(-1, 1, 9)
    self._noise_data.PorePressure_noise = np.random.uniform(0.3, 0.5)
    self._noise_data.CellPress_noise = np.random.uniform(-0.1, 0.1, time_len)
    self._noise_data.VerticalPress_noise = np.random.uniform(-0.1, 0.1, time_len)
    self._noise_data.b_CVI = np.round(np.random.uniform(0.95, 0.98), 2)
    self._noise_data.time_noise = np.random.uniform(0.5, 0.8)
    return time_len


# #Тестовые данные
# strain = np.array([0.,      0.0015,  0.001945, 0.002416, 0.002914, 0.003441, 0.004001, 0.004596,
#  0.00523,  0.005907, 0.006632, 0.006573, 0.006507, 0.006434, 0.006352, 0.006257,
#  0.006143, 0.006003, 0.005824, 0.005606, 0.007409, 0.008245, 0.009146, 0.01012,
#  0.011178, 0.012329, 0.013587, 0.014967, 0.016488, 0.018174, 0.020923, 0.0222,
#  0.023304, 0.024377, 0.025505, 0.026791, 0.028453, 0.031417])
#
# strain_rad = np.array([-0.,       -0.0015,   -0.001585, -0.001678, -0.001778, -0.001887, -0.002007,
#  -0.002139, -0.002285, -0.002448, -0.002629, -0.002605, -0.002579, -0.00255,
#  -0.002517, -0.002479, -0.002433, -0.002377, -0.002306, -0.002219, -0.002833,
#  -0.003065, -0.003329, -0.003635, -0.003992, -0.004414, -0.00492,  -0.005541,
#  -0.006317, -0.00732,  -0.008181, -0.008582, -0.008929, -0.009266, -0.009621,
#  -0.010025, -0.010547, -0.011479])
#
# deviator_numpy_array = np.array([0.,        920.909997, 1841.819994, 2762.729991, 3683.639988,
#   4604.549985,  5525.459982,  6446.369979,  7367.279976,  8288.189973,
#   9209.09997,   8288.189973,  7367.279976,  6446.369979,  5525.459982,
#   4604.549985,  3683.639988,  2762.729991,  1841.819994,   920.909997,
#  10130.009967, 11050.919964, 11971.829961, 12892.739958, 13813.649955,
#  14734.559952, 15655.469949, 16576.379946, 17497.289943, 18418.19994,
#  17497.289944, 16576.379947, 15655.46995,  14734.559953, 13813.649956,
#  12892.739959, 11971.829962, 11050.919965])
#  deviator_numpy_array = deviator_numpy_array/1000

#  connection_to_curve_indexes = np.array([15523, 65522])

strain_numpy_array = np.array([0., 0.0015, 0.001809, 0.002139, 0.002493, 0.002874, 0.003284, 0.003727,
                               0.004207, 0.004729, 0.005298, 0.005255, 0.005206, 0.005152, 0.005091, 0.005021,
                               0.004937, 0.004833, 0.0047, 0.004539, 0.005923, 0.00661, 0.00737, 0.008215,
                               0.009161, 0.010225, 0.011433, 0.012815, 0.014412, 0.016284, 0.017457, 0.017991,
                               0.018438, 0.018854, 0.019267, 0.019695, 0.020162, 0.020703, 0.0214, 0.022544])

strain_rad_numpy_array = np.array([-0., -0.0015, -0.001571, -0.001648, -0.001732, -0.001824, -0.001925,
                                   -0.002036, -0.002159, -0.002296, -0.002449, -0.002432, -0.002413, -0.002391,
                                   -0.002367, -0.002338, -0.002305, -0.002263, -0.00221, -0.002146, -0.002623,
                                   -0.00282, -0.003046, -0.003309, -0.003616, -0.003982, -0.004425, -0.004971,
                                   -0.005662, -0.00657, -0.007335, -0.007684, -0.007976, -0.008248, -0.008518,
                                   -0.008798, -0.009103, -0.009457, -0.009913, -0.010661])

deviator_numpy_array = np.array([0., 2536.08227, 5072.16454, 7608.24681, 10144.32908, 12680.41135,
                                 15216.49362, 17752.57589, 20288.65816, 22824.74043, 25360.8227, 22824.74043,
                                 20288.65816, 17752.57589, 15216.49362, 12680.41135, 10144.32908, 7608.24681,
                                 5072.16454, 2536.08227, 27896.90497, 30432.98724, 32969.06951, 35505.15178,
                                 38041.23405, 40577.31632, 43113.39859, 45649.48086, 48185.56313, 50721.6454,
                                 48185.5632, 45649.48093, 43113.39866, 40577.31639, 38041.23412, 35505.15185,
                                 32969.06958, 30432.98731, 27896.90504, 25360.82277])
deviator_numpy_array = deviator_numpy_array / 1000
connection_to_curve_indexes_numpy_array = np.array([12980, 62979])
sigma_3_MPa = 3.00


def rock_log_function(strain, strain_rad, deviator, connection, sigma_3_MPa):
    '''
    Функция обрабатывает полученные данные и формирует словарь для записи в Excel
    :param strain: Задаётся внешне для функции
    :param strain_rad: Задается внешне для функции
    :param deviator: Задаётся внешне для функции
    :param connection: Задаётся внешне для функции. Пока не используется
    :param sigma_3_MPa: Задаётся внешне для функции
    :return: rock_dict
    '''
    sample_height = 84  # В мм
    sample_diameter = 42  # В мм

    def start():
        # Вводные данные
        time = np.round(np.linspace(0, np.random.uniform(120, 180), 12), 2)
        # Составление массива Траектории
        trajectory = np.array([''] * (time.size - 7) + ['Consolidation'] * (time.size - 6) + ['CTC'])
        action_changed = np.array(['True', '', '', 'True', '', 'True', '', '', '', 'True', '', 'True'])
        action = np.array(
            ['', '', '', '', '' 'Start', 'Start', 'LoadStage', 'LoadStage', 'LoadStage', 'LoadStage', 'Wait', 'Wait'])
        cell_press = np.append(np.round(np.linspace(0, sigma_3_MPa - 0.001, 9), 3),
                               np.round(np.linspace(sigma_3_MPa + 0.0001, sigma_3_MPa + 0.001, 3), 3))
        vert_strain = np.append(np.round(np.linspace(-0.001, 0.003, 5), 3),
                                np.round(np.linspace(0.004, 1.0, 7), 3))
        radial_strain = np.append(np.round(np.linspace(-0.001, 0.003, 5), 3),
                                  np.round(np.linspace(0.004, 1.0, 7), 3))
        vertical_force = np.round(np.linspace(-0.001, 1, 12), 3)
        radial_deformation_mm = np.round(radial_strain * sample_diameter, 3)
        vertical_deformation2_mm = np.round(np.random.uniform(0.001, 0.02, time.size), 3)
        vertical_deformation1_mm = np.round(vert_strain * sample_height - vertical_deformation2_mm, 3)

        data = {
            "Time": time,
            "Action": action,
            "Action_Changed": action_changed,
            "MeanVerticalDeformation_mm": np.round((vertical_deformation1_mm - vertical_deformation2_mm) / 2, 3),
            "RadialDeformation_mm": radial_deformation_mm,
            "CellPress_MPa": cell_press,
            "VerticalForce_kN": vertical_force,
            "VerticalStrain": vert_strain,
            "RadialStrain": radial_strain,
            "Deviator_MPa": np.full(time.size, '0'),
            "VerticalDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
            "RadialDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
            "VerticalStrainOnDeviatorStage": np.full(time.size, '0'),
            "RadialStrainOnDeviatorStage": np.full(time.size, '0'),
            "VerticalDeformation1_mm": vertical_deformation1_mm,
            "VerticalDeformation2_mm": vertical_deformation2_mm,
            "Trajectory": trajectory,
        }

        return data

    # Запись стартовой части словаря
    start_dict = start()
    start_time_last_index = (start_dict["Time"].tolist())[-1]

    def deviator_func(start_dict, strain, strain_rad, deviator, connection):
        last_index = (start_dict["Time"].tolist())[-1]
        # Среднее значение дельты девиаторы для вычисления времени. Скорость 1 МПа/сек
        deviator_list = deviator.tolist()
        deviator_delta = []
        for i in range(5):
            deviator_delta.append(deviator_list[i + 1] - deviator_list[i])
        # Так как массив и с отрицательными значениями, взяты первые значение, по ним вычислено среднее
        deviator_delta = statistics.mean(deviator_delta)

        time = np.round(np.linspace(last_index + 1, last_index + (deviator_delta * deviator.size), deviator.size), 2)

        # Составление массива Траектории
        trajectory = np.array(['CTC'] * time.size)
        action = np.array(['WaitLimit'] * (time.size - 1) + ['TerminateCondition'])
        action_changed = np.array([''] * (time.size - 2) + ['True'] + [''])

        vert_strain = strain + start_dict['VerticalStrain'].tolist()[-1] + 0.001

        radial_strain = strain_rad + start_dict['RadialStrain'].tolist()[-1] + 0.001
        radial_deformation_mm = radial_strain * sample_diameter
        vert_force = deviator + start_dict["VerticalForce_kN"].tolist()[-1] + 0.001
        vertical_deformation2_mm = np.random.uniform(0.01, 0.2, time.size)
        vertical_deformation1_mm = vert_strain * sample_height - vertical_deformation2_mm
        data = {
            "Time": time,
            "Action": action,
            "Action_Changed": action_changed,

            "MeanVerticalDeformation_mm": np.round((vertical_deformation1_mm - vertical_deformation2_mm) / 2, 3),
            "RadialDeformation_mm": np.round(radial_deformation_mm, 3),
            "CellPress_MPa": np.full(time.size, sigma_3_MPa + 0.001),
            "VerticalForce_kN": np.round(vert_force, 3),
            "VerticalStrain": np.round(vert_strain, 3),
            "RadialStrain": np.round(radial_strain, 3),
            "Deviator_MPa": np.round(deviator, 3),
            "VerticalDeformationOnDeviatorStage_mm": np.round(strain * sample_height, 3),
            "RadialDeformationOnDeviatorStage_mm": np.round(strain_rad * sample_diameter, 3),
            "VerticalStrainOnDeviatorStage": np.round(strain, 3),
            "RadialStrainOnDeviatorStage": np.round(strain_rad, 3),
            "VerticalDeformation1_mm": np.round(vertical_deformation1_mm, 3),
            "VerticalDeformation2_mm": np.round(vertical_deformation2_mm, 3),
            "Trajectory": trajectory,
        }

        return data

    # Запись девиаторной части словаря
    deviator_dict = deviator_func(start_dict, strain, strain_rad, deviator, connection)

    # Совмещение словаря start и словаря девиатора
    rock_dict_withou_twice_True = {}
    for key in start_dict:
        rock_dict_withou_twice_True[key] = np.append(start_dict[key], deviator_dict[key])

    def twice_True(rock_dict):
        '''
        Функция возвращает словарь с задвоенными строками на True в Action_Changed
        :param rock_dict: сформированный словарь начального словаря и словаря девиации
        :return: rock_dict
        '''

        # Перевод value словаря в формат list
        for key in ['Time', 'Action', "Action_Changed", 'MeanVerticalDeformation_mm', 'RadialDeformation_mm',
                    'CellPress_MPa',
                    'VerticalForce_kN', 'VerticalStrain', 'RadialStrain', 'Deviator_MPa',
                    'VerticalDeformationOnDeviatorStage_mm', 'RadialDeformationOnDeviatorStage_mm',
                    'VerticalStrainOnDeviatorStage', 'RadialStrainOnDeviatorStage', 'VerticalDeformation1_mm',
                    'VerticalDeformation2_mm',
                    'Trajectory']:
            rock_dict[key] = rock_dict[key].tolist()

        # Задвоение строк с флагами True. На тестовых данных работает
        for index in range(len(rock_dict["Action"])):
            if rock_dict["Action_Changed"][index] == 'True':
                for key in ['Time', 'Action', "Action_Changed", 'MeanVerticalDeformation_mm', 'RadialDeformation_mm',
                            'CellPress_MPa', 'VerticalForce_kN', 'VerticalStrain', 'RadialStrain', 'Deviator_MPa',
                            'VerticalDeformationOnDeviatorStage_mm', 'RadialDeformationOnDeviatorStage_mm',
                            'VerticalStrainOnDeviatorStage', 'RadialStrainOnDeviatorStage', 'VerticalDeformation1_mm',
                            'VerticalDeformation2_mm',
                            'Trajectory']:
                    if key == "Action_Changed":
                        new_array = rock_dict[key][0:index + 1]
                        new_array.append('')
                        new_array.extend(rock_dict[key][index + 1:])
                        rock_dict[key] = new_array

                    elif key == 'Trajectory' or key == "Action":
                        new_array = rock_dict[key][0:index + 1]
                        new_array.append(rock_dict[key][index + 1])
                        new_array.extend(rock_dict[key][index + 1:])
                        rock_dict[key] = new_array
                    else:
                        new_array = rock_dict[key][0:index + 1]
                        new_array.append(rock_dict[key][index])
                        new_array.extend(rock_dict[key][index + 1:])
                        rock_dict[key] = new_array

        # Перевод value словаря в формат numpy array
        for key in ['Time', 'Action', "Action_Changed", 'MeanVerticalDeformation_mm', 'RadialDeformation_mm',
                    'CellPress_MPa',
                    'VerticalForce_kN', 'VerticalStrain', 'RadialStrain', 'Deviator_MPa',
                    'VerticalDeformationOnDeviatorStage_mm', 'RadialDeformationOnDeviatorStage_mm',
                    'VerticalStrainOnDeviatorStage',
                    'RadialStrainOnDeviatorStage', 'VerticalDeformation1_mm', 'VerticalDeformation2_mm',
                    'Trajectory']:
            rock_dict[key] = np.array(rock_dict[key])
        return rock_dict

    rock_dict = twice_True(rock_dict_withou_twice_True)
    return rock_dict


def create_excel_from_dict_list(data: list, output_filename: str, sheet_name='Sheet1'):
    '''
    Создаёт Excel по словарю
    :param data: Словарь для записи массива
    :param output_filename: имя файла
    :param sheet_name: имя вкладки
    :return: filepath
    '''

    # Создаем директорию, если она не существует
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', output_filename)

    # Создаем новую книгу Excel
    wb = Workbook()
    ws = wb.active

    ws.title = sheet_name
    df = pd.DataFrame(data)

    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    wb.save(filepath)
    return filepath


rock_log = rock_log_function(strain_numpy_array, strain_rad_numpy_array, deviator_numpy_array,
                             connection_to_curve_indexes_numpy_array, sigma_3_MPa)
# Для Excel
create_excel_from_dict_list(rock_log, 'proverka.xlsx')

# для понимания времени работы функций
finish = datetime.datetime.now()
print('Время работы: ' + str(finish - start))
