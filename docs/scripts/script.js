function main() {
  document.querySelector('#light-mode').addEventListener("click", () => {
    const root = document.documentElement;
    root.style.setProperty('--main-bg-color', '#AD1414');
    root.style.setProperty('--second-bg-color', '#333');
    root.style.setProperty('--main-color', 'white');
  });
  document.querySelector('#dark-mode').addEventListener("click", () => {
    const root = document.documentElement;
    root.style.setProperty('--main-bg-color', '#333');
    root.style.setProperty('--second-bg-color', '#AD1414');
    root.style.setProperty('--main-color', 'black');
  });
}

// document.addEventListener("DOMContentLoaded", main);
window.addEventListener("load", (event) => {
    console.log("Event Occurred: " + event);
    console.log("Page fully loaded.");
    main();
})
