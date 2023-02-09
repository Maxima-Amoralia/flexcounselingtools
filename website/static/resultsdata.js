const colors = [
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)',
    'rgb(0, 0, 0)',
  ];

const colorsTrans = [
    'rgb(255, 99, 132, .3)',
    'rgb(255, 159, 64, .3)',
    'rgb(255, 205, 86, .3)',
    'rgb(75, 192, 192, .3)',
    'rgb(54, 162, 235, .3)',
    'rgb(153, 102, 255, .3)',
    'rgb(201, 203, 207, .3)',
    'rgb(0, 0, 0, .3)',
  ];



$('#x-axis').change(function() {    
    datachart.options.scales.x.title.text=$('#x-axis option:selected').text();
    datachart.data.datasets.length =0;
    datachart.update();
})


$('#y-axis').change(function() {    
    datachart.options.scales.y.title.text=$('#y-axis option:selected').text();
    datachart.data.datasets.length =0;
    datachart.update();
})
  

$('form').submit(function(e) {
    e.preventDefault();

    var unindexed_array = $(this).serializeArray();
    var indexed_array = {};

    var xaxis = $('#x-axis').serializeArray();
    var yaxis = $('#y-axis').serializeArray();

    unindexed_array.push({name:'x-axis', value:xaxis[0]['value']});
    unindexed_array.push({name:'y-axis', value:yaxis[0]['value']});

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });


    var college = indexed_array['college'];
    var major_gen = indexed_array['major_gen'];

    var label = college; 
    if (major_gen!='null') {
        label = "'"+label+" "+ major_gen+"'";
    }
    else {
        label = "'"+label+"'";
    }

    var borColor = "'"+colors[indexed_array['color']]+"'";
    var bacColor = "'"+colorsTrans[indexed_array['color']]+"'";

    var output = JSON.stringify(indexed_array);

    fetch('/resultsdata/add', {
        method: "POST",    
        body: output,
    }).then(response=>response.text())
    .then(input=>{ 
        var newDataSet = {
            label: eval(label).toUpperCase(), 
            data: eval(input), 
            borderColor: eval(borColor),
            backgroundColor: eval(bacColor)
        };

        
        datachart.data.datasets.push(newDataSet);
        datachart.update();

    })

});


function clearData() {
    datachart.data.datasets.length =0;
    datachart.update();
}
