(function (horrible, vue_utils) {
    vue_utils.push_component('game', {
        data: function () {
            return {
                room: null,
                players: [],
                started: false
            };
        },
        created: function () {
            var that = this;
            horrible.socket.on('game_created', function (room) {
                that.room = room;
                that.$emit('set_control');
            });
            horrible.socket.on('game_started', function () {
                that.started = true;
            });
            horrible.socket.on('joined', function (username) {
                that.players.push(username);
            });
            horrible.socket.on('start_answers', function () {
                console.log('start answers')
            });
        },
        methods: {
            create_game: function () {
                horrible.socket.emit('create_game');
            },
            start_game: function () {
                horrible.socket.emit('start_game', this.room);
            }
        }
    });
}(window.horrible, window.vue_utils));
