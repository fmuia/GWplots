// static/js/scripts.js
function updatePlot(button_label) {
    console.log(button_label);

    const glyph = Bokeh.documents[0].get_model_by_name(button_label);
    glyph.visible = !glyph.visible;

    const annotation = Bokeh.documents[0].get_model_by_name(`annotation_${button_label}`);
    console.log(`Annotation for ${button_label} found: `, annotation);

    if (annotation) {
        console.log(`Current visibility of ${button_label}: `, annotation.visible);
        annotation.visible =  !annotation.visible; // Change visibility
        console.log(`New visibility of ${button_label}: `, annotation.visible);
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

