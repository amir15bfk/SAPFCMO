console.log("test")
function addAlert(type, message) {
    // Create the alert div
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible`;

    // Add the dismiss button
    alertDiv.innerHTML = `
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
        <h5><i class="icon fas fa-${type === 'danger' ? 'ban' : (type === 'info' ? 'info' : (type === 'warning' ? 'exclamation-triangle' : 'check'))}"></i> Alert!</h5>
        ${message}
    `;

    // Append the alert to the alert container
    const alertContainer = document.getElementById('alert-container');
    alertContainer.appendChild(alertDiv);
}

// Example usage


const socket = new WebSocket('ws://' + window.location.host + '/ws/');

    socket.onmessage = function(e) {
        console.log("server: " + e.data);
        let data = JSON.parse(e.data);
        // var temperatureCanvas_{{ machine.machine_id }} = $('#temperature_{{ machine.machine_id }}').get(0).getContext('2d')
        addAlert('danger', data.message);
    };

    socket.onopen = function(e) {
        console.log("WebSocket connection established.");

        // Send the first message upon connection
        socket.send(JSON.stringify({
            "message": "hi"
        }));
    };

// function initializeWebSocket() {
//     const socket = new WebSocket('ws://' + window.location.host + '/ws/');

//     socket.onmessage = function(e) {
//         console.log("server: " + e.data);
//         var temperatureCanvas_{{ machine.machine_id }} = $('#temperature_{{ machine.machine_id }}').get(0).getContext('2d')
//     };

//     socket.onopen = function(e) {
//         console.log("WebSocket connection established.");

//         // Send the first message upon connection
//         socket.send(JSON.stringify({
//             "machine_id": "welding_robot_006"
//         }));
//     };

//     sleep(2000);
//         // Start the WebSocket connection
//         console.log("Re-establishing WebSocket connection...");
//         socket.close(); // Close the previous connection 
//     // Set up an interval to repeat the WebSocket connection every 20 seconds
    
           
// }
// setInterval(() => {
// // Start the WebSocket connection
// initializeWebSocket();
// }, 20000);


