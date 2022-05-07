	console.log("start ...");

	var timer;

	var id;
	var tick;

	var canvas;
	var context;

	var screen_width;
	var screen_height;

	var colors = ["#DE6641", "#E8AC51", "#F2E55C", "#AAC863",
							  "#39A869", "#27ACA9", "#00AEE0", "#4784BF",
							  "#5D5099", "#A55B9A", "#DC669B", "#DD6673" ]

	var coloridx = -1;

	$(function() {

		//アプリインストール時の自動書き換えが行われていたら入力不可にする
		if ($("#id").val() != "12345678"){
			//id部を参照
			targetElement = document.getElementById('id');
			targetElement.disabled = true;
		}

		$("#startbutton").click(function(){
			//各パラメータをセット
			setParam();
	  	$("#startbutton").prop("disabled",true);
	  	$("#stopbutton").prop("disabled",false);
	  		startGetInfo();
			disp_init();
		});

		$("#stopbutton").click(function(){
			stopGetInfo();
	    $("#startbutton").prop("disabled",false);
	    $("#stopbutton").prop("disabled",true);
		});

	});

	//JSON取得を開始する
	function startGetInfo()
	{
		//JSONデータ取得
		getData();
	}


	// *******************
	//  パラメータの設定
	// *******************
	function setParam()
	{
	  id = $("#id").val();
	  tick = $("#tick").val();

	  //初期値
	  screen_width=640;
	  screen_height=480;

	}

	// ***************************
	//  データ取得と表示
	// ***************************
	function getData()
	{

		getImg();

		//指定時間後にもう一度自身を呼び出す
		timer = setTimeout("getData()", tick);
	}

	// ***************************
	//	画像データの取得と表示
	// ***************************
	function getImg()
	{
		var request  = new XMLHttpRequest();

		// リクエストパラメータとURLの設定
		var param = "methodName=sendDataToAdamApplication&installId=" + id + "&s_appDataType=1&s_appData="
		var url = "./adam.cgi?" + param;

		request.open("GET", url, true);

		// blob形式で受信する
		request.responseType = "blob";

		request.onreadystatechange = function() {

			//受信正常時
			if (request.readyState == 4 && request.status == 200) {

	  			// 受信した画像データのblob URLを取得
				var blobUrl = URL.createObjectURL(request.response);

				// 画像表示
				camera_img.src = blobUrl;

				// 描画エリアサイズの更新
				if(screen_width != camera_img.width || screen_height != camera_img.height)
				{
				  	screen_width = camera_img.width;
				  	screen_height = camera_img.height;

				  	resize_screen();
				}

			}
		}

	  	request .send("");
	}

	// *********
	//	初期化
	// *********
	function disp_init()
	{
		canvas = document.getElementById('disp');
		context = canvas.getContext('2d');

		// 画像表示領域（背景）を取得
		disp_parent = document.getElementById('disp_parent');
		disp_parent.style.background='#ffffff';

		// カメラ画像表示領域
		camera_img = document.getElementById('camera_img');

		// //JSONデータ表示領域
		// disp_json_area = document.getElementById('disp_json');

		resize_screen();

	}

	// *********************
	//	描画エリアリサイズ
	// *********************
	function resize_screen()
	{
		// 画像表示領域（背景）の更新
		disp_parent.style.width=screen_width;
		disp_parent.style.height=screen_height;

		// 描画エリア（カメラ画像＆検出表示canvas）設定の更新
		$('.relative').css('width', screen_width);
		$('.relative').css('height', screen_height);
		//描画機能が使えるブラウザであるかチェック
		if(canvas.getContext){

			//canvasタグの表示サイズを設定する
			$( 'canvas' ).get( 0 ).width  = screen_width;
			$( 'canvas' ).get( 0 ).height = screen_height;

			clearCanvas();
		}
		else
		{
			return 0;
		}
	}

	// **************
	//	矩形の描画
	// **************
	function drawSquare(baseX, baseY, width, height)
	{
		context.strokeStyle  = colors[++coloridx];			//矩形の色
		//矩形描画
		context.strokeRect(baseX, baseY, width, height);
	}

	//canvasエリアをクリアする
	function clearCanvas()
	{
		context.clearRect(0, 0, screen_width, screen_height);
		coloridx = -1;
	}

	//タイマーを解除する
	function stopGetInfo()
	{
	  if (timer) {
	    clearTimeout(timer);
	  }
	}
