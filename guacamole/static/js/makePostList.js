function makePostList(array) {
    // Create the list element:
    var parent = document.createElement('div');
    var template = document.querySelector('#post_template');
    for (var i = 0; i < array.length; i++) {
        var post = array[i];
        var clone = template.content.cloneNode(true);
        // SET ID
        clone.querySelector("#post_id").id = post['id'];
        clone.querySelector("#post_title").innerHTML = post['title'];
        clone.querySelector("#post_budget").innerHTML = post['budget'];
        clone.querySelector("#post_user").innerHTML = "@"+post['author_user'];
        clone.querySelector("#post_user").href = "/marketplace/user/"+post['author'];
        clone.querySelector("#post_date").innerHTML = post['timestamp'];
        clone.querySelector("#post_body").innerHTML = post['body'];

        var days = getCountdownDays(post['deadline']);
        var hours = getCountdownHours(post['deadline']);
        var minutes = getCountdownMins(post['deadline']);

        var countdown = getCountdown(post['deadline'])
        clone.querySelector("#post_deadline_days").innerHTML = countdown[2];
        clone.querySelector("#post_deadline_hours").innerHTML = countdown[1];
        clone.querySelector("#post_deadline_minutes").innerHTML = countdown[0];

        
        var user_id = document.getElementById('user_id').content;
        console.log(user_id);
        // if (user_id == post['author']) {
        //     clone.querySelector("#post_btn_action").innerHTML = "VIEW";
        //     clone.querySelector("#post_btn_action").href = "/me/post/"+post['key'];
        // } else {
        //     clone.querySelector("#post_btn_action").innerHTML = "BID";
        //     clone.querySelector("#post_btn_action").href = "/marketplace/"+post['key']+"/bid";
        // }
        
        parent.appendChild(clone);
    }

    // Finally, return the constructed list:
    return parent;
}