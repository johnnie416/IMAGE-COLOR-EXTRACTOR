function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied " + text + " to clipboard!");
    });
}