Plotly.newPlot('chart0', data, layout);

// code to make plotlyjs responsive
(function() {
  var d3 = Plotly.d3;
  var WIDTH_IN_PERCENT_OF_PARENT = 100,
      HEIGHT_IN_PERCENT_OF_PARENT = 100;

var gd3 = d3.selectAll(".responsive-plot")
        .style({
          width: 'fit-content',
          'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

          height: 'fit-content',
          'margin-top': '0vh'
        });

  var nodes_to_resize = gd3[0]; //not sure why but the goods are within a nested array
  window.onresize = function() {
    for (var i = 0; i < nodes_to_resize.length; i++) {
      Plotly.Plots.resize(nodes_to_resize[i]);
    }
  };

})();