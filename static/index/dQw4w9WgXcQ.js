// yeah it's a fucking easter egg :P
export const dQw4w9WgXcQ = {
    check: (url) => {
        try {
            const urlObj = new URL(url);
            let videoId = "";

            if (urlObj.host.split(".").slice(-2)[0] === "youtube") {
                if (urlObj.pathname.split("/")[1] === "watch") {
                    videoId = urlObj.searchParams.get("v");
                } else {
                    return false;
                }
            } else if (urlObj.host === "youtu.be") {
                videoId = urlObj.pathname.slice(1);
            } else {
                return false;
            }

            if (videoId ==="dQw4w9WgXcQ") return true;
            return false;
        } catch {
            return false
        }
    }
};
