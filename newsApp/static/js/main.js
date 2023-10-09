function loadResultsToLocalStorage(data) {
    var getData = JSON.stringify(data)
    var parseedData = JSON.parse(getData)
    console.log(typeof JSON.parse(parseedData));
}