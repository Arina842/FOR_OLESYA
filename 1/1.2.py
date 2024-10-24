import numpy as np
import os
from openpyxl import Workbook


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
# deviator = np.array([0.,        920.909997, 1841.819994, 2762.729991, 3683.639988,
#   4604.549985,  5525.459982,  6446.369979,  7367.279976,  8288.189973,
#   9209.09997,   8288.189973,  7367.279976,  6446.369979,  5525.459982,
#   4604.549985,  3683.639988,  2762.729991,  1841.819994,   920.909997,
#  10130.009967, 11050.919964, 11971.829961, 12892.739958, 13813.649955,
#  14734.559952, 15655.469949, 16576.379946, 17497.289943, 18418.19994,
#  17497.289944, 16576.379947, 15655.46995,  14734.559953, 13813.649956,
#  12892.739959, 11971.829962, 11050.919965])
#
# connection_to_curve_indexes = np.array([15523, 65522])

strain = np.array([0., 0.0015, 0.001809, 0.002139, 0.002493, 0.002874, 0.003284, 0.003727,
                   0.004207, 0.004729, 0.005298, 0.005255, 0.005206, 0.005152, 0.005091, 0.005021,
                   0.004937, 0.004833, 0.0047, 0.004539, 0.005923, 0.00661, 0.00737, 0.008215,
                   0.009161, 0.010225, 0.011433, 0.012815, 0.014412, 0.016284, 0.017457, 0.017991,
                   0.018438, 0.018854, 0.019267, 0.019695, 0.020162, 0.020703, 0.0214, 0.022544])

strain_rad = np.array([-0., -0.0015, -0.001571, -0.001648, -0.001732, -0.001824, -0.001925,
                       -0.002036, -0.002159, -0.002296, -0.002449, -0.002432, -0.002413, -0.002391,
                       -0.002367, -0.002338, -0.002305, -0.002263, -0.00221, -0.002146, -0.002623,
                       -0.00282, -0.003046, -0.003309, -0.003616, -0.003982, -0.004425, -0.004971,
                       -0.005662, -0.00657, -0.007335, -0.007684, -0.007976, -0.008248, -0.008518,
                       -0.008798, -0.009103, -0.009457, -0.009913, -0.010661])

deviator_test = np.array([0., 2536.08227, 5072.16454, 7608.24681, 10144.32908, 12680.41135,
                     15216.49362, 17752.57589, 20288.65816, 22824.74043, 25360.8227, 22824.74043,
                     20288.65816, 17752.57589, 15216.49362, 12680.41135, 10144.32908, 7608.24681,
                     5072.16454, 2536.08227, 27896.90497, 30432.98724, 32969.06951, 35505.15178,
                     38041.23405, 40577.31632, 43113.39859, 45649.48086, 48185.56313, 50721.6454,
                     48185.5632, 45649.48093, 43113.39866, 40577.31639, 38041.23412, 35505.15185,
                     32969.06958, 30432.98731, 27896.90504, 25360.82277])

connection_to_curve_indexes = np.array([12980, 62979])

sample_height = 84
sample_diameter = 42


def start():
    # Вводные данные
    time = np.linspace(0, np.random.uniform(106, 128), 9)
    # Составление массива Траектории
    trajectory = [''] * (time.size - 4) + ['Consolidation'] * (time.size - 6) + ['CTC']
    action_changed = ['True', '', '', 'True', 'True', 'True', '', '', 'True']
    action = ['', '', '', '', 'Start', 'LoadStage', 'Wait', 'Wait', 'Wait']

    data = {
        "Time": time,
        "Action": action,
        "Action_Changed": action_changed,

        "MeanVerticalDeformation_mm": np.full(time.size, '0'),
        "RadialDeformation_mm": np.full(time.size, '0'),
        "CellPress_MPa": np.full(time.size, '0'),
        "VerticalForce_kN": np.full(time.size, '0'),
        "VerticalStrain": np.full(time.size, '0'),
        "RadialStrain": np.full(time.size, '0'),
        "Deviator_MPa": np.full(time.size, '0'),
        "VerticalDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
        "RadialDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
        "VerticalStrainOnDeviatorStage": np.full(time.size, '0'),
        "RadialStrainOnDeviatorStage": np.full(time.size, '0'),
        "VerticalDeformation1_mm": np.full(time.size, '0'),
        "VerticalDeformation2_mm": np.full(time.size, '0'),
        "Trajectory": trajectory,
    }

    return data


start_data = start()


# def deviator(start_data, strain, strain_rad, deviator, connection_to_curve_indexes):
#     time = np.linspace(50 + 1, 60 + 120, deviator.size)
#     # Составление массива Траектории
#     trajectory = ['CTC'] * (time.size)
#     action = ['WaitLimit'] * (time.size - 1) + ['TerminateCondition']
#     action_changed = [''] * (time.size - 1) + ['True']
#     action = ['WaitLimit'] * (time.size)
#
#     data = {
#         "Time": time,
#         "Action": action,
#         "Action_Changed": action_changed,
#
#         "MeanVerticalDeformation_mm": np.full(time.size, '0'),
#         "RadialDeformation_mm": np.full(time.size, '0'),
#         "CellPress_MPa": np.full(time.size, '0'),
#         "VerticalForce_kN": np.full(time.size, '0'),
#         "VerticalStrain": np.full(time.size, '0'),
#         "RadialStrain": np.full(time.size, '0'),
#         "Deviator_MPa": deviator,
#         "VerticalDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
#         "RadialDeformationOnDeviatorStage_mm": strain_rad,
#         "VerticalStrainOnDeviatorStage": strain,
#         "RadialStrainOnDeviatorStage": np.full(time.size, '0'),
#         "VerticalDeformation1_mm": np.full(time.size, '0'),
#         "VerticalDeformation2_mm": np.full(time.size, '0'),
#         "Trajectory": trajectory,
#     }
#     return data
#
#
# deviator_dict = deviator(start, strain, strain_rad, deviator_test, connection_to_curve_indexes)


