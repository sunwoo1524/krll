const url_input = document.getElementById("url");
const to_shorten_btn = document.getElementById("to-shorten-btn");
const result_container = document.getElementById("result-container");
const short_url = document.getElementById("short-url");
const qr_code = document.getElementById("qr-code");
const error_message = document.getElementById("error");
const copy_message = document.getElementById("copied");

to_shorten_btn.addEventListener("click", async () => {
   const original_url = url_input.value
    // check if the url input is empty
    if (original_url.length === 0) {
        return;
    }

    // Easter egg: rick roll
    if (rickroll.check(original_url)){
        window.location.replace("https://youtu.be/dQw4w9WgXcQ");
    }

    // shorten the long url
    const response = await fetch("/api/urls", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: original_url
        })
    })

    // check if there is problems
    if (!response.ok) {
        if (response.status === 400) {
            // the url is invalid
            error_message.style.display = "block";
            setTimeout(() => error_message.style.display = "none", 5000);
        } else {
            // there is some problems in the server!
            alert("Sorry, an error has occured in the server...");
        }
        
        return;
    }

    const data = await response.json();
    const result = `https://krll.me/${data.key}`

    // show the short url
    short_url.innerText = result;

    // get the qr code of the short url and show it
    qr_code.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${result}`;
    qr_code.alt = result;
});

short_url.addEventListener("click", event => {
    // copy the short url to clipboard
    navigator.clipboard.writeText(event.target.innerText)
    .then(() => {
        // show a message
        copy_message.style.opacity = "1";
        setTimeout(() => copy_message.style.opacity = "0", 3000);
    })
    .catch(error => {
        alert("An error has occurred...\n" + error);
    });
});

const rickroll = {
    check: (url)=>{
	try {
	    const urlObj = new URL(url);
            let videoId = "";
            if (urlObj.host.split(".").slice(-2)[0] === "youtube") {
               if (urlObj.pathname.split("/")[1] === "watch") {
                   videoId = urlObj.searchParams.get("v");
               }
               else {
                   return false;
               }
            }
	    else if (urlObj.host === "youtu.be") {
                videoId = urlObj.pathname.slice(1);
            }
            else {
	        return false
            }
	    if (videoId ==="dQw4w9WgXcQ") return true
            return false
	}
        catch {
            return false
        }
    }
}

