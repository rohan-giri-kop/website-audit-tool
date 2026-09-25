
window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (!navbar) return;

    if (window.scrollY > 60) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }

});

// =====================================
// Active Navbar Link on Scroll
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-link");

    function activateNav() {

        let current = "";

        sections.forEach(section => {

            const top = section.offsetTop - 150;
            const bottom = top + section.offsetHeight;

            if (window.scrollY >= top && window.scrollY < bottom) {
                current = section.id;
            }

        });

        if (!current) return;

        // Change active navbar item
        navLinks.forEach(link => {
            link.classList.remove("active");

            if (link.getAttribute("href") === "/#" + current) {
                link.classList.add("active");
            }
        });

        // Update URL while scrolling
        if (window.location.hash !== "#" + current) {
            history.replaceState(null, null, "#" + current);
        }

    }    
    activateNav();

    window.addEventListener("scroll", activateNav);

    window.addEventListener("hashchange", activateNav);

});

const cards = document.querySelectorAll(".how-card");

const observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
        if(entry.isIntersecting){
            entry.target.classList.add("show");
        }
    });
},{
    threshold:0.15
});

cards.forEach(card=>observer.observe(card));


/* =========================================================
   TESTIMONIAL AUTO SLIDER
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const slider = document.getElementById("testimonialSlider");
    const track = slider?.querySelector(".testimonial-track");

    if (!slider || !track) {
        return;
    }

    let animationFrame = null;
    let isPaused = false;
    let isDragging = false;

    let startX = 0;
    let startScrollLeft = 0;

    /* -----------------------------------------
       AUTO SCROLL
    ----------------------------------------- */

    function autoScroll() {

        if (!isPaused && !isDragging) {

            slider.scrollLeft += 0.5;

            /*
             * Because the testimonials are duplicated,
             * reset after reaching the first complete set.
             */

            const halfWidth = track.scrollWidth / 2;

            if (slider.scrollLeft >= halfWidth) {
                slider.scrollLeft = 0;
            }

        }

        animationFrame = requestAnimationFrame(autoScroll);
    }


    /* -----------------------------------------
       START
    ----------------------------------------- */

    autoScroll();


    /* -----------------------------------------
       PAUSE ON HOVER
    ----------------------------------------- */

    slider.addEventListener("mouseenter", function () {

        isPaused = true;

    });


    /* -----------------------------------------
       RESUME AFTER HOVER
    ----------------------------------------- */

    slider.addEventListener("mouseleave", function () {

        isPaused = false;

    });


    /* -----------------------------------------
       MOUSE DRAG
    ----------------------------------------- */

    slider.addEventListener("mousedown", function (event) {

        isDragging = true;

        startX = event.pageX;

        startScrollLeft = slider.scrollLeft;

        slider.classList.add("dragging");

    });


    window.addEventListener("mouseup", function () {

        if (!isDragging) {
            return;
        }

        isDragging = false;

        slider.classList.remove("dragging");

    });


    slider.addEventListener("mousemove", function (event) {

        if (!isDragging) {
            return;
        }

        event.preventDefault();

        const distance = event.pageX - startX;

        slider.scrollLeft =
            startScrollLeft - distance * 1.5;

    });


    /* -----------------------------------------
       MOUSE WHEEL
    ----------------------------------------- */

    slider.addEventListener(
        "wheel",
        function (event) {

            event.preventDefault();

            slider.scrollLeft += event.deltaY;

        },
        {
            passive: false
        }
    );


    /* -----------------------------------------
       TOUCH SUPPORT
    ----------------------------------------- */

    slider.addEventListener("touchstart", function () {

        isPaused = true;

    }, { passive: true });


    slider.addEventListener("touchend", function () {

        isPaused = false;

    }, { passive: true });

});