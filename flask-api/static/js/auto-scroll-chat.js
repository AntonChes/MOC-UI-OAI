
function scrollToElement(container, el) {
    var cont = container;
    var position = el.offset().top - cont.offset().top + cont.scrollTop();
	cont.animate({
		scrollTop: position
	});
}