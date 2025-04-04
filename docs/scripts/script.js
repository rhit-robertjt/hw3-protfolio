/* Help Citation: MDN docs for CSS variables https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascading_variables/Using_CSS_custom_properties. 
I found out that you can change CSS variables from JS, so it was nice to make a "dark mode" even if it doesn't pass a11y standards */
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
