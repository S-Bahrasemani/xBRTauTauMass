
# BE CAREFUL, THE ORDER
# MATTERS -- TMVA YOU SUCK :-(


## HADHAD ORDER !!



# FEATURES = [
    
#     'dR_tau1_tau2',
#     'MET_et',
#     'sum_pt_tau1_tau2_met',
#     'transverse_mass_tau1_met',
#     'transverse_mass_tau2_met',
#     'pt_diff_tau1_tau2',

#     'mass_vis_tau1_tau2',
#     'sum_pt_tau1_tau2', 
#     'dPhi_tau1_tau2',
#     'transverse_mass_tau1_tau2',
    
#     'tau1_pt',  
#     'mass_collinear_tau1_tau2',
    
#     'cos_theta_tau1_tau2',
    
#     'tau2_pt',
#     'tau1_eta',
#     'tau2_eta',
    
#     'dPhi_tau1_MET',
#     'dPhi_tau2_MET',
#     'dPhi_tau1_tau2_MET',
    
#     'vector_sum_pt_tau1_tau2',
#     'vector_sum_pt_tau1_tau2_met',
    

#     ]




### LEPHAD ORDER



FEATURES = [
    
    'dR_tau1_tau2',
    'MET_et',
    'sum_pt_tau1_tau2_met',
    'transverse_mass_tau1_met',
    'transverse_mass_tau2_met',
    'pt_diff_tau1_tau2',
    'mass_vis_tau1_tau2',
    'sum_pt_tau1_tau2', 
    'dPhi_tau1_tau2',
    'dPhi_tau1_tau2_MET',
    'dPhi_tau1_MET',
    'transverse_mass_tau1_tau2',
    'tau1_pt',   
    'cos_theta_tau1_tau2',
    'tau2_pt',

    ]
#     'tau1_eta',
#     'tau2_eta',
#     'dPhi_tau2_MET',
#     'vector_sum_pt_tau1_tau2',
#     'vector_sum_pt_tau1_tau2_met',
#     'mass_collinear_tau1_tau2',
    
#     ]




### not very useful taus kinematics



#### ##### RELATIVE kinematics of jets and taus

# 'mass_ratio_jets_taus',
# 'sum_pt_ratio_jets_taus',
# 'vector_sum_pt_ratio_jets_taus',
# 'sum_pt_ratio_full_tausMET',
# 'dR_ratio_jets_taus',



# ####  NOT USEFUl FOR BRT  TRAINING , very low correlation with resonance mass ###

# 'dEta_jets',
# 'eta_product_jets',
# 'mass_jet1_jet2',
# 'mass_tau1_tau2_jet1',
# 'met_phi_centrality',
# 'tau1_eta_centrality',
# 'sum_pt_full',
# 'vector_sum_pt_full',
    
features_vbf = FEATURES
features_boosted = FEATURES
