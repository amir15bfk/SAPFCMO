console.log("test")
function initializeWebSocket() {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/');

    socket.onmessage = function(e) {
        console.log("server: " + e.data);
    };

    socket.onopen = function(e) {
        console.log("WebSocket connection established.");

        // Send the first message upon connection
        socket.send(JSON.stringify({
            "machine_id": "welding_robot_006"
        }));
    };
    sleep(2000);
        // Start the WebSocket connection
        console.log("Re-establishing WebSocket connection...");
        socket.close(); // Close the previous connection 
    // Set up an interval to repeat the WebSocket connection every 20 seconds
    
           
}
setInterval(() => {
// Start the WebSocket connection
initializeWebSocket();
}, 20000);


