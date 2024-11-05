import numpy as np
import os
import pandas as pd
import datetime
import statistics

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

"""
Представлены тестовые данные в приведённом виде и их обрезка, если reload_points_rad_numpy_array не равно [None, None]
Опционально считается время работы.

Функция rock_log_function включает в себя первоначальный перевод единиц и остальные функции. 
После Создания словаря start  и deviator происходит их объединение и наложение шума на некоторые столбцы.
Округление данных словаря до тысячных (3 знак после запятой)

Функция start создаёт по заданного размера, где action_changed, action и trajectory прописываются вручную. 
Все остальные величины в словаре задаются рандомно.

Функция deviator_func по тестовым данным записывает значения в колонки "Deviator_MPa"- deviator,
"VerticalStrainOnDeviatorStage" - strain, "RadialStrainOnDeviatorStage" - strain_rad. 
Остальные значения пересчитываются исходя из этих трёх. Если reload_points_rad_numpy_array не равно [None, None], 
то девиатор заканчивается action - Waitlimit , есть reload_points_rad_numpy_array равно двум числам,
то action заканчивается на Cyclic_Unloading

Функция twice_true Обрабатывает конечный словарь и добавляет дублирование строк.
Функция create_excel_from_dict опциональна. Создаёт excel файл для удобной проверки работы функции
"""

start = datetime.datetime.now()
# Тестовые данные
sigma_3 = 1000.0
strain_numpy_array = np.array([0., 0.0015, 0.00193431, 0.00246594, 0.00300467, 0.00361692,
                               0.00436166, 0.00492197, 0.00568057, 0.00635544, 0.007334, 0.00731614,
                               0.0071322, 0.00706693, 0.0071246, 0.00678212, 0.00685097, 0.00657452,
                               0.00638854, 0.006169, 0.00842317, 0.00928322, 0.01039635, 0.01160051,
                               0.01319362, 0.01440559, 0.01596397, 0.01833728, 0.02032469, 0.022962,
                               0.02590524, 0.02779313, 0.02782841, 0.02868413, 0.03002394, 0.03114306,
                               0.03172707, 0.03314354, 0.03521246, 0.03782629, 0.04086895])
strain_rad_numpy_array = np.array([0., -0.0015, -0.00165011, -0.00177113, -0.0019364, -0.00204633,
                                   -0.00223144, -0.00229832, -0.00246546, -0.00261906, -0.002783, -0.00282675,
                                   -0.00274856, -0.00274268, -0.00258617, -0.00259054, -0.00255805, -0.00254829,
                                   -0.0023635, -0.002318, -0.00292695, -0.00300518, -0.00313945, -0.00329315,
                                   -0.00365416, -0.00369043, -0.00395132, -0.0041085, -0.00405948, -0.004356,
                                   -0.00497057, -0.00511954, -0.0054995, -0.0055568, -0.00551239, -0.00600365,
                                   -0.00577248, -0.00649771, -0.00658468, -0.00720603, -0.00792156])
deviator_numpy_array = np.array([0., 1046.9699, 2093.9398, 3140.9097, 4187.8796, 5234.8495,
                                 6281.8194, 7328.7893, 8375.7592, 9422.7291, 10469.699, 9422.7291,
                                 8375.7592, 7328.7893, 6281.8194, 5234.8495, 4187.8796, 3140.9097,
                                 2093.9398, 1046.9699, 11516.6689, 12563.6388, 13610.6087, 14657.5786,
                                 15704.5485, 16751.5184, 17798.4883, 18845.4582, 19892.4281, 20939.398,
                                 19892.429, 18845.4591, 17798.4892, 16751.5193, 15704.5494, 14657.5795,
                                 13610.6096, 12563.6397, 11516.6698, 10469.6999, 9422.73])
reload_points_rad_numpy_array = [None, None]
# Обрезка тестовых данных
if reload_points_rad_numpy_array[0] and reload_points_rad_numpy_array[0] is not None:
    strain_numpy_array = strain_numpy_array[:reload_points_rad_numpy_array[1]]
    strain_rad_numpy_array = strain_rad_numpy_array[:reload_points_rad_numpy_array[1]]
    deviator_numpy_array = deviator_numpy_array[:reload_points_rad_numpy_array[1]]


