var msgs = document.getElementsByClassName("parent")[0];
var temp = 0;
var child;
msgs.innerHTML = '';
var str = '';
for (i = 0; i < messages.length; ++i) {
    str = '<div class="';
    if (messages[i].isMy) {
        str += 'my ';
    } else { str += 'friend '; }
    str += 'message" style="top: ' +
        (5 + temp) +
        'px"><h1>' +
        messages[i].username +
        '</h1>' +
        messages[i].context +
        '<p>' +
        messages[i].date +
        '</p></div>';

    msgs.innerHTML += str;
    console.log(msgs.childNodes[i].scrollHeight);
    temp += msgs.childNodes[i].scrollHeight + 5;
    console.log(msgs);
}
document.getElementsByClassName("chat-body")[0].scrollTop += 9999999999999999999;
