const app = Vue.createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      peopleData: [],
      columns: [],
      allDataLoaded: false,
      isLoading: false,
      fetchError: null,
      loadError: null,
      notFound: false,
      url: "http://127.0.0.1:8000/",
      file_id: location.pathname.replaceAll('/', '')
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData(startRow) {
      // Using standard fetch to avoid installing additional packages.
      // In a real-life project however, I would recommend using Axios instead.
      url = this.url + "api/people/" + this.file_id + '/'
      if (startRow) {
        url = url + '?start_row=' + startRow
      }
      fetch(url)
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status === 404) {
            this.notFound = true;
          } else {
            this.loadError = "Failed to load data, please try again later";
          }
        })
        .then((data) => {
          if (data.length < 10) {
            this.allDataLoaded = true;
          }
          this.peopleData = this.peopleData.concat(data);
          this.columns = Object.keys(data[0])
        });
    },
    getValue(dict, key) {
      return dict[key]
    }
  },
});

app.mount("#vue_app");
