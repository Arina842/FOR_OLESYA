import numpy as np
import matplotlib.pyplot as plt


# Составление массива Времени
time = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]

# Составление массива Траектории
trajectory = []
trajectory.extend(['', '', '', '', '', 'Consolidation', 'Consolidation', 'Consolidation', 'Consolidation', 'Consolidation'])
trajectory.extend(['CTC']*(len(time)-len(trajectory)))

action = []
action.extend(['', '', '', '', 'Start','Start','LoadStage ','LoadStage ','Wait','Wait'])
action.extend(['WaitLimit']*(len(time)-len(action)-1))
action.append('TerminateCondition')
print(len(action))


action_changed=[]
action.extend(['True', '', '', 'True', '','True',' ','True','','','True'])


# trajectory_consolidation = [' ','Consolidation','Consolidation','Consolidation','Consolidation','Consolidation']
# np.append(trajectory_empty,trajectory_consolidation)

# trajectory =np.append(trajectory_empty, (np.full(time.sum()-k,'CTC')))
# a=np.around(time.sum(),1)
print(len(trajectory))

# print(np.full(a, 0))
data = {
    "Time": time,
    "Action": action,
#     "Action_Changed": np.full(time.sum(), '0'),
    "SampleHeight_mm": np.full(len(time), 76),
    "SampleDiameter_mm": np.full(len(time), 38),
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
    "Trajectory": trajectory}

print(data)
