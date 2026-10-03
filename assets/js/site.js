const navigationToggle = document.querySelector(".nav-toggle");
const navigation = document.querySelector(".site-nav");

if (navigationToggle && navigation) {
  navigationToggle.addEventListener("click", () => {
    const open = navigation.classList.toggle("is-open");
    navigationToggle.setAttribute("aria-expanded", String(open));
  });

  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a") && navigation.classList.contains("is-open")) {
      navigation.classList.remove("is-open");
      navigationToggle.setAttribute("aria-expanded", "false");
    }
  });
}

const publicHeader = document.querySelector(".public-header");

if (publicHeader && document.body.classList.contains("public-home")) {
  const updateHeader = () => {
    publicHeader.classList.toggle("is-scrolled", window.scrollY > 24);
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
}

const revealItems = document.querySelectorAll(".hf-reveal, .hf-media-reveal");

if (revealItems.length) {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver(
      (entries, activeObserver) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            activeObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );

    revealItems.forEach((item) => observer.observe(item));
  }
}

