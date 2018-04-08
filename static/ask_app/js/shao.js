
$(document).ready(function(){
	$("#loadButton").click(function(){
		var temp = $(this);
		var page = temp.attr("page");
		var url = temp.attr("load");
		$.get(url+page,function(data,status){
			if(data == ''){
				temp.text("全部已加载");
				temp.attr("class","btn btn-default btn-block");
			}
			else{
				$("#answerList").append(data);
				temp.attr("page",Number(page)+1);
			}
		});
	});

	$("#answerList").on('click','[vote]',function(){
		var objtemp = $(this);
		$.getJSON(objtemp.attr('vote'),function(data,status){
			if(data['result'] == 'unlogin'){
				$('#myModal').modal();
			}
			else{
				objtemp.parent().find("[voteupCount]").html(data['data']);
			}
			
		});
	});

	$("#answerList").on('click','[favour]',function(){
		var objtemp = $(this);
		$.getJSON(objtemp.attr('favour'),function(data,status){
			if(data['result'] == 'favour'){
				objtemp.html("已收藏");
			}
			else if(data['result'] == 'unlogin'){
				$('#myModal').modal();
			}
			else{
				objtemp.html("<span class='fui-star-2'></span>收藏");
			}
		});
		return false;
	});
		
	$("#answerButton").click(function(){
		$("#answerDialog").toggle(200);
	});

	$("[follow]").click(function(){
		var temp = $(this);
		$.getJSON(temp.attr("follow"),function(data,status){
			if(data['result'] == 'follow'){
				temp.html("已关注");
			}
			else if(data['result'] == 'unlogin'){
				$('#myModal').modal();
			}
			else{
				temp.html("关注问题");
			}
		});
	});
	
	$("#loginButton").click(function(){
		var un = $("#login-name").val();
		var pw = $("#login-pass").val();
		var csrf = $("#csrf").val();
		data = {
			'username':un,
			'password':pw,
			'csrfmiddlewaretoken':csrf
		}
		$.post('/user/login_/',data,function(data,status){
			var data = $.parseJSON(data);
			if(data['result'] == 'success'){
				location.reload();
			}
			else{
				$("#loginInfo").html('<p class="text-danger">账号或密码错误!</p>');
			}
		});
		return false;
	});
});