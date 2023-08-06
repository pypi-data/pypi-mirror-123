(function() {
    var app = new Vue({
        el: '#app',
        data(){
        return {
                message: 'Yeah!',
                hosts: null,
                thermostats: null,
                defaultTemperatures: [5, 20, 25]
            }
        },
        async mounted() {
            this.hosts = (await axios.get('/api/hosts')).data;
            this.thermostats = (await axios.get('/api/thermostats')).data;
            // https://stackoverflow.com/a/55379279
            this.thermostats.forEach(t => this.$set(t, 'temperature', 22));
         },
        methods: {
            wakeupHost: (name) => {
                axios
                  .post('/api/wake-on-lan', {
                    name: name
                  })
            },
            changeToAutomatic: (name) => {
                axios
                  .post('/api/thermostats/change-to-automatic', {
                    name: name
                  })
            },
            changeTemperatureTo: (name, temperature) => {
                changeTemperatureTo(name, temperature)
            },
            changeTemperature: (thermostat) => {
                changeTemperatureTo(thermostat.name, thermostat.temperature)
            }
        }
    });


    function changeTemperatureTo(name, temperature) {
                axios
                  .post('/api/thermostats/change-temperature', {
                    name: name,
                    temperature: temperature
                  })
            }
})();