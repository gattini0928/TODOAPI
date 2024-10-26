$.ajax({
    type: 'POST',
    url: '{% url "add_task" %}',
    data: {
        'name': $('#task_name').val(),
        'category': $('#category').val(),
        'priority': $('#priority').val(),
        'due_date': $('#due_date').val(),
        'status': $('#status').val(),
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    success: function(response) {
        alert(response.message);
    },
    error: function() {
        alert('Error occurred');
    }
});
