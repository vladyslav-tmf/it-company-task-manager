document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".pagination a").forEach(function (paginationLink) {
        paginationLink.addEventListener("click", function (e) {
            sessionStorage.setItem("scrollPosition", window.scrollY);
        });
    });

    if (sessionStorage.getItem("scrollPosition") !== null) {
        window.scrollTo(0, parseInt(sessionStorage.getItem("scrollPosition")));
        sessionStorage.removeItem("scrollPosition");
    }
});
