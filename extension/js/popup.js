var server = "http://127.0.0.1:5000/api/v1/checkTweet"; // testing url

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

            // add information in a paragraph
            var stats = document.getElementById('stats');
            stats.innerHTML += "The tweet by " + data["tweet"]["user_screen_name"];
            if (data["fake_news"] >= 0.5) {
                stats.innerHTML += " may be FAKE NEWS! ".bold().fontcolor("red");
                stats.innerHTML += "<img src=\"/icons/fake.jpg\"/>";
            } else {
                stats.innerHTML += " is completely legit AFFFF ".bold().fontcolor("green");
                stats.innerHTML += "<img src=\"/icons/legit.jpg\"/>";
            }
            stats.innerHTML += "</br>" + data["fake_news"] + "%";

         }
    };
    xhttp.open("GET", server + "?url=" + url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}

window.onload = function() {
    // get tab url
      chrome.tabs.query({
        active: true,
        lastFocusedWindow: true
    }, function(tabs) {
        // and use that tab to fill in out title and url
        var tab = tabs[0];

        // for all statuses
        if (tab.url.includes("/status/") && tab.url.includes("twitter.com/")) {

            // check if fake news
            CheckTweet(tab);
        } else {
            var stats = document.getElementById('stats');
            stats.innerHTML += "<h2>You are not surfing Twitter right now...</h2></br>";
            stats.innerHTML += "<img src=\"/icons/hugewall.jpg\"/>";
        }
    });
};