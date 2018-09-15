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
            var x = document.createElement("P");
            var text = "The tweet by " + data["tweet"]["user_screen_name"] + " is ";
            if (data["fake_news"] == true) {
                text += "may a FAKE NEWS!";
            } else {
                text += "completely legit AFFFF";
            }
            var t = document.createTextNode(text);
            x.appendChild(t);
            document.getElementById("stats").appendChild(x);
            create_chart(data);
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


function create_chart(data) {
    // add chart! for now only a demo
    var ctx = document.getElementById("canvas");

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
};