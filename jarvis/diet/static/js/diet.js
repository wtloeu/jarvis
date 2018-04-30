$(document).ready(function(){
	// jQuery methods

	// Trigger modal window from buttons at top of page
	//
	// Implement single function that can figure out which button called it
	// and populate the modal window with the appropriate form. 

	//GLOBALS
	var typingTimer;    
	
	// Show add entry modal window when user clicks Add Entry button
	$("#btnAddEntry").click(function(){
		$("#nutrition_facts").hide();
		$("#modalAddEntry").modal('show');
	});

	// Show new food modal window when user clicks New Food button
	$("#btnNewFood").click(function(){
		$("#modalNewFood").modal('show');
		$("#fatsecret-serving-size").replaceWith('<select class="custom-select" id="fatsecret-serving-size" name="serving_size" onChange="selectedFoodServingSize();" required=""></select>')
		$("#fatsecret-serving-size").prop('disabled', 'disabled');
	});

	// Delete entry when user clicks the badge with the trash can
	$(".badge").click(function(){
		$(this).parent().submit();
	});

	$("#entry_amount_input").change(function(){
		var new_amt = $("#entry_amount_input").val();
		var old_amt = $("#cell_amount").html();
		var cal = $("#cell_calories").html();
		var fa = $("#cell_fat").html();
		var ca = $("#cell_carbohydrates").html();
		var fi = $("#cell_fiber").html();
		var pr = $("#cell_protein").html();
		var mult = new_amt / old_amt;
		$("#cell_amount").html(new_amt);
		$("#cell_calories").html(mult * cal);
		$("#cell_fat").html(mult * fa);
		$("#cell_carbohydrates").html(mult * ca);
		$("#cell_fiber").html(mult * fi);
		$("#cell_protein").html(mult * pr);
	});    

	//on keyup, start the countdown
	$("#fatsecret-search").on('keyup', function () {
	  clearTimeout(typingTimer);
	  typingTimer = setTimeout(doneTyping, 3000);
	});

	//on keydown, clear the countdown 
	$("#fatsecret-search").on('keydown', function () {
	  clearTimeout(typingTimer);
	});

	// Do an ajax search when the user selects a food to eat.
	// Use the response to populate the label to show the
	// amount in a single serving
	$("#select-food").change(function(){
		// Grab food ID from select form
		food = $("#select-food").val();

		$.ajax({
			url: 'food_info/' + food + '/',
			dataType: 'text',
			success: function(data) {
				var json = JSON.parse(data);
				$("#entry_amount_input").val(1);
				$("#cell_calories").html(json.calories);
				$("#cell_fat").html(json.fat);
				$("#cell_carbohydrates").html(json.carbohydrates);
				$("#cell_fiber").html(json.fiber);
				$("#cell_protein").html(json.protein);
				$("#cell_amount").html(1);
				$("#nutrition_facts").show();
			},
			failure: function(data) {
				alert("it didn't work");
			}
		});
	});

	// Automatically close alerts after 3 seconds
	setTimeout(function(){
		$(".alert").alert('close');
	}, 2000);
});

//user is "finished typing," do something
function doneTyping () {
  var search_term = $("#fatsecret-search").val();

	$.ajax({
	    url: 'search_fatsecret/' + search_term + '/',
	    dataType: 'text',
	    success: function(data) { 
	    	var json = JSON.parse(data);
	    	json.sort(function(a, b){
			    return a.food_name - b.food_name;
			});
	    	var options = '';

	    	json.forEach(function(item) {
	    		var description = item.food_description.split('|');
	    		var brand = (item.food_type == "Generic") ? "Generic":item.brand_name;
	    		options += '<option value="' + item.food_id + '">' + item.food_name + ' | ' + brand + '</option>';
	    	});

	    	$("#foods-datalist").html(options);
	    },
	    failure: function(data) {
	    	alert("it didn't work");
	    }
	});
}

function selectedFoodServingSize () {
	var food_id = $("#cell_ids").html();
	var serving_description = $("#fatsecret-serving-size").val();
	alert(serving_description); 
	$.ajax({
	    url: 'get_fatsecret_food/' + food_id + '/',
	    dataType: 'text',
	    success: function(data) { 
	    	var json = JSON.parse(data);
	    	json.servings.serving.forEach(function(item) {
	    		if (item.serving_description == serving_description) {
	    			// Use the first option to populate the fields
		    		$("#id_calories").val(item.calories);
					$("#id_fat").val(item.fat);
					$("#id_carbohydrates").val(item.carbohydrate);
					$("#id_fiber").val(item.fiber);
					$("#id_protein").val(item.protein);
	    		}
    		});	    	
	    },
	    failure: function(data) {
	    	alert("it didn't work");
	    }
	});
}

function selectedFoodFromDatalist () {
	var val = $("#fatsecret-search").val();
    var opts = $("#foods-datalist").children();
    for (var i = 0; i < opts.length; i++) {
    	if (opts[i].value === val) {
    		// User has selected a value from the list of fatsecret foods
    		// Use the food_id to gather the macronutrient info for the selected food
    		// Populate the form with the returned 
    		$("#cell_ids").html(val);
    		$.ajax({
			    url: 'get_fatsecret_food/' + val + '/',
			    dataType: 'text',
			    success: function(data) { 
			    	var json = JSON.parse(data);
			    	$("#fatsecret-search").val(json.food_name);
			    	//Clear current options from the select box
		    		var select_box = document.getElementById('fatsecret-serving-size');
		    		select_box.options.length = 0;
			    	// Check if json.servings.serving is an array or not
			    	if (json.servings.serving[0]) {
			    		// ARRAY: add each option for serving sizes to the array box
			    		json.servings.serving.forEach(function(item) {
			    			var opt = document.createElement('option');
			    			opt.value = item.serving_description;
			    			opt.innerHTML = item.serving_description;
			    			select_box.appendChild(opt);
			    		})

			    		// Use the first option to populate the fields
			    		$("#id_calories").val(json.servings.serving[0].calories);
						$("#id_fat").val(json.servings.serving[0].fat);
						$("#id_carbohydrates").val(json.servings.serving[0].carbohydrate);
						$("#id_fiber").val(json.servings.serving[0].fiber);
						$("#id_protein").val(json.servings.serving[0].protein);
			    	}
			    	else {
			    		// Only one option. use it to populate the fields
			    		var opt = document.createElement('option');
		    			opt.value = json.servings.serving.serving_description;
		    			opt.innerHTML = json.servings.serving.serving_description;
		    			select_box.appendChild(opt);
						$("#id_calories").val(json.servings.serving.calories);
						$("#id_fat").val(json.servings.serving.fat);
						$("#id_carbohydrates").val(json.servings.serving.carbohydrate);
						$("#id_fiber").val(json.servings.serving.fiber);
						$("#id_protein").val(json.servings.serving.protein);
			    	}
			    	$("#fatsecret-serving-size").prop('disabled', false);
			    },
			    failure: function(data) {
			    	alert("it didn't work");
			    }
			});
    		break;
      	}
    }
} 
