from mission_control.common_descriptors.routes_ed import Map, Nodes

def create_hospial_scenario_map() -> Map:
    map = Map()
    respiratory_control = Nodes("Respiratory Control", [-37, 35])
    ic_corridor = Nodes("IC Corridor", [-37, 15])
    ic_room_1 = Nodes("IC Room 1", [-38, 35])
    ic_room_2 = Nodes("IC Room 2", [-34, 35])
    ic_room_3 = Nodes("IC Room 3", [-38, 23])
    ic_room_4 = Nodes("IC Room 4", [-34, 17.5])
    ic_room_5 = Nodes("IC Room 5", [-38, 21.5])
    ic_room_6 = Nodes("IC Room 6", [-38, 10])
    pc_corridor = Nodes("PC Corridor", [-19, 16])
    pc_room_1 = Nodes("PC Room 1", [-28.5, 18])
    pc_room_2 = Nodes("PC Room 2", [-27.4, 18])
    pc_room_3 = Nodes("PC Room 3", [-21, 18])
    pc_room_4 = Nodes("PC Room 4", [-19, 18])
    pc_room_5 = Nodes("PC Room 5", [-13.5, 18])
    pc_room_6 = Nodes("PC Room 6", [-11.5, 18])
    pc_room_7 = Nodes("PC Room 7", [-4, 18])
    pc_room_8 = Nodes("PC Room 8", [-27, 13])
    pc_room_9 = Nodes("PC Room 9", [-26, 13])
    pc_room_10 = Nodes("PC Room 10", [-18, 13])
    reception = Nodes("Reception", [-1, 20])
    pharmacy_corridor = Nodes("Pharmacy Corridor", [0, 8])
    pharmacy = Nodes("Pharmacy", [-2, 2.6])

    respiratory_control.add_edges([ic_corridor])

    ic_corridor.add_edges([respiratory_control, ic_room_1, ic_room_2, ic_room_3,
                           ic_room_4, ic_room_5, ic_room_6, pc_corridor])

    ic_room_1.add_edges([ic_corridor])
    ic_room_2.add_edges([ic_corridor])
    ic_room_3.add_edges([ic_corridor])
    ic_room_4.add_edges([ic_corridor])
    ic_room_5.add_edges([ic_corridor])
    ic_room_6.add_edges([ic_corridor])

    pc_corridor.add_edges([ic_corridor, pharmacy_corridor, pc_room_1,
                           pc_room_2, pc_room_3, pc_room_4, pc_room_5,
                           pc_room_6, pc_room_7, pc_room_8, pc_room_9,
                           pc_room_10])

    pc_room_1.add_edges([pc_corridor])
    pc_room_2.add_edges([pc_corridor])
    pc_room_3.add_edges([pc_corridor])
    pc_room_4.add_edges([pc_corridor])
    pc_room_5.add_edges([pc_corridor])
    pc_room_6.add_edges([pc_corridor])
    pc_room_7.add_edges([pc_corridor])
    pc_room_8.add_edges([pc_corridor])
    pc_room_9.add_edges([pc_corridor])
    pc_room_10.add_edges([pc_corridor])

    pharmacy_corridor.add_edges([reception, pc_corridor, pharmacy])
    reception.add_edges([pharmacy_corridor])
    pharmacy.add_edges([pharmacy_corridor])

    map.add_nodes([respiratory_control, ic_corridor, ic_room_1, ic_room_2,
                   ic_room_3, ic_room_4, ic_room_5, ic_room_6, pc_corridor,
                   pc_room_1, pc_room_2, pc_room_3, pc_room_4, pc_room_5,
                   pc_room_6, pc_room_7, pc_room_8, pc_room_9, pc_room_10,
                   pharmacy_corridor, reception, pharmacy])
    return map
