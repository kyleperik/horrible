(function (horrible, vue_utils) {
    vue_utils.push_component('controller', {
        data: function () {
            return {
                joined: false,
                username: '',
                room: '',
                question: null,
                answer: '',
                quit: false
            };
        },
        created: function () {
            var that = this;
            horrible.socket.on('joined', function (username) {
                if (username === that.username) {
                    that.joined = true;
                    that.$emit("set_control");
                }
            });
            horrible.socket.on('game_started', function () {
                horrible.socket.emit('get_question', that.room);
            });
            horrible.socket.on('question', function (question) {
                that.question = question;
            });
            horrible.socket.on('quit', function () {
                that.quit = true;
            });
        },
        methods: {
            join_room: function () {
                horrible.socket.emit('join', {
                    username: this.username,
                    room: this.room
                });
            },
            submit: function () {
                horrible.socket.emit('answer', this.room, this.answer);
            }
        }
    });
}(window.horrible, window.vue_utils));
