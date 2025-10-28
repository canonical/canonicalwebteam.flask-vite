console.log("Hello from Flask-Vite!");

setTimeout(() => {
  const element = document.createElement("p");
  element.className = "text-bold";
  element.innerHTML =
    "This text was created and added to the page with with JS.";
  document.body.appendChild(element);
}, 1000);