#
# def consolidation_data(last_time):
#     #Вводные данные
#     time=np.linspace(last_time, last_time+np.random.uniform(106,120),4)
#     # Составление массива Траектории
#     trajectory = ['Consolidation']*(time.size-1)+['CTC']
#     action = [''] * time.size
#     action_changed = ['True', 'True', '', 'True']
#     action = ['Start', 'LoadStage', 'Wait', 'Wait']
#
#
#
#     data = {
#         "Time": time,
#         "Action": action,
#         "Action_Changed": action_changed,
#         "MeanVerticalDeformation_mm": np.full(time.size, '0'),
#         "RadialDeformation_mm": np.full(time.size, '0'),
#         "CellPress_MPa": np.full(time.size, '0'),
#         "VerticalForce_kN": np.full(time.size, '0'),
#         "VerticalStrain": np.full(time.size, '0'),
#         "RadialStrain": np.full(time.size, '0'),
#         "Deviator_MPa": np.full(time.size, '0'),
#         "VerticalDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
#         "RadialDeformationOnDeviatorStage_mm": np.full(time.size, '0'),
#         "VerticalStrainOnDeviatorStage": np.full(time.size, '0'),
#         "RadialStrainOnDeviatorStage": np.full(time.size, '0'),
#         "VerticalDeformation1_mm": np.full(time.size, '0'),
#         "VerticalDeformation2_mm": np.full(time.size, '0'),
#         "Trajectory": trajectory,
#     }
#     return data
#
# data=consolidation_data(last_time)
#
# print(data)
# data["Time"]=list(data["Time"])
# start["Time"]=list(start["Time"])

# dict={}
# for key in start.keys():
#     print(key)
#     d=np.append(start[key],data[key])
#     print(d)

# for d in (start, data): # you can list as many input dicts as you want here
#     for key, value in d.items():
#         dict[key].append(value)
# print(dict)
# trajectory.extend(['CTC'] * (len(time) - len(trajectory)))


# action.extend(['WaitLimit'] * (len(time) - len(action) - 1))
# action.append('TerminateCondition')
# # print(len(action))
#
# action_changed = []
# action.extend(['True', '', '', 'True', '', 'True', ' ', 'True', '', '', 'True'])
#
# # Также можно сделать стадиями
#
# # trajectory_consolidation = [' ','Consolidation','Consolidation','Consolidation','Consolidation','Consolidation']
# # np.append(trajectory_empty,trajectory_consolidation)
#
# # trajectory =np.append(trajectory_empty, (np.full(time.sum()-k,'CTC')))
# # a=np.around(time.sum(),1)
# # print(len(trajectory))
#
# # print(np.full(a, 0))
# data = {
#     "Time": time,
#     "Action": action,
#     "Action_Changed": action_changed,
#     # "SampleHeight_mm": np.full(len(time), 76),
#     # "SampleDiameter_mm": np.full(len(time), 38),
#     "MeanVerticalDeformation_mm": np.full(time.sum(), '0'),
#     "RadialDeformation_mm": np.full(time.sum(), '0'),
#     "CellPress_MPa": np.full(time.sum(), '0'),
#     "VerticalForce_kN": np.full(time.sum(), '0'),
#     "VerticalStrain": np.full(time.sum(), '0'),
#     "RadialStrain": np.full(time.sum(), '0'),
#     "Deviator_MPa": np.full(time.sum(), '0'),
#     "VerticalDeformationOnDeviatorStage_mm": np.full(time.sum(), '0'),
#     "RadialDeformationOnDeviatorStage_mm": np.full(time.sum(), '0'),
#     "VerticalStrainOnDeviatorStage": np.full(time.sum(), '0'),
#     "RadialStrainOnDeviatorStage": np.full(time.sum(), '0'),
#     "VerticalDeformation1_mm": np.full(time.sum(), '0'),
#     "VerticalDeformation2_mm": np.full(time.sum(), '0'),
#     "Trajectory": trajectory}
#
# print(data)
#
#
def create_excel_from_dict_list(data: list, output_filename: str, sheet_name='Sheet1'):
    # Создаем директорию, если она не существует
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', output_filename)

    # Создаем новую книгу Excel
    wb = Workbook()
    ws = wb.active

    ws.title = sheet_name

    # Записываем данные из списка словарей в Excel

    header = data.keys()
    if data:
        ws.append(header)
        for i in range(len(header)):
            a = list(data[header[i]])
            ws.append(a)
        for i, statN in enumerate(dict):
            ws.cell(row=1, column=i + 1).value = statN
        wb.save('some.xlsx')
        # k=1
        # for header in data:
        #     ws.append([header[k] for k in header])

    wb.save(filepath)
    return filepath


print(type(start_data))
print(start_data.keys())
create_excel_from_dict_list(start_data, 'рпd.xlsx')
# print(start["Time"])
# print(start["Action"])
# print(start["Action_Changed"])
# print(start["Trajectory"])
