// ========== Smooth Scroll to Anchor Links ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        }
    });
});

// ========== Dark Mode Toggle ==========
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    // Optional: save user preference in localStorage
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// ========== Load Dark Mode Preference on Page Load ==========
window.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }
});

// ========== Highlight Active Category Card ==========
document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        // Optional: Show alert or navigate
        showToast(`Browsing properties under: ${card.textContent}`);
    });
});


// ========== Toast Notification ==========
function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '30px';
    toast.style.right = '30px';
    toast.style.background = '#2b6cb0';
    toast.style.color = '#fff';
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '6px';
    toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    toast.style.zIndex = '9999';
    toast.style.transition = 'opacity 0.5s ease';
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = 0;
        setTimeout(() => document.body.removeChild(toast), 500);
    }, 3000);
}

'use strict';

/**
 *  navbar toggle in mobile
 */

const /** {NodeElement} */ $navbar = document.querySelector("[data-navbar]");
const /** {NodeElement} */ $navToggler = document.querySelector("[data-nav-toggler]");
const /** {NodeElement} */ $navLinks = document.querySelectorAll("[data-nav-link]");
$navToggler.addEventListener("click", () => {
  $navbar.classList.toggle("active");
});
$navLinks.forEach($link => {
  $link.addEventListener("click", () => {
    $navbar.classList.remove("active");
  });
});
/**
 *  header active on scroll
 */
const /** {NodeElement} */ $header = document.querySelector("[data-header]");
window.addEventListener("scroll", e => {
  if (window.scrollY > 50) {
    $header.classList.add("active");
  } else {
    $header.classList.remove("active");
  }
});
