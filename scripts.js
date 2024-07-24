function showAccommodation() {
    var accSection = document.querySelector('.accommodation-section');
    var contentSection = document.querySelector('.content');
    accSection.style.display = 'block';
    contentSection.style.display = 'none';
}

function hideAccommodation() {
    var accSection = document.querySelector('.accommodation-section');
    var contentSection = document.querySelector('.content');
    accSection.style.display = 'none';
    contentSection.style.display = 'block';
}

// Function to load and display the employment chart
window.addEventListener('DOMContentLoaded', function() {
    console.log("DOMContentLoaded event fired");

    // Sample data to replace CSV file
    var data = [
        {Sector: 'Agriculture', NOC: '80020', Employment: 447},
        {Sector: 'Agriculture', NOC: '84120', Employment: 97},
        {Sector: 'Agriculture', NOC: '85100', Employment: 45},
        {Sector: 'Agriculture', NOC: '80022', Employment: 34},
        {Sector: 'Agriculture', NOC: '18', Employment: 26},
        {Sector: 'Business', NOC: '10010', Employment: 532},
        {Sector: 'Business', NOC: '10020', Employment: 421},
        {Sector: 'Construction', NOC: '72000', Employment: 342},
        {Sector: 'Construction', NOC: '72300', Employment: 298},
        {Sector: 'Healthcare', NOC: '31100', Employment: 654},
        {Sector: 'Healthcare', NOC: '31200', Employment: 432},
        {Sector: 'Information', NOC: '52400', Employment: 78},
        {Sector: 'Information', NOC: '52500', Employment: 55},
        {Sector: 'Manufacturing', NOC: '94100', Employment: 97},
        {Sector: 'Manufacturing', NOC: '94200', Employment: 85},
        {Sector: 'Mining', NOC: '84100', Employment: 61},
        {Sector: 'Mining', NOC: '84200', Employment: 42},
        {Sector: 'Other Services', NOC: '65400', Employment: 104},
        {Sector: 'Other Services', NOC: '65500', Employment: 89},
        {Sector: 'Professional', NOC: '11200', Employment: 376},
        {Sector: 'Professional', NOC: '11300', Employment: 287},
        {Sector: 'Public Administration', NOC: '41400', Employment: 458},
        {Sector: 'Public Administration', NOC: '41500', Employment: 339},
        {Sector: 'Retail', NOC: '64200', Employment: 244},
        {Sector: 'Retail', NOC: '64300', Employment: 187},
        {Sector: 'Transportation', NOC: '75100', Employment: 289},
        {Sector: 'Transportation', NOC: '75200', Employment: 198},
        {Sector: 'Utilities', NOC: '92400', Employment: 73},
        {Sector: 'Utilities', NOC: '92500', Employment: 61},
        {Sector: 'Wholesale', NOC: '64100', Employment: 129},
        {Sector: 'Wholesale', NOC: '64200', Employment: 114},
    ];

    var sector_totals = {};
    var customdata = {};

    data.forEach(function(row) {
        console.log("Processing row: ", row);
        if (!sector_totals[row.Sector]) {
            sector_totals[row.Sector] = 0;
            customdata[row.Sector] = [];
        }
        sector_totals[row.Sector] += +row.Employment;
        customdata[row.Sector].push(`NOC ${row.NOC}: ${row.Employment} jobs`);
    });

    var values = Object.values(sector_totals);
    var labels = Object.keys(sector_totals);
    var customdata_values = labels.map(function(label) {
        return customdata[label].join('<br>');
    });

    console.log("Chart data values: ", values);
    console.log("Chart data labels: ", labels);
    console.log("Chart data customdata_values: ", customdata_values);

    var chart_data = [{
        values: values,
        labels: labels,
        type: 'pie',
        hovertemplate: '%{label}<br>Total: %{value}<br>%{customdata}',
        customdata: customdata_values
    }];

    var layout = {
        title: 'Total Employment by Sector'
    };

    Plotly.newPlot('employment-chart', chart_data, layout);
});
