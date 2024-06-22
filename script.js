// JavaScript is not strictly necessary for smooth scrolling if you use CSS scroll-behavior
// However, this code can enhance the user experience by handling some edge cases

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');

    for (const link of links) {
        link.addEventListener('click', smoothScroll);
    }

    function smoothScroll(event) {
        event.preventDefault();
        const targetId = event.currentTarget.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);

        window.scrollTo({
            top: targetSection.offsetTop - document.querySelector('header').offsetHeight,
            behavior: 'smooth'
        });
    }
});
