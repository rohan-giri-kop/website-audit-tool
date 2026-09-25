const ctx = document.getElementById("sampleRadar");

if (ctx) {

    new Chart(ctx, {

        type: "radar",

        data: {

            labels: [
                "SEO",
                "Performance",
                "Accessibility",
                "Security",
                "Best Practices"
            ],

            datasets: [{

                label: "Score",

                data: [96, 91, 95, 98, 100],

                borderColor: "#2563EB",

                backgroundColor: "rgba(37,99,235,.20)",

                pointBackgroundColor: "#2563EB",

                pointRadius: 4,

                borderWidth: 2

            }]

        },

        options:{
            responsive:true,
            maintainAspectRatio:false,

            plugins:{
                legend:{
                    display:false
                }
            },

            scales:{
                r:{
                    min:0,
                    max:100,

                    ticks:{
                        display:false
                    },

                    grid:{
                        color:"#E5E7EB"
                    },

                    angleLines:{
                        color:"#E5E7EB"
                    },

                    pointLabels:{
                        color:"#374151",
                        font:{
                            size:13,
                            weight:"600"
                        }
                    }
                }
            }
        }
    });

}

const screen = document.getElementById("reportScreen");

let autoScroll;

screen.addEventListener("mouseenter",()=>{

    autoScroll=setInterval(()=>{

        screen.scrollTop+=1;

        if(
            screen.scrollTop>=
            screen.scrollHeight-screen.clientHeight
        ){

            clearInterval(autoScroll);

        }

    },18);

});

screen.addEventListener("mouseleave",()=>{

    clearInterval(autoScroll);

    screen.scrollTo({

        top:0,

        behavior:"smooth"

    });

});