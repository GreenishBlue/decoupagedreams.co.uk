// Entrypoint for the application.
import { MDCTextField } from '@material/textfield';
import { MDCDrawer } from "@material/drawer";
import { MDCTopAppBar } from "@material/top-app-bar";

class App {

  constructor() {
  }

  onStart() {
    const textFields = document.querySelectorAll('.mdc-text-field');
    textFields.forEach((field) => {
      const textField = new MDCTextField(field);
    });

    const drawer = MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));

    const topAppBar = MDCTopAppBar.attachTo(document.getElementById('app-bar'));
    topAppBar.setScrollTarget(document.getElementById('main-content'));
    topAppBar.listen('MDCTopAppBar:nav', () => {
      drawer.open = !drawer.open;
    });

    const navDrawer = document.querySelector('.data-nav-drawer');
    const navDrawerButtons = document.querySelectorAll('.data-nav-toggle');
    navDrawerButtons.forEach((button) => {
      button.addEventListener('click', (e) => {
        // Toggle drawer.
	const closedStyle = 'fold-nav-drawer-closed';
	if(navDrawer.classList.contains(closedStyle)) {
          navDrawer.classList.remove(closedStyle);
	} else {
          navDrawer.classList.add(closedStyle);
	}
      }, false)
    });

    const lazyImages = [].slice.call(document.querySelectorAll('img.data-img-lazy'));
    let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          let lazyImage = entry.target;
	  if(lazyImage == null || lazyImage == undefined) {
            return;
	  }
          lazyImage.src = lazyImage.dataset.src;
          lazyImage.srcset = lazyImage.dataset.srcset;
          lazyImage.classList.remove('data-img-lazy');
          lazyImageObserver.unobserve(lazyImage);

 	  console.log('lazy loading image: ' + src);
        }
      });
    });
    lazyImages.forEach((imageElement) => {
      // Check if InteractionObserver is supported, otherwise just load images.
      if (!'IntersectionObserver' in window &&
          !'IntersectionObserverEntry' in window &&
          !'intersectionRatio' in window.IntersectionObserverEntry.prototype) {
        imageElement.setAttribute('src', this.source); 
      } else {
        lazyImageObserver.observe(imageElement);
      }
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

    // down: 40
    const konamiKeys = [
      38, 38, // up up
      40, 40, // down down,
      37, 39, // left right
      37, 39, // left right
      66, 65, // b, a
      13, // enter
    ];
    var recentKeys = [];
    document.onkeydown = (e) => {
      recentKeys.push(e.keyCode);
      const lastKeys = recentKeys.slice(-11);
      if(JSON.stringify(konamiKeys) == JSON.stringify(lastKeys)) {
	      console.log("triggered!");
        const easterEggStyle = 'easter-egg';
        const bodyElement = document.querySelector('body');    
        bodyElement.classList.add(easterEggStyle);
      }
    };
  }
}

window.app = new App();
(() => app.onStart())();
