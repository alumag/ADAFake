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
            if (data["fake_news"] == true) {
                stats.innerHTML += " may be FAKE NEWS! ".bold().fontcolor("red");
                stats.innerHTML += "<img src=\"/icons/fake.jpg\"/>";
            } else {
                stats.innerHTML += " is completely legit AFFFF ".bold().fontcolor("green");
                stats.innerHTML += "<img src=\"/icons/legit.jpg\"/>";
            }

            create_chart(data);
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
        }
    });
};


function create_chart(data) {
    // add chart! for now only a demo
    var ctx = document.getElementById("canvas");

    data = {
    datasets: [{
        data: [0.4, 1, 0.2],
        backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)'
        ]
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'Journalist',
        'Fake News',
        'Opinion'
    ]
    };

    var chart = new Chart(ctx, {
    data: data,
    type: 'doughnut',
    });
};