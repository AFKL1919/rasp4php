function show_username(un) {
    $("#login-username").append(
        document.createTextNode(un)
    );
}

export { show_username };