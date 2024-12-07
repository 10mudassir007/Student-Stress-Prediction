document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.target);
    const data = {
        study_hours: parseFloat(formData.get('study_hours')),
        extracrr_hours: parseFloat(formData.get('extracrr_hours')),
        sleep_hours: parseFloat(formData.get('sleep_hours')),
        social_hours: parseFloat(formData.get('social_hours')),
        phy_activity: parseFloat(formData.get('phy_activity')),
        gpa: parseFloat(formData.get('gpa'))
    };

    // Check if the values are being parsed correctly
    console.log(data);  // This will print the values to the console for debugging

    // Send POST request to the FastAPI prediction endpoint
    const response = await fetch('http://127.0.0.1:8000/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // Handle the response
    if (response.ok) {
        const result = await response.json();
        document.getElementById('prediction-result').textContent = result.prediction;
    } else {
        document.getElementById('prediction-result').textContent = 'Error in prediction';
    }
});
