"is strict"

$(document).ready(function() {
	loadJSON('./PY/data_week.json');	
	$(document).tooltip({
		item: ".channel_program_item_name_inner",
		position: {my: "left center", at: "right+10 center"},
		tooltipClass: "tooltip",
		show: {effect: 'none', delay:400},
		hide: {effect: 'fade', delay:400, duration:600},
		content: function(callback) {
			var elem = $(this);
			console.log($(elem).text());
			var tooltipHTML = $('<div/>').append("Подробная информация о программе <div class='tooltip_program'>" + $(elem).text() + "</div></div>");
			return tooltipHTML;
		}
	});
	//$(".ui-helper-hidden-accessible").hide();
});

var day = 'today'
var channels = [];
var data = [];
var dates = [];
var weekdays = [];

function loadJSON(url) {
	$.getJSON(url, function(jsonData) {
		data = jsonData['data'];
	}).done(function(jsonData) {
		loadChannels();
		loadLinks();
	})
	.fail(function() {
		console.log("json load error");
	})
}

function loadChannels() {
	$('#channels').empty();
	channels = data[day]['channels'];
	for (var i = 0; i < channels.length; i++) {
		var el = $("<div/>", {class : "channel"});
		var name = $("<div/>", {class : "channel_title", html: channels[i]['channel']});
		var label = $("<div/>", {class : "channel_name"});
		var icon = $("<div/>", {class : "channel_icon"});
		icon.css("background-image", 'url("' + channels[i]['icon'] + '")');
		
		icon.appendTo(label);
		name.appendTo(label);
		$(label).appendTo(el);

		var program = $("<div/>", {class : "channel_program"});
		for (var j = 0; j < channels[i]['programs'].length; j++) {
		 	var program_item = $("<div/>", {class : "channel_program_item"});
			var program_item_time = $("<div/>", {class : "channel_program_item_time", "html": channels[i]['programs'][j][0]});
			var program_name = "<span class='channel_program_item_name_inner' title=''>" + channels[i]['programs'][j][1] + "</span>";
			var program_item_name = $("<div/>", {class : "channel_program_item_name", "html": program_name});
			//$(program_item_name).attr('title',  "tooltip");
	
		 	program_item_time.appendTo(program_item);
		 	program_item_name.appendTo(program_item);
		 	program_item.appendTo(program);
		}
		$(program).appendTo(el);

		el.appendTo("#channels");
	}
}

function loadLinks() {
	for (dt in data) {
		if (data[dt]['weekday'] != 'today') {
			dates.push(data[dt]['date']);
			weekdays.push(data[dt]['weekday']);
		}
	}

	var dayDivs = $('.nav_day_link');
	for (var i = 0; i < 6; i++)	{
		$(dayDivs[i + 1]).text(dates[i] + ', ' + weekdays[i]);
	}
}

function selectLink() {
	dayDivs = $('.nav_day');
	$(dayDivs).removeClass('selected');
	if (day == 'today')
		$(dayDivs[0]).addClass('selected');
	else
		$(dayDivs[day]).addClass('selected');
}


function loadPrograms(day) {
		this.day = day;
		loadChannels();

		selectLink();
	}