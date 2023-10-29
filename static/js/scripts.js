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
            console.log(new_data);

            // Initialize an empty object to hold the updated data
            let updated_data = {};

            // Extract unique curve labels from new_data keys
            let curve_labels = new Set(Object.keys(new_data).map(key => key.split('_')[1]));
            console.log(curve_labels)

            // Loop through each key in new_data and update plot_source.data
            for (let curve_label of curve_labels) {
                if (new_data.hasOwnProperty(`x_${curve_label}`) && new_data.hasOwnProperty(`y_${curve_label}`)) {
                    updated_data[`x_${curve_label}`] = new_data[`x_${curve_label}`];
                    updated_data[`y_${curve_label}`] = new_data[`y_${curve_label}`];            
                }
            }

            plot_source.data = updated_data;
            plot_source.change.emit();
        }).catch(error => {
            console.error('Fetch error:', error);
        });
}

