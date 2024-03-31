import numpy as np
#some basic colors
clearer='#fd94aeff'
darker='#da76a2ff'
kblue='#569bd2ff'
# data_files.py
#Each row gives filename, short name, type (Direct bound/projected bound/projected curve/ indirect bound), color, depth level in plot

detector_data = [
    # Direct bounds. They are plotted as shaded areas, so line width and dash style will be ignored
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ('Curves/DetectorCurves/BAW.txt', 'BAW', 'Direct bound', darker, 1, 'solid', 1,'glyph', None, 7.E7, 2.E-17, np.pi/2, 'white', '9pt' ),
    ('Curves/DetectorCurves/OSQAR.txt', 'OSQAR', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, 1.3E15, +2*10**-26, np.pi/2, 'white', '9pt'),
    ('Curves/DetectorCurves/CAST.txt', 'CAST', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', 'Comment on CAST.', 1.2E18, 2.E-27, np.pi/2, 'white', '7pt'),
    ('Curves/DetectorCurves/HOL.txt', 'HOL', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', 'Comment on HOL.', 6*10**6, 2*10**-17, np.pi/2, 'white', '9pt'),
    ('Curves/DetectorCurves/Akutsu.txt', 'Akutsu', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None,0.5*10**9, 0, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/MagnonLow.txt', 'Magnon 2', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2, clearer, '7pt'),
    ('Curves/DetectorCurves/MagnonHigh.txt', 'Magnon 1', 'Direct bound', clearer, 1, 'solid', 1, 'glyph', None, 10**10, -12.9*10**-14, np.pi/2, clearer, '7pt'),
    # Projected bounds. They are plotted as curves, so include line style
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/DetectorCurves/LSDweak.txt', 'LSD 2', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 0, 5*10**-15, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/LSDstrong.txt', 'LSD 1', 'Projected bound', clearer, 1, 'solid',  1, 'underlay', None, 0, 0, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/IAXOSPD.txt', 'IAXOSPD', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', 'Comment on IAXOSPD.', 3.E11, 0, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/IAXOHET.txt', 'IAXOHET', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 4.3E11, 2*10**-22, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/IAXO.txt', 'IAXO', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/ALPSII.txt', 'ALPSII', 'Projected bound', darker, 1, 'solid', 1,  'glyph', None, 0, 0, np.pi/2, darker, '9pt'),
    ('Curves/DetectorCurves/JURA.txt', 'JURA', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', None, 0, 0, np.pi/2, clearer, '9pt'),
    ('Curves/DetectorCurves/ADMX.txt', 'ADMX', 'Projected bound', '#bd618aff', 1, 'solid', 1,  'glyph', None, 0.8*10**9, -2.31*10**-18, np.pi/2, '#bd618aff', '7pt'),
    ('Curves/DetectorCurves/HAYSTAC.txt', 'HAYSTAC', 'Projected bound', clearer, 1, 'solid', 1,  'glyph', None, 6.E9, -1.22E-17, np.pi/2, clearer, '7pt'),
    ('Curves/DetectorCurves/CAPP.txt', 'CAPP', 'Projected bound', 'gray', 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2,  'gray', '7pt'),
    ('Curves/DetectorCurves/SQMS.txt', 'SQMS', 'Projected bound', clearer, 1, 'solid', 1, 'underlay', None, 3*10**9, -1.45*10**-18, np.pi/2,  clearer, '7pt'),
    ('Curves/DetectorCurves/GaussianBeamWeak.txt', 'G.B. 2', 'Projected bound', darker, 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2,  darker, '9pt'),
    ('Curves/DetectorCurves/GaussianBeamStrong.txt', 'G.B. 1', 'Projected bound', darker, 1, 'dashed', 1, 'glyph', None, 0, 0, np.pi/2 ,  darker, '9pt'),
    ('Curves/DetectorCurves/ORGAN.txt', 'ORGAN', 'Projected bound', 'black', 1, 'solid', 1, 'glyph', None, 3.E11, 0, np.pi/2,  'black', '7pt'),
    # Projected Curves
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/DetectorCurves/ResonantAntennas.txt', 'Res. antennas', 'Projected curve', darker, 1, 'solid', 1, 'glyph', None, 0, 0, 0,  darker, '9pt'),
    ('Curves/DetectorCurves/DMR8.txt', 'DMR 8', 'Projected curve', darker, 1, 'solid',  1, 'glyph', None, 0, 0, np.pi/2,  darker, '9pt'),
    ('Curves/DetectorCurves/DMR100.txt', 'DMR 100', 'Projected curve', clearer, 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2,  clearer, '9pt'),
    ('Curves/DetectorCurves/BBO.txt', 'BBO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', 'Comment on BBO.',10**-1, -4.44051*10**-22, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/CE.txt', 'CE', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, 0, 0, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/DECIGO.txt', 'DECIGO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, 0, 0, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/ET.txt', 'ET', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, 0, 0, 0, kblue, '9pt'),
    ('Curves/DetectorCurves/LISA.txt', 'LISA', 'Projected curve', kblue, 1, 'solid', 1, 'glyph', None, 0, 0, 0, kblue, '9pt'),
    # Indirect bounds
    #(file, label, category, color, linewidth,linestyle, opacity,  depth level)
    ('Curves/DetectorCurves/StrongARCADE.txt', 'ARCADE 1', 'Indirect bound', 'darkgreen', 1, 'solid',  1, 'underlay', None, 0, 0, np.pi/2, 'darkgreen', '9pt'),
    ('Curves/DetectorCurves/WeakARCADE.txt', 'ARCADE 2', 'Indirect bound', 'green', 1, 'solid', 1, 'underlay', None, 4.E8, 0, np.pi/2, 'green', '7pt'),
    ('Curves/DetectorCurves/EDGESstrong.txt', 'EDGES 1', 'Indirect bound', 'darkgreen', 1, 'solid', 1, 'glyph', 'Comment on EDGEstrong.', 0, 0, np.pi/2,  'darkgreen', '9pt'),
    ('Curves/DetectorCurves/EDGESweak.txt', 'EDGES 2', 'Indirect bound', 'green', 1, 'solid', 1, 'glyph', None, 0, 0, np.pi/2,  'green', '8pt'),
    # ... (other file paths and labels)
]

signal_data = [
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-11', 'Global string Gmu=1E-11', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', 'Comment on Gmu = -11.', 0, 0, 0,  'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-12', 'Global string Gmu=1E-12', 'Signal curve', 'gray', 2, 'solid', 0.85, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-13', 'Global string Gmu=1E-13', 'Signal curve', 'gray', 2, 'solid', 0.7, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-14', 'Global string Gmu=1E-14', 'Signal curve', 'gray', 2, 'solid', 0.55, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-15', 'Global string Gmu=1E-15', 'Signal curve', 'gray', 2, 'solid', 0.4, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-16', 'Global string Gmu=1E-16', 'Signal curve', 'gray', 2, 'solid', 0.25, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-17', 'Global string Gmu=1E-17', 'Signal curve', 'gray', 2, 'solid', 0.1, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_1.txt', 'SMASH 1', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_2.txt', 'SMASH2', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    (' ','Global string', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, 0, 0, 0, 'gray', '9pt'),
    (' ','1st-order p.t.',  'Signal curve', 'gray', 2, 'solid', 1, 'glyph', None, 0, 0, np.pi/4, 'gray', '9pt')
    ]
