window.vue_utils = window.vue_utils || {};

(function (vue_utils) {
    vue_utils.root = '/'; // Site root
    vue_utils.path = 'static/vues/'; // Relative path to the vues
    
    function request_vue_template(name, callback) {
        return fetch(vue_utils.root + vue_utils.path + name + '.html')
        .then(r => r.text())
        .then(callback);
    }

    var components = {};
    
    vue_utils.push_component = function (name, component) {
        components[name] = component;
    };

    vue_utils.register_components = function (callback) {
        var component_names = Object.keys(components);
        var i = component_names.length;
        component_names.forEach(name => {
            var options = components[name];
            request_vue_template(name, template => {
                options.template = template;
                Vue.component(name, options);
                // decrement request counter
                i--;
                // if this is the last one, then we're finished, run callback
                if (i === 0 && typeof callback === 'function') callback();
            });
        });
    };
})(window.vue_utils);
