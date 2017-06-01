(function (horrible, vue_utils) {
    vue_utils.push_component('app', {
        data: function () {
            return {
                messages: [],
                screen_width: null,
                control: null,
                control_set: false  // whether the control is set in stone
            };
        },
        computed: {
            screen_size: function () {
                return this.screen_width > 500 ? 'LARGE' : 'SMALL';
            }
        },
        created: function () {
            var that = this;
            window.addEventListener('resize', function (e) {
                that.evaluate_screen_size();
            });
            this.evaluate_screen_size();
        },
        methods: {
            evaluate_screen_size: function () {
                this.screen_width = window.innerWidth;
            },
            set_control: function (control, control_set) {
                this.control = control;
                this.control_set = control_set || false;
            },
            push_message: function () {
                this.messages.push(message);
            }
        }
    });
}(window.horrible, window.vue_utils));
