document.addEventListener('DOMContentLoaded', function() {
    const techniqueSelector = document.getElementById('techniqueSelector');
    const conditionSelector = document.getElementById('conditionSelector');
    const axisSelector = document.getElementById('axisSelector');
    const filterSelector = document.getElementById('filterSelector')
    const image = document.getElementById('signalPlot');
    
    // Function to fetch and update the plot image
    function fetchAndUpdatePlot(condition, technique, axis, filter) {
        if (condition && technique) {
            image.style.display = 'none';  // Hide image until new plot is fetched
            document.getElementById('loadingIndicator').style.display = 'block'; // Show loading wheel

            fetch(`/signals/plot?condition=${encodeURIComponent(condition)}&technique=${encodeURIComponent(technique)}&axis=${encodeURIComponent(axis)}&filter=${encodeURIComponent(filter)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    document.getElementById('loadingIndicator').style.display = 'none'; 
                    if (data.image) {
                        image.src = 'data:image/png;base64,' + data.image;
                        image.style.display = 'block';
                    } else {
                        throw new Error('No image data received from the server.');
                    }
                })
                .catch(error => {
                    document.getElementById('loadingIndicator').style.display = 'none'; 
                    console.error('Error fetching the signal plot:', error);
                });
        } else {
            image.style.display = 'none';  // Hide image if condition or technique is not provided
        }
    }

    // default values are set
    if (techniqueSelector.value && conditionSelector.value && axisSelector.value && filterSelector.value) {
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelector.value, axisSelector.value, filterSelector.value);
    }
    
    // changed values are set
    conditionSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(this.value, techniqueSelector.value, axisSelector.value, filterSelector.value);
    });
    techniqueSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, this.value, axisSelector.value, filterSelector.value);
    });
    axisSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelector.value, this.value, filterSelector.value);
    });
    filterSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelector.value, axisSelector.value, this.value);
    });
});
