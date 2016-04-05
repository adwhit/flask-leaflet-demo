BASECOORDS = [-13.9626, 33.7741]

function makeMap() {
    var ACCESS_TOKEN = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw';
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>';
    var MB_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' + ACCESS_TOKEN;

    mymap = L.map('llmap').setView(BASECOORDS, 8);

    L.tileLayer(MB_URL, {attribution: MB_ATTR, id: 'mapbox.streets'}).addTo(mymap);
}

var layer = L.layerGroup();

function renderData(districtid) {
    $.getJSON("/district/" + districtid, function(obj) {
        var markers = obj.data.map(function(arr) {
            return L.marker([arr[0], arr[1]])
        });
        mymap.removeLayer(layer);
        layer = L.layerGroup(markers);
        mymap.addLayer(layer);
    })
}


$(function() {
    makeMap();
    renderData('0')
    $('#distsel').change(function() {
        var val = $('#distsel option:selected').val();
        renderData(val)
    });
})
