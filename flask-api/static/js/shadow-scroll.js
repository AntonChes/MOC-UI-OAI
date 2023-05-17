function scrollShadow(el) {

  var content = el.querySelector('.scroll-content'),
    wrapper = el.querySelector('.scroll-wrapper'),
    shadowTop = el.querySelector('.shadow--top'),
    shadowBottom = el.querySelector('.shadow--bottom'),
    contentScrollHeight = el.scrollHeight - wrapper.offsetHeight;

  content.addEventListener('scroll', function(){
    var currentScroll = this.scrollTop / (contentScrollHeight);  
    shadowTop.style.opacity = currentScroll;
    shadowBottom.style.display = "block";
    shadowBottom.style.opacity = 1 - currentScroll;
    
  });
}

$(".mconfigs-content").scroll(function(){
  let elem2 = document.getElementById('modelConfigSection');
  scrollShadow(elem2);  
});
let elem1 = document.getElementById('chatSection');
scrollShadow(elem1);

