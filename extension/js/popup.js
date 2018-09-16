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
            stats.innerHTML += "<h4>Chances of Fake-News (%) </h4>";
            add_bar(data["fake_news"]);
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

function add_bar(percent) {
  var data = [1 * 100, percent * 100]; // here are the data values; v1 = total, v2 = current value

  var chart = d3.select("#container").append("svg") // creating the svg object inside the container div
    .attr("class", "chart")
    .attr("width", 200) // bar has a fixed width
    .attr("height", 20 * data.length);

  var x = d3.scale.linear() // takes the fixed width and creates the percentage from the data values
    .domain([0, d3.max(data)])
    .range([0, 200]);

  chart.selectAll("rect") // this is what actually creates the bars
    .data(data)
  .enter().append("rect")
    .attr("width", x)
    .attr("height", 20)
    .attr("rx", 5) // rounded corners
    .attr("ry", 5);

  chart.selectAll("text") // adding the text labels to the bar
    .data(data)
  .enter().append("text")
    .attr("x", x)
    .attr("y", 10) // y position of the text inside bar
    .attr("dx", -3) // padding-right
    .attr("dy", ".35em") // vertical-align: middle
    .attr("text-anchor", "end") // text-align: right
    .text(String);

   document.body.appendChild(x);
}