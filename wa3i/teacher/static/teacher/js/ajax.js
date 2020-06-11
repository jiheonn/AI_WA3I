$(document).ready(function () {
    $('#menubar').click(function () {
        var username = $('#user-name').text();
        if (username == 'User') {
            alert('로그인을 하셔야 이용 가능합니다. 먼저 로그인을 해주세요.');
        }
    });
});
