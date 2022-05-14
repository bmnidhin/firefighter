
if(!apiBaseUrl || !apiKey){
    alert("API base URL and/or API key are not set.")
}

var axiosInstance = axios.create({
  baseURL: apiBaseUrl, //From apigw.js
  headers: {'X-api-key': apiKey}, //From apigw.js
  timeout: 6000,
});


var app = new Vue({
  el: '#app',
  
  methods: {
  	fetchFrames: function(){
		  console.log(apiBaseUrl, apiKey)
  		axiosInstance.get('enrichedframe')
			.then(response => {
		      // JSON responses are automatically parsed.
		      console.log(response.data,"is response data");
		      this.enrichedframes = response.data;
		    })
		    .catch(e => {
		      //this.errors.push(e);
		      console.log(e);
		    })
  	},
  	toggleFetchFrames: function(){
  		if(!this.autoload){
  			//this.autoloadTimer.stop();
  			this.autoloadTimer = setInterval(this.fetchFrames, 3000);
  			this.autoload=true;
  		}
  		else{
  			//this.autoloadTimer.start();
  			clearInterval(this.autoloadTimer);
  			this.autoload = false;
  		}

  	}
  },
  created: function () {
    this.toggleFetchFrames();
  },
  data: {
    enrichedframes : [],
    autoload: false,
  	autoloadTimer : null,
  },
})



