
#some basic colors
clearer='#fd94aeff'
darker='#da76a2ff'
kblue='#569bd2ff'
# data_files.py
#Each row gives filename, short name, type (Direct bound/projected bound/projected curve/ indirect bound), color, depth level in plot

detector_data = [
    # Direct bounds. They are plotted as shaded areas, so line width and dash style will be ignored
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/DetectorCurves/BAW.txt', 'BAW', 'Direct bound', darker, 1, 'solid', 1,'glyph'),
    ('Curves/DetectorCurves/OSQAR.txt', 'OSQAR', 'Direct bound', clearer, 1, 'solid', 1,'glyph' ),
    ('Curves/DetectorCurves/CAST.txt', 'CAST', 'Direct bound', clearer, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/HOL.txt', 'HOL', 'Direct bound', clearer, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/Akutsu.txt', 'Akutsu', 'Direct bound', clearer, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/MagnonLow.txt', 'MagnonLow', 'Direct bound', clearer, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/MagnonHigh.txt', 'MagnonHigh', 'Direct bound', clearer, 1, 'solid', 1, 'glyph'),
    # Projected bounds. They are plotted as curves, so include line style
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/DetectorCurves/LSDweak.txt', 'LSDweak', 'Projected bound', darker, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/LSDstrong.txt', 'LSDstrong', 'Projected bound', clearer, 1, 'solid',  1, 'underlay'),
    ('Curves/DetectorCurves/IAXOSPD.txt', 'IAXOSPD', 'Projected bound', clearer, 1, 'solid', 1,  'glyph'),
    ('Curves/DetectorCurves/IAXOHET.txt', 'IAXOHET', 'Projected bound', darker, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/IAXO.txt', 'IAXO', 'Projected bound', darker, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/ALPSII.txt', 'ALPSII', 'Projected bound', darker, 1, 'solid', 1,  'glyph'),
    ('Curves/DetectorCurves/JURA.txt', 'JURA', 'Projected bound', clearer, 1, 'solid', 1,  'glyph'),
    ('Curves/DetectorCurves/ADMX.txt', 'ADMX', 'Projected bound', '#bd618aff', 1, 'solid', 1,  'glyph'),
    ('Curves/DetectorCurves/HAYSTAC.txt', 'HAYSTAC', 'Projected bound', clearer, 1, 'solid', 1,  'glyph'),
    ('Curves/DetectorCurves/CAPP.txt', 'CAPP', 'Projected bound', 'black', 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/SQMS.txt', 'SQMS', 'Projected bound', clearer, 1, 'solid', 1, 'underlay'),
    ('Curves/DetectorCurves/GaussianBeamWeak.txt', 'GaussianBeamWeak', 'Projected bound', darker, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/GaussianBeamStrong.txt', 'GaussianBeamStrong', 'Projected bound', darker, 1, 'dashed', 1, 'glyph'),
    ('Curves/DetectorCurves/ORGAN.txt', 'ORGAN', 'Projected bound', darker, 1, 'solid', 1, 'glyph'),
    # Projected Curves
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/DetectorCurves/ResonantAntennas.txt', 'Resonant Antennas', 'Projected curve', darker, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/DMR8.txt', 'DMR 8', 'Projected curve', darker, 1, 'solid',  1, 'glyph'),
    ('Curves/DetectorCurves/DMR100.txt', 'DMR 100', 'Projected curve', clearer, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/BBO.txt', 'BBO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/CE.txt', 'CE', 'Projected curve', kblue, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/DECIGO.txt', 'DECIGO', 'Projected curve', kblue, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/ET.txt', 'ET', 'Projected curve', kblue, 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/LISA.txt', 'LISA', 'Projected curve', kblue, 1, 'solid', 1, 'glyph'),
    # Indirect bounds
    #(file, label, category, color, linewidth,linestyle, opacity,  depth level)
    ('Curves/DetectorCurves/StrongARCADE.txt', 'ARCADEstrong', 'Indirect bound', 'darkgreen', 1, 'solid',  1, 'underlay'),
    ('Curves/DetectorCurves/WeakARCADE.txt', 'ARCADEweak', 'Indirect bound', 'green', 1, 'solid', 1, 'underlay'),
    ('Curves/DetectorCurves/EDGESstrong.txt', 'EDGESstrong', 'Indirect bound', 'darkgreen', 1, 'solid', 1, 'glyph'),
    ('Curves/DetectorCurves/EDGESweak.txt', 'EDGESweak', 'Indirect bound', 'green', 1, 'solid', 1, 'glyph'),
    # ... (other file paths and labels)
]

signal_data = [
    #(file, label, category, color, linewidth,linestyle, opacity, depth level)
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-11', 'Global string Gmu=1E-11', 'Signal curve', 'gray', 2, 'solid', 1, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-12', 'Global string Gmu=1E-12', 'Signal curve', 'gray', 2, 'solid', 0.85, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-13', 'Global string Gmu=1E-13', 'Signal curve', 'gray', 2, 'solid', 0.7, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-14', 'Global string Gmu=1E-14', 'Signal curve', 'gray', 2, 'solid', 0.55, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-15', 'Global string Gmu=1E-15', 'Signal curve', 'gray', 2, 'solid', 0.4, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-16', 'Global string Gmu=1E-16', 'Signal curve', 'gray', 2, 'solid', 0.25, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/Strings/String_hc_spectrum_Gmu=1E-17', 'Global string Gmu=1E-17', 'Signal curve', 'gray', 2, 'solid', 0.1, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_1.txt', 'SMASH 1', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph'),
    ('Curves/SignalCurves/CosmologicalSources/hc_SMASH_full_benchmark_2.txt', 'SMASH2', 'Signal curve', 'orangered', 2, 'solid', 1, 'glyph'),
    ]
