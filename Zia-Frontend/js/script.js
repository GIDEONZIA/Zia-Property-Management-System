// === Smooth Scroll to Anchor Links ===
document.querySelectorAll('a[href^="#"]').forEach(anchor =>{
    anchor.addEventListener("click", function(e){
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({ behavior:"smooth"});
        }
    });
});

// === Optional: Dark Mode Toggle ===
function toggleDarkMode(){
    document.body.classList.toggle('dark-mode');
}

    // Optional visual feedback
    document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');

