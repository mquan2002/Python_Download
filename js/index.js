let title = $('.title');

title.on('mouseenter', function() { //hover text 
    cursorFollow.addClass('active') //cho cursor to lên
})
title.on('mouseleave', function() { //outhover text
    cursorFollow.removeClass('active')
})


let tl = gsap.timeline({ delay: 2 }) // delay 2s trước khi xuất hiện
tl.to([title, cursor, cursorFollow], { duration: 2, autoAlpha: 1 })
tl.play();