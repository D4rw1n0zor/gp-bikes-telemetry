UDP_IP = '127.0.0.1'
UDP_PORT = 30001
BUFFERSIZE = 220
#BUFFERSIZE = 880

# Blueprint of a packet: { variable/key: [ offset, variable short name, value-type, variable description ], ... }
# TODO:
# - Get this from a config-file (JSON or XML)
# - Add units (km/h, liters, ...)
# - Add formula convert (Example: int = (tm_speedometer[0]*3600)/1000)

''' Shape of an entry:
'unique key': [ offset, 'String value', 'data_type', 'Description', 'is_a_table', 'coordinate_x', 'coordinate_y']
'is_a_table' to be set to 0 or 1.
'''

PACKET_BLUEPRINT = { 'gpb_rpms': [ 13, 'RPMs', 'int', 'Revolutions per minute as engine-output before transmission.', '0' ],
                    'gpb_engine_temp': [ 17, 'Engine Temperature', 'float', 'Current temperature of the engine, measured at the ... .', '0' ],
                    'gpb_water_temp': [ 21, 'Water Temperature', 'float', 'Current cooling-water temperature measured at the radiator.', '0' ],
                    'gbp_gear': [ 25, 'Gear', 'int', 'Current gear position', '0' ],
                    'gbp_fuel': [ 29, 'Fuel Amount', 'float', 'Current fuel-amount in tank', '0' ],
                    'gbp_spdmeter': [ 33, 'Speedometer', 'float', 'Current speed', '0' ],
                    'gbp_wrldpos_x': [ 37, 'World Position X', 'float', 'World position X of a reference point attached to chassis ( not CG ).', '0' ],
                    'gbp_wrldpos_y': [ 41, 'World Position Y', 'float', 'World position Y of a reference point attached to chassis ( not CG ).', '0' ],
                    'gbp_wrldpos_z': [ 45, 'World Position Z', 'float', 'World position Z of a reference point attached to chassis ( not CG ).', '0' ],
                    'gbp_velocity_x': [49, 'Velocity X', 'float', 'Velocity X of CG in world coordinates.', '0' ],
                    'gbp_velocity_y': [ 53, 'Velocity Y', 'float', 'Velocity Y of CG in world coordinates.', '0' ],
                    'gbp_velocity_z': [ 57, 'Velocity Z', 'float', 'Velocity Z of CG in world coordinates.', '0' ],
                    'gbp_rot_mtx': [ 73, 'Rotation Matrix', 'f_array', 'Rotation matrix', '1', '3', '3'],
                  # 'gbp_rot_mtx_0': [ 73, 'Rotation Matrix 0', 'float', 'Rotation matrix', '1', '0', '0'],
                  # 'gbp_rot_mtx_1': [ 77, 'Rotation Matrix 1', 'float', 'Rotation matrix', '1', '1', '0'],
                  # 'gbp_rot_mtx_2': [ 81, 'Rotation Matrix 2', 'float', 'Rotation matrix', '1', '2', '0'],
                  # 'gbp_rot_mtx_3': [ 85, 'Rotation Matrix 3', 'float', 'Rotation matrix', '1', '1', '0'],
                  # 'gbp_rot_mtx_4': [ 89, 'Rotation Matrix 4', 'float', 'Rotation matrix', '1', '1', '1'],
                  # 'gbp_rot_mtx_5': [ 93, 'Rotation Matrix 5', 'float', 'Rotation matrix', '1', '1', '2'],
                  # 'gbp_rot_mtx_6': [ 97, 'Rotation Matrix 6', 'float', 'Rotation matrix', '2', '2', '0'],
                  # 'gbp_rot_mtx_7': [ 101, 'Rotation Matrix 7', 'float', 'Rotation matrix', '2', '2', '1'],
                  # 'gbp_rot_mtx_8': [ 105, 'Rotation Matrix 8', 'float', 'Rotation matrix', '2', '2', '2'],
                    'gbp_yaw': [ 109, 'Yaw', 'float', 'Yaw', '0'],
                    'gbp_pitch': [ 113, 'Pitch', 'float', 'Pitch', '0'],
                    'gbp_roll': [ 117, 'Roll', 'float', 'Roll', '0'],
                    'gbp_velocity_yaw': [ 121, 'Velocity Yaw', 'float', 'Velocity Yaw', '0'],
                    'gbp_velocity_pitch': [ 125, 'Velocity Pitch', 'float', 'Velocity Pitch', '0'],
                    'gbp_velocity_roll': [ 129, 'Velocity Roll', 'float', 'Velocity Roll', '0'],
                    'gbp_suspension_length1': [ 133, 'Suspension length 1', 'float', 'Suspension length 1', '0'],
                    'gbp_suspension_length2': [ 137, 'Suspension length 2', 'float', 'Suspension length 2', '0'],
                    'gbp_suspension_length1_velocity': [ 141, 'Suspension length 1 velocity', 'float', 'Suspension length 1 velocity', '0'],
                    'gbp_suspension_length2_velocity': [ 145, 'Suspension length 2 velocity', 'float', 'Suspension length 2 velocity', '0'],
                    'gpb_crashed': [ 149, 'Crashed', 'int', 'Crashed? 0 for no, 1 for yes', '0'],
                    'gpb_steer_angle': [ 153, 'Steering angle', 'float', 'Steering angle', '0'],
                    'gpb_throttle': [ 157, 'GAAAAAZZ', 'float', 'Throttle', '0'],
                    'gpb_f_brake': [ 161, 'Front brake', 'float', 'Front brake', '0'],
                    'gpb_r_brake': [ 165, 'Rear brake', 'float', 'Rear brake', '0'],
                    'gpb_clutch': [ 169, 'Clutch', 'float', 'Clutch. 0 to 1. 0 = Fully engaged', '0'],
                    'gpb_front_w_speed': [ 173, 'Front wheel speed', 'float', 'Front wheel speed', '0'],
                    'gpb_rear_w_speed': [ 177, 'Rear wheel speed', 'float', 'Rear wheel speed', '0'],
                    'gpb_wheel_material_front': [ 181, 'Front wheel material', 'int', 'Rear wheel material', '0'],
                    'gpb_wheel_material_rear': [ 185, 'Rear wheel material', 'int', 'Rear wheel material', '0'],
                    'gpb_steering_torque': [ 189, 'Steering torque', 'float', 'Steering torque', '0'],
                    'gpb_pit_limiter': [ 193, 'Pit limiter', 'float', 'Pit limiter', '0'],
                    

                    
                    
                    # TODO: 
                    # - Ammend with the remaining data-structures. (almost done)
                    # - Allow events, session, lap,  split structs
                    }
