import numpy as np
from matplotlib import pyplot as plt
#some basic colors
clearer='#fd94aeff'
darker='#da76a2ff'
kblue='#569bd2ff'
# data_files.py
#matplotlib default colors
#hc -> (8.54826*10^-19 Sqrt[Omega])/f
prop_cycle = plt.rcParams['axes.prop_cycle']
mplcolors = prop_cycle.by_key()['color']

#Each row gives filename, short name, type (Direct bound/projected bound/projected curve/ indirect bound), color, depth level in plot
detector_data = [
    # Direct bounds. They are plotted as shaded areas, so line width and dash style will be ignored
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ('Curves/DetectorCurves/BAW.txt', 'BAW', 'Direct bound', darker, 1, 'solid', 1,'glyph', None, 1.E6+7.E7,2.4e-19+ 2.E-17, np.pi/2, 'white', '9pt' ),
    ('Curves/DetectorCurves/OSQAR.txt', 'OSQAR', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, 1.2E15,6e-26 +2*10**-26, np.pi/2, 'white', '9pt'),
    ('Curves/DetectorCurves/CAST.txt', 'CAST', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', 'Comment on CAST.',1.4E18, 5e-28+2.E-27, np.pi/2, 'white', '7pt'),
    ('Curves/DetectorCurves/HOL.txt', 'HOL', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', 'Comment on HOL.',1e6+ 6*10**6, 2e-18+2*10**-17, np.pi/2, 'white', '9pt'),
    ('Curves/DetectorCurves/Akutsu.txt', 'Akutsu', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None,1e8+0.5*10**9, 9.8e-14, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/MagnonLow.txt', 'Magnon 2', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, None, None, np.pi/2, clearer, '7pt'),
    ('Curves/DetectorCurves/MagnonHigh.txt', 'Magnon 1', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, 1.27e10+10**10, 1.3e-13-12.9*10**-14, np.pi/2, clearer, '7pt'),
    # Projected bounds. They are plotted as curves, so include line style
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ('Curves/DetectorCurves/LSDweak.txt', 'LSD 2', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 1e4,1.07e-18+ 5*10**-15, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/LSDstrong.txt', 'LSD 1', 'Projected bound', clearer, 1, 'solid',  1, 'underlay', None, None, None, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/IAXOSPD.txt', 'IAXOSPD', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', 'Comment on IAXOSPD.', 2.5e10+3.E11, 8.79e-26, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/IAXOHET.txt', 'IAXOHET', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 2e10 + 4.3E11, 1.1e-22 + 2*10**-22, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/IAXO.txt', 'IAXO', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, None, None, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/ALPSII.txt', 'ALPSII', 'Projected bound', darker, 1, 'solid', 1,  'glyph', None, None, None, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/JURA.txt', 'JURA', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', None, None, None, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/ADMX.txt', 'ADMX', 'Projected bound', '#bd618aff', 1, 'solid', 1,  'glyph', None, 0.65e9 + 0.8e9, 2.32687e-18-2.31e-18, np.pi/2, '#bd618aff', '7pt'),
    ('Curves/DetectorCurves/HAYSTAC.txt', 'HAYSTAC', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', None, 5.6e9 + 6.E9,  1.21542e-17 - 1.215E-17, np.pi/2, clearer, '7pt'),
    ('Curves/DetectorCurves/CAPP.txt', 'CAPP', 'Projected bound', 'gray', 1, 'solid', 1, 'glyph', None, None, None, np.pi/2,  'gray', '7pt'),
    ('Curves/DetectorCurves/SQMS.txt', 'SQMS', 'Projected bound', clearer, 1, 'solid', 1, 'underlay', None, 1e9 + 3*10**9,  1.48628e-18 - 1.45*10**-18, np.pi/2,  clearer, '7pt'),
    ('Curves/DetectorCurves/GaussianBeamWeak.txt', 'G.B. 2', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, None, None, np.pi/2,  darker, '9pt'),
    ('Curves/DetectorCurves/GaussianBeamStrong.txt', 'G.B. 1', 'Projected bound', darker, 1, 'dashed', 1, 'glyph', None, None, None, np.pi/2 ,  darker, '9pt'),
    ('Curves/DetectorCurves/ORGAN.txt', 'ORGAN', 'Projected bound', 'black', 1, 'solid', 1, 'glyph', None, 26.531e9 + 3.E11, 2.10855e-15, np.pi/2,  'black', '7pt'),
    # Projected Curves
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    #('Curves/DetectorCurves/ResonantAntennas.txt', 'Res. antennas', 'Projected curve', darker, 1, 'solid', 1, 'glyph', None, None, None, 0,  darker, '9pt'),
    ('Curves/DetectorCurves/DMR8.txt', 'DMR 8', 'Projected curve', darker, 1, 'solid',  1, 'glyph', None, None, None, np.pi/2,  darker, '9pt'),
    ('Curves/DetectorCurves/DMR100.txt', 'DMR 100', 'Projected curve', clearer, 1, 'solid', 1, 'glyph', None, None, None, np.pi/2,  clearer, '9pt'),
    ('Curves/DetectorCurves/BBO.txt', 'BBO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', 'Comment on BBO.',1e-3+10**-1,4.440521733552400e-22 - 4.44051*10**-22, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/CE.txt', 'CE', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, None, None, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/DECIGO.txt', 'DECIGO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, 2.E-4, 8.E-21, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/ET.txt', 'ET', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, None, None, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/LISA.txt', 'LISA', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, None, None, 0, kblue, '9pt'),
    # Indirect bounds
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ('Curves/DetectorCurves/StrongARCADE.txt', 'ARCADE 1', 'Indirect bound', 'darkgreen', 1, 'solid',  1, 'underlay', None, None, None, np.pi/2, 'darkgreen', '9pt'),
    ('Curves/DetectorCurves/WeakARCADE.txt', 'ARCADE 2', 'Indirect bound', 'green', 1, 'solid', 1, 'underlay', None, 3.e9+4.E8, 1.4e-14, np.pi/2, 'green', '7pt'),
    ('Curves/DetectorCurves/EDGESstrong.txt', 'EDGES 1', 'Indirect bound', 'darkgreen', 1, 'solid', 1, 'glyph', 'Comment on EDGEstrong.', None, None, np.pi/2,  'darkgreen', '9pt'),
    ('Curves/DetectorCurves/EDGESweak.txt', 'EDGES 2', 'Indirect bound', 'green', 1, 'solid', 1, 'glyph', None, None, None, np.pi/2,  'green', '8pt'),
    # ... (other file paths and labels)
]

signal_data = [
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ###Global strings
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-11', 'Global string Gmu=1E-11', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', 'Comment on global strings: ', 0, 0, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-12', 'Global string Gmu=1E-12', 'Signal curve', 'gray', 2, 'solid', 0.85, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-13', 'Global string Gmu=1E-13', 'Signal curve', 'gray', 2, 'solid', 0.7, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-14', 'Global string Gmu=1E-14', 'Signal curve', 'gray', 2, 'solid', 0.55, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-15', 'Global string Gmu=1E-15', 'Signal curve', 'gray', 2, 'solid', 0.4, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-16', 'Global string Gmu=1E-16', 'Signal curve', 'gray', 2, 'solid', 0.25, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-17', 'Global string Gmu=1E-17', 'Signal curve', 'gray', 2, 'solid', 0.1, 'glyph', None, None, None, 0, 'gray', '9pt'),
    ####PBHs
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass6.txt', 'PBH_MPBH=1E-6', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', 'Comment on PBH : ', 0, 0, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass7.txt', 'PBH_MPBH=1E-7', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass8.txt', 'PBH_MPBH=1E-8', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass9.txt', 'PBH_MPBH=1E-9', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass10.txt', 'PBH_MPBH=1E-10', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass11.txt', 'PBH_MPBH=1E-11', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass12.txt', 'PBH_MPBH=1E-12', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass13.txt', 'PBH_MPBH=1E-13', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass14.txt', 'PBH_MPBH=1E-14', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass15.txt', 'PBH_MPBH=1E-15', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/PBHs/Stochastic/PBH_Stochastic_h_mass16.txt', 'PBH_MPBH=1E-16', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, None, None, 0,  'gray', '9pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_1.txt', 'SMASH 1', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph', None, 8E5, 9E-34, 0, 'orangered', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_2.txt', 'SMASH2', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph', None, 8E9, 1E-34, 0, 'orangered', '9pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Inflation - EFT.txt', 'Inflation-EFT', 'Signal line', mplcolors[0], 2, 'solid', 1, 'glyph', None, 2.E0, 3E-25, -0.732815, mplcolors[0], '7pt'),#-3.50251e-9+5.1*(8.54826e-19*np.sqrt(2.e-13)/1.e2)
    ('Curves/SignalCurves/CosmologicalSources/Inflation - scalar perturbations.txt', 'Inflation-scalar pert.', 'Signal line', mplcolors[1], 2, 'solid', 1, 'glyph', None, 1.E-3, 2E-21,-0.785397, mplcolors[1], '7pt'),
    ('Curves/SignalCurves/CosmologicalSources/Inflation - extra-species.txt', 'Inflation-extra species', 'Signal line', mplcolors[2], 2, 'solid', 1, 'glyph', None, 1.E3, 1.5E-29, -1.*0.785398, mplcolors[2], '7pt'),
    ###
    ('Curves/SignalCurves/CosmologicalSources/PhaseTransitions_12.txt', 'Phase trans. (env.)', 'Signal line', mplcolors[3], 2, 'solid', 1, 'glyph', None, 0, 0, -1.*np.pi/4, mplcolors[3], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Oscillons.txt', 'Oscillons', 'Signal line', mplcolors[4], 2, 'solid', 1, 'glyph', None, 2E6, 1e-31,-1.*0.887245, mplcolors[4], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Metastable strings.txt', 'Metastable strings', 'Signal line', mplcolors[5], 2, 'solid', 1, 'glyph', None, 1E3, 1E-24, -1.*np.pi/4, mplcolors[5], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Strings.txt', 'Cosmic strings (env.)', 'Signal line', mplcolors[6], 2, 'solid', 1, 'glyph', None, 1E3, 1.2E-27, -1.*np.pi/4, mplcolors[6], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Gauge textures.txt', 'Gauge textures', 'Signal line', mplcolors[7], 2, 'solid', 1, 'glyph', None, 1.2E11, 3.E-33, np.pi/4, mplcolors[7], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Preheating1.txt', 'Preheating (quart.)', 'Signal line', mplcolors[8], 2, 'solid', 1, 'glyph', None, 1E8, 1E-33, -1.*np.pi/4, mplcolors[8], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Preheating2.txt', 'Preheating (quadr.)', 'Signal line', mplcolors[9], 2, 'solid', 1, 'glyph', None, 1E8, 2E-32, -1.*np.pi/4, mplcolors[9], '7pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/hcCGMB_SM_Mp','CGMB',  'Signal curve', mplcolors[2], 2, 'solid', 1, 'glyph', None, None, None, 0, mplcolors[2], '9pt'),
    (' ','Global strings', 'Signal curve', mplcolors[0], 2, 'solid', 1, 'glyph', None, None, None, 0, mplcolors[0], '9pt'),
    (' ','1st-order p.t.',  'Signal curve', mplcolors[1], 2, 'solid', 1, 'glyph', None, None, None, np.pi/4, mplcolors[1], '9pt'),
    (' ','PBHs', 'Signal curve', mplcolors[3], 2, 'solid', 1, 'glyph', None, None, None, 0, mplcolors[3], '9pt'),
    ]

theoretical_bounds_data = [#(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
     ('Curves/TheoreticalBoundsCurves/DR.txt', 'D.R. bound',  'Theoretical Bound', 'gray', 2, 'dashed', 1, 'glyph', None,1.E15, 4.81E-37, -np.pi/4, 'gray', '9pt')]
