document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript Loaded!');
});

function showSection(sectionId) {
            const sections = document.querySelectorAll('.form-section');
            sections.forEach(section => section.style.display = 'none');
            document.getElementById(sectionId).style.display = 'block';
        }

document.getElementById('register-link').addEventListener('click', function() {
    document.getElementById('hero-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
});

document.getElementById('login-link').addEventListener('click', function() {
    document.getElementById('hero-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
});

document.getElementById('home-link').addEventListener('click', function() {
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('hero-section').style.display = 'block';
});
