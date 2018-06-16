
/**
 * operation button in id-list.html
 * open popuwindow for audit user'id
 * @param {int} user_id 
 */
function openAuditIdPopuWindow(user_id) {
    $('#user_id').val(user_id);
    $('#id-modal').modal('show');
    $('#pass_button').click(function(event){
        event.preventDefault();
        var data = {};
        data.pass_kyc = "1";
        data.user_id = user_id;
        data.level = $('#level').val();
        var comment = $('#id_comment').val();
        comment = " " + comment;
        data.comment = comment;
        $.post('/newtonadmin/tokenexchange/id/confirm/', 
            data, 
            function(json){
                if (json['error_code'] == 1) {
                alert('success,we had send a email to user');
                location.reload();
                } else {
                alert(json['error_message']);
                }
            });
    });
    $('#reject_button').click(function(event){
        event.preventDefault();
        var data = {};
        data.pass_kyc = "2";
        data.user_id = user_id;
        var comment = $('#id_comment').val();
        comment = " " + comment;
        data.comment = comment;
        data.level = $('#level').val();
        $.post('/newtonadmin/tokenexchange/id/confirm/', 
            data, 
            function(json){
                if (json['error_code'] == 1) {
                alert('success, we had reject user');
                location.reload();
                } else {
                alert(json['error_message']);
                }
            });
        });
    $('#deny_button').click(function(event){
        event.preventDefault();
        var data = {};
        data.pass_kyc = "3";
        data.user_id = user_id;
        var comment = $('#id_comment').val();
        comment = " " + comment;
        data.comment = comment;
        data.level = $('#level').val();
        $.post('/newtonadmin/tokenexchange/id/confirm/', 
            data, 
            function(json){
                if (json['error_code'] == 1) {
                alert('success, we had deny user');
                location.reload();
                } else {
                alert(json['error_message']);
                }
            });
        });
}

/**
 * send invite button in te-waiting-list.html
 * prepare invite checked user apply tokenexchange
 * @param {int} user_id 
 */
function preInviteUser(user_id) {
    var data = {};
    var user_list = [user_id];
    user_list = user_list.join(",");
    data.user_list = user_list;
    $.post('/newtonadmin/tokenexchange/invite/'+ phase_id + '/post/', 
        data, 
        function(json){
        if (json['error_code'] == 1) {
            alert('success');
            location.reload();
        } else {
            alert(json['error_message']);
        }
    });
}
/**
 * all check checkbox in te-waiting-list.html
 * 
 */
$("#all-check-pre-invite").change(function(){
    var isAllCheck = $("#all-check-pre-invite")[0].checked;
    if(isAllCheck){
        // all Check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = true;
        }
    }else{
        // cancel all check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = false;
        }
    }
});

/**
 * bulk operation for prepare invite user apply token exchange.
 */
function preInviteSelectedUser(){
    var user_list = [];
    var checkboxes = $("input[type='checkbox']")
    for(var i = 0; i < checkboxes.length; i++){
        var checkbox = checkboxes[i]
        if(checkbox.checked){
            var value = checkbox.value
            if(value != "on"){
                user_list.push(value);
            }
        }
    }
    user_list = user_list.join(",");
    var data = {}
    data.user_list = user_list;
    $.post("/newtonadmin/tokenexchange/invite/" + phase_id + "/post/",data,function(json){
        if (json['error_code'] == 1) {  
            alert('success');
            location.reload();
        } else {
            alert(json['error_message']);
        }
    });
}

/**
 * operation button in te-completed-list
 * send notify email for checked user
 * @param {int} user_id user'id
 */
function sendPerInviteEmail(user_id) {
    var data = {};
    var user_list = [user_id];
    user_list = user_list.join(",");
    data.user_list = user_list;
    $.post('/newtonadmin/tokenexchange/invite/' + phase_id + '/send/', 
        data, 
        function(json){
        if (json['error_code'] == 1) {
            alert('success');
            location.reload();
        } else {
            alert(json['error_message']);
        }
    });
}

/**
 * all check checkbox in te-completed-list.html
 */
$("#all-check-invite").change(function(){
    var isAllCheck = $("#all-check-invite")[0].checked;
    if(isAllCheck){
        // all Check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = true;
        }
    }else{
        // cancel all check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = false;
        }
    }
});

