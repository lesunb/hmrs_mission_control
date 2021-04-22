from mission_control.ensemble import ensemble_factory, has_intersection_skills_membership_function_facotry




def test_create_ensemble():
    mf = has_intersection_skills_membership_function_facotry(['navigate'])
    ensemble = ensemble_factory(id = 'lab_samples_mission_control', membership = mf)
    assert ensemble.id == 'lab_samples_mission_control'