// Entrypoint for the application.
//

class App {

  constructor() {
  }

  onStart() {
    console.log('onStart called');

    const mastheadContainer = document.querySelector('.data-masthead');

    const appShell = document.querySelector('.data-app-shell');

    // Setup navigation event listeners.
    const navLinks = document.querySelectorAll('.data-href-spa');
    navLinks.forEach((link) => {
      console.log('Binding link: ' + link.href);
    });

  }
}

window.app = new App();
(() => app.onStart())();



