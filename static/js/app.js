document.addEventListener("DOMContentLoaded",()=>{
 document.querySelectorAll(".panel,.stat,.dash-stats>div").forEach((el,i)=>{
  el.style.setProperty("--delay",`${Math.min(i*55,400)}ms`);
 });
});
