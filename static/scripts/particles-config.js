particlesJS("particles-js", {
  particles: {
    number: {
      value: 90,
      density: {
        enable: true,
        value_area: 900
      }
    },

    color: {
      value: ["#00bfff", "#ffffff", "#38bdf8"]
    },

    shape: {
      type: ["circle", "triangle", "polygon", "edge"]
    },

    opacity: {
      value: 0.6,
      random: true
    },

    size: {
      value: 4,
      random: true,
      anim: {
        enable: true,
        speed: 2,
        size_min: 0.5,
        sync: false
      }
    },

    line_linked: {
      enable: true,
      distance: 130,
      color: "#00bfff",
      opacity: 0.25,
      width: 1
    },

    move: {
      enable: true,
      speed: 1.2,
      direction: "none",
      random: true,
      straight: false,
      out_mode: "out"
    }
  },

  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "repulse"
      },
      onclick: {
        enable: true,
        mode: "push"
      }
    }
  },

  retina_detect: true
});
