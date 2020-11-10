// let i = 0;

// function clonar() {
//     if (i >= 0) {
//         i++;
//         dates = [
//             $("#developer_id").clone().prop({id:'ia'+ i}).appendTo("#list"),
//             $("#type_task_id").clone().prop({id:'ia'+ i}).appendTo("#list"),
//             $("#task_id").clone().prop({id:'ia'+ i}).appendTo("#list"),
//             $("#description_id").clone().prop({id:'ia'+ i}).appendTo("#list"),
//             $("#state_id").clone().prop({id:'ia'+ i}).appendTo("#list"),
//         ];

//         sessionStorage.setItem('sessions'+i, dates);
//     }
// }

<script>
    $('#data').submit(function (e) {
        e.preventDefault();

        var serializer = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '{% url 'tasks: serializer' %}',
            data: serializer,
            success: function (response) {
                alert('holi')
            }
        })
    })
</script>