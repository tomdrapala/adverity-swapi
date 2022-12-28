const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            enteredGoalValue: '',
            people: people
        };
    },
    computed: {
    },
    methods: {
        fetchData() {
            this.people.push(this.enteredGoalValue);
        },
        removeGoal(idx) {
            this.people.splice(idx, 1);
        }
    }
});

app.mount('#collections');
