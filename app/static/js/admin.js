(()=>{"use strict";var e={593:(e,n)=>{function t(e){e.classList.add("hidden")}Object.defineProperty(n,"__esModule",{value:!0}),n.handleHideElements=void 0,n.handleHideElements=function(e,n){void 0===n&&(n=[]),e.classList.toggle("hidden"),window.addEventListener("mouseup",(function(o){!function(e,n,o){n.contains(e.target)||o.some((function(n){return n.contains(e.target)}))||t(n)}(o,e,n)})),document.addEventListener("keydown",(function(n){"Escape"===n.key&&t(e)}))}}},n={};function t(o){var d=n[o];if(void 0!==d)return d.exports;var r=n[o]={exports:{}};return e[o](r,r.exports,t),r.exports}(()=>{var e=t(593);console.log("file admin.ts loaded"),console.log("admin.ts loaded 5 row");var n=document.querySelector("#event-dates"),o=document.querySelector("#event-dates-dropdown");n.addEventListener("click",(function(){var n=document.querySelectorAll(".datepicker"),t=Array.from(n);(0,e.handleHideElements)(o,t)}))})()})();