// Entrypoint for the application.
import { MDCTextField } from '@material/textfield';

class App {

  constructor() {
  }

  onStart() {
    const textFields = document.querySelectorAll('.mdc-text-field');
    textFields.forEach((field) => {
      const textField = new MDCTextField(field);
    });

    // Register service worker.
    if ('serviceWorker' in navigator) {
      console.log("Attempting to reigster service worker.");
      navigator.serviceWorker.register('static/service-worker.js')
        .then(function (reg) {
          console.log("Registered service worker!");
        }).catch(function (err) {
          console.log("Failed to register service worker:", err)
        });
    }
  }
}

window.app = new App();
(() => app.onStart())();