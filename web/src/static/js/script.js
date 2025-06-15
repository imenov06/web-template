    AOS.init({
        duration: 600, /* Faster animations */
        once: true,
        offset: 40, /* Trigger animations a bit sooner */
        easing: 'ease-out-cubic',
    });

    document.getElementById('currentYearV2').textContent = new Date().getFullYear();

    const mainNav = document.body.querySelector('#navbar');
    let scrollSpyOffset = 80;
    if (mainNav) {
        const updateScrollSpyOffset = () => {
            scrollSpyOffset = mainNav.offsetHeight > 0 ? mainNav.offsetHeight + 10 : 85; // Adjusted offset
        };
        updateScrollSpyOffset();
        window.addEventListener('resize', updateScrollSpyOffset);

        new bootstrap.ScrollSpy(document.body, {
            target: '#navbar',
            offset: scrollSpyOffset,
        });
    }

    const navLinks = document.querySelectorAll('#navbarNav .nav-link');
    const navbarCollapseEl = document.getElementById('navbarNav');
    const bsNavbarCollapse = navbarCollapseEl ? new bootstrap.Collapse(navbarCollapseEl, {toggle: false}) : null;

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (bsNavbarCollapse && navbarCollapseEl.classList.contains('show')) {
                bsNavbarCollapse.hide();
            }
        });
    });

    const fixedCtaBtn = document.getElementById('fixedCtaBtnV2');
    if (fixedCtaBtn) {
        window.addEventListener('scroll', function () {
            if (window.pageYOffset > 700) { // Show button after more scroll
                fixedCtaBtn.classList.add('show');
            } else {
                fixedCtaBtn.classList.remove('show');
            }
        }, false);
    }
