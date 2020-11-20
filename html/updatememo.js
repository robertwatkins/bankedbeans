var hidden_columns = ["id","transaction_type", "balance", "category", "subcategory"];
var _table_ = document.createElement('table'),
  _tr_ = document.createElement('tr'),
  _th_ = document.createElement('th'),
  _td_ = document.createElement('td');

// Builds the HTML Table out of myList json data from Ivy restful service.
function buildHtmlTable(arr) {
  var table = _table_.cloneNode(false),
    columns = addAllColumnHeaders(arr, table);
  for (var i = 0, maxi = arr.length; i < maxi; ++i) {
    var tr = _tr_.cloneNode(false);
    for (var j = 0, maxj = columns.length; j < maxj; ++j) {
      var td = _td_.cloneNode(false);
      cellValue = arr[i][columns[j]];
      columnname = columns[j]
      if (columnname == "memo") {
        var input = document.createElement("input");
        input.type = "text";
        input.value = arr[i]["memo"];
        input.name = "memofortransaction" + arr[i]["id"];
        td.appendChild(input);
      } else {
        td.appendChild(document.createTextNode(arr[i][columnname] || ''));
      }
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
  return table;
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(arr, table) {
  var columnSet = [],
    tr = _tr_.cloneNode(false);
  for (var i = 0, l = arr.length; i < l; i++) {
    for (var key in arr[i]) {
      if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1 && (hidden_columns.indexOf(key) === -1)) {
        columnSet.push(key);
        key = key.replace("automated","");
        var th = _th_.cloneNode(false);
        th.appendChild(document.createTextNode(key));
        tr.appendChild(th);
      }
    }
  }
  table.appendChild(tr);
  return columnSet;
}

function setmemo(){
    console.log("Starting to process memo data");
    var memoform = document.getElementById("memoform")
    var memoupdates = memoform.elements;
    var memoupdatelist = [];
    for (i=0; i<memoupdates.length; i++){
        var memoupdate = memoupdates[i];
        if (memoupdate.name != "submit"){
            var memojson = new Object();
            var id = (memoupdates[i].name).substring(18);
            var value = memoupdates[i].value;
            memojson.id = id;
            memojson.memo = value;
            memoupdatelist.push(memojson);
        }
    }
    var memodata = JSON.stringify(memoupdatelist)
    console.log(memodata);
    var xhr = new XMLHttpRequest();
    var url = "/memobyid/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(memodata);
    var topsubmitbutton = document.getElementById("submit_button_top");
    topsubmitbutton.value = "Submitting...";
    var bottomsubmitbutton = document.getElementById("submit_button_bottom");
    bottomsubmitbutton.value = "Submitting...";
    setTimeout(function(){
        console.log('Janky Wait :)');
        memoform.reset();
        window.location.reload(false);
        console.log("Finished processing memo data");
    }, 3000);

}

function updatetitle (datasource) {
    console.log(datasource);
    var contentdescription = document.getElementById("contentdescription");
    contentdescription.appendChild(document.createTextNode(datasource));
}