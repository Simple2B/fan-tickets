document.addEventListener("DOMContentLoaded",(function(){var e=document.querySelector(".notification-container"),t=document.getElementById("notification-new-label"),n=document.getElementById("notification-scroll-to-bottom"),o=document.getElementById("scroll-on-bottom-svg"),s=document.getElementById("scroll-on-bottom-messages-count"),c=!1,i=0,d=function(){c=e.scrollTop>=e.scrollHeight-e.clientHeight};e.addEventListener("scroll",(function(){d(),i>0?(o.classList.add("hidden"),s.classList.remove("hidden")):(o.classList.remove("hidden"),s.classList.add("hidden")),c?(n.classList.add("hidden"),i=0):n.classList.remove("hidden")})),n.addEventListener("click",(function(){e.scrollTo(0,e.scrollHeight)})),document.addEventListener("htmx:beforeSwap",(function(){d()})),document.addEventListener("htmx:load",(function(n){var d=n.target;d.classList.contains("new-notification")?(t.classList.contains("hidden")&&(t.classList.remove("hidden"),t.classList.add("flex")),c&&e.scrollTo(0,e.scrollHeight),i++,s.innerText=i.toString(),o.classList.add("hidden"),s.classList.remove("hidden")):e.scrollTo(0,5*d.scrollHeight)}));var l=document.getElementById("user-uuid").value;new EventSource("/sse".concat("?channel=room:".concat(l))).onmessage=function(e){console.log(e)}}));