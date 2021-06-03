from math import pi, sqrt

MATERIAL = {
    'EN 10270-1': {
        'E': 206e9,
        'G': 81.5e9,
        'rho': 7850
    },
    'EN 10270-2': {
        'E': 206e9,
        'G': 79.5e9,
        'rho': 7850
    },
    'EN 10089': {
        'E': 206e9,
        'G': 78.5e9,
        'rho': 7850
    },
    'CuSn6 R950 EN 12166': {
        'E': 115e9,
        'G': 42e9,
        'rho': 8730
    },
    'CuSn36 R700 EN 12166': {
        'E': 110e9,
        'G': 39e9,
        'rho': 8400
    },
    'CuBe2 EN 12166': {
        'E': 120e9,
        'G': 47e9,
        'rho': 8800
    },
    'CuCo2Be EN 12166': {
        'E': 130e9,
        'G': 48e9,
        'rho': 8800
    },
}


def calculate_compression_spring(outside_dia,
                                 inside_dia,
                                 wire_dia,
                                 active_coils,
                                 material,
                                 deflection=None,
                                 force=None):
    mean_dia = (outside_dia + inside_dia) / 2
    spring_index = mean_dia / wire_dia
    stress_correction = (spring_index + .5) / (spring_index - .75)
    spring_rate = MATERIAL[material]['G'] * wire_dia**4 / (8 * mean_dia**3 *
                                                           active_coils)
    if deflection:
        spring_work = MATERIAL[material]['G'] * wire_dia**4 * deflection / (
            8 * mean_dia**3 * active_coils)
        force = MATERIAL[material]['G'] * wire_dia**4 * deflection / (
            8 * mean_dia**3 * active_coils)
        torsional_stress = MATERIAL[material]['G'] * wire_dia * deflection / (
            pi * active_coils * mean_dia**2)
    if force:
        torsional_stress = 8 * mean_dia * force / (pi * wire_dia**3)
        deflection = 8 * mean_dia**3 * active_coils * force / (
            MATERIAL[material]['G'] * wire_dia**4)
    fund_frequency = 3560 * wire_dia * sqrt(
        MATERIAL[material]['G'] / MATERIAL[material]['rho']) / (active_coils *
                                                                mean_dia**2)
    print(f'Rate = {round(spring_rate*1e-3, 2)} N/mm',
          f'Torsional stress = {round(torsional_stress*1e-6, 2)} MPa',
          f'Fundamental frequency = {round(fund_frequency*1e-3, 2)} kHz',
          sep='\n')


def calculate_torsion_spring(outside_dia,
                             inside_dia,
                             wire_dia,
                             active_coils,
                             material,
                             deflection=None,
                             torque=None):
    mean_dia = (outside_dia + inside_dia) / 2
    spring_index = mean_dia / wire_dia
    spring_rate = wire_dia**4 * MATERIAL[material]['E'] / (3667 * mean_dia *
                                                           active_coils)
    if deflection:
        spring_torque = wire_dia**4 * MATERIAL[material]['E'] * deflection / (
            3667 * mean_dia * active_coils)
        outside_coil_dia = mean_dia * active_coils / (
            active_coils - deflection / 360) + wire_dia
        inside_coil_dia = mean_dia * active_coils / (
            active_coils + deflection / 360) - wire_dia
    if torque:
        torsional_angle = 3667 * mean_dia * torque * active_coils / (
            MATERIAL[material]['E'] * wire_dia**4)
        bending_stress = 32 * torque / (pi * wire_dia ** 3)
    print(f'Rate = {round(spring_rate, 2)} N/deg',
          f'Spring torque = {round(spring_torque, 2)} N m',
          f'Outside coil diameter = {round(outside_coil_dia*1e3, 2)} mm',
          f'Inside coil diameter = {round(inside_coil_dia*1e3, 2)} mm',
          sep='\n')