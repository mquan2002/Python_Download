let cursor = $('.cursor');
let cursorFollow = $('.cursorFollow');

$(window).on('mousemove', function(e) {
    console.log('mousemove');
    gsap.to(cursor, {
        x: e.clientX - (cursor.width() / 2), //lấy toạ độ chuột X
        y: e.clientY - (cursor.height() / 2), //lấy toạ độ chuột Ys // -() để cho vào trọng tâm mouse
        duration: 0.2
    });

    gsap.to(cursorFollow, {
        x: e.clientX - (cursorFollow.width() / 2),
        y: e.clientY - (cursorFollow.height() / 2),
        duration: 0.4
    })
})