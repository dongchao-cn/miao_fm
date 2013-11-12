
function unix_to_datetime(unix) {
    var now = new Date(parseInt(unix));
    return now.toUTCString();
}
