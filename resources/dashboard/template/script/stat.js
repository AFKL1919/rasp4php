// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// -- Area Chart Example
var area = {
  ctx: null,
  myAreaChart: null,
  config: {
    type: 'line',
    data: {
      labels: null,
      datasets: [{
        label: "Attacks",
        lineTension: 0.3,
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 20,
        pointBorderWidth: 2,
        data: null,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 5,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
  },
  init_chart: function (data) {
    this.ctx = $("#myAreaChart");
    
    this.config.data.labels = Object.keys(data);
    this.config.data.datasets[0].data = Object.values(data);

    var data_max = Math.max(...Object.values(data));
    this.config.options.scales.yAxes[0].ticks.max = Math.ceil(data_max * 1.5);

    this.myAreaChart = new Chart(this.ctx, this.config);
  }
}

// -- Bar Chart Example
var bar = {
  ctx: null,
  myBarChart: null,
  config: {
    type: 'bar',
    data: {
      labels: null,
      datasets: [{
        label: "Attack IP",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: null,
      }],
    },
    options: {
      responsive: true,
      scales: {
        xAxes: [{
          time: {
            unit: 'month'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 6
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 15000,
            maxTicksLimit: 5
          },
          gridLines: {
            display: true
          }
        }],
      },
      legend: {
        display: false
      }
    }
  },
  init_chart: function (data) {
    this.ctx = $("#myBarChart");

    this.config.data.labels = Object.keys(data);
    this.config.data.datasets[0].data = Object.values(data);

    var data_max = Math.max(...Object.values(data));
    this.config.options.scales.yAxes[0].ticks.max = Math.ceil(data_max * 1.5);

    this.myBarChart = new Chart(this.ctx, this.config);
  }
}

var tran = {
  code_execution: '代码执行攻击',
  command_execution: '命令执行攻击',
  file_upload: '文件上传攻击',
  file_operation: '文件非法操作',
  network_access: '网络非法访问',
  info_leak: '敏感信息泄露',
  database_operation: '数据库攻击',
  deserialization: '反序列化攻击',
  xml_external_entity: 'xml实体攻击',
  start_request: '黑名单阻拦'
}

var pie_color = [
  '#ff0000', '#ff6600', '#ffff00', '#00ff00',
  '#ff0000', '#0000ff', '#ff00ff', '#99ff00'
];

// -- Pie Chart Example
var pie = {
  ctx: null,
  myPieChart: null,
  config: {
    type: 'pie',
    data: {
      labels: null,
      datasets: [{
        data: null,
        backgroundColor: pie_color,
        options: {
          responsive: true
        }
      }],
    },
  },
  init_chart: function (data) {
    this.ctx = $("#myPieChart");

    var data_keys = Object.keys(data);
    data_keys.forEach((element, index) => {
      data_keys[index] = tran[element];
    });

    this.config.data.labels = data_keys;
    this.config.data.datasets[0].data = Object.values(data);

    this.myPieChart = new Chart(this.ctx, this.config);
  }
}

function set_stat_data(url, chart) {
  $.ajax({
    url: url,
    type: 'POST',
    success: function (data) {
      if (data["status"] == 200) {
        chart.init_chart(data["data"]);
      } else {
        alert('请求数据失败！');
      }
    },
    error: function () {
      alert('请求数据失败！');
    }
  });
}

export { area, bar, pie, set_stat_data };