function getCountdown(date) {
    var deadline = new Date(date);
    var today = new Date(Date.now());
    var modulo = 12 % 9;
    var Difference_In_Minutes =
    parseInt(deadline.getTime() - today.getTime()) / (60 * 1000);
    var days = parseInt(Difference_In_Minutes / (60 * 24));
    var hours = parseInt((Difference_In_Minutes % (60 * 24)) / 60);
    var minutes = parseInt((Difference_In_Minutes % (60 * 24)) % 60);
    return [
    ("0" + days).slice(-2),
    ("0" + hours).slice(-2),
    ("0" + minutes).slice(-2)
    ];
}
function getCountdownDays(date) {
    values = getCountdown(date);
    return values[0];
}
function getCountdownHours(date) {
    values = getCountdown(date);
    return values[1];
}
function getCountdownMins(date) {
    values = getCountdown(date);
    return values[2];
}