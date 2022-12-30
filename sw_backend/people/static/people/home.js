const app = Vue.createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      peopleData: [],
      isLoading: false,
      fetchError: null,
      loadError: null,
      url: "http://127.0.0.1:8000/",
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      // Using standard fetch to avoid installing additional packages.
      // In a real-life project however, I would recommend using Axios instead.
      fetch(this.url + "api/people/")
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            this.loadError = "Failed to load data, please try again later";
          }
        })
        .then((data) => {
          const results = [];
          for (const id in data) {
            results.push({
              id: data[id].id,
              file_name: data[id].file_name,
              date_created: data[id].date_created,
            });
          }
          this.peopleData = results;
        });
    },
    fetchNewData() {
      this.isLoading = true;
      fetch(this.url + "api/fetch_people_data/", { method: "POST" })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            this.fetchError = "Failed to fetch data, please try again later";
          }
        })
        .then((data) => {
          this.isLoading = false;
          this.peopleData.unshift({
            id: data.id,
            file_name: data.file_name,
            date_created: data.date_created,
          });
        });
    },
  },
});

app.mount("#vue_app");
