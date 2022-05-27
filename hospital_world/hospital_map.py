from mission_control.common_descriptors.routes_ed import Map, Nodes

def create_hospital_scenario_map() -> Map:
    map = Map()
    respiratory_control = Nodes("Respiratory Control", [-37, 36])
    ic_corridor_1 = Nodes("IC Corridor 1",[-37.00, 10.00])
    ic_corner = Nodes("IC Corner",[-37.00,16.00])
    ic_corridor_2 = Nodes("IC Corridor 2",[-37.00, 21.50])
    ic_corridor_3 = Nodes("IC Corridor 3",[-37.00, 25.37])
    ic_corridor_4 = Nodes("IC Corridor 4",[-37.00, 33.95])
    ic_corridor_5 = Nodes("IC Corridor 5",[-37.00, 33.98])
    ic_corridor_6 = Nodes("IC Corridor 6",[-37.00, 18.93])

    ic_room_1 = Nodes("IC Room 1",[-38.00, 10.00, 0.00])
    ic_room_2 = Nodes("IC Room 2",[-38.00, 21.50, 0.00])
    ic_room_3 = Nodes("IC Room 3",[-40.23, 25.37, 0.00])
    ic_room_4 = Nodes("IC Room 4",[-39.44, 33.95, 0.00])
    ic_room_5 = Nodes("IC Room 5",[-32.88, 33.98, 3.14])
    ic_room_6 = Nodes("IC Room 6",[-33.90, 18.93, 3.14])

    pc_corridor_1 = Nodes("PC Corridor 1",[-27.25, 16.00])
    pc_corridor_2 = Nodes("PC Corridor 2",[-18.00, 16.00])
    pc_corridor_3 = Nodes("PC Corridor 3",[-28.50, 16.00])
    pc_corridor_4 = Nodes("PC Corridor 4",[-27.23, 16.00])
    pc_corridor_5 = Nodes("PC Corridor 5",[-21.00, 16.00])
    pc_corridor_6 = Nodes("PC Corridor 6",[-19.00, 16.00])
    pc_corridor_7 = Nodes("PC Corridor 7",[-13.50, 16.00])
    pc_corridor_8 = Nodes("PC Corridor 8",[-11.50, 16.00])

    pc_room_1 = Nodes("PC Room 1",[-27.25, 13.00, 1.57])
    pc_room_2 = Nodes("PC Room 2",[-18.00, 13.00, 1.57])
    pc_room_3 = Nodes("PC Room 3",[-28.50, 18.00,-1.57])
    pc_room_4 = Nodes("PC Room 4",[-27.23, 18.00,-1.57])
    pc_room_5 = Nodes("PC Room 5",[-21.00, 18.00,-1.57])
    pc_room_6 = Nodes("PC Room 6",[-19.00, 18.00,-1.57])
    pc_room_7 = Nodes("PC Room 7",[-13.50, 18.00,-1.57])
    pc_room_8 = Nodes("PC Room 8",[-11.50, 18.00,-1.57])

    lab_corridor = Nodes("Laboratory Corridor",[-26.00, 16.00])
    lab = Nodes("Laboratory",[-26.00, 13.00, 1.57])

    respiratory_control.add_edges([ic_corridor_5])

    ic_corridor_1.add_edges([ic_room_1, ic_corner])
    ic_corner.add_edges([ic_corridor_1, ic_corridor_6, pc_corridor_3])
    ic_corridor_6.add_edges([ic_room_6, ic_corridor_2, ic_corner])
    ic_corridor_2.add_edges([ic_room_2, ic_corridor_6, ic_corridor_3])
    ic_corridor_3.add_edges([ic_room_3, ic_corridor_2, ic_corridor_4])
    ic_corridor_4.add_edges([ic_room_4, ic_corridor_3, ic_corridor_5])
    ic_corridor_5.add_edges([ic_room_5, ic_corridor_4, respiratory_control])

    ic_room_1.add_edges([ic_corridor_1])
    ic_room_2.add_edges([ic_corridor_2])
    ic_room_3.add_edges([ic_corridor_3])
    ic_room_4.add_edges([ic_corridor_4])
    ic_room_5.add_edges([ic_corridor_5])
    ic_room_6.add_edges([ic_corridor_6])

    pc_corridor_3.add_edges([ic_corner, pc_room_3, pc_corridor_1])
    pc_corridor_1.add_edges([pc_room_1, pc_corridor_3, pc_corridor_4])
    pc_corridor_4.add_edges([pc_room_4, pc_corridor_1, lab_corridor])
    lab_corridor.add_edges([lab, pc_corridor_4, pc_corridor_5])
    pc_corridor_5.add_edges([pc_room_5, lab_corridor, pc_corridor_6])
    pc_corridor_6.add_edges([pc_room_6, pc_corridor_5, pc_corridor_2])
    pc_corridor_2.add_edges([pc_room_2, pc_corridor_6, pc_corridor_7])
    pc_corridor_7.add_edges([pc_room_7, pc_corridor_2, pc_corridor_8])
    pc_corridor_8.add_edges([pc_room_8, pc_corridor_7])

    pc_room_1.add_edges([pc_corridor_1])
    pc_room_2.add_edges([pc_corridor_2])
    pc_room_3.add_edges([pc_corridor_3])
    pc_room_4.add_edges([pc_corridor_4])
    pc_room_5.add_edges([pc_corridor_5])
    pc_room_6.add_edges([pc_corridor_6])
    pc_room_7.add_edges([pc_corridor_7])
    pc_room_8.add_edges([pc_corridor_8])

    lab.add_edges([lab_corridor])

    map.add_nodes([respiratory_control, ic_corner,
                   ic_corridor_1, ic_corridor_2, ic_corridor_3,
                   ic_corridor_4, ic_corridor_5, ic_corridor_6,
                   ic_room_1, ic_room_2, ic_room_3, ic_room_4, ic_room_5, ic_room_6,
                   pc_corridor_1, pc_corridor_2, pc_corridor_3, pc_corridor_4,
                   pc_corridor_5, pc_corridor_6, pc_corridor_7, pc_corridor_8,
                   pc_room_1, pc_room_2, pc_room_3, pc_room_4, pc_room_5,
                   pc_room_6, pc_room_7, pc_room_8, lab, lab_corridor])
    return map
