var server = "http://127.0.0.1:5000/api/v1/checkTweet"; // testing url

chrome.runtime.onInstalled.addListener(function() {
chrome.contextMenus.create({
  "id": "sampleContextMenu",
  "title": "Sample Context Menu",
  "contexts": ["selection"]
});
});

function CheckTweet(tab) {
    var url = tab.url;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            fake_news = data["fake_news"];

            if (fake_news == true) {
                chrome.tabs.executeScript({code: 'document.body.style.backgroundColor="red"'});
            } else if (fake_news == false) {
                chrome.tabs.executeScript({code: 'document.body.style.backgroundColor="green"'});
            }

            chrome.runtime.sendMessage({msg: "chart", data: {}});
         }
    };
    xhttp.open("GET", server + "?url=" + url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
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
            CheckTweet(tab);
        }
    });
}, {url: [{urlMatches : 'https://twitter.com/'}]});
