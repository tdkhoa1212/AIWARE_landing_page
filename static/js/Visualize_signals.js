document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const conditionSelector = document.getElementById('conditionSelector');
    const filterSelector = document.getElementById('filterSelector');
    const axisSelector = document.getElementById('axisSelector');
    const image = document.getElementById('signalPlot');
    const techniqueRadios = document.querySelectorAll('input[name="techniqueSelector"]');
    const techniqueSelector1 = document.getElementById('techniqueSelector1');
    const techniqueSelector2 = document.getElementById('techniqueSelector2');
    let techniqueSelectorValue = null; 

    // Initialize
    const initialTechniqueRadio = document.querySelector('input[name="techniqueSelector"]:checked');
    if (initialTechniqueRadio) {
        updateTechniqueSelector(initialTechniqueRadio.value);
    } else {
        console.error('No initial technique radio button is selected.');
    }

    // Functions
    function updateTechniqueSelector(value) {
        if (value === "technique1") {
            techniqueSelector1.disabled = false;
            techniqueSelector2.disabled = true;
            techniqueSelectorValue = techniqueSelector1.value;
            updateFilterSelector(techniqueSelectorValue);
        } else if (value === "technique2") {
            techniqueSelector1.disabled = true;
            techniqueSelector2.disabled = false;
            techniqueSelectorValue = techniqueSelector2.value;
            console.log(techniqueSelectorValue);
            updateFilterSelector(techniqueSelectorValue);
        }
    }
    
    function updateFilterSelector(techniqueSelectorValue) {
        console.log(techniqueSelectorValue)
        if (techniqueSelectorValue == "Magnitude") {
            filterSelector.value = "none";
            filterSelector.disabled = true;
        } else {
            filterSelector.disabled = false;
        }
    }

    function initialParameters(){
        if (conditionSelector.value, techniqueSelectorValue, axisSelector.value, filterSelector.value){
            fetchAndUpdatePlot(conditionSelector.value, techniqueSelectorValue, axisSelector.value, filterSelector.value);
        }
    }

    function fetchAndUpdatePlot(condition, technique, axis, filter) {
        if (condition && technique) {
            image.style.display = 'none';  
            document.getElementById('loadingIndicator').style.display = 'block'; 

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
            image.style.display = 'none';  
        }
    }

    // Event Listeners
    techniqueRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            updateTechniqueSelector(this.value);
            initialParameters();
        });
    });    

    initialParameters();

    techniqueSelector1.addEventListener('change', function() {
        updateFilterSelector(techniqueSelector1.value);
    });
    techniqueSelector2.addEventListener('change', function() {
        updateFilterSelector(techniqueSelector2.value);
    });

    conditionSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(this.value, techniqueSelectorValue, axisSelector.value, filterSelector.value);
    });
    techniqueSelector1.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, this.value, axisSelector.value, filterSelector.value);
    });
    techniqueSelector2.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, this.value, axisSelector.value, filterSelector.value);
    });
    axisSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelectorValue, this.value, filterSelector.value);
    });
    filterSelector.addEventListener('change', function() {
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelectorValue, axisSelector.value, this.value);
    });
});
