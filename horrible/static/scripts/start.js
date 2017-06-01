window.horrible = {};

(function (horrible) {
    function init_vue() {
        new Vue({
            el: '#Content'
        });
    }

    function init_socket() {
        horrible.socket = io.connect('http://' + document.domain + ':' + location.port);
        return new Promise(function (resolve, reject) {
            horrible.socket.on('connect', function() {
                resolve();
            });
        });
    }

    function start() {
        init_socket()
        .then(init_vue);
    }
    
    window.onload = function () {
        window.vue_utils.register_components(start);
    };
}(window.horrible));
