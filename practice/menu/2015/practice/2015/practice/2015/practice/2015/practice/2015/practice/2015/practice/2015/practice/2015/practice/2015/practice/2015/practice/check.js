function main() {
    check = window.prompt("半角でパスワードを入力してください","");
    if(check == 's1200213')
	window.alert('ようこそ。');
    else {
	window.alert('パスワードが違います。');
	location.href = "../index.html";
    }	
}