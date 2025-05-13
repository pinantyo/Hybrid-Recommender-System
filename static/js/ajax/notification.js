// Long poling

const getNotifications = () => {
    $.ajax({
        url:'/api/get-status-changes',
        type:'GET',
        data:{
            'user': "{{ user }}"
        },
        success:(res)=>{

        },
        error:(err)=>{

        }
    });
}