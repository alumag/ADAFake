var server = "http://127.0.0.1:5000/api/v1/checkTwit"; // testing url

chrome.runtime.onInstalled.addListener(function() {
chrome.contextMenus.create({
  "id": "sampleContextMenu",
  "title": "Sample Context Menu",
  "contexts": ["selection"]
});
});

function CheckTwit(url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText);
             if (this.responseText == "is fake news") {
                return 0;
             } else {
                return 1;
             }
         }
    };
    xhttp.open("GET", server, true);
    xhttp.setRequestHeader("Content-type", "application/json");

    xhttp.send("{url: " + url + "}");
}

chrome.webNavigation.onCompleted.addListener(function() {
    // get tab url
      chrome.tabs.query({
        active: true,
        lastFocusedWindow: true
    }, function(tabs) {
        // and use that tab to fill in out title and url
        var tab = tabs[0];

        // for all statuses
        if (tab.url.includes("/status/")) {
            // check if fake news
            if (1 == CheckTwit(tab.url)) {
            chrome.tabs.executeScript({code: 'document.body.style.backgroundColor="green"'});
            } else {
            chrome.tabs.executeScript({code: 'document.body.style.backgroundColor="red"'});
            }
        }
    });
}, {url: [{urlMatches : 'https://twitter.com/'}]});
