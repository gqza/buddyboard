// real shit

function enlarge(url) {
    const overlay = document.createElement("div");
    overlay.className = "overlay";

    const image = document.createElement("img");
    image.src = url;
    image.style.position = "fixed"; // Use 'fixed' to position relative to the viewport
    image.style.top = "50%";
    image.style.left = "50%";
    image.style.transform = "translate(-50%, -50%)";
    image.style.maxWidth = "90vw";
    image.style.maxHeight = "90vh";
    image.style.zIndex = "1000";
    image.style.border = "2px solid #333";
    image.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.5)";
    image.className = "large";
    
    overlay.appendChild(image);
    document.body.appendChild(overlay);

    overlay.onclick = function() {
        document.body.removeChild(overlay);
    };
}

async function ratePost(post, rating) {
    const response = await fetch(`../vote/${post}/${rating}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "rating": rating }),
    });
    if (response.status == 429) {
        displayBottomMessage("You already voted today!");
    }
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    console.log(response.status);
    const responseData = await response.json();
    console.log(responseData);
    window.location.reload();

}

function displayBottomMessage(messageText) {
    let messageContainer = document.getElementById('api-message-container');

    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.id = 'notification';
        messageContainer.style.position = 'fixed';
        messageContainer.style.bottom = '10px';
        messageContainer.style.left = '10px';
        document.body.appendChild(messageContainer);
    }

    messageContainer.textContent = messageText;

    setTimeout(() => {
        if (messageContainer && messageContainer.parentNode) {
            messageContainer.parentNode.removeChild(messageContainer);
        }
    }, 1500);
}