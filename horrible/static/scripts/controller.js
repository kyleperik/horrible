(function (horrible, vue_utils) {
    vue_utils.push_component('controller', {
        data: function () {
            return {
                joined: false,
                username: '',
                room: '',
                question: null,
                answer: ''
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
                horrible.socket.emit('get_question', that.username, that.room);
            });
            horrible.socket.on('question', function (question) {
                that.question = question;
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
                horrible.socket.emit('answer', this.answer);
            }
        }
    });
}(window.horrible, window.vue_utils));
