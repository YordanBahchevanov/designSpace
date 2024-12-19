document.addEventListener("DOMContentLoaded", function () {
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = lightbox.querySelector(".lightbox-image");
    const closeLightbox = lightbox.querySelector(".close");

    document.querySelectorAll(".lightbox-trigger").forEach(img => {
        img.addEventListener("click", function () {
            const imageUrl = this.getAttribute("data-image-url");
            lightboxImage.src = imageUrl;
            lightbox.classList.remove("hidden");
        });
    });

    closeLightbox.addEventListener("click", function () {
        lightbox.classList.add("hidden");
        lightboxImage.src = "";
    });

    lightbox.addEventListener("click", function (e) {
        if (e.target === lightbox) {
            lightbox.classList.add("hidden");
            lightboxImage.src = "";
        }
    });
});
