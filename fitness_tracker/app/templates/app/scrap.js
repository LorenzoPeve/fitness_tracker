let availableExercises = [
    'Bench Press',
    'Deadlift',
    'pull-ups',
    'barbell row',
    'barbell ski',
    'barbell curls'
]

var exercise_input_box = document.getElementById('exercise')

exercise_input_box.onkeyup = function(){
	let result = [];
	let input = exercise_input_box.value;
    const exercise_list = document.getElementById("exercise_list");

	if (input.length){
		result  = availableExercises.filter((keyword)=>{
            return keyword.toLowerCase().includes(input.toLowerCase());
        });

        console.log(display(result));
        exercise_list.innerHTML = display(result);
	} else {
        exercise_list.innerHTML = '';
    }
}

function display(result){
    const content = result.map((option)=>{
        return '<a class="list-group-item" onclick=selectInput(this)>' + option + '</a>';
    }).join('');
    return content
}

function selectInput(option){
    exercise_input_box.value = option.innerHTML;
    exercise_list.innerHTML = '';
}