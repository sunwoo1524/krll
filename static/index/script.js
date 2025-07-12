const url_input = document.getElementById("url");
const to_shorten_btn = document.getElementById("to-shorten-btn");
const short_url = document.getElementById("short-url");
const qr_code = document.getElementById("qr-code");
const error_message = document.getElementById("error");
const copy_message = document.getElementById("copied");
const cap_widget = document.querySelector("#cap");

const error_message_list = {
    "FAILURE_CAPTCHA": "The captcha failed.",
    "INVALID_URL": "The link is invalid.",
    "URL_MAX_LENGTH_EXCEEDED": "The link is too long.",
    "BLOCKED_URL": "The link has been blocked."
}

if (cap_widget !== null) cap_widget.addEventListener("solve", function (e) {
    cap_token = e.detail.token;
});

let qrcodejs;
let cfts_token = null;
let cap_token = null;

const shorten = async () => {
    // check cloudflare captcha
    if (captcha_mode === "turnstile") {
        cfts_token = turnstile.getResponse();
        if (!cfts_token || turnstile.isExpired()) {
            turnstile.reset();
            return;
        }
    }
    
    const original_url = url_input.value;

    // check if the url input is empty
    if (original_url.length === 0) {
        return;
    }

    const { dQw4w9WgXcQ } = await import("./dQw4w9WgXcQ.js");
    if (dQw4w9WgXcQ.check(original_url)) {
        location.href = "https://youtu.be/dQw4w9WgXcQ";
        return;
    }

    // shorten the long url
    const response = await fetch("/api/urls", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: original_url,
            token: cfts_token || cap_token
        })
    })

    // check if there is problems
    if (!response.ok) {
        if (response.status === 400) {
            const detail = (await response.json()).detail;
            if (detail == "FAILURE_CAPTCHA") {
                if (captcha_mode === "turnstile") {
                    turnstile.reset();
                }
            }
            // the url is invalid
            error_message.innerText = error_message_list[detail] || detail;
            error_message.style.display = "block";
            setTimeout(() => error_message.style.display = "none", 5000);
        } else {
            // some error is occured in the server!
            alert("Sorry, an error has occured in the server...");
        }
        
        return;
    }

    const data = await response.json();
    const result = `${host}/${data.key}`;

    // show the short url
    short_url.innerText = result;

    // get the qr code of the short url and show it
    if (qrcodejs) {
        qrcodejs.clear();
        qrcodejs.makeCode(result);
    } else {
        qrcodejs = new QRCode(qr_code, {
            text: result,
            width: 256,
            height: 256,
            colorDark : "#000000",
            colorLight : "#ffffff",
        });
        qr_code.className += "generated";
    }
    
    // qr_code.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${result}`;
    // qr_code.alt = result;
}

to_shorten_btn.addEventListener("click", shorten);
addEventListener("keydown", (event) => { if (event.key === "Enter") shorten() });

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
