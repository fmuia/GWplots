// static/js/scripts.js

function waitForBokeh() {
    if (typeof Bokeh !== 'undefined' && Bokeh.documents && Bokeh.documents[0]) {
        exploreBokehDocument(Bokeh.documents[0]);
    } else {
        // Wait a bit and then try again
        setTimeout(waitForBokeh, 100);
    }
}

function exploreBokehDocument(doc) {
    if (doc.roots) {
        doc.roots().forEach(root => {
            console.log('Root:', root);
        });
    }
}

// Start the process
waitForBokeh();



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

var checkedCurves = {}; // Object to store label and comment

function updateComments(checkboxElement) {
    const label = checkboxElement.value;
    const isChecked = checkboxElement.checked;
    const commentsBox = document.getElementById('comments-box');

    console.log("Checkbox clicked:", label, "Checked:", isChecked);

    if (isChecked) {
        console.log("Fetching comments for:", label);
        fetch(`/get_comments?label=${label}`)
            .then(response => response.json())
            .then(data => {
                console.log("Data received for:", label, "Comment:", data.comment);
                if (data.comment) {
                    checkedCurves[label] = data.comment;
                } else {
                    delete checkedCurves[label];
                }
                displayComments();
            })
            .catch(error => {
                console.error('Error fetching comments for:', label, error);
                delete checkedCurves[label];
                displayComments();
            });
    } else {
        delete checkedCurves[label];
        displayComments();
    }
}

function displayComments() {
    const commentsBox = document.getElementById('comments-box');
    const allCommentsHtml = Object.entries(checkedCurves)
        .filter(([label, comment]) => comment && comment.trim() !== '')
        .map(([label, comment]) => '<strong>' + label + ':</strong> ' + comment)  // Format with label and comment
        .join('<br><br>');  // Use double HTML line break for spacing

    console.log("All comments to display (HTML):", allCommentsHtml);
    commentsBox.innerHTML = allCommentsHtml;  // Set as innerHTML to render HTML content
}


document.addEventListener('DOMContentLoaded', function() {
    console.log("Bokeh Document:", Bokeh.documents[0]);
    Bokeh.documents[0].roots().forEach(root => {
        console.log("Model type:", root.type, "Model name:", root.name);
    });

    function updatePlotAxis(plotType) {
        const plot = Bokeh.documents[0].roots()[0];
        console.log("Plot:", plot);

        if (!plot) {
            console.error("Plot model not found!");
            return;
        }

        console.log("Y-axis:", plot.yaxis);
        console.log("X-range:", plot.x_range);

        const y_axis = plot.yaxis[0];
        const x_range = plot.x_range;

        if (plotType === 'h') {
            y_axis.axis_label = 'h';
            x_range.start = Math.pow(10, -10);
            x_range.end = Math.pow(10, 20);
        } else if (plotType === 'omega') {
            y_axis.axis_label = 'Ω';
            x_range.start = Math.pow(10, 3);
            x_range.end = Math.pow(10, 20);
        }

        y_axis.change.emit();
        x_range.change.emit();
    }

    document.querySelectorAll('input[name="plotType"]').forEach(function(radioButton) {
        radioButton.addEventListener('change', function(event) {
            updatePlotAxis(event.target.value);
        });
    });

    // ... Rest of your existing code ...
});