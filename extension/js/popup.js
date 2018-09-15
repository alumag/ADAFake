chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse){
        if(request.msg == "chart"){

            // add information in a paragraph
            var data = request.data;
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
        }
});