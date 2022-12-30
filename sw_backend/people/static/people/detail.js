const app = Vue.createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      allDataLoaded: false,
      aggregatedPeopleData: [],
      aggregatedPeopleColumns: [],
      columns: [],
      fetchError: null,
      fileId: location.pathname.replaceAll('/', ''),
      fileName: '',
      generalView: true,
      ignoredColumns: [],
      isLoading: false,
      loadError: null,
      notFound: false,
      peopleData: [],
      selectedColumns: [],
      url: "http://127.0.0.1:8000/",
    };
  },
  computed: {
    detailUrl() {
      return this.url + 'api/people/' + this.fileId + '/'
    },
  },
  mounted() {
    this.loadData();
    this.getFileName();
  },
  methods: {
    loadData(startRow) {
      url = this.detailUrl
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
          this.columns = Object.keys(data[0]);
        });
    },
    resetSelectedColumns() {
      this.selectedColumns = []
    },
    loadAggregatedData() {
      url = this.detailUrl + 'value_count/?columns=' + this.selectedColumns.join()
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
          this.aggregatedPeopleData = data;
          this.aggregatedPeopleColumns = Object.keys(data[0]);
        });
    },
    clearAggregatedTable() {
      this.aggregatedPeopleColumns = []
      this.aggregatedPeopleData = []
    },
    getCellValue(dict, key) {
      // TODO: parse list data to strings
      // return dict[key]
      if (dict[key][0] && dict[key][0] === '[') {
        return dict[key].slice(1,-1).replaceAll("'", "")
      } else {
        return dict[key]
      }
    },
    getFileName() {
      url = this.detailUrl + 'file_name/'
      fetch(url)
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          this.fileName = data.file_name;
        });
    },
    toggleColumn(column) {
      column = column[0][0]
      if (this.selectedColumns.includes(column)) {
        this.selectedColumns = this.selectedColumns.filter(e => e !== column);
      } else {
        this.selectedColumns.push(column)
      }
    },
    isColumnSelected(column) {
      return this.selectedColumns.includes(column[0][0])
    },
    toggleView() {
      this.generalView = !this.generalView
    }
  },
});

app.mount("#vue_app");