def rock_log_function(strain, strain_rad, deviator, connection, sigma_3):
    """
    Функция обрабатывает полученные данные и формирует словарь для записи в Excel
    :param strain: задаётся внешне для функции
    :param strain_rad: задается внешне для функции
    :param deviator: задаётся внешне для функции
    :param connection: задаётся внешне для функции (пока не используется)
    :param sigma_3: задаётся внешне для функции
    :return: rock_dict
    """

    sample_height = 84  # В мм
    sample_diameter = 42  # В мм
    # Перевод в нужные величины
    sigma_3_MPa = sigma_3 / 1000  # В MPa
    deviator = deviator / 1000  # В MPa

    def noise(time: np.array) -> dict:
        """
        Создаёт словарь шума
        :param time: массив времени
        :return: data_noise
        """
        data_noise = {
            'Unload_noise': np.round(np.random.uniform(-1, 1, time.size), 3),
            'PorePressure_noise': np.round(np.random.uniform(0.3, 0.5, time.size), 3),
            'CellPress_noise': np.round(np.random.uniform(-0.1, 0.1, time.size), 3),
            'VerticalPress_noise': np.round(np.random.uniform(-0.1, 0.1, time.size), 3),
            'b_CVI': np.round(np.random.uniform(0.95, 0.98, time.size), 3),
            'Time_noise': np.round(np.random.uniform(0.5, 0.8, time.size), 2)}
        return data_noise

    def start_func(sigma_3_MPa: float) -> dict:
        """
        Создаёт стартовый словарь
        :param sigma_3_MPa: сигма 3
        :return: data
        """

        # Задаваемые данные размерностей
        size_start = 6
        size_consolidation = 6
        size_dict = 12

        # Составление в ручную массивов time,trajectory,action_changed,action
        time = np.linspace(0, np.random.uniform(120, 180), size_dict)
        trajectory = np.array([''] * (time.size - 7) + ['Consolidation'] * (time.size - 6) + ['CTC'])
        action_changed = np.array(['True', '', '', 'True', '', 'True', '', '', '', 'True', '', 'True'])
        action = np.array(
            ['', '', '', '', '' 'Start', 'Start', 'LoadStage', 'LoadStage', 'LoadStage', 'LoadStage', 'Wait', 'Wait'])

        # Составление остальных массивов словаря
        cell_press = np.append(np.linspace(0, sigma_3_MPa - 0.001, time.size - size_start),
                               np.linspace(sigma_3_MPa + 0.0001, sigma_3_MPa + (np.random.uniform(0.001, 0.006)),
                                           time.size - size_consolidation))

        vert_strain = np.append(
            np.linspace(0.001, (np.random.uniform(0.015, 0.023)), time.size - size_start),
            np.linspace(0.004, (np.random.uniform(0.017, 0.022)), time.size - size_consolidation))

        vertical_force2 = np.append(np.linspace(-0.001, np.random.uniform(1.2, 1.6), size_start - 1),
                                    np.linspace(0.000, np.random.uniform(1.8, 2.0), size_consolidation))
        vertical_force = np.append(vertical_force2, [0], axis=0)

        radial_strain = np.linspace(0.001, np.max(vert_strain * sample_diameter) * 0.1, time.size)
        radial_deformation_mm = radial_strain * sample_diameter

        # mean_vertical_deformation_mm - среднее от vertical_deformation1_mm и vertical_deformation2_mm
        mean_vertical_deformation_mm = np.linspace(np.random.uniform(0.002, 0.02),
                                                   np.max(vert_strain * sample_height * 0.1),
                                                   time.size) + np.random.uniform(0.001, 0.01, time.size)
        random = np.random.uniform(0.001, 0.01, time.size)
        vertical_deformation1_mm = mean_vertical_deformation_mm + random
        vertical_deformation2_mm = mean_vertical_deformation_mm - random

        data = {
            "Time": np.round(time, 2),
            "Action": action,
            "Action_Changed": action_changed,
            "MeanVerticalDeformation_mm": np.round(mean_vertical_deformation_mm, 3),
            "RadialDeformation_mm": np.round(radial_deformation_mm, 3),
            "CellPress_MPa": np.round(cell_press, 3),
            "VerticalForce_kN": np.round(vertical_force, 3),
            "VerticalStrain": np.round(vert_strain, 4),
            "RadialStrain": np.round(radial_strain, 4),
            "Deviator_MPa": np.full(time.size, 0.0),
            "VerticalDeformationOnDeviatorStage_mm": np.full(time.size, 0.0),
            "RadialDeformationOnDeviatorStage_mm": np.full(time.size, 0.0),
            "VerticalStrainOnDeviatorStage": np.full(time.size, 0.0),
            "RadialStrainOnDeviatorStage": np.full(time.size, 0.0),
            "VerticalDeformation1_mm": np.round(vertical_deformation1_mm, 3),
            "VerticalDeformation2_mm": np.round(vertical_deformation2_mm, 3),
            "Trajectory": trajectory,
        }

        return data

    # Запись стартовой части словаря
    start_dict = start_func(sigma_3_MPa)

    def deviator_func(start_dict: dict, strain: np.array, strain_rad: np.array, deviator: np.array,
                      connection: list) -> dict:
        """
        Создаёт словарь на фазе девиатора
        :param start_dict: стартовый словарь
        :param strain: обрабатываемый массив вертикальной абсолютной деформации
        :param strain_rad: обрабатываемый массив радиальной абсолютной деформации
        :param deviator: обрабатываемый массив девиатора
        :param connection: обрабатываемый массив присутствия фазы Cyclic_Unloading
        :return:data
        """

        # Среднее значение дельты девиатора для вычисления времени. Скорость 1 МПа/сек
        deviator_list = deviator.tolist()
        deviator_delta = []
        for i in range(5):
            deviator_delta.append(deviator_list[i + 1] - deviator_list[i])
        # Так как массив и с отрицательными значениями, взяты первые значение, по ним вычислено среднее
        deviator_delta = statistics.mean(deviator_delta)

        # Составление массивов time,trajectory,action_changed,action
        time = np.round(np.linspace((start_dict["Time"].tolist())[-1] + 1, (start_dict["Time"].tolist())[-1]
                                    + (deviator_delta * deviator.size), deviator.size), 2)
        trajectory = np.array(['CTC'] * time.size)
        if connection[0] and connection[1] is not None:
            action = np.array(
                ['WaitLimit'] * (connection[0]) + ['CyclicUnloading'] * (connection[1] - connection[0]))
        else:
            action = np.array(['WaitLimit'] * time.size)
        action_changed = np.array([''] * (time.size - 1) + ['True'])

        # Составление остальных массивов словаря
        vert_strain = strain + start_dict['VerticalStrain'].tolist()[-1] + np.random.uniform(0.001, 0.009)
        radial_strain = strain_rad + start_dict['RadialStrain'].tolist()[-1] + np.random.uniform(0.001, 0.020)

        # vert_force рассчитывается как девиатор умноженный на площадь образца
        vert_force = (deviator * np.pi * sample_diameter * (
                sample_height + sample_diameter / 2)) / 1000000 + np.random.uniform(0.001, 0.006)
        radial_deformation_mm = radial_strain * sample_diameter

        # mean_vertical_deformation_mm - среднее от vertical_deformation1_mm и vertical_deformation2_mm
        mean_vertical_deformation_mm = (
                start_dict["MeanVerticalDeformation_mm"].tolist()[-1] + (strain * sample_height) +
                np.random.uniform(0.001, 0.01, time.size))
        random = np.random.uniform(0.001, 0.01, time.size)
        vertical_deformation1_mm = mean_vertical_deformation_mm + random
        vertical_deformation2_mm = mean_vertical_deformation_mm - random
        data = {
            "Time": time,
            "Action": action,
            "Action_Changed": action_changed,
            "MeanVerticalDeformation_mm": np.round(mean_vertical_deformation_mm, 3),
            "RadialDeformation_mm": np.round(radial_deformation_mm, 3),
            "CellPress_MPa": np.full(time.size, sigma_3_MPa + 0.001),
            "VerticalForce_kN": np.round(vert_force, 3),
            "VerticalStrain": np.round(vert_strain, 4),
            "RadialStrain": np.round(radial_strain, 4),
            "Deviator_MPa": np.round(deviator, 4),
            "VerticalDeformationOnDeviatorStage_mm": np.round(strain * sample_height, 3),
            "RadialDeformationOnDeviatorStage_mm": np.round(strain_rad * sample_diameter, 3),
            "VerticalStrainOnDeviatorStage": np.round(strain, 4),
            "RadialStrainOnDeviatorStage": np.round(strain_rad, 4),
            "VerticalDeformation1_mm": np.round(vertical_deformation1_mm, 3),
            "VerticalDeformation2_mm": np.round(vertical_deformation2_mm, 3),
            "Trajectory": trajectory,
        }

        return data

    # Запись девиаторной части словаря
    deviator_dict = deviator_func(start_dict, strain, strain_rad, deviator, connection)

    # Совмещение словаря start и словаря девиатора
    rock_dict_without_twice_true = {}
    for key in start_dict:
        rock_dict_without_twice_true[key] = np.append(start_dict[key], deviator_dict[key])

    # Запись шума
    noise_data = noise(rock_dict_without_twice_true['Time'])
    rock_dict_without_twice_true['CellPress_MPa'] += noise_data['CellPress_noise']
    rock_dict_without_twice_true['Time'] += noise_data['Time_noise']

    def twice_true(rock_dict_without_twice_true: dict) -> dict:
        """
        Функция возвращает словарь с удвоенными строками на True в Action_Changed
        :param rock_dict_without_twice_true: сформированный словарь начального словаря и словаря девиации
        :return: rock_dict
        """

        # Перевод value словаря в формат list
        for key in rock_dict_without_twice_true:
            rock_dict_without_twice_true[key] = rock_dict_without_twice_true[key].tolist()

        # Удвоение строк с флагами True. На тестовых данных работает
        for index in range(len(rock_dict_without_twice_true["Action"])):
            if rock_dict_without_twice_true["Action_Changed"][index] == 'True':
                for key in rock_dict_without_twice_true:
                    if key == "Action_Changed":
                        new_array = rock_dict_without_twice_true[key][0:index + 1]
                        new_array.append('')
                        new_array.extend(rock_dict_without_twice_true[key][index + 1:])
                        rock_dict_without_twice_true[key] = new_array

                    elif key == 'Trajectory' or key == "Action":
                        new_array = rock_dict_without_twice_true[key][0:index + 1]
                        new_array.append(rock_dict_without_twice_true[key][index + 1])
                        new_array.extend(rock_dict_without_twice_true[key][index + 1:])
                        rock_dict_without_twice_true[key] = new_array
                    else:
                        new_array = rock_dict_without_twice_true[key][0:index + 1]
                        new_array.append(rock_dict_without_twice_true[key][index])
                        new_array.extend(rock_dict_without_twice_true[key][index + 1:])
                        rock_dict_without_twice_true[key] = new_array

        # Удвоение последней строчки
        for key in rock_dict_without_twice_true:
            rock_dict_without_twice_true[key].append(rock_dict_without_twice_true[key][-1])
        rock_dict_without_twice_true['Action'][-1] = 'TerminateCondition'
        rock_dict_without_twice_true['Action_Changed'][-1] = ' '

        # Перевод value словаря в формат numpy array и запись
        rock_dict_fine = {}
        for key in rock_dict_without_twice_true:
            rock_dict_fine[key] = np.array(rock_dict_without_twice_true[key])
        return rock_dict_fine

    rock_dict = twice_true(rock_dict_without_twice_true)
    return rock_dict


def create_excel_from_dict(data: dict, output_filename: str, sheet_name='Sheet1'):
    """
    Создаёт Excel по словарю. Возвращает созданный файл
    :param data: Словарь для записи Excel файла
    :param output_filename: имя файла
    :param sheet_name: имя вкладки
    :return: filepath
    """

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
                             reload_points_rad_numpy_array, sigma_3)
# Для Excel
try:
    create_excel_from_dict(rock_log, 'example.xlsx')
except Exception as Ex:
    print('Закройте Excel файл, ошибка: "', Ex, '"')
# для понимания времени работы функций
finish = datetime.datetime.now()
print('Время работы: ' + str(finish - start))
