// static/js/scripts.js
function updatePlot(button_label) {
    console.log(button_label);
    fetch(`/update_plot?button_label=${button_label}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(new_data => {
            const plot_source = Bokeh.documents[0].get_model_by_name('plot_source');
            const plot_source_proj = Bokeh.documents[0].get_model_by_name('plot_source_proj');
            const plot_source_proj_curves = Bokeh.documents[0].get_model_by_name('plot_source_proj_curves');
            console.log(new_data);

            // Initialize an empty object to hold the updated data
            let updated_data = {};
            let updated_data_proj = {};
            let updated_data_proj_curves = {};

            // Extract unique curve labels from new_data keys
            let curve_labels = new Set(Object.keys(new_data).map(key => key.split('_')[1]));
            console.log(curve_labels)

            // Loop through each key in new_data and update plot_source.data
            for (let curve_label of curve_labels) {
                //Data of current bounds has x, y, y2
                if (new_data.hasOwnProperty(`x_${curve_label}`) && new_data.hasOwnProperty(`y_${curve_label}`)  && new_data.hasOwnProperty(`y2_${curve_label}`)) {
                    updated_data[`x_${curve_label}`] = new_data[`x_${curve_label}`];
                    updated_data[`y_${curve_label}`] = new_data[`y_${curve_label}`];
                    updated_data[`y2_${curve_label}`] = new_data[`y2_${curve_label}`];
                }
               // Data of simple projected bounds has x, y
               if ( (!(new_data.hasOwnProperty(`y2_${curve_label}`))) && (new_data.hasOwnProperty(`x_${curve_label}`)) && (new_data.hasOwnProperty(`y_${curve_label}`)))
               {
                    updated_data_proj[`x_${curve_label}`] = new_data[`x_${curve_label}`];
                    updated_data_proj[`y_${curve_label}`] = new_data[`y_${curve_label}`];
                }
               // Data of  projected bounds in the form of curves has xCurve, yCurve
               if (  (new_data.hasOwnProperty(`xCurve_${curve_label}`)) && (new_data.hasOwnProperty(`yCurve_${curve_label}`)))
               {
                    updated_data_proj_curves[`xCurve_${curve_label}`] = new_data[`xCurve_${curve_label}`];
                    updated_data_proj_curves[`yCurve_${curve_label}`] = new_data[`yCurve_${curve_label}`];
                }
            }

            plot_source.data = updated_data;
            plot_source.change.emit();

            plot_source_proj.data = updated_data_proj;
            plot_source_proj.change.emit();
            
            plot_source_proj_curves.data = updated_data_proj_curves;
            plot_source_proj_curves.change.emit();


        // Call toggleAnnotationVisibility for the clicked label
            const checkbox = document.getElementById(button_label);
            if (checkbox) {
                toggleAnnotationVisibility(button_label, checkbox.checked);
            }
        }).catch(error => {
            console.error('Fetch error:', error);
        });
}

function toggleAnnotationVisibility(curveLabel, isVisible) {
    var annotation = Bokeh.documents[0].get_model_by_name(`annotation_${curveLabel}`);
    console.log(`Annotation for ${curveLabel} found: `, annotation);

    if (annotation) {
        console.log(`Current visibility of ${curveLabel}: `, annotation.visible);
        annotation.visible = isVisible; // Toggle visibility
        console.log(`New visibility of ${curveLabel}: `, annotation.visible);
    }
}

