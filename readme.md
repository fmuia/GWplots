# GWplots: Gravitational Waves Plotter

### Created, updated and maintained by Francesco Muia, Andreas Ringwald and Carlos Tamarit.

GWplots is an interactive web application designed for visualizing and analyzing gravitational wave data. It offers a user-friendly interface for plotting various gravitational wave signals and detector sensitivity curves, allowing researchers and enthusiasts to explore and interpret gravitational wave data effectively.

## Project Structure

The application is organized as follows:

```
GWplots/                            # Project directory
│
├── Curves                          # Repository containing all the curves to be plotted
│   ├── DetectorCurves              # Repository containing all detector curves
│   └── SignalCurves                # Repository containing all signal curves, divided into "Cosmological sources" and "PBHs"
│       ├── CosmologicalSources
│       └── PBHs
│
├── aux                             # Repository containing auxiliary files
│   ├── aux_functions.py            # File containing auxiliary functions
│   ├── data_files.py               # File containing information about the curves to be plotted
│   └── import.py                   # File containing all the imports
│   
├── static/                         # Static files
│   ├── css/                        # CSS files
│   │   └── styles.css              # Main stylesheet
│   └── js/                         # JavaScript files
│       └── scripts.js              # JavaScript logic
│
├── templates/                      # HTML templates
│   └── index.html                  # Main HTML template
│
├── app.py                          # Main Flask application
└── README.md                       # README file
```

## Features

### Current Features

- Interactive plotting of gravitational wave signals.
- Toggle visibility of different gravitational wave detector sensitivity curves.
- Annotations on the plot that provide additional information.
- Customizable plot ranges and dimensions through interactive sliders.

## Still to be checked

- Make sure that we use a consistent definition of characteristic strain h for the data

### Planned Features

1. **Customization of Annotation Positions and Styles**: Enhance the flexibility in positioning and styling annotations on the plot to cater to various presentation needs.

2. **Multiple Tunable Curves for the Same Signal**: Implement the capability to plot and adjust multiple versions of the same signal, allowing for comparative analysis.

3. **Custom Curve Addition**: Introduce options for users to add their custom curves, either through mathematical expressions or by uploading data files in txt/csv formats.

4. **Implementation of Warnings**: Integrate warning systems to alert users of potential data inaccuracies or interpretational errors.

5. **Total ΔN<sub>eff</sub> Calculation**: Provide a feature to calculate the total effective number of relativistic species (ΔN<sub>eff</sub>), based on the plotted signals.

6. **Parametrization of Detector Curves**: Allow users to parametrize and modify detector sensitivity curves, enhancing the tool's utility for theoretical explorations and scenario testing.



## Contributing

Contributions to GWplots are welcome, whether they be in the form of feature requests, bug reports, or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This is a public project, open to everyone, and aimed at serving the scientific community by providing a standard yet fully customizable gravitational waves plotter.

Users are free to use, modify, and distribute this software. If you utilize this project in your research or in any other capacity, please acknowledge the authors by citing the relevant publications.
