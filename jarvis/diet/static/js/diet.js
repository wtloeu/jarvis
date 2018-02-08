$(document).ready(function(){
	// jQuery methods

	// Trigger modal window from buttons at top of page
	//
	// Implement single function that can figure out which button called it
	// and populate the modal window with the appropriate form. 
	
	// Show add entry modal window when user clicks Add Entry button
	$("#btnAddEntry").click(function(){
		$("#nutrition_facts").hide();
		$("#modalAddEntry").modal('show');
	});

	// Show new food modal window when user clicks New Food button
	$("#btnNewFood").click(function(){
		$("#modalNewFood").modal('show');
	});

	// Delete entry when user clicks the badge with the trash can
	$(".badge").click(function(){
		$(this).parent().submit();
	});

	$("#entry_amount_input").change(function(){
		var new_amt = $("#entry_amount_input").val();
		var old_amt = $("#cell_amount").html();
		var cal = $("#cell_calories").html();
		var pr = $("#cell_protein").html();
		var ca = $("#cell_carbohydrates").html();
		var fa = $("#cell_fat").html();
		var fi = $("#cell_fiber").html();
		var mult = new_amt / old_amt;
		$("#cell_amount").html(new_amt);
		$("#cell_calories").html(mult * cal);
		$("#cell_protein").html(mult * pr);
		$("#cell_carbohydrates").html(mult * ca);
		$("#cell_fat").html(mult * fa);
		$("#cell_fiber").html(mult * fi);
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
				$("#entry_amount_input").val(json.serving_size);
				$("#cell_calories").html(json.calories);
				$("#cell_protein").html(json.protein);
				$("#cell_carbohydrates").html(json.carbohydrates);
				$("#cell_fat").html(json.fat);
				$("#cell_fiber").html(json.fiber);
				$("#cell_amount").html(json.serving_size);
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
	}, 3000);
});
