document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const conditionSelector = document.getElementById('conditionSelector');
    const filterSelector = document.getElementById('filterSelector');
    const axisSelector = document.getElementById('axisSelector');
    
    const techniqueRadios = document.querySelectorAll('input[name="techniqueSelector"]');
    const techniqueSelector1 = document.getElementById('techniqueSelector1');
    const techniqueSelector2 = document.getElementById('techniqueSelector2');
    let techniqueSelectorValue = null; 

    const signalsPlot = document.getElementById('signalsPlot');
    const labelsPlot = document.getElementById('labelsPlot');

    const preprocessingDescription = document.getElementById('preprocessingDescription');

    // Initialize
    const initialTechniqueRadio = document.querySelector('input[name="techniqueSelector"]:checked');
    if (initialTechniqueRadio) {
        updateTechniqueSelector(initialTechniqueRadio.value);
    } else {
        console.error('No initial technique radio button is selected.');
    }

    // Preprocessing description update
    function UpdateConfigDescription(filterSelector, techniqueSelectorValue) {
        if (filterSelector && techniqueSelectorValue) {
            if (filterSelector.value) {
                preprocessingDescription.textContent = 'Each short input vector signal is condensed into a single point using ' 
                    + techniqueSelectorValue 
                    + ', with this point representing the input vector signal. ';
                preprocessingDescription.textContent += (filterSelector.value != 'none') ? 
                    'The ' + techniqueSelectorValue + ' indicator is then smoothed using ' + filterSelector.value + ' function' : '';
            } else {
                preprocessingDescription.textContent = '';
            }
        } else {
            preprocessingDescription.textContent = 'Please select options to view preprocessing description.';
        }
    }     

    // Functions
    function updateTechniqueSelector(value) {
        if (value === "technique1") {
            techniqueSelector1.disabled = false;
            techniqueSelector2.disabled = true;
            techniqueSelectorValue = techniqueSelector1.value;
        } else if (value === "technique2") {
            techniqueSelector1.disabled = true;
            techniqueSelector2.disabled = false;
            techniqueSelectorValue = techniqueSelector2.value;
            
        }
        updateFilterSelector(techniqueSelectorValue);
        UpdateConfigDescription(filterSelector, techniqueSelectorValue)
    }
    
    function updateFilterSelector(techniqueSelectorValue) {
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
        return new Promise((resolve, reject) => {
            if (condition && technique) {
                signalsPlot.style.display = 'none';
                labelsPlot.style.display = 'none';
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
                        if (data.plotted_signals) {
                            signalsPlot.src = 'data:plotted_signals/png;base64,' + data.plotted_signals;
                            signalsPlot.style.display = 'block';
                            
                            labelsPlot.innerHTML = data.plotted_labels.data;
                            labelsPlot.style.display = 'block';
    
                            resolve(); // Resolve the Promise when data is fetched and updated
                        } else {
                            throw new Error('No image data received from the server.');
                        }
                    })
                    .catch(error => {
                        document.getElementById('loadingIndicator').style.display = 'none';
                        console.error('Error fetching the signal plot:', error);
                        reject(error); // Reject the Promise if there's an error
                    });
            } else {
                signalsPlot.style.display = 'none';
                labelsPlot.style.display = 'none';
                reject(new Error('Invalid parameters')); // Reject the Promise if parameters are invalid
            }
        });
    }
    
    // Event Listeners
    techniqueRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            updateTechniqueSelector(this.value);
            initialParameters();
        });
    });    

    initialParameters();
    UpdateConfigDescription(filterSelector, techniqueSelectorValue);

    techniqueSelector1.addEventListener('change', function() {
        updateFilterSelector(techniqueSelector1.value);
        UpdateConfigDescription(filterSelector, techniqueSelector1.value);
    });
    techniqueSelector2.addEventListener('change', function() {
        updateFilterSelector(techniqueSelector2.value);
        UpdateConfigDescription(filterSelector, techniqueSelector2.value);
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
        UpdateConfigDescription(this, techniqueSelectorValue);
        fetchAndUpdatePlot(conditionSelector.value, techniqueSelectorValue, axisSelector.value, this.value);
    });

});