/**
 * send email button in te-completed-list.html
 * send email to checked user.
 */
function sendSelectedEmailForInvite(){
    var user_list = [];
    var checkboxes = $("input[type='checkbox']")
    for(var i = 0; i < checkboxes.length; i++){
        var checkbox = checkboxes[i]
        if(checkbox.checked){
            var value = checkbox.value
            if(value != "on"){
                user_list.push(value);
            }
        }
    }
    user_list = user_list.join(",");
    var data = {}
    data.user_list = user_list;
    $.post('/newtonadmin/tokenexchange/invite/' + phase_id + '/send/',data,function(json){
        if (json['error_code'] == 1) {  
            alert('success');
            location.reload();
        } else {
            alert(json['error_message']);
        }
    });
}


/**
 * operation button in amount-list.html.
 * distribute coin for user according to expect limit.
 * @param {string} user_id 
 * @param {int} phase_id 1 for first tokenexchange. 2 for second
 * @param {int} expect_ela 
 * @param {int} expect_btc 
 */
function amountPopupWindow(user_id, phase_id, expect_ela, expect_btc) {
    $('#user_id').val(user_id);
    $('#phase_id').val(phase_id)
    if(expect_ela===0){
        $("#ela-limit").addClass("hide")
    }else{
        $("#ela-limit").removeClass("hide")
    }
    if(expect_btc===0){
        $("#btc-limit").addClass("hide")
    }else{
        $("#btc-limit").removeClass("hide")
    }
    $('#amount_modal').modal('show');
    $('#confirm_button').click(function(event){
        event.preventDefault();
        var data = {};
        data.assign_btc = $('#assign_btc').val();
        data.assign_ela = $('#assign_ela').val();
        data.user_id = user_id;
        data.phase_id = phase_id;
        if(data.assign_btc != 0 && data.assign_btc < btcLimit){
            alert("btc 额度大于等于"+btcLimit);
            return;
        }
        if(data.assign_ela != 0 && data.assign_ela < elaLimit){
            alert("ela 额度需要大于等于"+elaLimit);
            return;
        }
        $.post('/newtonadmin/tokenexchange/amount/'+phase_id+'/post/', 
            data, 
            function(json){
                if (json['error_code'] == 1) {
                alert('success');
                location.reload();
                } else {
                alert(json['error_message']);
                }
        });
    });
}

/**
 * sendemail button in receive-list.html.
 * send email to notify user that newton have received coin.
 * @param {string} user_id 
 */

function sendPerEmail(user_id) {
    var data = {};
    var user_list = [user_id];
    user_list = user_list.join(",");
    data.user_list = user_list;
    $.post('/newtonadmin/tokenexchange/receive/' + phase_id + '/send/', 
        data,
        function(json){
            if (json['error_code'] == 1) {
            alert('success,we had send address to user.');
            location.reload();
            } else {
            alert(json['error_message']);
            }
        });
}

/**
 * all-check checkbox in receive-list.html.
 * all-check checkbox's listener.
 */
$("#all-check-receive-coin").change(function(){
    var isAllCheck = $("#all-check-receive-coin")[0].checked;
    if(isAllCheck){
        // all Check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = true;
        }
    }else{
        // cancel all check
        var checkboxes = $("input[type='checkbox']")
        for(var i = 0; i < checkboxes.length; i++){
            checkboxes[i].checked = false;
        }
    }
});

/**
 * send selected email button in receive-list.html.
 * send selected email which to notify user that newton have received coin.
 */
function sendEmailForReceivedCoin(){
    var user_list = [];
    var checkboxes = $("input[type='checkbox']")
    for(var i = 0; i < checkboxes.length; i++){
        var checkbox = checkboxes[i]
        if(checkbox.checked){
            var value = checkbox.value
            if(value != "on"){
                user_list.push(value);
            }
        }
    }
    user_list = user_list.join(",");
    var data = {}
    data.user_list = user_list;
    $.post('/newtonadmin/tokenexchange/receive/' + phase_id + '/send/',data,function(json){
        if (json['error_code'] == 1) {  
            alert('success');
            location.reload();
        } else {
            alert(json['error_message']);
        }
    });
}