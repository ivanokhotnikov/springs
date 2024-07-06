from math import pi, sqrt

MATERIAL = {
    1: {
        'name': 'EN 10270-1',
        'E': 206e9,
        'G': 81.5e9,
        'rho': 7850
    },
    2: {
        'name': 'EN 10270-2',
        'E': 206e9,
        'G': 79.5e9,
        'rho': 7850
    },
    3: {
        'name': 'EN 10089',
        'E': 206e9,
        'G': 78.5e9,
        'rho': 7850
    },
    4: {
        'name': 'CuSn6 R950 EN 12166',
        'E': 115e9,
        'G': 42e9,
        'rho': 8730
    },
    5: {
        'name': 'CuSn36 R700 EN 12166',
        'E': 110e9,
        'G': 39e9,
        'rho': 8400
    },
    6: {
        'name': 'CuBe2 EN 12166',
        'E': 120e9,
        'G': 47e9,
        'rho': 8800
    },
    7: {
        'name': 'CuCo2Be EN 12166',
        'E': 130e9,
        'G': 48e9,
        'rho': 8800
    },
}

def get_material_choice():
    print("Choose a material:")
    for key, mat_data in MATERIAL.items():
        print(f"{key}. {mat_data['name']}")
    choice = int(input("Enter your choice (1-7): "))
    return MATERIAL.get(choice)

def calculate_compression_spring(material):
    print("=== Compression Spring Calculation ===")
    outside_dia = float(input("Outside diameter (mm): "))
    inside_dia = float(input("Inside diameter (mm): "))
    wire_dia = float(input("Wire diameter (mm): "))
    active_coils = float(input("Number of active coils: "))
    deflection = float(input("Deflection (mm): "))

    mean_dia = (outside_dia + inside_dia) / 2
    spring_index = mean_dia / wire_dia
    stress_correction = (spring_index + .5) / (spring_index - .75)
    spring_rate = material['G'] * wire_dia**4 / (8 * mean_dia**3 * active_coils)
    spring_work = material['G'] * wire_dia**4 * deflection / (8 * mean_dia**3 * active_coils)
    force = material['G'] * wire_dia**4 * deflection / (8 * mean_dia**3 * active_coils)
    torsional_stress = material['G'] * wire_dia * deflection / (pi * active_coils * mean_dia**2)
    fund_frequency = 3560 * wire_dia * sqrt(material['G'] / material['rho']) / (active_coils * mean_dia**2)

    print(f'Rate = {round(spring_rate*1e-3, 2)} N/mm')
    print(f'Torsional stress = {round(torsional_stress*1e-6, 2)} MPa')
    print(f'Fundamental frequency = {round(fund_frequency*1e-3, 2)} kHz')

def calculate_torsion_spring(material):
    print("=== Torsion Spring Calculation ===")
    outside_dia = float(input("Outside diameter (mm): "))
    inside_dia = float(input("Inside diameter (mm): "))
    wire_dia = float(input("Wire diameter (mm): "))
    active_coils = float(input("Number of active coils: "))
    deflection = float(input("Deflection (degrees): "))

    mean_dia = (outside_dia + inside_dia) / 2
    spring_index = mean_dia / wire_dia
    spring_rate = wire_dia**4 * material['E'] / (3667 * mean_dia * active_coils)
    spring_torque = wire_dia**4 * material['E'] * deflection / (3667 * mean_dia * active_coils)
    outside_coil_dia = mean_dia * active_coils / (active_coils - deflection / 360) + wire_dia
    inside_coil_dia = mean_dia * active_coils / (active_coils + deflection / 360) - wire_dia
    torsional_angle = 3667 * mean_dia * spring_torque * active_coils / (material['E'] * wire_dia**4)
    bending_stress = 32 * spring_torque / (pi * wire_dia ** 3)

    print(f'Rate = {round(spring_rate, 2)} N/deg')
    print(f'Spring torque = {round(spring_torque, 2)} N m')
    print(f'Outside coil diameter = {round(outside_coil_dia*1e3, 2)} mm')
    print(f'Inside coil diameter = {round(inside_coil_dia*1e3, 2)} mm')

# Main program (For user input dialog)
while True:
    print("\nMenu:")
    print("1. Calculate Compression Spring")
    print("2. Calculate Torsion Spring")
    print("3. Exit")

    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        material = get_material_choice()
        if material:
            calculate_compression_spring(material)
        else:
            print("Invalid material choice. Please choose again.")
    elif choice == '2':
        material = get_material_choice()
        if material:
            calculate_torsion_spring(material)
        else:
            print("Invalid material choice. Please choose again.")
    elif choice == '3':
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Please choose again.")
